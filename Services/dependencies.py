from sqlalchemy.ext.asyncio import AsyncSession
from db.db_crud import SignalCRUD, ChatCRUD, MarketNewsAnalysisCRUD
from fastapi import Depends
from db.dependencies import get_db_session
from datetime import datetime
from utils.db_infos import get_ticker_list
from Services.TradingSignal.TradingSignalProvider import generate_all_signals
from Services.TradingSignal.TradingSignalProvider import ticker_list
from Services.MarketNewsAnalysis.market_news_analysis import make_market_news_analysis, update_market_news_analysis

def signal_crud(
    session: AsyncSession = Depends(get_db_session)
) -> SignalCRUD:
    print(session)
    return SignalCRUD(session)

def chat_crud(
    session: AsyncSession = Depends(get_db_session)
) -> ChatCRUD:
    return ChatCRUD(session)

async def create_signal(
    ticker : str,
    signal : int,
    prob : float,
    ranking: int,
    session: AsyncSession
):
    crud = SignalCRUD(session)
    date = datetime.now().strftime('%Y-%m-%d')
    await crud.create_signal(ticker, signal, prob, ranking, date)

async def save_signals(
    session: AsyncSession
):
    print(session)
    print('save!!')
    result = await generate_all_signals()
    for ticker in ticker_list:
        signal, percent, rank = result[ticker]
        print(ticker, signal, percent, rank)
        await create_signal(
            ticker, signal, percent, rank, session
        )

async def save_market_news_analysis(
    session: AsyncSession
):
    now = datetime.now().strftime('%Y-%m-%d-%Hh')
    print(now)
    report = make_market_news_analysis(now)
    print(report)
    crud = MarketNewsAnalysisCRUD(session)
    
    await crud.create_news_analysis(
        analysis=report,
        date=now
    )

async def update_analysis(
    session: AsyncSession
):
    now = datetime.now().strftime('%Y-%m-%d-%Hh')
    crud = MarketNewsAnalysisCRUD(session)

    existing_report = await crud.get_latest_news_analysis()
    
    # print(existing_report)
    # print(existing_report[0].analy)
    report = existing_report[0].analy
    new_report = update_market_news_analysis(report, now)
    
    await crud.create_news_analysis(
        analysis=new_report,
        date=now
    )

# async def get_signal(
#     ticker : str,
#     crud : SignalCRUD = Depends(signal_crud)
# ):
#     try:
#         await crud.get_signal(ticker)
#     except:
#         return 'GET Signal Error!'