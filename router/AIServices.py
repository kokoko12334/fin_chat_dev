from fastapi import APIRouter
from fastapi import Depends
from db.db_crud import SignalCRUD
from Services.dependencies import signal_crud
from pydantic import BaseModel
from datetime import datetime


class StockQuery(BaseModel):
    ticker: str
    date: str
    
ai_service = APIRouter(prefix='/ai')

@ai_service.post('/signal')
async def get_signal(
    Stock : StockQuery,
    crud : SignalCRUD = Depends(signal_crud)
):
    try:
        if not Stock.date:
            Stock.date = datetime.now().strftime('%Y-%m-%d')
        return await crud.get_signal(Stock.ticker, Stock.date)
    except Exception as e:
        print(e)
        return 'GET Signal Error!'

@ai_service.get('/recommend')
async def get_trading_recommend(
    crud : SignalCRUD = Depends(signal_crud)
):
    # 아직 업데이터 되지 않아서 데이터가 없다면??
    # 매매 신호 저장 일정 언제?
    date = datetime.now().strftime('%Y-%m-%d')
    return await crud.get_sorted_signals_by_date(date=date)
    # await get_stock_recommend()