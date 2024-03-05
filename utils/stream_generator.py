from datetime import datetime
from utils.generate_chat_history import generate_chat_history
import asyncio
from MofinChatBot.OpenAIServices import OpenAIServices
from pydantic import BaseModel
async def create_gen(service: OpenAIServices, msg: BaseModel, callback_handler):
    task = asyncio.create_task(
        service.arun_agent(message=msg, callbacks=[callback_handler])
        )
    #데이터를 받고 넘기는 비동기 제너레이터
    try:
        async for token in callback_handler.aiter():
            yield token
    finally:
        #큐에 데이터를 넣는 태스크
        
        await task
    #제너레이터가 먼저 실행되어야 함. await를 먼저 두면 병렬처리가 안됨