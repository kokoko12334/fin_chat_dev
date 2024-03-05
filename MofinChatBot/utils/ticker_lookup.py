
import requests
import streamlit as st
from requests.exceptions import JSONDecodeError
class TickerNotFoundError(Exception):
    pass


def ticker_lookup(company_name):
    
    url = f"https://api.iex.cloud/v1/search/{company_name}?token={st.secrets.IEX_API_KEY}"
    try:
        res = requests.get(url).json()
        search_res = res[0]
        ticker = search_res["symbol"]
    except:
        raise TickerNotFoundError("{company_name}에 대한 ticker를 찾을 수 없습니다. 회사 이름을 영어로 써보세요.")
    
    return ticker