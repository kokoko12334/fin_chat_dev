
import requests
from settings import settings

class TickerNotFoundError(Exception):
    pass


def ticker_lookup(company_name):

    url = f"https://api.iex.cloud/v1/search/{company_name}?token={settings.IEX_API_KEY}"
    res = requests.get(url).json()
    
    if res:
        search_res = res[0]
        ticker = search_res["symbol"]
    else:
        raise TickerNotFoundError("{company_name}에 대한 ticker를 찾을 수 없습니다. 회사 이름을 영어로 써보세요.")
    
    return ticker