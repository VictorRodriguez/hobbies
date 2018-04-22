from flask import Flask
app = Flask(__name__)
 
@app.route("/")
def hello():
    return "hi there"

if __name__ == "__main__":
    #app.run()
    app.run(host='0.0.0.0', port=8080, debug=True)

