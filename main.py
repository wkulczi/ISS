from bokeh.document import Document
from bokeh.io import show, curdoc
from bokeh.models import TextInput, Button, Spinner, DataTable, ColumnDataSource, TableColumn
from bokeh.plotting import figure
import math

# base values
Tp = 1.0
Qd = 1.0
Beta = 1.0
A = 1.0
T = 1.0
N = 0
STEPS = 0

data = {"y": [], "x": []}
qd_queue = []
source = ColumnDataSource(data)
graph_callback_task = None

# components
start_button = Button(label="Start", button_type="success", name="start_button", sizing_mode="stretch_width")
stop_button = Button(label="Stop", button_type="success", name="stop_button", sizing_mode="stretch_width")
clear_button = Button(label="Clear", button_type="success", name="clear_button", sizing_mode="stretch_width")
step_button = Button(label="Step", button_type="success", name="step_button", sizing_mode="stretch_width")
send_button = Button(label="Send", button_type="success", name="send_button", sizing_mode="stretch_width")

a_spinner = Spinner(low=0, value=1.0, step=0.2,    width_policy="min", name="a_spinner")
h0_spinner = Spinner(low=0, value=1.0, step=0.2,   width_policy="min", high=20, name="h0_spinner")
beta_spinner = Spinner(low=0, value=1.0, step=0.2, width_policy="min", name="beta_spinner")
qd_spinner = Spinner(low=0, value=1.0, step=0.2,   width_policy="min", name="qd_spinner")
tp_spinner = Spinner(low=0, value=0.5, step=0.2,   width_policy="min", name="tp_spinner")
t_spinner = Spinner(low=0, value=30, step=0.2,     width_policy="min", name="t_spinner")

p = figure(
    plot_height=120,
    name="bokeh_jinja_figure", sizing_mode="scale_width", toolbar_location="below")
p.line(source=source, x='x', y='y', line_width=2, alpha=0.7)
table = DataTable(sizing_mode="stretch_width", height_policy="max", name='table', source=source, columns=[TableColumn(field="y", title="H", sortable = False)],editable=True)


def start_button_handler():
    # load all values
    load_global_values()

    start_callbacks()


def load_global_values():
    global Tp, Qd, Beta, A, T, N
    Tp = tp_spinner.value
    Qd = qd_spinner.value
    Beta = beta_spinner.value
    A = a_spinner.value
    T = t_spinner.value
    N = T / Tp


def stop_button_handler():
    print("stop")
    stop_callbacks()


def clear_button_handler():
    global data
    global source
    data = {"y": [], "x": []}
    source.data = data


def step_button_handler():
    load_global_values()
    calculate_and_add_new_data()


def calculate_next_h(previous_h):
    global Tp, Qd, Beta, A, T, qd_queue
    if qd_queue:
        Qd = qd_queue.pop()
    hn = (((-Beta * math.sqrt(previous_h) + Qd) * Tp) / A) + previous_h
    return float("{:.2f}".format(hn))


def calculate_new_data_if_N():
    global STEPS, N
    if STEPS < int(N):
        calculate_and_add_new_data()
        STEPS += 1
    else:
        stop_callbacks()


def calculate_and_add_new_data():
    h0 = h0_spinner.value

    new_data = {'x': [], 'y': []}
    if len(data['x']) < 1:
        h = h0
    else:
        h = calculate_next_h(data['y'][-1])
    new_data['x'].append(len(data['x']))
    new_data['y'].append(h)

    source.stream(new_data=new_data)


def start_callbacks():
    global graph_callback_task
    if STEPS < int(N):
        graph_callback_task = curdoc().add_periodic_callback(calculate_new_data_if_N, 1000)

        step_button.disabled = True
        start_button.disabled = True
        clear_button.disabled = True
        stop_button.disabled = False

        a_spinner.disabled = True
        t_spinner.disabled = True
        tp_spinner.disabled = True
        h0_spinner.disabled = True
        beta_spinner.disabled = True


def stop_callbacks():
    global STEPS, graph_callback_task
    STEPS = 0
    curdoc().remove_periodic_callback(graph_callback_task)

    start_button.disabled = False
    step_button.disabled = False
    clear_button.disabled = False
    stop_button.disabled = True

    a_spinner.disabled = False
    t_spinner.disabled = False
    tp_spinner.disabled = False
    h0_spinner.disabled = False
    beta_spinner.disabled = False


def apply_qd_change():
    global Qd
    change_value = qd_spinner.value - Qd
    if abs(change_value) > 0.5:
        change_step = change_value / 2
        print("applying change. New value should be: {}, change: {}, half the change is: {}".format(qd_spinner.value,
                                                                                                    change_value,
                                                                                                    change_step))
        qd_queue.extend([qd_spinner.value, Qd + change_step])
    else:
        Qd = qd_spinner.value


# component callbacks
start_button.on_click(start_button_handler)
stop_button.on_click(stop_button_handler)
clear_button.on_click(clear_button_handler)
step_button.on_click(step_button_handler)
send_button.on_click(apply_qd_change)
# other component configuration
p.toolbar.autohide = True
stop_button.disabled = True
clear_button.disabled = True
#
curdoc().add_root(a_spinner)
curdoc().add_root(send_button)
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

doc = Document()


def closeStuff(session_context):
    stop_callbacks()


doc.on_session_destroyed(closeStuff)
