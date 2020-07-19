from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return '<p style="font-size:2em; margin:40px; background-color:yellow">Here comes a game that will help you to understand the concept of *expected value*. \
    <br> Also, why most people lose in casinos. \
    <br><br> Stay tuned! \
    <br><br> (Stack: Python + Flask + nginx)</p>'

if __name__ == "__main__":
    app.run(host='0.0.0.0')