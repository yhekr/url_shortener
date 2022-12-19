from flask import request, redirect
from hashlib import md5
import validators

HOST_NAME = "http://127.0.0.1:5000/"
link_length = 10


def shortener(app, url_decoder_dict):
    # Function for validation that the input json is correct
    def input_validate(input):
        if 'url' not in input:
            return {"error": "input must contain url"}, 400
        url = input['url']
        if type(url) != str:
            return {"error": "url must be a string"}, 400
        if not validators.url(url):
            return {"error": "invalid url"}, 400
        return True

    # Function for encoding your URL
    @app.route("/encode", methods=['POST'])
    def encoder():
        input = request.get_json()
        input_validate_result = input_validate(input)
        if input_validate_result is not True:
            return input_validate_result
        url = input['url']
        url_code = md5(url.encode('utf-8')).hexdigest()[:link_length]
        new_url = HOST_NAME + url_code
        url_decoder_dict[url_code] = url
        return {"url": new_url}

    # Function for redirection from the short URL to the original URL
    @app.route('/<path>')
    def url_redirect(path):
        if path in url_decoder_dict:
            old_path = url_decoder_dict[path]
            return redirect(old_path)
        else:
            return {"error": "invalid url"}, 404

    # Function for decoding the short URL
    @app.route("/decode", methods=['GET'])
    def decoder():
        input = request.get_json()
        input_validate_result = input_validate(input)
        if input_validate_result is not True:
            return input_validate_result
        url = input['url']
        url_code = url[-link_length:]
        if url_code in url_decoder_dict:
            old_path = url_decoder_dict[url_code]
            return {"url": old_path}
        else:
            return {"error": "invalid url"}, 404

    return app
