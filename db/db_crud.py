from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, delete

from db.models import TradingSignal, ChatLog, CompanyInfo, MarketNewsAnalysis

from datetime import datetime

class DBCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session
    

class SignalCRUD(DBCRUD):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        
    async def create_signal(self, ticker:str, signal : int, prob:float, ranking: int, date:str):
        # delete with same ticker and date
        condition = and_(
            TradingSignal.ticker == ticker,
            TradingSignal.date == date
        )
        await self.session.execute(delete(TradingSignal).where(condition))
        
        return await TradingSignal(
            ticker=ticker, signals=signal,
            ranking=ranking, prob=prob, date=date
        ).save(self.session)
    
    async def get_signal(self, ticker:str, date:str):
        query = select(TradingSignal).filter(
            and_(
                TradingSignal.ticker == ticker,
                TradingSignal.date == date
            )
        )
        return (await self.session.execute(query)).scalars().all()
    
    async def get_sorted_signals_by_date(self, date:str):
        query = select(TradingSignal).filter(
            TradingSignal.date == date
        ).order_by(TradingSignal.ranking)
        return (await self.session.execute(query)).scalars().all()
    

class ChatCRUD(DBCRUD):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        
    async def create_chat(
        self, usr_seq:int, chat_question:str,
        chat_reply:str, rating:int):
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return await ChatLog(
            usr_seq=usr_seq, chat_question=chat_question,
            chat_reply=chat_reply, rating=rating, date=date
        ).save(self.session)

class CompanyInfoCRUD(DBCRUD):
    
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        
    async def get_report_by_ticker(self, ticker:str):
        query = select(CompanyInfo.report).filter(
            CompanyInfo.ticker == ticker
        )

        return (await self.session.execute(query)).fetchone().tuple()
    
date_format = "%Y-%m-%d-%Hh"

# 문자열을 DateTime 객체로 변환
class MarketNewsAnalysisCRUD(DBCRUD):
    
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        
    async def get_news_analysis(self, date):
        date_object = datetime.strptime(date, date_format)
        
        query = select(MarketNewsAnalysis).filter(
            MarketNewsAnalysis.date == date_object
        )
        
        return (await self.session.execute(query)).fetchone().tuple()
    
    async def get_latest_news_analysis(self):
        query = select(MarketNewsAnalysis).order_by(
            MarketNewsAnalysis.date.desc()
            ).limit(1)
        
        return (await self.session.execute(query)).fetchone().tuple()
    
    async def create_news_analysis(self, analysis, date):
        date_object = datetime.strptime(date, date_format)
        
        return await MarketNewsAnalysis(
            analy=analysis, date=date_object
        ).save(self.session)