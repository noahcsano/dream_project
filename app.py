from flask import Flask, redirect, url_for

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return "Home Page!"

@app.route("/about")
def about():
    return "About Page!"

if __name__ == '__main':
    app.run(debug=True)