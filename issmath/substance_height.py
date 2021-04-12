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

    def __init__(self, h0, A, Tp, beta) -> None:
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
        self._Tp = Tp
        self._A = A
        self._beta = beta

    def calculate(self, Qdn=0):
        return self._count_and_add_step(Qdn)

    def _count_h_step(self, Qdn):
        return (((-self._beta * math.sqrt(self._h[-1]) + Qdn) * self._Tp) / self._A) + self._h[-1]

    def _count_and_add_step(self, Qdn, return_value=True):
        hn = self._count_h_step(Qdn)
        self._h.append(hn)
        if return_value:
            return hn
