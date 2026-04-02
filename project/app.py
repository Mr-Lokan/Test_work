import requests
from flask import Flask, render_template
from datetime import datetime, timedelta

app = Flask(__name__)

PANDASCORE_TOKEN = 'qSBN029vUrCqqZtlz1_lsuI_NJACcmMhVPdDa7DLlk-fbHuXi5k' 
BASE_URL = "https://api.pandascore.co/matches"

def get_matches(date_str):
    headers = {"Authorization": f"Bearer {PANDASCORE_TOKEN}"}
    params = {
        "range[begin_at]": f"{date_str}T00:00:00Z,{date_str}T23:59:59Z",
        "sort": "begin_at"
    }
    response = requests.get(BASE_URL, headers=headers, params=params)
    return response.json() if response.status_code == 200 else []

@app.route('/matches/<day_type>')
def show_matches(day_type):
    today = datetime.utcnow()
    
    if day_type == 'yesterday':
        target_date = today - timedelta(days=1)
        title = "Матчи за вчера"
    elif day_type == 'tomorrow':
        target_date = today + timedelta(days=1)
        title = "Матчи на завтра"
    else:
        target_date = today
        title = "Матчи на сегодня"
        day_type = 'today'

    date_str = target_date.strftime('%Y-%m-%d')
    matches = get_matches(date_str)
    
    # SEO Данные
    seo = {
        "title": f"{title} - Киберспортивный портал",
        "description": f"Результаты и расписание киберспортивных матчей за {date_str}.",
        "url": f"https://yourdomain.com/matches/{day_type}"
    }

    return render_template('index.html', matches=matches, seo=seo, title=title, date=date_str)

if __name__ == '__main__':
    app.run(debug=True)