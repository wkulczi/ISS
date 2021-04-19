# wartość początkowa poziomu
# okres próbkowania
# pole powierzchni pola poprzecznego
# współczynnik wypływu


# h w chwili 0
# A o polu przekroju
# czas / próbkowanie  = n = warunek stopu
# A, beta, Tp, natężenie dopływu i on nam policzy h(n)
# Tp = okres próbkowania
# A = pole powierzchni przekroju poprzecznego zbiornika
# beta = uproszczona wartość określająca wypływ swobodny

# czas badania / okres próbkowania = n obrotów


def count_step(hn, Tp, Qdn, beta, A):
    import math
    return (((-beta * math.sqrt(hn) + Qdn) * Tp) / A) + hn


def getQdn():
    # tutaj bokehem z okienka z wartością musi być fetchowane per krok, żeby tym sterować
    return 1


# Proces I: napełnianie zbiornika
def proc1(h0=0, t=20, Tp=0.5, beta=1, A=1):
    h = [h0]
    N = t / Tp
    for step in range(0, int(N)):
        Qdn = getQdn()
        hn = count_step(hn=h[step], Tp=Tp, Qdn=Qdn, beta=beta, A=A)
        h.append(hn)
    print(h)


if __name__ == "__main__":
    proc1(beta=0)
