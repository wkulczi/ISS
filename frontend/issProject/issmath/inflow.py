# natężenie dopływu = Qd
class Inflow:
    """
          Klasa do wyznaczania wartości natężenia dopływu

          ...
          Methods
          -------
          calculate(un)

              No w sumie to nie wiem co ta funkcja ma robić, nie wspomnieliśmy o tym

              Na razie zrobię Un=Qd

              Parameters
              ----------
              un : float
                      wyznaczona wartość uchybu regulacji w chwili n
          """
    def calculate(self, un):
        return un