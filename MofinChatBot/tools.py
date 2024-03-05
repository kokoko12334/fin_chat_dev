from langchain.agents import Tool
from langchain.agents import create_csv_agent
from langchain.agents.agent_types import AgentType

from langchain.tools import BaseTool
from langchain.tools import tool
from langchain.chat_models import ChatOpenAI
from langchain.tools import PythonREPLTool
# from langchain.llms import OpenAI

from langchain import WikipediaAPIWrapper
from MofinChatBot.prompts import conversation_prompt
from MofinChatBot.SummarizeCompany import SummarizeCompanyTool
from MofinChatBot.PriceProcessor import StockPriceQuoteTool
from MofinChatBot.ConversationTool import ConversationTool
from MofinChatBot.CompanyTickerFinder import TickerLookup
from MofinChatBot.vectorDB import get_pinecone_index
import pandas as pd
import ast
from MofinChatBot.FinancialStatementAnalyzer import FinancialStatementAnalyzer
from MofinChatBot.TradingSignalProvider import TradingSignalProviderTool
from MofinChatBot.StockRecommendTool import StockRecommendTool
from MofinChatBot.CompanyReport import CompanyReportTool
from MofinChatBot.MarketNewsAnalysis import MarketNewsAnalysisTool
def get_embedding_data(path='./Data/AAPL_emb.csv'):
    embedding_data = pd.read_csv(path)
    
    embedding_data['embedding'] = embedding_data['Vector'].apply(lambda x : ast.literal_eval(x))
    return embedding_data

index = get_pinecone_index()
embedding_data = get_embedding_data()

def get_available_tools():
    tools = []
    
    # tools.append(StockPriceReader())
    # tools.append(PythonREPLTool())
    # tools.append(TradingSignalProvider())
    # tools.append(ConversationTool())
    
    tools.append(StockRecommendTool())
    tools.append(TradingSignalProviderTool())
    # tools.append(WikiSearchTool())
    tools.append(SummarizeCompanyTool())
    tools.append(StockPriceQuoteTool())
    tools.append(FinancialStatementAnalyzer())
    tools.append(CompanyReportTool())
    tools.append(MarketNewsAnalysisTool())
    # tools.append(TickerLookup())
    
    return tools


class WikiSearchTool(BaseTool):
    name = "WikiSearchTool"
    description = "Use this tool to search Terminology related to stocks, query using specific nouns"
    api_wrapper = WikipediaAPIWrapper
    # args_schema 
    def _run(self, data: str):
        
        return self.api_wrapper(lang='ko').run(query=data)

# class CompanyInsightAgent(BaseTool):
#     name = "CompanyInsightAgent"
#     description = "Use this tool to get company insight, such as stock price, company news, company financials, and more"
#     return_direct = True
#     llm = OpenAI(temperature=0, model_name='gpt-3.5-turbo-16k')
    
#     def _run(self, data: str):
        
#         return self.llm(conversation_prompt.format(message=data))