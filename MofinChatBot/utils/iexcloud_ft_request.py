import requests
import streamlit as st
import json
iex_api_key = st.secrets.IEX_API_KEY

def ft_request_annual(ticker):
    url = f'https://api.iex.cloud/v1/data/core/income/{ticker}/annual?last=99999&token={iex_api_key}'

    
    response = requests.get(url)  

    # 서버로부터의 응답을 처리합니다.
    if response.status_code == 200: 
        
        json_data = json.loads(response.text)
        return json_data
    else:
        print(f"요청이 실패했습니다. 응답 코드: {response.status_code}")


def ft_request_quarterly(ticker):
    url = f'https://api.iex.cloud/v1/data/core/income/{ticker}/quarterly?last=99999&token={iex_api_key}'

    response = requests.get(url)  

    # 서버로부터의 응답을 처리합니다.
    if response.status_code == 200: 
        
        json_data = json.loads(response.text)
        return json_data
    else:
        print(f"요청이 실패했습니다. 응답 코드: {response.status_code}")