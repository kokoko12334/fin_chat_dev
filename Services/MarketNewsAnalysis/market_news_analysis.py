from Services.MarketNewsAnalysis.get_market_news import get_general_news
from Services.MarketNewsAnalysis.chat_completion import make_chat_completion
from Services.MarketNewsAnalysis.make_messages import (
    make_market_news_report_prompt,
    make_news_data_prompt,
    make_update_prompt
)


def save_news_last_id(last_id):
    with open("./Data/market_news/id.txt", "w") as f:
        f.write(str(last_id))
        
def load_news_last_id():
    with open("./Data/market_news/id.txt", 'r') as f:
        id = int(f.read())
    return id

def make_market_news_analysis(now):
    
    min_id = 0
    news_data, last_id = get_general_news(min_id=min_id)
    
    report_prompt = make_market_news_report_prompt(now=now)
    news_data_prompt = make_news_data_prompt(news_data)
    report = make_chat_completion(
        system_prompt=report_prompt,
        data_prompt=news_data_prompt)
    
    save_news_last_id(last_id)
    
    return report

def update_market_news_analysis(existing_report, now):
    try:
    # try:
        last_news_id = load_news_last_id()
        news_data, last_id = get_general_news(min_id=last_news_id)
        
        report_prompt = make_update_prompt(
            existing_report=existing_report,
            now=now)
        
        news_data_prompt = make_news_data_prompt(news_data)
        
        report = make_chat_completion(
            system_prompt=report_prompt,
            data_prompt=news_data_prompt)
        
        save_news_last_id(last_id)
            
    except Exception:
        raise Exception("Failed to update market news analysis")
        
    return report
