from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type

import requests
import streamlit as st

class CompanyInfoInput(BaseModel):
    """Inputs for TickerLookup"""
    
    company_name: str = Field(description="company name")

class TickerLookup(BaseTool):
    name = "TickerLookup"
    description = """
    회사의 이름에 맞는 ticker를 찾아주는 도구야. 
    회사에 대해 물어보면 먼저 이 도구를 통해 ticker를 알아내!.
    """
    args_schema: Type[BaseModel] = CompanyInfoInput 
    
    def _run(self, company_name: str):
        url = f"https://api.iex.cloud/v1/search/{company_name}?token={st.secrets.IEX_API_KEY}"
        res = requests.get(url).json()
        
        if res:
            self.return_direct = False
            
            search_res = res[0]
            ticker = search_res["symbol"]
        else:
            self.return_direct = True
            ticker = "알 수 없는 회사입니다. 회사 이름을 영어로 적어주세요."
        
        return ticker