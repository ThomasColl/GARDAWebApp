from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/items')
def items():
    return render_template('items.html')


@app.route('/preferences')
def preferences():
    return render_template('preferences.html')


@app.route('/analytics')
def analytics():
    return render_template('analytics.html')
