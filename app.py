from flask import Flask, request, Response #ini object request flask
import json
import requests #ini untuk http request
import sys

token = "903109049:AAG2huOp8K3cS1h7LZRu2WfD02mergVUhJ4"
tlgApi = "https://api.telegram.org/bot"
bot = tlgApi + token
app = Flask(__name__)

# app.config['debug'] = True
def write_json(data,filename = 'data.json'):
    with open('data.json', 'w') as f:
        json.dump(data, f)

def check_storage():
    # run check storage
    return 'here is the storage lists'

def get_order(order):
    allowed_order = {
        '/strg' : 'check_storage'
    }
    if order in allowed_order:
        return allowed_order[order]
    else:
        return ''

def send_message(chat_id, text = ""):
    return requests.post(bot + "/sendMessage", {
        'chat_id' : chat_id,
        'text' : text
    })


# set webhook
#https://api.telegram.org/bot903109049:AAG2huOp8K3cS1h7LZRu2WfD02mergVUhJ4/setWebhook?url=https://a1d2e9ce.ngrok.io/

@app.route('/', methods=["GET", "POST"])
def main():
    if request.method == "GET":
        return "hello worlds"

    if request.method == "POST":
        msg = request.get_json()
        write_json(msg)

        chat_id = msg['message']['chat']['id']
        txt = msg['message']['text']

        order = get_order(txt)
        
        if not order:
            # order not found
            send_message(chat_id, "sorry, I don't understand :( ")
        else:
            res = getattr(sys.modules[__name__], order )()
            send_message(chat_id, res )
        # print msg
        return Response("OK", status=200 )


if __name__ == "__main__":
    app.run(debug=True)
