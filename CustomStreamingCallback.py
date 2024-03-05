import asyncio
from typing import Any, AsyncIterator, Dict, List, Literal, Union, cast
from langchain.callbacks.streaming_stdout_final_only import (
    FinalStreamingStdOutCallbackHandler,
)
from langchain.schema.output import LLMResult

class StreamCallbackHandler(FinalStreamingStdOutCallbackHandler):
    """Callback handler that returns an async iterator."""
    answer_prefix_tokens = ['Final', 'Answer',":"]
    
    queue: asyncio.Queue[str]

    done: asyncio.Event

    @property
    def always_verbose(self) -> bool:
        return True

    def __init__(self) -> None:
        self.queue = asyncio.Queue()
        self.done = asyncio.Event()
        self.last_tokens = [""] * len(self.answer_prefix_tokens)
        self.last_tokens_stripped = [""] * len(self.answer_prefix_tokens)
        self.answer_reached = False
        self.first_token_processed = False

    async def on_llm_start(
            self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        # If two calls are made in a row, this resets the state
        self.done.clear()

    async def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        self.last_tokens.append(token.strip())
        
        if len(self.last_tokens) > len(self.answer_prefix_tokens):
            self.last_tokens.pop(0)
        # Check if the last n tokens match the answer_prefix_tokens list ...
        if self.last_tokens == self.answer_prefix_tokens:
            self.answer_reached = True
            # Do not print the last token in answer_prefix_tokens,
            # as it's not part of the answer yet
            return

        # ... if yes, then append tokens to queue
        if self.answer_reached:
            # strip space from front of first token
            if not self.first_token_processed:
                token = token.lstrip()
                self.first_token_processed = True
                
            self.queue.put_nowait(token)


    async def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        if self.answer_reached:
            self.done.set()

    async def on_llm_error(
            self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> None:
        self.done.set()

    async def aiter(self) -> AsyncIterator[str]:
        while not self.queue.empty() or not self.done.is_set():
            # Wait for the next token in the queue,
            # but stop waiting if the done event is set
            done, other = await asyncio.wait(
                [
                    # NOTE: If you add other tasks here, update the code below,
                    # which assumes each set has exactly one task each
                    asyncio.ensure_future(self.queue.get()),
                    asyncio.ensure_future(self.done.wait()),
                ],
                return_when=asyncio.FIRST_COMPLETED,
            )

            # Cancel the other task
            if other:
                other.pop().cancel()

            # Extract the value of the first completed task
            token_or_done = cast(Union[str, Literal[True]], done.pop().result())

            # If the extracted value is the boolean True, the done event was set
            if token_or_done is True:
                break

            # Otherwise, the extracted value is a token, which we yield
            yield token_or_done