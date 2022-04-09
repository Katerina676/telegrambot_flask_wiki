from flask import Flask
from flask_sslify import SSLify
import requests
from flask import request
from flask import jsonify
import wikipedia


app = Flask(__name__)
sslify = SSLify(app)
URL = 'https://api.telegram.org/bot<token>/'


def send_msg(chat_id, text='bla'):
    url = URL + 'sendMessage'
    answer = {'chat_id' : chat_id, 'text': text}
    r = requests.get(url, json=answer)
    return r.json()


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        r = request.get_json()
        chat_id = r['message']['chat']['id']
        msg = r['message']['text']
        wikipedia.set_lang("ru")
        try:
            word = wikipedia.summary(msg)
            send_msg(chat_id, text=word)
        except:
            send_msg(chat_id, text='Не удалось найти')

        return jsonify(r)
    return 'Welcome'


if __name__ == '__main__':
    app.run()


