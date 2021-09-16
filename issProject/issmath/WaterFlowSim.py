from issProject.issmath.substance_height import SubstanceHeight


class WaterFlowSim:
    def __init__(self, t=1, Tp=1, A=1, h0=1, hmax = 10, beta=1, Qdn=1) -> None:
        self.substance_height = SubstanceHeight(h0, A, Tp, beta, hmax)
        self._Qdn = Qdn
        self.N = int(t * Tp)
        self.step_number = 1

    def run_all(self):
        try:
            for x in range(0, self.N):
                self.run_step()
            return 0
        except ValueError:
            return 1

    def run_step(self, check_stop_condition=True):
        if check_stop_condition:
            if self.step_number < self.N:
                self.execute_blocks()
                self.step_number += 1
        else:
            self.execute_blocks()

    def execute_blocks(self):
        self.substance_height.calculate(self._Qdn)

    def get_h_values_dict(self) -> dict:
        return self.substance_height.get_hs_dict()

    def get_h_values_list(self) -> []:
        return self.substance_height.get_hs_list()
