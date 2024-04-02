from flask import Flask, request
from flask_wtf import CSRFProtect

from twilio.twiml.messaging_response import MessagingResponse

import os

from openai import OpenAI

client = OpenAI()

app = Flask(__name__)
csrf = CSRFProtect(app)

@csrf.exempt
@app.route("/sms", methods=['POST'])
def chatgpt():
    print("the request has been heard")
    inb_msg = request.form['Body'].lower()
    print(inb_msg)
    
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": inb_msg} 
    ]
    )

    resp = MessagingResponse()
    resp.message(response.choices[0].message.content)

    # Use the helper function to construct the response
    twiml = resp.to_xml()
    print(twiml)
    return twiml







if __name__ == "__main__":
    app.run(debug=True,port= 7259)