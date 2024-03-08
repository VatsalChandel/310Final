from flask import Flask, render_template, request, session, redirect, url_for
import os
import requests
import urllib.request
import json
from bs4 import BeautifulSoup

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'


@app.route("/")
def login():
    return render_template("index.html")

@app.route("/submit-details", methods=["POST"])
def submit_login():
    form_data = request.form
    session['make'] = form_data['make']
    session['model'] = form_data['model']
    session['fuel'] = form_data['fuel']
    session['drive'] = form_data['drive']
    session['year'] = form_data['year']
    session['min_mpg'] = form_data['min_mpg']
    session['price_min'] = form_data['price_min']
    session['price_max'] = form_data['price_max']
    session['milage_high'] = form_data['milage_high']
    session['milage_low'] = form_data['milage_low']
    
    return redirect(url_for('submit-details'))


@app.route("/submit-details", methods=["POST"])
def submit_details():
    
    get_info(session['make'], session['model'], session['fuel'], session['drive'], session['year'], session['min_mpg'], session['price_max'], session['price_min'], session['milage_high'], session['milage_low'])

    #results = scrape(make, model, fuel, drive, year, min_mpg, price_max, price_min, milage_high, milage_low)
    
    results = "Results"
    return render_template("results.html", results=results)






def get_info(make=None, model=None, fuel=None, drive=None, year=None, min_mpg=None, price_max=None, price_min=None,  milage_high=None, milage_low=None,limit=5):
    """
    This function makes sure that we can find the make and model of a specific car to pass into the web scrapper to get more information
    """
    api_url = "https://api.api-ninjas.com/v1/cars?"
    if make:
        api_url += f"&make={make}"
    if model:
        api_url += f"&model={model}"
    if fuel:
        api_url += f"&fuel={fuel}"
    if year:
        api_url += f"&year={year}"
    if drive:
        api_url += f"&drive={drive}"
    if min_mpg:
        api_url += f"&min_mpg={min_mpg}"

    if api_url == "https://api.api-ninjas.com/v1/cars?":
        print("Invalid parameters")
        return 
    print(api_url)
    
    response = requests.get(api_url, headers={'X-Api-Key': 'yRJd6XVFaGA4Uq6N97xnmA==8wQXpzLdseHdo1uq'})
    if response.status_code == requests.codes.ok and response.text != '[]':
        data = json.loads(response.text)
        if not make:
            for i in range(1):
                make = data[i]["make"]
        
    model = model.replace(' ', "-")
    return (make.lower(), model.lower(), fuel, drive.upper(), year, min_mpg, price_max, price_min, milage_high, milage_low)
    
    
    
if __name__ == '__main__':
    app.run()