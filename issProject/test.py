import pandas as pd

from issmath.UAR import UAR
uar = UAR(t=30, Tp=2, A=1, h0=0, hset=3, beta=0.75, kp=0.025, Td=0.035, Ti=0.02)
uar.run_all()
values = uar.get_h_values_dict()
x = pd.DataFrame.from_dict(values, orient="index")

print(x)

x.plot.line()
