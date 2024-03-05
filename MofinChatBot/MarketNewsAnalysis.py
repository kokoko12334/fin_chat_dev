from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from db.connection import create_async_session, create_engine
from db.SSH_connection import ssh
from db.db_crud import MarketNewsAnalysisCRUD
prompt = """
{report}


"""
class MarketNewsAnalysisTool(BaseTool):
    
    name = "MarketNewsAnalysisTool"
    
    description = """
        Use this tool to get analysis(Hot Issue, Sector) based on recent market news."
    """
    
    def _run(self):
        
        return {}
    
    async def _arun(self):
        engine = create_engine(ssh)
        async with create_async_session(engine) as session:
            try:
                crud = MarketNewsAnalysisCRUD(session)
                
                res = await crud.get_latest_news_analysis()
                analysis = res[0].analy
                
            except Exception as e:
                return "Failed to get MarketNews Analysis."
            
        # print(analysis)
        await engine.dispose()
        return analysis