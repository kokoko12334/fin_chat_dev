from Services.MarketNewsAnalysis.prompts import (
    MARKETNEWS_PROMPT,
    UPDATE_PROMPT,
    DATA_PROMPT
)

def make_market_news_report_prompt(now):
    return MARKETNEWS_PROMPT.format(now=now)

def make_news_data_prompt(news_data):
    return DATA_PROMPT.format(news_data=news_data)

def make_update_prompt(existing_report, now):
    return UPDATE_PROMPT.format(report=existing_report, now=now)