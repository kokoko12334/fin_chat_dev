import pandas as pd

company_info = pd.read_csv('./Data/Company_info')
company_list = str(list(company_info.companyName)).replace("'","")
ticker_list = str(list(company_info.Ticker)).replace("'","")

def get_company_list():
    return company_list

def get_ticker_list():
    return ticker_list