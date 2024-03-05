from typing import Any, List, Optional, Sequence, Tuple
from langchain.agents.structured_chat.base import StructuredChatAgent
from langchain.agents.structured_chat.output_parser import StructuredChatOutputParserWithRetries
from langchain.schema import AgentAction, BasePromptTemplate
from langchain.schema.language_model import BaseLanguageModel
from langchain.tools.base import BaseTool
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import (
    ChatPromptTemplate,
    ChatMessagePromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.agents.agent import AgentOutputParser
from langchain.callbacks.base import BaseCallbackManager
from langchain.chains.llm import LLMChain
from langchain.agents.agent import Agent

from MofinChatBot.MOGEAgent.prompt import PREFIX, SUFFIX, FORMAT_INSTRUCTIONS, HISTORY_PROMPT
from MofinChatBot.MOGEAgent.output_parser import MogeOutputParserWithRetries
import re
from pydantic import Field


# Please write in ENGLISH language.\n\n

HUMAN_MESSAGE_TEMPLATE = """
{input}\n\n
{agent_scratchpad}\n
"""

class MogeAgent(Agent):
    """MOGEAGENT"""
    output_parser: AgentOutputParser = Field(
        default_factory=StructuredChatOutputParserWithRetries
    )
    """Output parser for the agent."""

    @property
    def observation_prefix(self) -> str:
        """Prefix to append the observation with."""
        return "Observation: "

    @property
    def llm_prefix(self) -> str:
        """Prefix to append the llm call with."""
        return "Thought:"

    def _construct_scratchpad(
        self, intermediate_steps: List[Tuple[AgentAction, str]]
    ) -> str:
        agent_scratchpad = super()._construct_scratchpad(intermediate_steps)
        if not isinstance(agent_scratchpad, str):
            raise ValueError("agent_scratchpad should be of type string.")
        if agent_scratchpad:
            return (
                f"This was your previous work "
                f"(but I haven't seen any of it! I only see what "
                f"you return as final answer):\n{agent_scratchpad}"
            )
        else:
            return agent_scratchpad

    @classmethod
    def _validate_tools(cls, tools: Sequence[BaseTool]) -> None:
        pass

    @classmethod
    def _get_default_output_parser(
        cls, llm: Optional[BaseLanguageModel] = None, **kwargs: Any
    ) -> AgentOutputParser:
        return MogeOutputParserWithRetries.from_llm(llm=llm)

    # @property
    # def _stop(self) -> List[str]:
    #     return ["Observation:"]

    @classmethod
    def create_prompt(
        cls,
        tools: Sequence[BaseTool],
        prefix: str = PREFIX,
        suffix: str = SUFFIX,
        human_message_template: str = HUMAN_MESSAGE_TEMPLATE,
        format_instructions: str = FORMAT_INSTRUCTIONS,
        input_variables: Optional[List[str]] = None,
        history_template: str = HISTORY_PROMPT,
        memory_prompts: Optional[List[BasePromptTemplate]] = None,
    ) -> BasePromptTemplate:
        """
        PROMPT 순서
        PREFIX
        
        TOOL DESCRIPTION + ARGS
        
        TOOL NAMES
        
        SUFFIX
        """
        # TOOL DESCRIPTION + ARGS
        tool_strings = []
        for tool in tools:
            args_schema = re.sub("}", "}}}}", re.sub("{", "{{{{", str(tool.args)))
            tool_strings.append(f"{tool.name}: {tool.description}, args: {args_schema}")
        # tool 설명, args를 한줄씩 붙여서 하나의 string으로 만듦
        formatted_tools = "\n".join(tool_strings)
        # tool 이름은 comma로 연결
        tool_names = ", ".join([tool.name for tool in tools])
        # prompt에 format_instruction에 tool_names 변수로 들어감
        format_instructions = format_instructions.format(tool_names=tool_names)
        # prefix, 툴 설명, 툴 이름, suffix 순으로 template 구성
        template = "\n\n".join([prefix, formatted_tools, format_instructions, suffix])
        # TODO: agent_scratchpad 가 뭔데?? 알아
        if input_variables is None:
            input_variables = ["input", "agent_scratchpad", "history_user", "history_ai", "date"]
        messages = [
            SystemMessagePromptTemplate.from_template(template),
            SystemMessagePromptTemplate.from_template(history_template),
            HumanMessagePromptTemplate.from_template(human_message_template),
        ]
        
        return ChatPromptTemplate(input_variables=input_variables, messages=messages)

    @classmethod
    def from_llm_and_tools(
        cls,
        llm: BaseLanguageModel,
        tools: Sequence[BaseTool],
        callback_manager: Optional[BaseCallbackManager] = None,
        output_parser: Optional[AgentOutputParser] = None,
        prefix: str = PREFIX,
        suffix: str = SUFFIX,
        human_message_template: str = HUMAN_MESSAGE_TEMPLATE,
        format_instructions: str = FORMAT_INSTRUCTIONS,
        input_variables: Optional[List[str]] = None,
        memory_prompts: Optional[List[BasePromptTemplate]] = None,
        **kwargs: Any,
    ) -> Agent:
        """Construct an agent from an LLM and tools."""
        cls._validate_tools(tools)
        prompt = cls.create_prompt(
            tools,
            prefix=prefix,
            suffix=suffix,
            human_message_template=human_message_template,
            format_instructions=format_instructions,
            input_variables=input_variables,
            memory_prompts=memory_prompts,
        )
        llm_chain = LLMChain(
            llm=llm,
            prompt=prompt,
            callback_manager=callback_manager,
        )
        tool_names = [tool.name for tool in tools]
        _output_parser = output_parser or cls._get_default_output_parser(llm=llm)
        return cls(
            llm_chain=llm_chain,
            allowed_tools=tool_names,
            output_parser=_output_parser,
            **kwargs,
        )

    @property
    def _agent_type(self) -> str:
        raise ValueError
