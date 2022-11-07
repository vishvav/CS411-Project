from flask import Flask

api = Flask(__name__)

@api.route('/profile')
def my_profile():
    response_body = {
        "name": "..",
        "about": "hello world"
    }
    return response_body