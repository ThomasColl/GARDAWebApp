from flask import Flask, render_template, request, redirect, url_for
import json
import requests

app = Flask(__name__)


base_url = "http://127.0.0.1:5000/"
item_response = ""
item = ""
g = globals()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/items')
def items():
    response = requests.get(base_url + "rec")
    if g["item_response"]:
        resp = g["item_response"]
        g["item_response"] = ""
    else:
        resp = ""
    # response = requests.get(base_url + "rec/")
    raw_items = json.loads(response.text)
    return render_template('items.html', items=raw_items, response=resp)


@app.route('/object', methods=['GET', 'POST'])
def specific_item():
    if request.method == 'GET':
        return "This is an invalid access attempt"
    elif request.method == 'POST':
        g["item"] = request.form['item']
        response = requests.get(base_url + "recs", data = {'key': g["item"]})
        raw_items = json.loads(response.text)
        if raw_items[0] == "Switch":
            options = ["On", "Off"]
        else:
            options = ["On", "Off"]
    return render_template('objects.html', name=item, options=options)


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
        option = request.form['action']
        r = requests.post(base_url + 'sec', json={"key": g["item"],
                                                  "option": option,
                                                  "subject": "user",
                                                  "object": "items",
                                                  "action": "edit"})
        g["item"] = ""
        if r.text == "pass":
            g["item_response"] = "Successful Request"
        return redirect(url_for("items"))


@app.route('/sendPreferences', methods=['GET', 'POST'])
def formJSON():
    if request.method == 'GET':
        return "This is an invalid access attempt"
    elif request.method == 'POST':
        jsonString = "{"
        for key, value in request.form.items():
            if value:
                jsonString += "\"" + key + "\":\"" + value + "\","
        if jsonString is not "{":
            jsonString = jsonString[: -1]
            jsonString += "}"

        return jsonString


if __name__ == '__main__':
    app.run()
