### Objective

This is the URL shortening service, that is created using Python and Flask. 
Also, I use pytest for testing and validators for validating urls.


### Installation

Install with pip:

```
$ pip install -r requirements.txt
```

### Configure the server name

You can configure it in shortener.py

HOST_NAME : the name of the server

### Getting started

You should navigate to shortener directory

```
$ cd shortener
```

In shortener/

```
$ flask run
```
or
```
$ python app.py
```

After that you can open a new terminal and there you can send 
requests using curl. Make sure that the app is running in the another terminal,
otherwise you won't be able to send requests.

## Encode URL

To encode the URL use

```
$ curl -d '{"url": "#YOUR_URL#"}' -X POST -H "Content-Type: application/json" #YOUR_HOST_NAME#/encode
```

Make sure that your URL is valid. Valid url should start with "http://" or 
"https://". If it is valid, you will see

```
$ {"url":"#SHORT_URL#"}
```

Otherwise, you will get

```
{"error":"invalid url"}
```

For example,
```
$ curl -d '{"url": "https://www.finn.auto/en-US"}' -X POST -H "Content-Type: application/json" localhost:5000/encode
```
will give you

```
{"url":"http://127.0.0.1:5000/702a255f66"}
```

You can open this link in a browser, and it will redirect you to https://www.finn.auto/en-US

### Decode URL

To decode the URL use

```
$ curl -d '{"url": "#SHORT_URL#"}' -X GET -H "Content-Type: application/json" #YOUR_HOST_NAME#/decode
```

Make sure that the short URL that you entered is valid and correct (you got this URL before using /encode, and you 
haven't stopped running the app after that. If you stop running the app and 
after that run it again, it won't remember your old URLs, because they are 
saved in memory). If it 
is, you will see

```
{"url":"#ORIGINAL_URL#"}
```

If it isn't valid and correct, you will get

```
{"error":"invalid url"}
```

For example,
```
$ curl -d '{"url": "http://127.0.0.1:5000/702a255f66"}' -X GET -H "Content-Type: application/json" localhost:5000/decode
```
will give you

```
{"url":"https://www.finn.auto/en-US"}
```

### Video instructions on how to use it using Insomnia

Sometimes curl doesn't work on Windows, but you also can send requests using 
apps like Insomnia. This is video instructions on how to do it.

https://drive.google.com/file/d/1laRLWZBz9YErYW8VWssYTFY-CSeSkCVU/view?usp=sharing

### Run tests

In shortener/

```
$ pytest test.py
```

Thank you for reading,

Iya Volkova