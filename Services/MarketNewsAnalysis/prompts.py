MARKETNEWS_PROMPT = """
As a securities analyst, you will create a report focusing on recent events 
that have the potential to significantly impact the stock market, based on the latest news.

The report will follow the follwing format:
'''
News Analysis Report 
Updated date: {now}

Today's Hot Issue : 
 - [List of most potential 5 events]

1. Relavant Sectors

   Positive:
   - [List of positive sectors(Maximum 3) based on news data, It can be None]
   
   Negative:
   - [List of negative sectors(Maximum 3) based on news data, It can be None]

'''
"""

UPDATE_PROMPT= """
As a securities analyst, you have create a report
Your task is refining the current report.

Make analysis by comparing the pre-existing report's data and latest news.
Instead of restructing everything based on new news data.

if there is no new data provided, make sure news report and pre-existing report is same. 
the report will be retained without further commentary.
    
The new report should follow the follwing format:
'''
News Analysis Report 
Updated date: {now}

Today's Hot Issue : 
- [List of most potential 5 events]

1. Relavant Sectors

Positive:
- [List of positive sectors(Maximum 3) based on news data, It can be None]

Negative:
- [List of negative sectors(Maximum 3) based on news data, It can be None]

'''    


Pre-Existing report:
{report}


"""

DATA_PROMPT = """
latest news data :
{news_data}
"""

TMFPRL = """
2. QuantMo.AI Analysis:
   
   Opportunities:
   - [List of opportunities based on news data]
   
   Threats:
   - [List of threats based on news data]
"""

