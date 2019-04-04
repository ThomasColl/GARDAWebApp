import json

import requests
from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message

import PlottingMethods
import RSAMethods

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'gardasmarthome@gmail.com'
app.config['MAIL_PASSWORD'] = '1-2GARDA@itcarlow'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

base_url = "http://127.0.0.1:5000/"
email_response = ""
item_response = ""
item = ""
response = ""
g = globals()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/send_feedback')
def send_feedback():
    response = g["email_response"]
    g["email_response"] = ""
    return render_template('send_feedback.html', response=response)


@app.route('/feedback', methods=['POST'])
def feedback():
    send_email(request.form["sender_email"],
               request.form["sender_subject"],
               request.form["sender_feedback"])
    g["email_response"] = "Feedback sent!"
    return redirect(url_for("send_feedback"))


def send_email(senders_email, senders_subject, senders_feedback):
    with open('encrypted_data.txt', 'rb') as payload:
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        json = "{\"email\": \"" + senders_email + \
               "\", \"sub\": \"" + senders_subject + \
               "\", \"feed\": \"" + senders_feedback + "\"}"
        RSAMethods.encrypt(json)
        r = requests.post(base_url + "receive_feedback", data=payload, headers=headers)
    print("email " + senders_email)
    print("sub " + senders_subject)
    print("feed " + senders_feedback)
    msg = Message('Feedback from ' + senders_email,
                  sender='gardasmarthome@gmail.com',
                  recipients=['gardasmarthome@gmail.com'])
    print("message defined")
    msg.body = "Users Subject: " + senders_subject + \
               "\n" + "Users Feedback: " + senders_feedback
    print("body set")
    mail.send(msg)
    print("message sent")



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
        response = requests.get(base_url + "request_item_options", data={'key': g["item"]})
        raw_items = json.loads(response.text)
        if raw_items == "Switch":
            options = ["ON", "OFF"]
        else:
            options = ["On", "Off"]
    return render_template('specific_item.html', name=item, options=options, type=raw_items)


@app.route('/send_request_items', methods=['GET', 'POST'])
def send_request_items():
    if request.method == 'GET':
        return "This is an invalid access attempt"
    elif request.method == 'POST':
        option = request.form['action']
        with open('encrypted_data.txt', 'rb') as payload:
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            json = "{\"key\": \"" + g["item"] + \
                   "\", \"option\": \"" + option + \
                   "\", \"subject\": \"user\", \"object\": \"items\", \"action\": \"adjust\" }"
            RSAMethods.encrypt(json)
            r = requests.post(base_url + "update_item_state", data=payload, headers=headers)
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
            new = request.form["name"] + ", " + request.form["resource"] + ", " + request.form["action"]
            print(new)
            with open('encrypted_data.txt', 'rb') as payload:
                headers = {'content-type': 'application/x-www-form-urlencoded'}
                json_string = "{\"subject\": \"user\"" \
                              ", \"object\": \"policies\"" \
                              ", \"action\": \"add\" " \
                              ", \"new\": \"" + new.strip() + "\"}"
                print(json_string)
                RSAMethods.encrypt(json_string)
                r = requests.post(base_url + "update_policies", data=payload, headers=headers)
        elif option == "edit":
            new = request.form["name"] + ", " + request.form["resource"] + ", " + request.form["action"]
            old = request.form["policy"]
            with open('encrypted_data.txt', 'rb') as payload:
                headers = {'content-type': 'application/x-www-form-urlencoded'}
                json_string = "{\"subject\": \"user\"" \
                              ", \"object\": \"policies\"" \
                              ", \"action\": \"edit\" " \
                              ", \"new\": \"" + new.strip() + \
                              "\", \"old\": \"" + old.strip() + "\"}"
                print(json_string)
                RSAMethods.encrypt(json_string)
                r = requests.post(base_url + "update_policies", data=payload, headers=headers)
        elif option == "del":
            old = request.form["policy"]
            with open('encrypted_data.txt', 'rb') as payload:
                headers = {'content-type': 'application/x-www-form-urlencoded'}
                json_string = "{\"subject\": \"user\"" \
                              ", \"object\": \"policies\"" \
                              ", \"action\": \"del\" " \
                              ", \"old\": \"" + old.strip() + "\"}"
                print(json_string)
                RSAMethods.encrypt(json_string)
                r = requests.post(base_url + "update_policies", data=payload, headers=headers)
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
        with open('encrypted_data.txt', 'rb') as payload:
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            json_string = "{" \
                          "\"subject\": \"user\"," \
                          "\"object\": \"analytics\"," \
                          "\"action\": \"request\" ," \
                          "\"type\": " + str(choice) + \
                          "}"
            print(json_string)
            RSAMethods.encrypt(json_string)
            r = requests.post(base_url + "request_analytics", data=payload, headers=headers)
        lists = json.loads(r.text)
        x = lists[0]
        y = lists[1]
        if not x or not y:
            print(lists)
            return render_template('render_analytics.html', img="", title=title)
        img = PlottingMethods.retrieve_image_uri(x, y)
        return render_template('render_analytics.html', img=img, title=title)


if __name__ == '__main__':
    app.run()
