from flask import Flask, redirect, url_for, render_template, request, session
import google_api

app = Flask(__name__)
app.static_folder = "static"
cart = {}

sheets = google_api.main()

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/categories", methods = ["GET", 'POST'])
def category():
    if request.method == 'POST':
        category = request.form['cat']
        return redirect(url_for('sub_cat', cat=category))
    return render_template('categories.html', categories=sheets.keys())

@app.route('/sub_categories/<cat>', methods = ["GET", 'POST'])
def sub_cat(cat):
    if request.method == 'POST':
        sub_cat = request.form['filter']
        return redirect(url_for('survey_Qs', category=cat, sub_category=sub_cat))
    else:
        return render_template('sub_cat.html', category=cat, sub_cats=sheets[cat].keys())

@app.route('/survey_Qs/<category>/<sub_category>')
def survey_Qs(category, sub_category):
    return render_template('Survey_Qs.html', Qs=sheets[category][sub_category])

@app.route("/about")
def about():
    return render_template('about.html')

# Add to Cart route
@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = {}

    if product_id not in session['cart']:
        session['cart'][product_id] = 1
    else:
        session['cart'][product_id] += 1

    return 'Product added to cart!'

if __name__ == '__main__':
    app.run(debug=True)