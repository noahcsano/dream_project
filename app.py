from flask import Flask, redirect, url_for, render_template
import google_api

app = Flask(__name__)

sheets = google_api.main()

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/categories")
def category():
    return render_template('categories.html', categories=sheets.keys())

@app.route("/about")
def about():
    return render_template('about.html')

if __name__ == '__main':
    app.run(debug=True)