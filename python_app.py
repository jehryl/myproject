from flask import Flask, render_template, request, redirect, url_for, session
from flask_oauthlib.client import OAuth
import requests
from pytrends.request import TrendReq
import os
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest
import io
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from datetime import datetime,timedelta
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'random_secret_key'

oauth = OAuth(app)

google = oauth.remote_app(
    'google',
    consumer_key="812917638396-4qoqndq1bjskmgro5ga8j32rl5ekh14h.apps.googleusercontent.com",
    consumer_secret="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",
    request_token_params={
        'scope': 'https://www.googleapis.com/auth/analytics.readonly'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

last_message = ''


@app.route('/')
def hello_world():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f0f0f0;
                margin: 0;
                padding: 0;
                text-align: center;
            }

            header {
                background-color: #007BFF;
                padding: 20px 0;
            }

            header h1 {
                color: #fff;
            }

            .container {
                margin: 20px;
                padding: 20px;
                background-color: #fff;
                border-radius: 5px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }

            a {
                text-decoration: none;
                color: #007BFF;
                margin: 10px;
            }

            button {
                background-color: #007BFF;
                color: #fff;
                border: none;
                padding: 10px 20px;
                cursor: pointer;
                border-radius: 5px;
                font-size: 16px;
                margin: 10px;
            }

            button:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>
        <header>
            <h1>Mon Application Web</h1>
        </header>
        <div class="container">
            <a href="/logger">Accéder au Journal</a>
            <a href="/google-request">Effectuer une Requête Google / Analytics</a>
            <a href="/chart-image">Acceder au Chart</a>

        </div>
    </body>
    </html>
    """


@app.route('/login')
def login():
    return google.authorize(callback=url_for('authorized', _external=True))



@app.route('/logger', methods=['GET', 'POST'])
def logger():
    global last_message

    if request.method == 'POST':
        last_message = request.form['log_message']
        app.logger.warning(f"Message de journal depuis Python : {last_message}")

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f0f0f0;
                margin: 0;
                padding: 0;
                text-align: center;
            }

            header {
                background-color: #007BFF;
                padding: 20px 0;
            }

            header h1 {
                color: #fff;
            }

            .container {
                margin: 20px;
                padding: 20px;
                background-color: #fff;
                border-radius: 5px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }

            a {
                text-decoration: none;
                color: #007BFF;
                margin: 10px;
            }

            form {
                margin: 20px 0;
            }

            label {
                display: block;
                margin-bottom: 10px;
            }

            input[type="text"] {
                width: 100%;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }

            input[type="submit"] {
                background-color: #007BFF;
                color: #fff;
                border: none;
                padding: 10px 20px;
                cursor: pointer;
                border-radius: 5px;
                font-size: 16px;
                margin: 10px;
            }

            input[type="submit"]:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>
        <header>
            <h1>Journal</h1>
        </header>
        <div class="container">
            <a href="/">Retour à la page d'accueil</a>
            <a href="/chart-image">Acceder au Chart</a>
            <a href="/google-request">Effectuer une requête Google</a>
            <form method="POST">
                <label for="log_message">Message de journal : </label>
                <input type="text" id="log_message" name="log_message">
                <input type="submit" value="Enregistrer">
            </form>""" +f"<p>Dernier message enregistré : {last_message}</p>"  +"""</div>
    </body>
    </html>
    """


@app.route('/google-request', methods=['GET', 'POST'])
def google_request():
    cookies_str = ""

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'digitaltracestp-244261c91180.json'
    PROPERTY_ID = '407448032'
    starting_date = "28daysAgo"
    ending_date = "yesterday"

    client = BetaAnalyticsDataClient()
    
    def get_visitor_count(client, property_id):
        request = RunReportRequest(
            property=f"properties/{property_id}",
            date_ranges=[{"start_date": starting_date, "end_date": ending_date}],
            metrics=[{"name": "activeUsers"}]
        )

        response = client.run_report(request)
        
        return response
    # Hi

    # Get the visitor count using the function
    response = get_visitor_count(client, PROPERTY_ID)

    if response and response.row_count > 0:
        metric_value = response.rows[0].metric_values[0].value
    else:
        metric_value = 0  # Handle the case where there is no data

    if request.method == 'POST':
        action = request.form.get('action')

        if action == "google_request":
            req = requests.get("https://www.google.com/")
            cookies_str = str(req.cookies._cookies)

        elif action == "ganalytics_request":
            req2 = requests.get("https://analytics.google.com/analytics/web/#/p407461953/reports/intelligenthome")
            cookies_str = str(req2.cookies._cookies)

        elif action == "visitors_number":
            return f'Number of visitors : {metric_value}'

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f0f0f0;
                margin: 0;
                padding: 0;
                text-align: center;
            }

            header {
                background-color: #007BFF;
                padding: 20px 0;
            }

            header h1 {
                color: #fff;
            }

            .container {
                margin: 20px;
                padding: 20px;
                background-color: #fff;
                border-radius: 5px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }

            a {
                text-decoration: none;
                color: #007BFF;
                margin: 10px;
            }

            form {
                margin: 20px 0;
            }

            input[type="submit"] {
                background-color: #007BFF;
                color: #fff;
                border: none;
                padding: 10px 20px;
                cursor: pointer;
                border-radius: 5px;
                font-size: 16px;
                margin: 10px;
            }

            input[type="submit"]:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>
        <header>
            <h1>Requêtes Google</h1>
        </header>
        <div class="container">
            <a href="/">Retour à la page d'accueil</a>
            <a href="/chart-image">Acceder au Chart</a>
            <a href="/logger">Accéder au journal</a>
            <form method="POST">
                <input type="submit" name="action" value="google_request" placeholder="Effectuer une requête Google">
                <input type="submit" name="action" value="ganalytics_request" placeholder="Effectuer une requête Google Analytics">
                <input type="submit" name="action" value="visitors_number" placeholder="Obtenir le nombre de visiteurs">
            </form>""" + f"<p>{cookies_str}</p>" + """</div>
    </body>
    </html>
    """

@app.route('/chart-image')
def chart_image():
    # Create a pytrends client and fetch data as previously mentioned
    pytrends = TrendReq(hl='en-US', tz=360, geo='FR')
    keywords = ['Jude Bellingham', 'Erling Haaland']
    timeframe = 'today 3-m'
    pytrends.build_payload(keywords, timeframe=timeframe)
    interest_over_time_df = pytrends.interest_over_time()

    # Create a time series chart
    plt.figure(figsize=(10, 6))
    for keyword in keywords:
        plt.plot(interest_over_time_df.index, interest_over_time_df[keyword], label=keyword)
    plt.xlabel('Date')
    plt.ylabel('Interest Over Time')
    plt.title('Google Trends Comparison')
    plt.legend()

    # Save the chart as an image
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    img_data = base64.b64encode(img_buffer.read()).decode()

    return f'<img src="data:image/png;base64,{img_data}" alt="Google Trends Chart">'

if __name__ == '__main__':
    app.run(debug=True)