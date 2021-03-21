from bokeh.io import show, curdoc
from bokeh.models import TextInput, Button, Spinner, DataTable, ColumnDataSource, TableColumn
from bokeh.plotting import figure

data = {"y": [], "x": []}
source = ColumnDataSource(data)
graph_callback_task = None

# components
start_button = Button(label="Start", button_type="success", name="start_button", sizing_mode="stretch_width")
stop_button = Button(label="Stop", button_type="success", name="stop_button"   , sizing_mode="stretch_width")
clear_button = Button(label="Clear", button_type="success", name="clear_button", sizing_mode="stretch_width")
step_button = Button(label="Step", button_type="success", name="step_button"   , sizing_mode="stretch_width")

a_spinner = Spinner   (low=0,value = 1, step = 0.3,name="a_spinner")
h0_spinner = Spinner  (low=0,value = 1, step = 0.3,high=20, name="h0_spinner")
beta_spinner = Spinner(low=0,value = 1, step = 0.3,name="beta_spinner")
qd_spinner = Spinner  (low=0,value = 1, step = 0.3,name="qd_spinner")
tp_spinner = Spinner  (low=0,value = 1, step = 0.3,name="tp_spinner")
t_spinner = Spinner   (low=0,value = 1, step = 0.3,name="t_spinner")

p = figure(
    name="bokeh_jinja_figure", sizing_mode="stretch_width")
p.line(source=source, x='x', y='y', line_width=2, alpha=0.7)
p.toolbar.autohide = True
table = DataTable(name='table', source=source, columns=[TableColumn(field="y", title="H")], editable=True)


def start_button_handler():
    start_callbacks()
    print("start")


def stop_button_handler():
    print("stop")
    stop_callbacks()


def clear_button_handler():
    print("clear")


def step_button_handler():
    print("step")


def calculate_next_h(last_h):
    return last_h + 1


def calculate_and_add_new_data():
    new_data = {'x': [], 'y': []}
    if len(data['x']) < 1:
        # todo weź to ze spinnera
        h = calculate_next_h(0)
    else:
        h = calculate_next_h(data['y'][-1])
    new_data['x'].append(len(data['x']))
    new_data['y'].append(h)

    source.stream(new_data=new_data)

#  i wystarczy graf powiązać z source.data i odpalić callback funkcją start_callbacks

def start_callbacks():
    global graph_callback_task
    graph_callback_task = curdoc().add_periodic_callback(calculate_and_add_new_data, 1500)


def stop_callbacks():
    global graph_callback_task
    curdoc().remove_periodic_callback(graph_callback_task)
    print("callback stopped")


# component callbacks
start_button.on_click(start_button_handler)
stop_button.on_click(stop_button_handler)
clear_button.on_click(clear_button_handler)
step_button.on_click(step_button_handler)

#
curdoc().add_root(a_spinner)
curdoc().add_root(h0_spinner)
curdoc().add_root(beta_spinner)
curdoc().add_root(qd_spinner)
curdoc().add_root(tp_spinner)
curdoc().add_root(t_spinner)
curdoc().add_root(start_button)
curdoc().add_root(stop_button)
curdoc().add_root(clear_button)
curdoc().add_root(step_button)
curdoc().add_root(p)
curdoc().add_root(table)
