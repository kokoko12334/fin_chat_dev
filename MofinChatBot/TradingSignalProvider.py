from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type

from MofinChatBot.utils.ticker_lookup import ticker_lookup, TickerNotFoundError
import streamlit as st

import openai
from MofinChatBot.vectorDB import get_pinecone_index
from MofinChatBot.utils.query_result_handler import process_query_result
from MofinChatBot.utils.price_data_handler import get_price_data, processing_data
from fastapi import Depends
from db.db_crud import SignalCRUD
from Services.dependencies import signal_crud
from datetime import datetime
from db.connection import create_async_session, create_engine
# from db.db_crud import SignalCRUD
from db.SSH_connection import ssh

openai.api_key = st.secrets.OPENAI_API_KEY

index = get_pinecone_index()

def get_price_embedding(text, model='text-embedding-ada-002'):
    text = text.replace("\n", " ")
    return openai.Embedding.create(input = [text], model=model)['data'][0]['embedding']
    

class TradingSignalProviderInput(BaseModel):
    company_name: list = Field(description="company name or ticker, ONLY ENGLISH", examples=["APPLE", "MSFT"])
    # interval: str = Field(description="interval")

# buy_or_sell = {1 : '오를 것으로 예측하고 있습니다.', 0:'떨어질 것으로 예측하고 있습니다.'}
buy_or_sell = {1 : 'is predicted to rise', 0:'is predicted to fall'}

return_prompt = """
The analysis results from QuantMo.AI are as follows: 
{ticker} is {buy_or_sell} with a probability of {percentage}% .
"""
class TradingSignalProviderTool(BaseTool):
    name = "TradingSignalProviderTool"
    description = """
    Use this tool to get trading signals of the company
    """
    args_schema: Type[BaseModel] = TradingSignalProviderInput

    def _run(self, company_name:list):
        result = {}
        for company in company_name:
            try:
                ticker = ticker_lookup(company)
                price = get_price_data(ticker)
                prompt = processing_data(price)
                embedding = get_price_embedding(prompt)
                
                query_result = index.query(embedding, top_k=51, include_metadata=True)
                percentage, res = process_query_result(query_result)
                
                result[ticker] = return_prompt.format(
                    ticker=ticker,
                    buy_or_sell=buy_or_sell[res],
                    percentage=percentage)
                
            except TickerNotFoundError as e:
                # return '회사에 대한 정보를 찾을 수 없습니다. 회사 이름을 영어로 바꿔봐'
                result[company] = f'{company} is not supported..'
            # return f"퀀트모.AI의 분석 결과는 다음과 같습니다. {ticker} 주식은 {percentage} % 확률로 {buy_or_sell[res]}\n{table}" 
        
        return result
    
    async def _arun(self, company_name:list):
        result = {}
        engine = create_engine(ssh)
        for company in company_name:
            async with create_async_session(engine) as session:
                try:
                    ticker = ticker_lookup(company)
                    signal_crud = SignalCRUD(session)
                    
                    date = datetime.now().strftime('%Y-%m-%d')
                    signal = await signal_crud.get_signal(ticker, date)
                    signal_dict = signal[0].__dict__
                    print(signal_dict)
                    await session.commit()
                    result[ticker] = return_prompt.format(
                        ticker=ticker,
                        buy_or_sell=buy_or_sell[signal_dict['signals']],
                        percentage=signal_dict['prob'])
                    
                except TickerNotFoundError as e:
                    result[company] = f'{company} is not supported..'
                except Exception as e:
                    print(f"An error occurred: {e}")
                    
                    result[company] = f'{company} is not supported..'
                # finally:
                #     session.close()
        await engine.dispose()
        return result
        
    # async def _arun(self, company_name:str):
    #     # company name -> ticker
        
    #     # get today's signal from db
    #     # if signal exists, return signal
    #     # else, return "today's signal provide when ~~"
        
    #     try:
    #         ticker = ticker_lookup(company_name)
    #     except TickerNotFoundError as e:
    #         return f'{company_name} is not supported..'
        
    #     session = create_async_session(self.ssh)
    #     signal_crud = SignalCRUD(session)
    #     print(signal_crud)
    #     try:
            
    #         if signal := await signal_crud.get_signal(
    #             ticker, date=datetime.now().strftime('%Y-%m-%d')):
    #             print(signal)
    #             return signal
    #         return f"signal is updated in KST 7AM"
    #     finally:
    #         session.close()
    #         # return f"{company_name} is not supported"
    
