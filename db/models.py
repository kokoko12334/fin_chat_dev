from sqlalchemy import String, Integer, Float, BigInteger, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from db.base import Base

from datetime import datetime


class TradingSignal(Base):
    """
    create table tbs_trading_signal_log (    
	  signal_seq BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY comment '신호순번'
    , ticker VARCHAR(50) comment '종목코드'
    , signals INT comment '신호'
    , prob FLOAT comment '확률'
    , ranking INT comment '순위'
    , date DATE comment '일시')
    comment '매매신호내역' engine=innodb DEFAULT CHARSET=utf8mb4;
    """
    __tablename__ = "tbs_trading_signal_log"
    
    signal_seq: Mapped[str] = mapped_column(
        BigInteger, primary_key=True,
        autoincrement=True, nullable=False)
    
    ticker = mapped_column(String(50), nullable=False)
    signals = mapped_column(Integer, nullable=False)
    prob = mapped_column(Float, nullable=False)
    ranking = mapped_column(Integer, nullable=False)
    date = mapped_column(String(10), nullable=False)

class ChatLog(Base):
    """
    CREATE TABLE tbs_chat_log (
        chat_seq BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY comment '채팅순번',
        usr_seq BIGINT comment '사용자순번',
        chat_question VARCHAR(128) COMMENT '채팅질문',
        chat_reply LONGTEXT COMMENT '채팅답변',
        rating INT COMMENT '선호'
    ) COMMENT '채팅내역' ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """
    __tablename__ = "tbs_chat_log"
    
    chat_seq: Mapped[str] = mapped_column(
        BigInteger, primary_key=True,
        autoincrement=True, nullable=False)
    
    usr_seq = mapped_column(BigInteger, nullable=False)
    chat_question = mapped_column(String(128), nullable=False)
    chat_reply = mapped_column(Text, nullable=False)
    rating = mapped_column(Integer, nullable=True)
    date = mapped_column(String(10), nullable=False)

class CompanyInfo(Base):
    
    __tablename__ = "tbs_company_info"
    
    ticker: Mapped[str] = mapped_column(
        String(50), primary_key=True,
        nullable=False)
    
    company_nm = mapped_column(String(50), nullable=False)
    stock_exchange_nm = mapped_column(String(512), nullable=False)
    company_desc = mapped_column(Text, nullable=False)
    sector = mapped_column(String(512), nullable=False)
    tags = mapped_column(String(512), nullable=False)
    cntry = mapped_column(String(512), nullable=False)

    report = mapped_column(Text, nullable=False)
    

class MarketNewsAnalysis(Base):
    """
    CREATE TABLE tbs_national_news_analy (
    analy_seq BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY comment '뉴스분석순번',
    market_news_analy varchar(512) NOT NULL COMMENT '시장뉴스분석',
    analy longtext NOT NULL COMMENT '분석내용',
    date date DEFAULT NULL COMMENT '분석일시'
    ) COMMENT '국제뉴스분석' ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """
    __tablename__ = "tbs_national_news_analy"
    
    analy_seq: Mapped[str] = mapped_column(
        BigInteger, primary_key=True,
        autoincrement=True, nullable=False)
    
    analy = mapped_column(Text, nullable=False)
    date = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
