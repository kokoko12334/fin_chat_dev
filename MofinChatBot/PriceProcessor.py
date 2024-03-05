from langchain.tools import BaseTool

from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import AIMessage, HumanMessage, SystemMessage

from MofinChatBot.utils.db_infos import *
from MofinChatBot.utils.ticker_lookup import ticker_lookup, TickerNotFoundError

import streamlit as st

from pydantic import BaseModel, Field
from typing import Type
import requests
import json
import datetime
from datetime import timedelta
class PriceQuoteInput(BaseModel):
    """Inputs for StockPriceQuoteTool"""
    company_name: list = Field(description="company name or ticker, ONLY ENGLISH", examples=["APPLE", "MSFT"])
    # pattern=r"^\d{4}-\d{2}-\d{2}$"
    dates: list = Field(description="Dates want to know the stock prices", example=["2023-09-14", "2023-11-01"])

date_format = "%Y-%m-%d"
columns = ['close', 'open', 'high', 'low', 'volume']
class StockPriceQuoteTool(BaseTool):
    name = "StockPriceQuoteTool"
    description = """
    Use This tool to get the price of company's stock
    """
    args_schema: Type[BaseModel] = PriceQuoteInput

    def _run(self, company_name:list, dates:list):
        result = {}
        #TODO: company_name 한번에 넣어서 api 요청
        for company in company_name:
            price = {}
            try:
                ticker = ticker_lookup(company)
                for date in dates:
                    for _ in range(10):
                        url = f"https://api.iex.cloud/v1/data/core/historical_prices/{ticker}?on={date}&token={st.secrets.IEX_API_KEY}"
                        res = requests.get(url).json()
                        if res:
                            price[date] = {col: res[0][col] for col in columns}
                            break
                        date = datetime.datetime.strptime(date, date_format)
                        # print(date)
                        date -= timedelta(days=1)
                        date = date.strftime(date_format)
                    if not res:
                        price[date] = f"{date} is not supported"
                    
                result[ticker] = price
            except TickerNotFoundError as e:
                result[company] = f'{company} is not supported..'
            except Exception as e:
                return f"An error occurred: {e}"

            
        return result
            
            # while(True):
                
            #     url = f"https://api.iex.cloud/v1/data/core/historical_prices/{ticker}?on={date}&token={st.secrets.IEX_API_KEY}"
            #     res = requests.get(url).json()
            #     if res:
            #         return f"{{{date}}} : {{{res}}}"
            #     date = datetime.datetime.strptime(date, date_format)
            #     print(date)
            #     date -= timedelta(days=1)
            #     date = date.strftime(date_format)
                