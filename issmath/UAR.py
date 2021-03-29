import math


class UAR:
    def __init__(self, h0=1, A=1, Tp=1, t=1, Qdn=1, beta=1, hset=1) -> None:
        self.set_values(h0, A, Tp, t, Qdn, beta, hset)
        self.qdn_queue = []
        self.step_number = 0

    def set_values(self, h0=0, A=0, Tp=0, t=0, Qdn=0, beta=0, hset=0, reset_h=True):
        if reset_h:
            self._h = [h0]
        self._A = A
        self._Tp = Tp
        self._t = t
        self._Qdn = Qdn
        self._beta = beta
        self._hset = hset
        self.N = self.calculate_max_steps()


    def calculate_max_steps(self):
        return self._t / self._Tp

    def get_Qdn(self):
        if self.qdn_queue:
            return self.qdn_queue.pop()
        else:
            return self._Qdn

    def set_Qdn(self, newQdn):
        change_value = self._Qdn - newQdn
        if abs(change_value) > 0.5:
            change_step = change_value / 2
            self.qdn_queue.extend([newQdn.value, self._Qdn + change_step])
        self._Qdn = newQdn

    def get_h(self):
        return self._h

    def get_previous_h(self):
        return self._h[-1]

    def count_h_step(self):
        return (((-self._beta * math.sqrt(self._h[-1]) + self.get_Qdn()) * self._Tp) / self._A) + self._h[-1]

    def count_and_add_h_step(self, return_value=False):
        if self.step_number < self.N:
            hn = self.count_h_step()
            self._h.append(hn)
            self.step_number += 1
            if return_value:
                return hn

    def should_stop(self):
        return self.step_number >= self.N

    def get_latest_h(self):
        return self._h[-1]

    def reset_steps(self):
        self.step_number = 0
