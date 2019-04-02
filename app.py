from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message

import json
import requests
import PlottingMethods

app = Flask(__name__)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'gardasmarthome@gmail.com'
app.config['MAIL_PASSWORD'] = '1-2GARDA@itcarlow'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)


base_url = "http://127.0.0.1:5000/"
item_response = ""
item = ""
response = ""
g = globals()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/send_feedback')
def send_feedback():
    response = g["response"]
    g["response"] = ""
    return render_template('send_feedback.html', response=response)


@app.route('/feedback', methods=['POST'])
def feedback():
    send_email(request.form["sender_email"], request.form["sender_subject"], request.form["sender_feedback"])
    g["response"] = "Feedback sent!"
    return redirect(url_for("send_feedback"))


def send_email(senders_email, sender_subject, sender_feedback):
    msg = Message('Feedback from ' + senders_email, sender='gardasmarthome@gmail.com',
                  recipients=['gardasmarthome@gmail.com'])
    msg.body = "Users Subject: " + sender_subject + "\n" + "Users Feedback: " + sender_feedback
    mail.send(msg)


@app.route('/items')
def items():
    response = requests.get(base_url + "request_item_list")
    if g["item_response"]:
        resp = g["item_response"]
        g["item_response"] = ""
    else:
        resp = ""
    raw_items = json.loads(response.text)
    return render_template('items.html', items=raw_items, response=resp)


@app.route('/specific_item', methods=['GET', 'POST'])
def specific_item():
    if request.method == 'GET':
        return "This is an invalid access attempt"
    elif request.method == 'POST':
        g["item"] = request.form['item']
        response = requests.get(base_url + "request_item_options", data = {'key': g["item"]})
        raw_items = json.loads(response.text)
        if raw_items[0] == "Switch":
            options = ["On", "Off"]
        else:
            options = ["On", "Off"]
    return render_template('specific_item.html', name=item, options=options)


@app.route('/send_request_items', methods=['GET', 'POST'])
def send_request_items():
    if request.method == 'GET':
        return "This is an invalid access attempt"
    elif request.method == 'POST':
        option = request.form['action']
        r = requests.post(base_url + 'update_item_state',
                          json={"key": g["item"],
                                "option": option,
                                "subject": "user",
                                "object": "items",
                                "action": "edit"
                                },
                          )
        g["item"] = ""
        if r.text == "1":
            g["item_response"] = "Successful Request"
        return redirect(url_for("items"))


@app.route('/preferences')
def preferences():
    raw = requests.get(base_url + "request_policies_with_item_access").text
    users = json.loads(raw)
    return render_template('preferences.html', users=users)


@app.route('/adjust_preferences', methods=['GET', 'POST'])
def adjust_preferences():
    if request.method == 'GET':
        return "This is an invalid access attempt"
    elif request.method == 'POST':
        # TODO Add in drop down list in html
        action = request.form["action"]
        print(action)
        policies = ""
        if action == "edit" or action == "del":
            raw = requests.get(base_url + "request_all_policies").text
            policies = json.loads(raw)
        return render_template('adjust_preferences.html', action=action, policy=policies)


@app.route('/send_request_policies', methods=['GET', 'POST'])
def send_request_policies():
    if request.method == 'GET':
        return "This is an invalid access attempt"
    elif request.method == 'POST':
        option = request.form['choice']
        print("/send_request_policies: Option = " + option)
        if option == "add":
            new = request.form["name"] + ", " + request.form["policy"] + ", " + request.form["action"]
            r = requests.post(base_url + 'update_policies', json={"subject": "user",
                                                                  "object": "policies",
                                                                  "action": "add",
                                                                  "new": new.strip()})
        elif option == "edit":
            new = request.form["name"] + ", " + request.form["resource"] + ", " + request.form["action"]
            old = request.form["policy"]
            r = requests.post(base_url + 'update_policies', json={"subject": "user",
                                                                  "object": "policies",
                                                                  "action": "edit",
                                                                  "new": new.strip(),
                                                                  "old": old.strip()})
        elif option == "del":
            old = request.form["policy"]
            r = requests.post(base_url + 'update_policies', json={"subject": "user",
                                                                  "object": "policies",
                                                                  "action": "del",
                                                                  "old": old.strip()})
        print(r.text)
        if r.text == "1":
            g["item_response"] = "Successful Request"
        return redirect(url_for("preferences"))


@app.route('/analytics')
def analytics():
    choices = [
        "Requests over time",
        "Successful requests over time",
        "Unsuccessful requests over time"
    ]
    return render_template('analytics.html', choices=choices)


@app.route('/render_analytics', methods=['GET', 'POST'])
def render_analytics():
    if request.method == 'GET':
        return "This is an invalid access attempt"
    else:
        title = request.form["choice"]
        choice = 0
        if title == "Requests over time":
            choice = 1
        elif title == "Successful requests over time":
            choice = 2
        elif title == "Unsuccessful requests over time":
            choice = 3
        r = requests.post(base_url + 'request_analytics', json={"subject": "user",
                                                                "object": "analytics",
                                                                "action": "request",
                                                                "type": choice})
        lists = json.loads(r.text)
        x = lists[0]
        y = lists[1]
        if not x or not y:
            print(lists)
            return render_template('render_analytics.html', img="", title=title)
        img = PlottingMethods.retrieve_image_uri(x,y)
        return render_template('render_analytics.html', img=img, title=title)


if __name__ == '__main__':
    app.run()
