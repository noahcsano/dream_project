from flask import Flask, redirect, url_for, render_template, request, session
import google_api

app = Flask(__name__)
app.static_folder = "static"
cart = []

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

@app.route('/survey_Qs/<category>/<sub_category>', methods = ["GET", 'POST'])
def survey_Qs(category, sub_category):
    global cart
    if request.method == 'POST':
        questions = request.form['q']
        return redirect(url_for('question_option', question = questions))
    else:
        return render_template('Survey_Qs.html', Qs=sheets[category][sub_category], cart = cart, category=category, sub_category=sub_category)

@app.route("/about")
def about():
    return render_template('about.html')

@app.route('/cart')
def view_cart():
    global cart
    return render_template('cart_view.html', cart = cart)

@app.route('/add_to_cart/<question>')
def question_option(question):

    # Create a method to get the actual question from the string itself (ie. get_question(question)) or we can create a dictionary of all the
    # questions when we initialize the other stuff and we can just do a simple look up (ie. q = dictionary[question])    
    global cart
    return render_template('question.html', q=question)

if __name__ == '__main__':
    app.run(debug=True)