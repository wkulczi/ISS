from issProject.issmath.error import Error
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

          """

    def __init__(self, t=0, Tp=2, A=1, h0=0, hset=2, beta=0.5, kp=0.2, Td=0.1, Ti=0.1, hmax=10) -> None:
        self.error = Error(hz=hset)
        self.substance_height = SubstanceHeight(h0, A, Tp, beta, hmax)
        self.N = int(t * Tp)  # ilosc krokow
        self.step_number = 1
        self._I = 1  # poprzednia wartosc jednnostki I
        self._kp = kp
        self._Tp = Tp
        self._Td = Td
        self._Ti = Ti

    def run_step(self, check_stop_condition=True):
        if check_stop_condition:
            if self.step_number < self.N:
                self.execute_blocks()
                self.step_number += 1
        else:
            self.execute_blocks()

    def execute_blocks(self):
        err, er_sum, err_delta = self.error.calculate(self.substance_height.get_latest_h())
        un = self.calculatepid(err, err_delta)
        qdn = un
        self.substance_height.calculate(qdn)

    def run_all(self):
        try:
            for x in range(0, self.N):
                self.run_step()
            return 0
        except ValueError:
            return 1

    def calculatepid(self, en, en_delta):
        P = self._kp * en
        self._I = self._I + self._Ti * en * self._Tp
        D = self._Td * en_delta / self._Tp
        return P + self._I + D

    def get_h_values_dict(self) -> dict:
        return self.substance_height.get_hs_dict()

    def get_h_values_list(self) -> []:
        return self.substance_height.get_hs_list()