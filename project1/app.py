from flask import Flask, render_template
from dotvenv import load_dotvenv
import requests
import os

load_dotvenv()
API_KEY = os.getvenv("APIKEY")
url = "https://api.api-ninjas.com/v2/randomquotes?categories=success,wisdom"
headers={'X-Api-Key': API_KEY}

def get_quote():
    response = requests.get(url, headers=headers)
    data = response.json()
    if isinstance(data, list) and len(data) > 0:
        quote_value=data[0]['quote']
        author_value=data[0]['author']
        category_value=data[0]['category']
        return quote_value, author_value, category_value
    else:
        return "No quote found", "Unknown", "Unknown"

app = Flask(name)

@app.route('/')
def home():
    quote, author, category = get_quote()
    return render_template('ai_quote.html', quote=quote, author=author, category=category)

@app.route('/login')
def Login():
    return render_template('login.html')

@app.route('/regristration')
def Registration():
    return render_template('registration.html')


if name == 'main':
    app.run(debug=True)