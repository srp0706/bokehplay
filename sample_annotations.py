# General imports
from bokeh.io import curdoc
from bokeh.layouts import column, gridplot
from bokeh.plotting import figure
from bokeh.models import BoxAnnotation, Span
from bokeh.models.sources import ColumnDataSource
from bokeh.models.widgets import Button, TextInput

# Some data
data1 = {'x': [10,20,30,40,50], 'y': [45,  18,  36,  21,  63]}
data2 = {'x': [1, 2, 3, 4, 5],  'y': [2.6, 3.2, 4.4, 1.5, 2.2]}
cds1 = ColumnDataSource(data1)
cds2 = ColumnDataSource(data2)

# Helper functions
def draw_range():
    try:
        lower = float(txtLower.value)
        upper = float(txtUpper.value)
    except TypeError:
        print("Wrong number type, could not convert to float")
        return
    box_range = BoxAnnotation(left=42, bottom=lower, top=upper, fill_alpha=0.1, fill_color="green")
    fig1.add_layout(box_range)

def draw_span():
    try:
        span = float(txtSpan.value)
    except TypeError:
        print("Wrong number type, could not convert to float")
        return
    draw = Span(name="span", dimension="width", location=span,
                line_alpha=0.5, line_color="red", line_dash="dashed")
    fig1.add_layout(draw)

def sync_axes():
    x1 = data1["x"]
    x2 = data2["x"]
    ratio = (x2[-1]-x2[0])/(x1[-1]-x1[0])
    fig2.x_range.start = x2[0] + ratio*(fig1.x_range.start - x1[0])
    fig2.x_range.end   = x2[0] + ratio*(fig1.x_range.end   - x1[0])


# Set interactions
txtLower = TextInput(title="Lower:", value="{0:.1f}".format(25))
txtUpper = TextInput(title="Upper:", value="{0:.1f}".format(45))
btnDrawLims = Button(width=200, label="Draw range")
btnDrawLims.on_click(draw_range)
txtSpan = TextInput(title="Span:", value="{0:.1f}".format(15))
btnDrawSpan = Button(width=200, label="Draw stop")
btnDrawSpan.on_click(draw_span)
btnSyncAxes = Button(width=200, label="Sync X axes")
btnSyncAxes.on_click(sync_axes)

# Set figures
fig1 = figure(plot_width=400, plot_height=300)
fig1.circle(name="data1", x="x", y="y", fill_color="blue", line_color="blue", source=cds1)
fig2 = figure(plot_width=400, plot_height=300)
fig2.circle(name="data2", x="x", y="y", fill_color="red", line_color="red", source=cds2)

# Set layout and hand over execution to bokeh server
buttons_layout = column(children=[txtLower, txtUpper, btnDrawLims,
                        txtSpan, btnDrawSpan, btnSyncAxes],
                        sizing_mode="scale_width", width=210)
graphs_layout = column(fig2, fig1)
fig2.title.text = "Sample bokeh interactions demo"
curdoc().add_root(gridplot([buttons_layout, graphs_layout], ncols = 2))