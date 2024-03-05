from fastapi import FastAPI
from fastapi import Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from MofinChatBot.OpenAIServices import OpenAIServices, MessageWithHistory
from MofinChatBot.callbacks.AgentFinishCallbacks import AgentFinishCallback

from starlette.requests import Request
import datetime
from pydantic import BaseModel
import markdown
import asyncio

from db.connection import _setup_db
from db.db_crud import ChatCRUD
from router.AIServices import ai_service
from Services.dependencies import chat_crud

from utils.stream_generator import create_gen
from db.SSH_connection import *


class Message(BaseModel):
    content: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 여기에 허용할 도메인 또는 오리진 목록을 추가 (모두 허용할 경우 "*" 사용)
    allow_credentials=False,  # 자격 증명 (예: 쿠키)를 허용할 경우 True로 설정
    allow_methods=["*"],  # 허용할 HTTP 메서드 (GET, POST, 등) 목록
    allow_headers=["*"],  # 허용할 HTTP 헤더 목록
)
app.include_router(ai_service)

chatservice = OpenAIServices()

ssh = SSHConnection()
# signal_provider = TradingSignalProvider()


@app.on_event("shutdown")
def shutdown() -> None:  # noqa: WPS430
    print('shutdown')
    app.state.db_engine.dispose()
    ssh.disconnect()

@app.on_event("startup")
async def startup():
    print('startup')

    _setup_db(app,ssh)
    # # scheduler.add_job(cron_job2, 'cron', hour=17, minute=30)
    # scheduler.add_job(cron_job2, 'interval', seconds=10)
    # scheduler.start()
   

app.mount("/templates", StaticFiles(directory="templates"), name="templates")

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root(request: Request):
    # 템플릿 렌더링 및 HTML 반환
    return templates.TemplateResponse("index.html", {"request": request, "name": "MofinChat"})

@app.post("/chat")
async def chat(msg: MessageWithHistory):
    response = chatservice.run_agent(msg)
    # response = chatservice.agent.run(f"{datetime.datetime.now().strftime('%Y-%m-%d')}" + msg.content)
    html_text = markdown.markdown(response, extensions=["tables"])
    return html_text
    
@app.post("/streaming")
async def chat(msg: MessageWithHistory,
               chat_crud: ChatCRUD = Depends(chat_crud)):

    # callback_handler = StreamCallbackHandler()
    callback_handler = AgentFinishCallback(crud=chat_crud, usr_msg=msg.content)
    
    # chatservice.llmCallbacksSetter(callback_handler)

    streaming_generator = create_gen(chatservice, msg, callback_handler)

    return StreamingResponse(streaming_generator, media_type="text/event-stream")


# def run_app():
#     uvicorn.run("main:app", host="127.0.0.1", port=8000, workers=4)
    
# def main():
#     app_process = multiprocessing.Process(target=run_app)
#     app_process.start()
    
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(cron_job2, 'cron', hour=17, minute=30)
#     scheduler.start()
    
#     app_process.join()
    
# if __name__ == "__main__":
#     main()