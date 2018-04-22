from flask import Flask, request, render_template
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup
import datetime


@app.route("/")
def hello():

    build_url="https://download.clearlinux.org/current/latest"
    current_build = requests.get(build_url).text

    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
   
    status = get_status()

    render = render_template('index.html', \
            current_build=current_build, \
            date=date,\
            status=status)
    
    return render


def get_status():
    # based on the % of perfomrance we decide if the build pass or not form the
    # PNP perspective
    return "PASS"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)

