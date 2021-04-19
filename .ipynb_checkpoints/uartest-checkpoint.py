import pandas as pd

from issProject.issmath.UAR import UAR

uar = UAR(30, 0.5, 1, 0, 3, 0.75, 0.025, 0.035, 0.02)
uar.run_all()
values = uar.get_h_values()
x = pd.DataFrame.from_dict(values, orient="index")

print(x)

x.plot.line()