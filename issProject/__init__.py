import os

from flask import Flask, request
import UAR from issProject.issmath

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'


    @app.route('/api/pid', methods=["POST"])
    def plot():
        uar = UAR()
        print(request.json)
        return 'nic'
    return app