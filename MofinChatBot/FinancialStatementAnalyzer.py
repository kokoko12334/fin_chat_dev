from langchain.tools import BaseTool
from MofinChatBot.vectorDB import get_pinecone_index2
import openai
import streamlit as st
from pydantic import BaseModel
from typing import Type
from MofinChatBot.utils.ticker_lookup import TickerNotFoundError,ticker_lookup
from pydantic import BaseModel, Field
from langchain.prompts import PromptTemplate
from MofinChatBot.utils.iexcloud_ft_request import *
from langchain.chat_models import ChatOpenAI

# from langchain.llms import OpenAI
# from langchain.chains import LLMChain

index = get_pinecone_index2()
openai.api_key = st.secrets.OPENAI_API_KEY
ftk_api_key = st.secrets.FTK_API_KEY
iex_api_key = st.secrets.IEX_API_KEY
# and Certainly, the sentence "Final Answer: your answer"
#     Furthermore, 'Final Answer:' must always be prefixed to the response. 
#     For example, if the answer is 'Hello', it should become 'Final Answer: Hello.
#     Write simple only one setence for the table at the end.
# Arrange it in a table by year, and include a '$'sign in front of the numbers


prompt = PromptTemplate.from_template(
    """
    Arrange fundamentals statements in a table by year or quarters
    include a '$'sign in front of the numbers
    
    fundamentals statements :
    {input}    
    """   
)

col_list = ['symbol','fiscalYear','fiscalQuarter','currency',
            'costOfRevenue','grossProfit','operatingIncome',
            'netIncome','operatingExpense','ebit']

class FinancialStatementInput(BaseModel):

    """FinancialStatementAnalyzer"""
    company_name: list = Field(description="Company name or ticker, ONLY ENGLISH", example="[Samsung]")
    year_list: list = Field(description="Years that want to know the financial statements", example=[2022, 2023])
    report_type : int = Field(description="financial statements quarter 0:anuual, 1: quarterly", example=0)
    # quart : list = Field(default=0, description="financial statements quarter 0:anuual,1:1st,2:2nd,3:3rd,4:4th", example=[3])
    # country: str = Field(description="country where the company is listed", example="United States")
class FinancialStatementAnalyzer(BaseTool):

    name = "FinancialStatementAnalyzer"
    
    description = '''
    Use this tool when inquiring about a company's financial statements
    '''
    # gpt-4-1106-preview
    llm = ChatOpenAI(temperature=0, model="gpt-4-1106-preview")
    
    return_direct = False
    
    args_schema: Type[BaseModel] = FinancialStatementInput

    # def _run(self, company_name:list, year_list:list, end_year:int, quart:list, country: str) -> str:
    def _run(self, company_name:list, year_list:list, report_type=int) -> str:
        result = {}
        # years = set([year for year in range(end_year,start_year+1)])
        for company in company_name:
            try:
                ticker = ticker_lookup(company)
                # ft requst 
                if report_type == 0:
                    ft_json = ft_request_annual(ticker)
                else:
                    ft_json = ft_request_quarterly(ticker)
                final_json_data = []
                
                for data in ft_json:
                    json_data = dict(zip(col_list, [""*len(col_list)]))
                    if data['fiscalYear'] in year_list and data['filingType'] in {'10-K','10-Q'}:
                        for col in col_list:
                            json_data[col] = data[col]
                        print(json_data)
                        final_json_data.append(json_data)
                
                result[ticker] = final_json_data
                
            except TickerNotFoundError as e :
                result[company] = f'{company_name} is not supported..'
            except Exception as e:
                result[company] = f'{company_name} is not supported..'

        # TODO: prompt와 함께 반환이 필요하면 추가하기
        # return result
        messages = prompt.format_prompt(input=str(result)).to_messages()
        response = self.llm(messages)
        return response.content
            
        # return "sorry. we are preparing financial analyzer"
    

        # final_json_data = ""
        
        # years = set([year for year in range(end_year,start_year+1)])
        
        # quart = set(quart)

        # for company in company_name:
            
        #     ticker = ""

        #     try:
        #         ticker = ticker_lookup(company)
        #     except TickerNotFoundError as e :
        #         return f'{company_name} is not supported..'
                
                   
        #     if 0 in quart and len(quart) == 1:
        #         ft_json = ft_request_annual(ticker)
        #     else:
        #         ft_json = ft_request_quarterly(ticker)

            
        #     for data in ft_json:

        #         json_data = dict(zip(col_list, [""*len(col_list)]))

        #         if data['fiscalYear'] in years and data['fiscalQuarter'] in quart and data['filingType'] in {'10-K','10-Q'}:
        #             for col in col_list:
        #                 json_data[col] = data[col]
                    
        #             final_json_data += str(json_data).replace(" ","")
        
        # if final_json_data:
            
        #     return prompt.format(input=str(final_json_data))
        
        # else:
        #     return "해당 기간의 재무제표를 구할 수 없습니다."

