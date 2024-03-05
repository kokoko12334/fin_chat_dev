from langchain.tools import BaseTool
from langchain.agents import create_csv_agent
# from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI

from langchain.agents.agent_types import AgentType
from langchain import PromptTemplate

from MofinChatBot.utils.ticker_lookup import ticker_lookup, TickerNotFoundError
import streamlit as st

from pydantic import BaseModel, Field
from typing import Type

import requests
import pandas as pd
import json

class SummarizeCompanyInput(BaseModel):
    """ Inputs for SummarizeCompanyTool"""
    company_name: list = Field(description="company name or ticker, ONLY ENGLISH", examples=["APPLE", "MSFT"])
    

class SummarizeCompanyTool(BaseTool):
    name = "SummarizeCompanyTool"
    description = """
    Use this tool to get a summary of the company's information and business.
    """
    args_schema: Type[BaseModel] = SummarizeCompanyInput
    
    def _run(self, company_name: list):
        result = {}
        for company in company_name:
            try:
                ticker = ticker_lookup(company_name=company)
                url = f'https://api.iex.cloud/v1/data/core/company/{ticker}/?token={st.secrets.IEX_API_KEY}'
                res = requests.get(url).json()
                
                if res:
                    # self.return_direct = True
                    result[ticker] = res[0]['longDescription']
                    
            except TickerNotFoundError as e:
                result[company] = f'{company} is not supported..'
            except Exception as e:
                result[company] = f'{company} is not supported..'
            
            return result