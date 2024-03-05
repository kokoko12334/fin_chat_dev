import json
import re

from typing import Optional, Any, Union
from langchain.agents.agent import AgentOutputParser
from langchain.schema.language_model import BaseLanguageModel
from langchain.output_parsers import OutputFixingParser
from langchain.schema import AgentAction, AgentFinish, OutputParserException

from pydantic import Field

from MofinChatBot.MOGEAgent.prompt import FORMAT_INSTRUCTIONS

FINAL_ANSWER_ACTION = "Final Answer:"

class MogeOutputParser(AgentOutputParser):
    """Output parser for the structured chat agent."""
    
    def get_format_instructions(self) -> str:
        return FORMAT_INSTRUCTIONS
    
    def parse(self, text: str) -> Union[AgentAction, AgentFinish]:
        try:
            # ```로 감싸진 부분 찾기
            # action_match = re.search(r"```(.*?)```?", text, re.DOTALL)
            action_match = re.search(r"```(?:\s*json)?(.*?)```", text, re.DOTALL)
            
            
            if action_match is not None:
                action_section = action_match.group(1).strip()
            else:
                # Action 부분이 없을 경우 전체 텍스트를 사용
                if "Action:" in text:
                    action_section = text.split("Action:", 1)[1]
                # elif "Final Answer:" in text:
                #     action_section = text.split("Final Answer:", 1)[1]
                else:
                    action_section = text

            print(action_section)
            
            response = json.loads(action_section, strict=False)

            if isinstance(response, list):
                response = response[0]

            if response["action"] == "Final Answer":
                return AgentFinish({"output": response.get("action_input", {})}, text)
            else:
                print(response)
                print(response.get("action_input", {}))
                return AgentAction(response["action"], response.get("action_input", {}), text)
        except Exception as e:
            # 에러 처리
            print("exception")
            return AgentFinish({"output": action_section}, text)
        
    @property
    def _type(self) -> str:
        return "moge_chat"


class MogeOutputParserWithRetries(AgentOutputParser):
    """Output parser with retries for the structured chat agent."""

    base_parser: AgentOutputParser = Field(default_factory=MogeOutputParser)
    """The base parser to use."""
    output_fixing_parser: Optional[OutputFixingParser] = None
    """The output fixing parser to use."""

    def get_format_instructions(self) -> str:
        return FORMAT_INSTRUCTIONS

    def parse(self, text: str) -> Union[AgentAction, AgentFinish]:
        try:
            if self.output_fixing_parser is not None:
                parsed_obj: Union[
                    AgentAction, AgentFinish
                ] = self.output_fixing_parser.parse(text)
            else:
                parsed_obj = self.base_parser.parse(text)
            return parsed_obj
        except Exception as e:
            raise OutputParserException(f"Could not parse LLM output: {text}") from e

    @classmethod
    def from_llm(
        cls,
        llm: Optional[BaseLanguageModel] = None,
        base_parser: Optional[MogeOutputParser] = None,
    ):
        if llm is not None:
            base_parser = base_parser or MogeOutputParser()
            output_fixing_parser = OutputFixingParser.from_llm(
                llm=llm, parser=base_parser
            )
            return cls(output_fixing_parser=output_fixing_parser)
        elif base_parser is not None:
            return cls(base_parser=base_parser)
        else:
            return cls()

    @property
    def _type(self) -> str:
        return "moge_chat_with_retries"
