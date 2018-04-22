from flask import Flask, request, render_template
app = Flask(__name__)
 
@app.route("/")
def hello():
    animal = "dog"
    return render_template('index.html', value=animal)

if __name__ == "__main__":
    #app.run()
    app.run(host='0.0.0.0', port=8080, debug=True)

