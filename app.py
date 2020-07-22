from collections import defaultdict
from flask import Flask, jsonify, request
import requests
import traceback
from datetime import datetime
import os
from html.parser import HTMLParser

app = Flask(__name__)

class HTMLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


class Server:
    def __init__(self, api_key):
        self.history = defaultdict(dict)
        self.api_key = api_key

    def strip_tags(self, html):
        s = HTMLStripper()
        s.feed(html)
        return s.get_data()

    def create_sendgrid_json(self, request_data):
        data = {"personalizations": [
            {"to": [
                {
                    "email": request_data['to'],
                    "name": request_data['to_name']
                }
            ],
                "subject": "Your Chat App Message!"
            }],
            "from": {
                "email": request_data['from'],
                "name": request_data['from_name']
            },
            "content": [
                {
                    "type": "text/plain",
                    "value": request_data['body']
                }
            ]
        }
        return data

    def check_date(self, old_date):
        time_between_dates = datetime.now() - old_date
        print(time_between_dates)
        if time_between_dates.days < 30:
            return True
        else:
            return False

    def get_recent_messages(self):
        return_body = []

        # check for empty dictionary
        if not self.history:
            return return_body
        try:
            for email in self.history:
                for body in self.history[email]:
                    # check that there aren't already 100 messages ready to be sent:
                    if len(return_body) > 100:
                        return return_body

                    # check that this messages isn't more than 30 days old
                    if self.check_date(self.history[email][body][1]):
                        node = {'to': email, 'message': body, 'from': self.history[email][body][0],
                                'time': str(self.history[email][body][1])}
                        return_body.append(node)

            return return_body
        except Exception as e:
            print(traceback.print_exc())
            return []

    def get_specific_messages(self, from_email, to_email):
        return_body = []

        # check for empty dictionary
        if not self.history:
            return return_body
        try:
            for email in self.history:
                if email == to_email:
                    for body in self.history[email]:
                        if self.history[email][body][0] == from_email:
                            # check that there aren't already 100 messages ready to be sent:
                            if len(return_body) > 100:
                                return return_body
                            # check that this messages isn't more than 30 days old
                            if self.check_date(self.history[email][body][1]):
                                node = {'to': email, 'message': body, 'from': self.history[email][body][0],
                                        'time': str(self.history[email][body][1])}
                                return_body.append(node)

            return return_body
        except Exception as e:
            print(traceback.print_exc())
            return []

    def add_to_history(self, to_email, body, from_email):
        # going to use a dictionary with two keys for history
        self.history[to_email][body] = [from_email, datetime.now()]

    def send_message(self, request_data):

        hed = {'Authorization': 'Bearer ' + self.api_key}
        response = requests.post(url='https://api.sendgrid.com/v3/mail/send',
                                 json=self.create_sendgrid_json(request_data), headers=hed)

        # lets return an error if this wasn't successful
        if response.status_code != 202:
            print("bad status code from sendgrid: " + str(response))
            return 400
        self.add_to_history(request_data['to'], request_data['body'], request_data['from'])
        return 200


@app.route('/message', methods=['POST'])
def email():

    request_data = ''
    try:
        request_data = request.json
    except Exception as e:
        print(traceback.print_exc())
        return "BAD REQUEST", 400

    params = ['to_name', 'from_name', 'body']
    try:
        # check for valid emails
        if '@' not in request_data['to'] or '@' not in request_data['from']:
            return "BAD REQUEST", 400

        # check all of the other parameters are present
        for param in params:
            if param not in request_data:
                return "BAD REQUEST", 400

        # strip html to avoid sending someone a virus, etc
        request_data['body'] = server.strip_tags(request_data['body'])

        # send request to api
        if server.send_message(request_data) != 200:
            return "BAD REQUEST", 400
        return "ok", 200

    except Exception as e:
        print(traceback.print_exc())
        return "BAD REQUEST", 400

# check for bad configuration(s)
if 'SENDGRID_API_KEY' not in os.environ:
    print("SENDGRID_API_KEY not set, exiting now")
    os.sys.exit(-1)

sendgrid_api_key = os.environ['SENDGRID_API_KEY']

server = Server(sendgrid_api_key)


# these methods are nice for kubernetes and debugging
# (e.g. is this actually running?)
@app.route('/_status')
def status():
    return "ok", 200

@app.route('/messages/user', methods=['GET'])
def messages_from_user():
    print(request.args)
    try:
        from_email = request.args.get('to')
        to_email = request.args.get('from')
        print(from_email)
    except Exception as e:
        print(traceback.print_exc())
        return "BAD REQUEST", 400

    if '@' not in from_email or '@' not in to_email:
        return "BAD REQUEST", 400

    body = jsonify(server.get_specific_messages(from_email, to_email))
    return body, 200

@app.route('/messages')
def messages():
    body = jsonify(server.get_recent_messages())
    return body, 200


if __name__ == '__main__':
    app.run(debug=False, use_reloader=False, host='0.0.0.0', port='5000')
