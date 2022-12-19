from flask import Flask
from shortener import shortener

app = Flask(__name__)
url_decoder_dict = dict()

shortener(app, url_decoder_dict)

if __name__ == '__main__':
    app.run()
