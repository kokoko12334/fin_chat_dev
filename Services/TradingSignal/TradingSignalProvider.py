from Services.TradingSignal.query_result_handler import process_query_result
import pinecone
from utils.price_data_handler import (
    get_price_data,
    processing_data
)
import openai
from settings import settings
from utils.db_infos import get_ticker_list
from pydantic import BaseModel

openai.api_key = settings.OPENAI_API_KEY

async def get_price_embedding(text, model='text-embedding-ada-002'):
    text = text.replace("\n", " ")
    embedding = await openai.Embedding.acreate(input = [text], model=model)
    return embedding['data'][0]['embedding']
    # return await openai.Embedding.acreate(input = [text], model=model)['data'][0]['embedding']
    
index_name = 'openai-price-embedding'

async def signal_generate(ticker):
    index = pinecone.Index(index_name)
    
    # TODO : async get price
    price = get_price_data(ticker)
    
    if price.empty:
        return 0, 0
    
    prompt = processing_data(price)
    embedding = await get_price_embedding(prompt)

    # TODO : async index query 방법
    query_result = index.query(embedding, top_k=51, include_metadata=True, )
    signal, percent =  process_query_result(query_result)
    
    return signal, percent

def recommend_stock(result, m):
    sorted_data = sorted(enumerate(result), key=lambda x: x[1][1], reverse=True)
    print(sorted_data)
    # 상위 m개의 튜플을 선택하고 각 튜플의 인덱스 값을 추출
    top_m_indices = [item[0] for item in sorted_data[:m]]

    return top_m_indices


class Signal(BaseModel):
    ticker:str
    signal: int
    prob:float
    ranking:int
    
ticker_list = get_ticker_list()
    
async def generate_all_signals():
    result = {}
    for ticker in ticker_list:
        print('generate signal for ', ticker)
        signal, percent = await signal_generate(ticker)
        result[ticker] = [signal, percent]
    
    # create ranking by percent and append to result
    sorted_result = sorted(result.items(), key=lambda item: item[1][1], reverse=True)
    result_list = []
    for item in sorted_result:
        key, value = item
        value.append(sorted_result.index((key, value)) + 1)
        result_list.append((key, value))
    
    # create dictionary of result_list - (ticker, [signal, percent, rank])
    result_dict = {}
    for item in result_list:
        key, value = item
        result_dict[key] = value
    return result_dict

