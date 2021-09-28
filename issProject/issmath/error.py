class Error:
    """
      Klasa do wyznaczenia wartości uchybu regulacji
      ...
      Attributes
      ----------
      hz : float
          zadana wysokość słupa substancji w zbiorniku
      e : table
          tablica uchybów = różnica obecnego i pożądanego poziomu wody
      """
    def __init__(self, hz):
        self._e = []
        self._hz = hz

    def _calculate_delta(self):
        if len(self._e) >= 2:
            return self._e[-1] - self._e[-2]
        elif len(self._e) <= 1:
            return 0

    def calculate(self, hn):
        en = self._hz - hn
        self._e.append(en)
        en_sum = sum(self._e)
        en_delta = self._calculate_delta()
        return en, en_sum, en_delta
