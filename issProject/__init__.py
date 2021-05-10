import os

from flask import Flask, request, make_response, jsonify

from issProject.issmath.UAR import UAR


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
        payload = request.json
        uar = UAR(t=float(payload['test_duration']), Tp=float(payload['sampling_frequency']),
                  A=float(payload['cross_section_tank_area']),
                  h0=float(payload['height_at_zero']), hset=float(payload['height_set']),
                  beta=float(payload['free_outflow_rate']),
                  kp=float(payload['regulator_gain']), Td=float(payload['lead_time']),
                  Ti=float(payload['doubling_time']))
        uar.run_all()
        response_body = {
            'simulation_values': uar.get_h_values_list()
        }
        res = make_response(jsonify(response_body), 200)
        return res

    return app
