from langchain.chat_models import ChatOpenAI
from langchain.tools import BaseTool
from langchain.prompts.chat import(
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder
)
from pydantic import BaseModel, Field
from settings import settings
from utils.generate_chat_history import generate_chat_history

PREFIX="""
You're a Mogenious(AI Assistant), called MOGE, for helping user to use effectively QuantMO.AI application



"""
HUMAN_PROMPT="""
{message}

Final response should be in {language} language.

"""

HISTORY_PROMPT="""
Question : {history_user}
Reply : {history_ai}

"""
class ConversationToolInput(BaseModel):
    message: str = Field(description="User input message")
    history_user: str = Field(description="User history message")
    history_ai: str = Field(description="AI history message")
    language: str = Field(description="Language in which the final answer should be provided.")
    
system_prompt = SystemMessagePromptTemplate.from_template(PREFIX)
chat_history_prompt = SystemMessagePromptTemplate.from_template(HISTORY_PROMPT)
human_prompt = HumanMessagePromptTemplate.from_template(HUMAN_PROMPT)
chat_prompt = ChatPromptTemplate.from_messages([
    system_prompt,
    chat_history_prompt,
    human_prompt
])


class ConversationTool(BaseTool):
    name = "ConversationTool"
    description = "This tool Provides quick and accurate answers to questions."
    return_direct = True
    # llm = OpenAI(temperature=0, model_name='gpt-3.5-turbo-16k')
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
    def _run(self, message: str, history_user:str, history_ai:str, language:str):
        # chat_history = generate_chat_history(history_user, history_ai)

        messages = chat_prompt.format_prompt(
            message=message,
            history_user=history_user,
            history_ai=history_ai,
            language=language

        ).to_messages()
        response = self.llm(messages)
        return response.content