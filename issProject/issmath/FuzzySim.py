import math

from issProject.issmath.error import Error
from issProject.issmath.fuzzy_logic import FuzzyLogic
from issProject.issmath.substance_height import SubstanceHeight


class FuzzySim:
    def __init__(self, t=0, Tp=2, A=1, h0=0, hset=2, beta=0.5, hmax=10) -> None:
        self.error = Error(hz=hset)
        self.simulator = FuzzyLogic()
        self.substance_height = SubstanceHeight(h0, A, Tp, beta, hmax)
        self.N = int(t * Tp)  # ilosc krokow
        self.step_number = 1
        self._beta = beta
        self._hmax = hmax

    def run_step(self, check_stop_condition=True):
        if check_stop_condition:
            if self.step_number < self.N:
                self.execute_blocks()
                self.step_number += 1
        else:
            self.execute_blocks()

    def execute_blocks(self):
        err, err_sum, err_delta = self.error.calculate(self.substance_height.get_latest_h())
        un = self.simulator.calculate(err, err_delta)
        qdn = self.calculate_qdn(un)
        self.substance_height.calculate(qdn)

    def calculate_qdn(self, output):
        qdn = output + self._beta * math.sqrt(self.substance_height.get_latest_h())  # Q0
        if qdn < 0:
            qdn = 0
        elif qdn > self._hmax:
            qdn = self._hmax
        return qdn

    def run_all(self):
        try:
            for x in range(0, self.N):
                self.run_step()
            return 0
        except ValueError:
            return 1

    def get_h_values_dict(self) -> dict:
        return self.substance_height.get_hs_dict()

    def get_h_values_list(self) -> []:
        return self.substance_height.get_hs_list()
