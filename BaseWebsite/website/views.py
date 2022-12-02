from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user

# import nasapy
# import os
from datetime import datetime
# import urllib.request
#from gtts import gTTS
import requests, json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    # stores APi key and Api URL
    nasakey = "l1YsgpdqqiBEXpx1IqHfEp1DkqgysDrBvzjIeKVR"
    url = 'https://api.nasa.gov/planetary/apod?'
    
    if request.method == 'POST':
        date_changed = request.form.get('dateInput')    # type: ignore
        # if there is user input, get the date and enter into parameters
        if date_changed:
            date_changed = datetime.strptime(date_changed, '%m/%d/%Y').date()
        params={
            'api_key': nasakey,
            'hd': 'True',
            'date': date_changed
         } 
    else:
        params={
            'api_key': nasakey,
            'hd': 'True',
            'date': datetime.today().strftime('%Y-%m-%d')
    }

    response = requests.get(url, params=params)
    # data has copyright, date, explaination, hdurl, media_type, service_version, title, url
    data = response.json()
    print(data)
        
    return render_template("home.jinja", user=current_user, data=data)
