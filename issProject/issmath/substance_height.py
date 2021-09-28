# poziom substancji w zbiorniku
import math

class SubstanceHeight:
    """
   Klasa do policzenia wysokości słupa substancji w zbiorniku

   ...

   Attributes
   ----------
   h : float
       historia wysokości słupa substancji w zbiorniku
   A : float
       pole powierzchni przekroju poprzecznego zbiornika [m^2]
   Tp : float
       Czas próbkowania (co ile sekund jest następny tick) [s]
   beta : float
       współczynnik wypływu substancji przez otwór w zbiorniku [(m^(5/2))/s]

   Methods
   -------
   calculate(Qdn=0)
       Parameters
       ----------
       Qdn : float
               Natężenie dopływu w chwili n
       Liczy wysokość słupa substancji w chwili n i zapisuje do historii
   """

    def __init__(self, h0, A, Tp, beta:float, hmax) -> None:
        """
           Parameters
           ----------
           h0 : float
               wysokość słupa cieczy w chwili 0
           A : float
               pole powierzchni przekroju poprzecznego zbiornika [m^2]
           Tp : int
               Czas próbkowania (co ile sekund jest następny tick) [s]
           beta : int
                współczynnik wypływu substancji przez otwór w zbiorniku [(m^(5/2))/s]
           """
        self._h = [h0]
        self._Tp = 1/Tp
        self._A = A
        self._beta = beta
        self._hmax = hmax

    def _count_h_step(self, Qdn):
        h1=self._h[-1]
        Q0=self._beta*math.sqrt(h1)
        h=(Qdn-Q0)*(self._Tp/self._A)+h1
        return h

    def calculate(self, Qdn, return_value=False):
        hn = self._count_h_step(Qdn)
        if hn > self._hmax:
            self._h.append(self._hmax)
        else:
            self._h.append(hn)
        if return_value:
            return hn

    def get_latest_h(self):
        return self._h[-1]

    def get_hs_dict(self) -> dict:
        return {i: self._h[i] for i in range(0, len(self._h))}

    def get_hs_list(self) -> list():
        return [round(x,2) for x in self._h]
