from issProject.issmath.error import Error
from issProject.issmath.inflow import Inflow
from issProject.issmath.pid import PID
from issProject.issmath.substance_height import SubstanceHeight


class UAR:
    """
          Klasa stanowiąca implementację wszystkich kroków UAR

          ...

          Attributes
          ----------
          t : float
              czas badania [s]
          Tp : float
              częstotliwość próbkowania [Hz]
          A : float
            pole powierzchni przekroju poprzecznego zbiornika [m^2]
          h0 : float
              poziom substancji w zbiorniku w chwili 0 [m]
          hset : float
              wartość zadana (wysokości substancji w zbiorniku) [m]
          beta : float
              współczynnik wypływu swobodnego ze zbiornika [m(^5/2)/s]
          kp : float
              wzmocnienie regulatora
          Td : float
              czas wyprzedzenia [s]
          Ti : float
              czas zdwojenia [s]

          Methods
          -------
          run_step(check_stop_condition=0)
              odpala jedno przejście wszystkich bloków

              Parameters
              ----------
              check_stop_condition : bool, optional
                      przełącznik decydujący o tym, czy warunek stopu ma być brany pod uwagę

          execute_blocks()
              wywołuje wszystkie bloki dla jednego przejścia

          calculate_max_steps()
              oblicza wartość warunku stopu

          should_go()
              sprawdza czy symulacja nadal powinna trwać
              :returns boolean
          """

    def __init__(self, t=0, Tp=2, A=1, h0=0, hset=2, beta=0.5, kp=0.2, Td=0.1, Ti=0.1, hmax=10) -> None:
        self.error = Error(hz=hset)
        self.pid = PID(kp, Tp, Ti, Td)
        self.inflow = Inflow()
        self.substance_height = SubstanceHeight(h0, A*hmax, Tp, beta, hmax)
        self.N = self.calculate_max_steps(t, Tp)
        self.step_number = 1

    def run_step(self, check_stop_condition=True):
        if check_stop_condition:
            if self.should_go():
                self.execute_blocks()
                self.step_number += 1
        else:
            self.execute_blocks()

    def execute_blocks(self):
        err, err_sum, err_delta = self.error.calculate(self.substance_height.get_latest_h())
        un = self.pid.calculate(err, err_sum, err_delta)
        qdn = un
        self.substance_height.calculate(qdn)

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
