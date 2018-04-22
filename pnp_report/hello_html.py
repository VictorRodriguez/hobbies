from flask import Flask, request, render_template
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup


@app.route("/")
def hello():
    build_url="https://download.clearlinux.org/current/latest"
    current_build = requests.get(build_url).text
    return render_template('index.html', current_build=current_build)

if __name__ == "__main__":
    #app.run()
    app.run(host='0.0.0.0', port=8080, debug=True)

