# General imports
import pandas as pd
from bokeh.io import curdoc
from bokeh.layouts import gridplot
from bokeh.plotting import figure
from bokeh.models.sources import ColumnDataSource
from bokeh.models.widgets import Button
from datetime import date, datetime, timedelta
from numpy import array

# Prepare the data series
superset = pd.DataFrame({'date': [date(2018, 6, 4), 
                                  date(2018, 6, 5), 
                                  date(2018, 6, 6), 
                                  date(2018, 6, 7), 
                                  date(2018, 6, 8), 
                                  date(2018, 6, 11), 
                                  date(2018, 6, 12), 
                                  date(2018, 6, 13), 
                                  date(2018, 6, 14), 
                                  date(2018, 6, 15), 
                                  date(2018, 6, 18), 
                                  date(2018, 6, 19), 
                                  date(2018, 6, 20), 
                                  date(2018, 6, 21), 
                                  date(2018, 6, 22), 
                                  date(2018, 6, 25), 
                                  date(2018, 6, 26), 
                                  date(2018, 6, 27), 
                                  date(2018, 6, 28), 
                                  date(2018, 6, 29), 
                                  date(2018,7, 2), 
                                  date(2018, 7, 3), 
                                  date(2018, 7, 4), 
                                  date(2018, 7, 5), 
                                  date(2018, 7, 6), 
                                  date(2018, 7, 10), 
                                  date(2018, 7, 11), 
                                  date(2018, 7, 12), 
                                  date(2018, 7, 13),
                                  date(2018, 7, 16)],
                         'values': [37.7, 36.7, 35.6, 33.2, 34.0, 32.3, 33.2, 32.9, 31.9, 29.8, 
                                    29.6, 30.1, 30.7, 29.0, 28.6, 28.6, 28.4, 28.6, 29.7, 29.3, 
                                    28.9, 31.0, 32.9, 32.4, 32.2, 31.5, 30.1, 32.9, 33.3, 32.8],
                         'x_pos': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                                   10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                                   20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
                        })

def get_graph_data(data,init_pos,time_delta):
    # A function that receives a DataFrame with a date column and returns a filtered
    #     DataFrame with the data from init_date through 6 months.
    init_date = data.iloc[init_pos,:].loc["date"]
    if ((data.iloc[-1,:].loc["date"] - init_date) > timedelta(days=time_delta)):
        final_pos = init_pos + 1
        final_date = data.iloc[final_pos,:].loc["date"]
    else:
        print("Error. Init point too close to data series end.")
        return None
        
    while ((final_date - init_date < timedelta(days=time_delta)) and (final_pos < len(data.loc[:,"date"]))):
        final_pos = final_pos + 1
        final_date = data.iloc[final_pos,:].loc["date"]
    print("Getting graph data... final date is {0:%F}".format(final_date))
    return data.iloc[init_pos:final_pos+1,:]


def build_graph(datasource):
    # A function to build the main graph  
    # Create graph
    TOOLS = "pan,wheel_zoom,box_zoom,reset"
    fig = figure(tools=TOOLS, plot_width=950, plot_height=225)
    fig.xaxis.major_label_text_font_size='0pt'
    fig.xgrid.grid_line_color="#000000"
    fig.xgrid.grid_line_alpha=0.3

    # Add glyphs
    fig.circle(x='x_pos', y='values', name='points', color='blue', source=datasource)
    return fig


def add_one_day():
    # This function will add one data point to the graph
    if (not isinstance(subset.data["date"][-1],date)):
        print("dates are not of type datetime.date. value: {0}\nConverting...".format(subset.data["date"][-1]))
        import pytz
        utc = pytz.timezone("UTC")
        conv_dates = []
        for el in subset.data["date"]:
            tmp_date = datetime.fromtimestamp(el/1000,utc)
            el = date(tmp_date.year, tmp_date.month, tmp_date.day)
            conv_dates.append(el)
        subset.data["date"]=conv_dates
        print("After conversion:\n{0}".format(subset.data))
    days_distance = subset.data["date"][-1] - subset.data["date"][0]
    # Get new data series
    if (days_distance.days + 1 < 35):
        update_subset = ColumnDataSource(get_graph_data(superset, 0, days_distance.days+1))
        subset.data.update(update_subset.data)
    else:
        print("End of preview reached.")

print("Helper functions defined.")

# Get data for graph
subset = ColumnDataSource(get_graph_data(superset, 0, 30))
print("subset defined. type: {0}\n dates: {1}".format(type(subset.data["date"][-1]), subset.data["date"]))

# Setup graph
graph = build_graph(subset)

# Add control button
btnAddOneDay = Button(label="Add one day")
btnAddOneDay.on_click(add_one_day)

# Show graphs
curdoc().add_root(gridplot([btnAddOneDay, graph],
                           ncols = 2))