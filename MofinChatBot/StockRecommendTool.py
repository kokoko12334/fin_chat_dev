from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from db.SSH_connection import ssh
from db.connection import create_engine, create_async_session
from db.db_crud import SignalCRUD
from datetime import datetime

# When signal is 1, it indicates 'BUY,' and when it's 0, it means 'SELL.'
# arrange it in a table by ranking

return_prompt = """
The Recommend results from QuantMo.AI are as follows: 
The results are based on the calculation of the probability of the price increasing.

Today's Recommend results: 
{result}

"""
stock_info_prompt = """Rank {ranking}. {ticker}, Probability of Price Increasing:{prob}
"""


class StockRecommendToolInput(BaseModel):
    n_stocks: int = Field(description="desired quantity of stocks", default=5)
    

class StockRecommendTool(BaseTool):
    name="StockRecommendTool"
    description="This tool provide today's recommended stocks"
    
    def _run(self, n_stocks:int):
        return self._arun(n_stocks)
    
    async def _arun(self, n_stocks:int):
        result = ""
        engine = create_engine(ssh)
        async with create_async_session(engine) as session:
            try:
                signal_crud = SignalCRUD(session)
                date = datetime.now().strftime('%Y-%m-%d')
                
                recommended = await signal_crud.get_sorted_signals_by_date(date=date)
                for i in range(min(len(recommended), n_stocks)):
                    stock = recommended[i].__dict__
                    print(stock)
                    result += stock_info_prompt.format(
                        ranking= i + 1,
                        ticker=stock['ticker'],
                        signal=stock['signals'],
                        prob=stock['prob']
                        )
                    
            except Exception as e:
                print(f"An error occurred: {e}")
                return f"An error occurred: {e}"
                
        await engine.dispose()
        
        if result == "":
            result = "Today's RECOMMENDED stock will be released at 5PM"
            return result
        return return_prompt.format(result=result)
