from issProject.issmath.error import Error
from issProject.issmath.fuzzy_logic import FuzzyLogic
from issProject.issmath.inflow import Inflow
from issProject.issmath.substance_height import SubstanceHeight


class FuzzySim:
    def __init__(self, t=0, Tp=2, A=1, h0=0, hset=2, beta=0.5, hmax=10) -> None:
        self.error = Error(hz=hset)
        self.simulator = FuzzyLogic()
        self.inflow = Inflow()
        self.substance_height = SubstanceHeight(h0, A, Tp, beta, hmax)
        self.N = self.calculate_max_steps(t, Tp)
        self.step_number = 1
        self.un2 = 0  # poprzednia wartość uchybu

    def run_step(self, check_stop_condition=True):
        if check_stop_condition:
            if self.should_go():
                self.execute_blocks()
                self.step_number += 1
        else:
            self.execute_blocks()

    def execute_blocks(self):
        err, err_sum, err_delta = self.error.calculate(self.substance_height.get_latest_h())
        un = self.simulator.calculate(err, err_sum, err_delta)
        qdn = un# tu inflow cos moze bd trzeba zaimplementowac
        self.substance_height.calculate(qdn)
        self.un2 = un

    def run_all(self):
        try:
            for x in range(0, self.N):
                self.run_step()
            return 0
        except ValueError:
            return 1

    @staticmethod
    def calculate_max_steps(t, Tp):
        return int(t * Tp)

    def should_go(self):
        return self.step_number < self.N

    def reset_steps(self):
        self.step_number = 0

    def get_h_values_dict(self) -> dict:
        return self.substance_height.get_hs_dict()

    def get_h_values_list(self) -> []:
        return self.substance_height.get_hs_list()
