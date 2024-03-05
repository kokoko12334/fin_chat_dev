from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from MofinChatBot.utils.ticker_lookup import ticker_lookup, TickerNotFoundError
import streamlit as st
import openai
from db.db_crud import CompanyInfoCRUD
from db.connection import create_async_session, create_engine
from db.SSH_connection import ssh
from langchain.prompts import PromptTemplate

openai.api_key = st.secrets.OPENAI_API_KEY


prompt = PromptTemplate.from_template(
    """
    Summarize the following report briefly in 2~3 sentences.
    
    report :
    
    {input}    
    
    """   
)

class CompanyReportInput(BaseModel):
    
    company_name: list = Field(description="company name or ticker, ONLY ENGLISH", examples=["APPLE", "MSFT"])

class CompanyReportTool(BaseTool):
    
    name = "CompanyReportTool"
    
    description = """
        Use this tool to analyze the company stock and get Corporate Outlook and an Analysis Report"
    """
    
    args_schema: Type[BaseModel] = CompanyReportInput
    
    def _run(self, company_name:list):
        
        result = {}
        
        return result    
        
    async def _arun(self, company_name:list):
        
        result = {}
        
        engine = create_engine(ssh)
        
        for company in company_name:
            
            async with create_async_session(engine) as session:
                
                try:
                    
                    ticker = ticker_lookup(company)
                    
                    company_info_crud = CompanyInfoCRUD(session)
                    
                    report = await company_info_crud.get_report_by_ticker(ticker)
                    
                    if report[0] != None:
                        
                        result[ticker] = report[0]
                        
                    else:
                        
                        result[ticker] = "I'm sorry. The report for the specific company is not available yet."
                        
                except TickerNotFoundError as e:
                    
                    result[company] = f'{company} is not supported..'
                    
                except Exception as e:
                    
                    print(f"An error occurred: {e}")
                    
                    result[company] = f'{company} is not supported..'
                
        await engine.dispose()
        
        return prompt.format_prompt(input=str(result))

