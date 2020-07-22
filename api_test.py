import requests
import json

testingUrl = 'http://localhost:5000/'


def test_client():
    # lets assert that a simple get request works
    request = requests.get(testingUrl + "_status")
    assert request.status_code == 200

    # a correctly formed json sends a message
    body = {
        "to": "dzirinsky@gmail.com",
        "to_name": "David z",
        "from_name": "David",
        "from": "dzirinsky@gmail.com",
        "body": "Hi!"
    }
    request = requests.post(testingUrl + "message", data=json.dumps(body), headers={"Content-Type": "application/json"})
    assert request.status_code == 200

    # assert a malformed json is rejected
    body = {"to": "true"}
    request = requests.post(testingUrl + "message", data=json.dumps(body), headers={"Content-Type": "application/json"})
    assert request.status_code == 400

    # assert you can get all messages
    request = requests.get(testingUrl + "messages", headers={"Content-Type": "application/json"})
    assert request.status_code == 200
    response_json = request.json()[0]

    # timestamp is generated dynamically so lets test the other fields in the json
    assert response_json["to"] == "dzirinsky@gmail.com"
    assert response_json["message"] == "Hi!"
    assert response_json["from"] == "dzirinsky@gmail.com"

    # assert you can get a subset of messages
    request = requests.get(testingUrl + "messages/user?to=dzirinsky@gmail.com&from=dzirinsky@gmail.com", headers={"Content-Type": "application/json"})
    assert request.status_code == 200
    response_json = request.json()[0]

    assert response_json["to"] == "dzirinsky@gmail.com"
    assert response_json["message"] == "Hi!"
    assert response_json["from"] == "dzirinsky@gmail.com"


if __name__ == "__main__":
    print("starting")
    test_client()
    print("Everything passed")
