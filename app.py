from flask import Flask, redirect, url_for, render_template, request
import google_api

app = Flask(__name__)
app.static_folder = "static"

sheets = google_api.main()

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/categories", methods = ["GET", 'POST'])
def category():
    if request.method == 'POST':
        category = request.form['input']
        return redirect(url_for('sub_cat', cat=category))
    return render_template('categories.html', categories=sheets.keys())

@app.route('/sub_categories/<cat>')
def sub_cat(cat):
    return render_template('sub_cat.html', sub_cats=sheets[cat].keys())

@app.route("/about")
def about():
    return render_template('about.html')

if __name__ == '__main':
    app.run(debug=True)