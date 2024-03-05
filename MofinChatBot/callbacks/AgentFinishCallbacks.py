from typing import Any, AsyncIterator, Dict, List, Literal, Optional, Union, cast

from uuid import UUID
from langchain.callbacks.base import BaseCallbackHandler, AsyncCallbackHandler
from langchain.schema.agent import AgentFinish
from db.db_crud import ChatCRUD
import asyncio
import re


class AgentFinishCallback(AsyncCallbackHandler):
    
    def __init__(self,
                 crud:ChatCRUD,
                 usr_msg:str) -> None:
        super().__init__()
        self.crud = crud
        self.usr_msg = usr_msg
        self.queue = asyncio.Queue()
        self.done = asyncio.Event()
        # self.queue_empty_event = asyncio.Event()
        
    async def on_agent_finish(
        self,
        finish: AgentFinish,
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        tags: List[str] | None = None,
        **kwargs: Any) -> None:
        self.done.clear()
        # agent가 끝나면 generator로 finish의 데이터를 토큰으로 잘라서 뿌려주기
        print(finish)
        text = str(finish.return_values['output'])
        print("agent_finish : ")
        for token in re.split(r'(\s+|\n)', text):
            await asyncio.sleep(0.03)
            # print('token', token)
            self.queue.put_nowait(token)
        
        ### self.done.set()을 여기에 두면 queue에 있는 게 generate되지 않은 시점에 끝내버릴 수 있음. 
        # 모든 데이터가 스트리밍될 때까지 대기
        # 이렇게 하면 너무 느려..
        # while not self.queue.empty():
        #     await asyncio.sleep(0.1) 

        # 모든 데이터가 스트리밍되었으므로 self.done 설정
        await self.on_streaming_finished(text)
        return
    
    async def on_chain_end(
        self,
        outputs: Dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
        ...
        # self.done.set()
        
    async def on_streaming_finished(self, text:str) -> None:
        print("streaming finished")
        # https://stackoverflow.com/questions/55673421/why-are-all-the-tasks-completed-in-asyncio-wait-when-i-clearly-indicate-that-i
        # (asyncio.wait이) 동시에 실행되는 경우가 있어서 sleep 끼워넣기
        await asyncio.sleep(0.1)
        self.done.set()
        await self.crud.create_chat(
            usr_seq=5, chat_question=self.usr_msg,
            chat_reply=text, rating=0
        )
        return
        
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