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
    raw = requests.get("http://127.0.0.1:5000/polr").text
    users = json.loads(raw)
    return render_template('preferences.html', users=users)


@app.route('/adjustPreferences')
def adjust_preferences():
    # TODO Add in drop down list in html
    action = request.form["action"]
    policies = ""
    if action == "edit" or action == "del":
        raw = requests.get("http://127.0.0.1:5000/poll").text
        policies = json.loads(raw)
    return render_template('adjustPreferences.html', action=action, policy=policies)


@app.route('/analytics')
def analytics():
    return render_template('analytics.html')


@app.route('/sendItems', methods=['GET', 'POST'])
def send_rest_items_request():
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
def form_json():
    if request.method == 'GET':
        return "This is an invalid access attempt"
    elif request.method == 'POST':
        option = request.form['action']
        if option == "add":
            new = request.form["name"] + ", " + request.form["policy"] + ", " + request.form["action"]
            r = requests.post(base_url + 'sec', json={"subject": "user",
                                                      "object": "items",
                                                      "action": "edit",
                                                      "new": new})
        elif option == "edit":
            new = request.form["name"] + ", " + request.form["resource"] + ", " + request.form["action"]
            old = request.form["policy"]
            r = requests.post(base_url + 'sec', json={"subject": "user",
                                                      "object": "items",
                                                      "action": "edit",
                                                      "new": new,
                                                      "old": old})
        elif option == "del":
            old = request.form["policy"]
            r = requests.post(base_url + 'sec', json={"subject": "user",
                                                      "object": "items",
                                                      "action": "edit",
                                                      "old": old})

        if r.text == "pass":
            g["item_response"] = "Successful Request"
        return redirect(url_for("object"))


if __name__ == '__main__':
    app.run()
