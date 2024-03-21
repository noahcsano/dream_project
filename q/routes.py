import pickle
from flask import Flask, redirect, url_for, render_template, request, session, flash
import q.google_api as google_api
from q import app

app.static_folder = "static"

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
    return render_template('categories.html', categories=sheets.keys(), categ=True)

@app.route('/sub_categories/<cat>', methods = ["GET", 'POST'])
def sub_cat(cat):
    if request.method == 'POST':
        sub_cat = request.form['sub_category']
        return redirect(url_for('survey_Qs', category=cat, sub_category=sub_cat))
    else:
        return render_template('categories.html', category=cat, sub_cats=sheets[cat].keys(), s_cat=True)

@app.route('/survey_Qs/<category>/<sub_category>', methods = ["GET", 'POST'])
def survey_Qs(category, sub_category):
    if 'cart' not in session:
        session['cart'] = []
    if request.method == 'POST':
        cart = session.get('cart', [])
        q_obj = None
        q = request.form['q']
        q_obj = q
        '''
        for item in sheets[category][sub_category]:
            if str(item) == q:
                q_obj = item
        '''
        if q_obj:
            if q_obj in session['cart']:
                flash("The selected question is already in your cart. Please choose another question, or proceed to checkout by selecting the cart tab if you have finished.")
            else:
                session['cart'].append(q_obj)
                flash("The question has been added to your cart.")
    return render_template('categories.html', Qs=sheets[category][sub_category], category=category, sub_category=sub_category)

@app.route("/about")
def about():
    return render_template('about.html')

@app.route('/cart')
def view_cart():
    return render_template('cart_view.html', shopping_cart=session['cart'])

@app.route('/add_to_cart/<question>')
def question_option(question):

    # Create a method to get the actual question from the string itself (ie. get_question(question)) or we can create a dictionary of all the
    # questions when we initialize the other stuff and we can just do a simple look up (ie. q = dictionary[question])    
    global cart
    return render_template('question.html', q=question)