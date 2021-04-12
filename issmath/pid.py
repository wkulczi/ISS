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
        return self._kp * (en + (self._Tp / self._Ti) * en_sum + (self._Td / self._Tp) * en_delta)
