import pytest as pytest
from flask import Flask
from shortener import shortener, link_length

url_decoder_dict = dict({"702a255f66": "https://www.finn.auto/en-US",
                         "30bf0251d2": "https://en.wikipedia.org/wiki/Cat",
                         "8ffdefbdec": "https://www.google.com"})
HOST_NAME = "http://127.0.0.1:5000/"


@pytest.fixture()
def app():
    app = Flask(__name__)
    app.config.update({
        "TESTING": True,
    })
    yield shortener(app, url_decoder_dict)


@pytest.fixture()
def client(app):
    return app.test_client()


# Unit test that tests encoder function if the input json is correct
@pytest.mark.parametrize(
    "url", ["https://www.finn.auto/en-US",
            "https://en.wikipedia.org/wiki/Cat",
            "https://www.google.com"]
)
def test_encoder_if_input_json_is_correct(app, client, url):
    input_json = {"url": url}
    new_url_response = client.post('/encode', json=input_json)
    assert new_url_response.status_code == 200


# Unit test that tests encoder function if the input json doesn't contain url
def test_encoder_if_input_json_doesnt_contain_url(app, client):
    input_json = {"link": "https://www.finn.auto/en-US"}
    new_url_response = client.post('/encode', json=input_json)
    assert new_url_response.status_code == 400


# Unit test that tests encoder function if the url from the input json isn't a
# string
def test_encoder_if_url_not_string(app, client):
    input_json = {"url": 1}
    new_url_response = client.post('/encode', json=input_json)
    assert new_url_response.status_code == 400


# Unit test that tests encoder function if the url from the input json is
# invalid
def test_encoder_if_url_is_invalid(app, client):
    input_json = {"url": "http:/invalidurl.com"}
    new_url_response = client.post('/encode', json=input_json)
    assert new_url_response.status_code == 400


# Unit test that tests redirect function if the input url is correct
@pytest.mark.parametrize(
    "new_url_end, url", url_decoder_dict.items()
)
def test_redirect_if_url_is_correct(app, client, url, new_url_end):
    redirect_response = client.get(new_url_end)
    link_redirect_to = redirect_response.headers['Location']
    assert redirect_response.status_code == 302
    assert link_redirect_to == url


# Unit test that tests redirect function if the input url isn't in the decoder
# dictionary
def test_redirect_if_url_not_from_dictionary(app, client):
    redirect_response = client.get("/__________")
    assert redirect_response.status_code == 404


# Unit test that tests decoder function if the input json is correct
@pytest.mark.parametrize(
    "new_url_end", url_decoder_dict.keys()
)
def test_decoder_if_input_json_is_correct(app, client, new_url_end):
    input_json = {"url": HOST_NAME + new_url_end}
    old_url = client.get('/decode', json=input_json)
    assert old_url.status_code == 200
    assert old_url.get_json()["url"] == url_decoder_dict[new_url_end]


# Unit test that tests decoder function if the url from the input json isn't
# in the decoder dictionary
def test_decoder_if_url_not_from_dictionary(app, client):
    input_json = {"url": HOST_NAME + "__________"}
    old_url = client.get('/decode', json=input_json)
    assert old_url.status_code == 404


# Unit test that tests decoder function if the input json doesn't contain url
def test_decoder_if_input_json_doesnt_contain_url(app, client):
    input_json = {"link": "https://www.finn.auto/en-US"}
    old_url = client.get('/decode', json=input_json)
    assert old_url.status_code == 400


# Unit test that tests decoder function if the url from the input json isn't a
# string
def test_decoder_if_url_is_not_string(app, client):
    input_json = {"url": 1}
    old_url = client.get('/decode', json=input_json)
    assert old_url.status_code == 400


# Unit test that tests decoder function if the url from the input json is
# invalid
def test_decoder_if_url_is_invalid(app, client):
    input_json = {"url": "http:/invalidurl.com"}
    old_url = client.get('/decode', json=input_json)
    assert old_url.status_code == 400


# Integration test that tests encoder, redirect and decoder functions
@pytest.mark.parametrize(
    "url", ["https://www.finn.auto/en-US",
            "https://en.wikipedia.org/wiki/Cat",
            "https://www.google.com"]
)
def test_encoder_redirect_decoder(app, client, url):
    input_json = {"url": url}
    new_url_response = client.post('/encode', json=input_json)
    assert new_url_response.status_code == 200
    new_url_json = new_url_response.get_json()
    new_url_link = '/' + new_url_json['url'][-link_length:]
    redirect_response = client.get(new_url_link)
    link_redirect_to = redirect_response.headers['Location']
    assert redirect_response.status_code == 302
    assert link_redirect_to == url
    old_url = client.get('/decode', json=new_url_json)
    assert old_url.status_code == 200
    assert old_url.get_json() == input_json
