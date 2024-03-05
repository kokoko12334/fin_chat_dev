# MofinChat

## Python Environment 설정
~~~
conda install -n <env-name> python=3.10
conda activate <env-name>
cd MofinChat
pip install -r requirements.txt
~~~

## secrets 파일 설정
.streamlit 폴더 내에서 secrets.toml 파일 생성
OPENAI_API_KEY 등 설정

## streamlit Application 실행
~~~
streamlit run streamlit_app.py
~~~


## FASTAPI APP 실행 - BY gunicorn

gunicorn_config.py 에서 daemon=True면 background에서 동작함 - (log 확인은 log파일을 통해.. )
- logger 세팅하기
~~~
gunicorn main:app -c gunicorn_config.py
~~~


# 서버 실행

- 서버 접속

- 실행 환경 설정
```shell
conda activate chatbot-env
cd MofinChat
```

- 서버 실행
```shell
# gunicorn으로 실행된 프로세스 확인
ps -ef | grep gunicorn
# 만약 grep을 제외하고 프로세스가 존재한다면 kill 하고나서 실행하기

pkill -f gunicorn
# gunicorn 실행된 것 꺼질 때까지 기다리기 (!ps 계속 실행해서 확인)

# fastapi app gunicorn을 통해 실행
gunicorn main:app -c gunicorn_config.py

```

- 매매 시그널 저장하는 로직 실행

```shell
# 매매시그널 저장 로직 실행
python save_signals.py
# COMMIT 나오는 것 까지 확인하기
# 중간에 에러나면 다시 실행하기
```