## Overview
 This is a messenger API that sends messages from one user to another, it also stores messages for later retrieval. This app is hosted with Heroku, but can also be ran locally, as you can see below.
 This app uses email as a vehicle to send messages, no one ever said this would be a fast process!
 HTML is also removed from any message. 
 ## How to run this with Docker
 Run: `docker build -t chat:latest . --no-cache &&  docker run -e SENDGRID_API_KEY=<YOUR API KEY GOES HERE> chat `
  
 Note that the `SENDGRID_API_KEY` you may have to create a Sendgrid account to obtain your own key
 
 ## If you want to run this locally
 1. Make sure you have python3 and pip3 installed on your local environment
 
 2. In the root level of your project run: `pip3 install -r requirements.txt`
 If that doesn't work do `pip3 install <missing dependency that pip complains about>`
 
 3. For the `SENDGRID_API_KEY` environment variable set that locally on your machine
    (e.g. `sudo export ENDGRID_API_KEY=<YOUR API KEY GOES HERE`). 
 
 ##Running tests
 The test cases assume that you have a server running on `localhost:5000`, that can be changed by changing the `testingUrl` 
 variable at the top of the file. 
 
 From there run `pytest server_test.py `
 or alternatively `python3 server_test.py `
 
# API Methods: 
 ### Base Url:
 **Locally:**
 `localhost:5000`, this can be changed in app.py in the main section
 
 **Online**: `https://chatappdz.herokuapp.com`
 ### Status/ Is this actually running?
 
 Useful for debugging and for kubernetes liveness probes
 
 **URL** : `/_status`
 
 **Method** : `get`
 
 
 #### Success Response
 
 **Code** : `200 OK`
 
 ### Get all Messages
 
 Used to get all messages sent in the past 30 days or the last 100 messages if there are more than 100 messages sent in the past 30 days.
 
 
 **URL** : `/messages`
 
 **Method** : `get`
 
 **Auth required** : NO
 
 #### Success Response
 
 **Code** : `200 OK`
 
 **Content example**
 
 ```json
 [
     {
         "from": "dzirinsky@gmail.com",
         "message": "Hello there!",
         "time": "2020-07-22 20:58:20.235556",
         "to": "dzirinsky@gmail.com"
     },
     {
         "from": "dzirinsky@gmail.com",
         "message": "Hello there!",
         "time": "2020-07-22 20:58:35.031935",
         "to": "dzirinsky1@gmail.com"
     }
 ]
 ```
 
 ### Get messages sent between two specific users
 
  Used to get all messages sent between two specified emails in the past 30 days or the last 100 messages if there are more than 100 messages sent in the past 30 days.
 
 **URL** : `/messages/user`
 
 **URL Parameters** : `to=[string]` where `to` is the email address that the message was sent to,
 `from=[string]` where `from` is the email of the user that sent the email. Ex: `/messages/user?to=dzirinsky@gmail.com&from=dzirinsky@gmail.com`
 
 **Method** : `GET`
 
 **Auth required** : NO
 
 #### Success Response
 
 **Code** : `200 OK`
 
 **Content example**
 
 ```json
 [
     {
         "from": "dzirinsky@gmail.com",
         "message": "Hello2  there!",
         "time": "2020-07-22 14:14:08.548378",
         "to": "dzirinsky@gmail.com"
     }
 ]
 ```
 
 #### Error Response
 
 **Condition** : If either email isn't a valid email (e.g. foo@bar.com will work, bar.com will not)
 
 **Code** : `400 BAD REQUEST`
 
 ### Send a Message
 
 Used to send a Message from one user to another 
 
 **URL** : `/message`
 
 **Method** : `POST`
 
 **Auth required** : NO
 
 **Data constraints**
 
 ```json
 {
 "to": "[valid email address]",
 "from": "[valid email address]"
 }
 ```
 
 **Data example**
 
 ```json
 {
  "to": "dzirignsky@gmail.com",
  "to_name": "Mr. Fake",
  "from_name": "David",
  "from": "dzirinsky@gmail.com",
  "body": "Whatever you want"
  }
 ```
 
 #### Success Response
 
 **Code** : `200 OK`
 
 **Content example**
 
 
 #### Error Response
 
 **Condition** : If either email isn't a valid email (e.g. foo@bar.com will work, bar.com will not)
 
 **Code** : `400 BAD REQUEST`
 


 
