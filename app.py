from flask import Flask, redirect, url_for, render_template
import google_api

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/categories")
def category():
    sheets = google_api.main().keys()
    return render_template('categories.html', categories=sheets)

@app.route("/about")
def about():
    return "About Page!"

if __name__ == '__main':
    app.run(debug=True)