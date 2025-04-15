import os
import pandas as pd
import json
from flask import Flask, render_template
import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta, MO
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_api_key():
    api_key = os.getenv("FMP_API_KEY")
    if not api_key:
        raise ValueError("API key not found in environment variables")
    return api_key
    
def get_sp500_earnings_calendar(start_date, end_date):
    apikey = get_api_key()
    url = f'https://financialmodelingprep.com/api/v3/sp500_constituent?apikey={apikey}'
    r = requests.get(url)
    sp500_members = pd.DataFrame(json.loads(r.text))

    url = f'https://financialmodelingprep.com/api/v3/earning_calendar?from={start_date}&to={end_date}&apikey={apikey}'
    r = requests.get(url)
    r_data = json.loads(r.text)
    earning_calendar = pd.DataFrame(r_data)

    con1 = earning_calendar.symbol.isin(sp500_members['symbol'].tolist())
    sp500_earning_calendar = earning_calendar[con1].reset_index(drop=True)
    
    # Merge with sp500_members to get name and sector
    sp500_earning_calendar = pd.merge(
        sp500_earning_calendar, 
        sp500_members[['symbol', 'name', 'sector']], 
        on='symbol', 
        how='left'
    )
    
    return sp500_earning_calendar    

def get_calendar_data(year, month):
    first_day_of_month = datetime(year, month, 1)
    last_day_of_month = datetime(year, month, 1) + relativedelta(months=1, days=-1)
    
    start_date_str = first_day_of_month.strftime('%Y-%m-%d')
    end_date_str = last_day_of_month.strftime('%Y-%m-%d')

    sp500_earnings_calendar = get_sp500_earnings_calendar(start_date_str, end_date_str)
    
    calendar_data = {}
    for _, row in sp500_earnings_calendar.iterrows():
        report_date = datetime.strptime(row['date'], '%Y-%m-%d').date()
        date_str = report_date.strftime('%Y-%m-%d')
        if date_str not in calendar_data:
            calendar_data[date_str] = []
        
        company_info = {
            'symbol': row['symbol'],
            'name': row['name'],
            'sector': row['sector'],
            'fiscalDateEnding': row.get('fiscalDateEnding', 'N/A'),
            'epsEstimated': row.get('epsEstimated', 'N/A'),
            'revenueEstimated': row.get('revenueEstimated', 'N/A')
        }
        calendar_data[date_str].append(company_info)
    
    first_day_of_calendar = first_day_of_month + relativedelta(weekday=MO(-1))
    last_day_of_calendar = last_day_of_month + relativedelta(weekday=MO(+1))
    current_date = first_day_of_calendar
    
    calendar_days=[]
    while current_date<=last_day_of_calendar:
      calendar_days.append(current_date)
      current_date+=relativedelta(days=1)
    
    return calendar_days, calendar_data

app = Flask(__name__)

@app.route("/<int:year>/<int:month>")
@app.route("/", defaults={'year': datetime.now().year, 'month': datetime.now().month})
def index(year, month):
    calendar_days, calendar_data = get_calendar_data(year, month)
    return render_template('index.html', calendar_days=calendar_days, calendar_data=calendar_data, current_year=year, current_month=month, today = datetime.today().day)

def main():
    app.run(host='0.0.0.0', port=8080, debug=True)

if __name__ == '__main__':
    main() 