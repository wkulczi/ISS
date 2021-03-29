from bokeh.document import Document
from bokeh.io import show, curdoc
from bokeh.models import TextInput, Button, Spinner, DataTable, ColumnDataSource, TableColumn
from bokeh.plotting import figure

from issmath.UAR import UAR

uar = UAR()

data = {"y": [], "x": []}
source = ColumnDataSource(data)
graph_callback_task = None

# components
start_button = Button(label="Start", button_type="success", name="start_button", sizing_mode="stretch_width")
stop_button = Button(label="Stop", button_type="success", name="stop_button", sizing_mode="stretch_width")
clear_button = Button(label="Clear", button_type="success", name="clear_button", sizing_mode="stretch_width")
step_button = Button(label="Step", button_type="success", name="step_button", sizing_mode="stretch_width")
send_button = Button(label="Send", button_type="success", name="send_button", sizing_mode="stretch_width")

a_spinner = Spinner(low=0, value=1.0, step=0.2, width_policy="min", name="a_spinner")
h0_spinner = Spinner(low=0, value=1.0, step=0.2, width_policy="min", high=20, name="h0_spinner")
beta_spinner = Spinner(low=0, value=1.0, step=0.2, width_policy="min", name="beta_spinner")
qd_spinner = Spinner(low=0, value=1.0, step=0.2, width_policy="min", name="qd_spinner")
tp_spinner = Spinner(low=0, value=0.5, step=0.2, width_policy="min", name="tp_spinner")
t_spinner = Spinner(low=0, value=30, step=0.2, width_policy="min", name="t_spinner")

p = figure(
    plot_height=120,
    name="bokeh_jinja_figure", sizing_mode="scale_width", toolbar_location="below")
p.line(source=source, x='x', y='y', line_width=2, alpha=0.7)
table = DataTable(sizing_mode="stretch_width", height_policy="max", name='table', source=source,
                  columns=[TableColumn(field="y", title="H", sortable=False)], editable=True)


def start_button_handler():
    # load all values
    init_uar()
    start_callbacks()


def init_uar(reset_h = True):
    uar.set_values(h0=h0_spinner.value,
                   A=a_spinner.value,
                   Tp=tp_spinner.value,
                   t=t_spinner.value,
                   Qdn=qd_spinner.value,
                   beta=beta_spinner.value,
                   reset_h = reset_h)


def stop_button_handler():
    print("stop")
    stop_callbacks()


def clear_button_handler():
    global data
    global source
    data = {"y": [], "x": []}
    source.data = data


def step_button_handler():
    init_uar(reset_h = False)
    calc_step()


def calculate_new_data_if_N():
    if not uar.should_stop():
        calc_step()
    else:
        stop_callbacks()


def calc_step():
    new_h = uar.count_and_add_h_step(return_value=True)
    append_to_table(float("{:.2f}".format(new_h)))


def append_to_table(new_h):
    new_data = {'x': [], 'y': []}
    new_data['x'].append(len(data['x']))
    new_data['y'].append(new_h)

    source.stream(new_data=new_data)


def start_callbacks():
    global graph_callback_task
    if not uar.should_stop():
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
    uar.reset_steps()
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
    print(qd_spinner)
    print(type(qd_spinner))
    uar.set_Qdn(qd_spinner.value)


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
