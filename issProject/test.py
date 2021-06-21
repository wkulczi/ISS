# import pandas as pd
#
# from issmath.UAR import UAR
# uar = UAR(t=30, Tp=2, A=1, h0=0, hset=3, beta=0.75, kp=0.025, Td=0.035, Ti=0.02)
# uar = UAR(30, 0.5, 1, 0, 3, 0.75, 0.025, 0.035, 0.02)
#
# uar.run_all()
# values = uar.get_h_values_dict()
# x = pd.DataFrame.from_dict(values, orient="index")
#
# print(x)
#
# x.plot.line()


import pandas as pd
from issProject.issmath.WaterFlowSim import WaterFlowSim

waterFlow = WaterFlowSim(t=30, Tp=2, A=1, h0=0, hmax=10, beta=0, Qdn=1)
waterFlow.run_all()
values = waterFlow.get_h_values_dict()
x = pd.DataFrame.from_dict(values, orient="index")

print(x)

x.plot.line()
