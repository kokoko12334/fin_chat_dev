from settings import settings
import finnhub

from datetime import datetime
finnhub_client = finnhub.Client(api_key=settings.FINNHUB_API_KEY)


def get_general_news(category='general', min_id=0):
    
    res = finnhub_client.general_news('general', min_id=min_id)
    news_data = []
    for i in res:
        unix_time = i['datetime']
        # print(i)
        news_time = datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d')
        news_data.append(f"headline:{i['headline']}, summary:{i['summary']},article_time:{news_time}")

    if res:
        last_id = res[0]['id']
    else:
        last_id=min_id
        
    return news_data, last_id