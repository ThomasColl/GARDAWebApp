from flask import Flask, render_template, request
import json

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/items')
def object():
    return render_template('items.html')


@app.route('/object', methods=['GET', 'POST'])
def specificObject():
    if request.method == 'GET':
        return "This is an invalid access attempt"
    elif request.method == 'POST':
        name = request.form['item']
    return render_template('objects.html', name=name,)


@app.route('/preferences')
def preferences():
    return render_template('preferences.html')

@app.route('/adjustPreferences')
def adjustPreferences():
    return render_template('adjustPreferences.html')


@app.route('/analytics')
def analytics():
    return render_template('analytics.html')


@app.route('/sendItems', methods=['GET', 'POST'])
def sendRESTItemsRequest():
    if request.method == 'GET':
        return "This is an invalid access attempt"
    elif request.method == 'POST':
        name = request.form['item']
        jsonString = "{"
        for key, value in request.form.items():
            jsonString += "\"" + key + "\":\"" + value + "\","
        jsonString = jsonString[: -1]
        jsonString += "}"

        return jsonString


@app.route('/sendPreferences', methods=['GET', 'POST'])
def sendRESTPreferencesRequest():
    if request.method == 'GET':
        return "This is an invalid access attempt"
    elif request.method == 'POST':
        jsonString = "{"
        for key, value in request.form.items():
            jsonString += "\"" + key + "\":\"" + value + "\","
        jsonString = jsonString[: -1]
        jsonString += "}"

        return jsonString

