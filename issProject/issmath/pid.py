# wielkość sterująca - PID

class PID:
    """
       Klasa do wyznaczenia wartości wielkości sterującej

       ...

       Attributes
       ----------
       kp : float
           wzmocnienie regulatora
       Td : float
           czas wyprzedzenia [s]
       Ti : float
           czas zdwojenia [s]
       Tp : float
           Czas próbkowania (co ile sekund jest następny tick) [s]

       Methods
       -------
       calculate(sound=None)
           Liczy wysokość słupa substancji w chwili n i zapisuje do historii
       """

    def __init__(self, kp, Tp, Ti, Td):
        self._kp = kp
        self._Tp = Tp
        self._Ti = Ti
        self._Td = Td
        self._I = 1

    def calculate(self, en, en_sum, en_delta):
        """
           Parameters
           ----------
           en : float
               uchyb regulacji w chwili n
           en_sum : float
               suma uchybów regulacji od chwili 0 do n
           en_delta : int
               różnica uchybów regulacji e(n) - e(n-1)
        """
        P = self._kp * en
        self._I = self._I + self._Ti * en * self._Tp
        D = self._Td * en_delta / self._Tp
        return P + self._I + D
