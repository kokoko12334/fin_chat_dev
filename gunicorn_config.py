import os
import subprocess
        
wsgi_app = 'main:app'

workers = 4

worker_class= "uvicorn.workers.UvicornWorker"
logconfig = os.getcwd() + "/logs/uvicorn_log.ini"

daemon= True
timeout=90

bind = "0.0.0.0:8000"
def cron_job():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(script_dir, "save_signals.py")
    subprocess.call(["python3" , script_path])

def cron_job_market_news():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(script_dir, "test_market_news.py")
    subprocess.call(["python3" , script_path])

def on_worker_init(worker):
    from apscheduler.schedulers.background import BackgroundScheduler
    
    scheduler = BackgroundScheduler()
    scheduler.add_job(cron_job, 'cron', hour=17, minute=30)
    
    scheduler.add_job(cron_job, 'cron', hour=7, minute=30)
    
    # 3시간에 한번씩 실행
    scheduler.add_job(cron_job_market_news, 'interval', hours=3)
    # scheduler.add_job(cron_job_market_news, 'interval', seconds=10)
    # scheduler.add_job(cron_job, 'interval', seconds=10)
    scheduler.start()

def post_fork(server, worker):
    # server.log.info('worker attribute %s', vars(worker).keys())
    if not server.WORKERS:
        on_worker_init(worker)
        server.log.info("첫번째 worker, Worker spawned (pid: %s)", worker.pid)
    server.log.info("Worker spawned (pid: %s)", worker.pid)