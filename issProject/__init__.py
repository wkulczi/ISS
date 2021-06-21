import os

from flask import Flask, request, make_response, jsonify

from issProject.issmath.UAR import UAR
from issProject.issmath.WaterFlowSim import WaterFlowSim


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
    def plot_pid():
        payload = request.json
        uar = UAR(t=float(payload['test_duration']), Tp=float(payload['sampling_frequency']),
                  A=float(payload['cross_section_tank_area']),
                  h0=float(payload['height_at_zero']), hset=float(payload['height_set']),
                  beta=float(payload['free_outflow_rate']),
                  kp=float(payload['regulator_gain']), Td=float(payload['lead_time']),
                  Ti=float(payload['doubling_time']),
                  hmax=float(payload['container_height'])
                  )
        result = uar.run_all()
        response_body = {
            'is_error': result,
            'simulation_values': uar.get_h_values_list()
        }
        res = make_response(jsonify(response_body), 200)
        return res @ app.route('/api/pid', methods=["POST"])

    @app.route('/api/free', methods=["POST"])
    def plot_free():
        payload = request.json
        waterFlowSim = WaterFlowSim(t=float(payload['test_duration']),
                           Tp=float(payload['sampling_frequency']),
                           A=float(payload['cross_section_tank_area']),
                           h0=float(payload['height_at_zero']),
                           beta=float(payload['free_outflow_rate']),
                           hmax=float(payload['container_height']),
                           Qdn=float(payload['inflow_rate']),
                           )
        result = waterFlowSim.run_all()
        response_body = {
            'is_error': result,
            'simulation_values': waterFlowSim.get_h_values_list()
        }
        res = make_response(jsonify(response_body), 200)
        return res

    return app
