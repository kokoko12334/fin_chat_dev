from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
from langchain.agents import AgentExecutor
import langchain
from langchain.cache import InMemoryCache
langchain.llm_cache = InMemoryCache()

from CustomStreamingCallback import *
from MofinChatBot.tools import get_available_tools
from MofinChatBot.MOGEAgent.MogeAgent import MogeAgent
import re
from pydantic import BaseModel

from datetime import datetime

def initialize_mogeagent(tools, llm, verbose=True):
    agent = MogeAgent.from_llm_and_tools(
        llm=llm,
        tools=tools
    )
    agent_executor = AgentExecutor.from_agent_and_tools(
        agent=agent, tools=tools, verbose=verbose
    )
    return agent_executor

class MessageWithHistory(BaseModel):
    content: str
    history_user: str
    history_ai: str
    
class OpenAIServices():
    def __init__(self) -> None:
        self.tools = get_available_tools()
        # self.llm = OpenAI(temperature=0, model_name='gpt-3.5-turbo-16k')
        self.llm = ChatOpenAI(temperature=0, model="gpt-4-1106-preview")
        self.agent_type = AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION
        # self.agent = initialize_agent(self.tools, self.llm, self.agent_type, verbose=True)
        self.agent = initialize_mogeagent(self.tools, self.llm, verbose=True)
        # self.agent.agent.llm_chain.verbose=True
        
    def run_agent(self, message:MessageWithHistory, callbacks=None):
        msg, history_user, history_ai = self._make_input_chat_history(message)
        date = datetime.now().strftime('%Y-%m-%d')
        return self.agent.run(input=msg, history_user=history_user,
                              history_ai=history_ai,
                              date=date, callbacks=callbacks)
        # return self.agent.run(f"{datetime.datetime.now().strftime('%Y-%m-%d')} " + message, callbacks=callbacks)

    async def arun_agent(self, message:MessageWithHistory, callbacks=None):
        msg, history_user, history_ai = self._make_input_chat_history(message)
        date = datetime.now().strftime('%Y-%m-%d')
        return (await self.agent.arun(input=msg,
                                     history_user=history_user,
                                     history_ai=history_ai,
                                     date=date,
                                     callbacks=callbacks))
        
    def _make_input_chat_history(self, message:MessageWithHistory):
        msg = message.content
        # chat_history = generate_chat_history(message.history_user, message.history_ai)
        # print(msg, chat_history)
        history_user = re.sub(r'\s+', ' ', message.history_user)
        history_ai = re.sub(r'\s+', ' ', message.history_ai)
        
        return msg, history_user, history_ai
    
    def llmCallbacksSetter(self,callbacks):
        self.llm.callbacks = [callbacks]