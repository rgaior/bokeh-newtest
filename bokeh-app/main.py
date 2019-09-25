''' Create a simple stocks correlation dashboard.

Choose stocks to compare in the drop down widgets, and make selections
on the plots to update the summary and histograms accordingly.

.. note::
    Running this example requires downloading sample data. See
    the included `README`_ for more information.

Use the ``bokeh serve`` command to run the example by executing:

    bokeh serve stocks

at your command prompt. Then navigate to the URL

    http://localhost:5006/stocks

.. _README: https://github.com/bokeh/bokeh/blob/master/examples/app/stocks/README.md

'''
try:
    from functools import lru_cache
except ImportError:
    # Python 2 does stdlib does not have lru_cache so let's just
    # create a dummy decorator to avoid crashing
    print ("WARNING: Cache for this example is available on Python 3 only.")
    def lru_cache():
        def dec(f):
            def _(*args, **kws):
                return f(*args, **kws)
            return _
        return dec

from os.path import dirname, join

import pandas as pd
import numpy as np
from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import PreText, Select
from bokeh.plotting import figure
from bokeh.layouts import gridplot


DATA_TICKERS = ['IDM', 'POSTIDM', 'ALL']

def nix(val, lst):
    return [x for x in lst if x != val]

data_dict = {'IDM':'datalowEIDM.pkl','POSTIDM':'datalowEPostIDM.pkl','ALL':'datalowE.pkl'}
#data_dict = {'IDM':'datalowE.pkl','POSTIDM':'datalowE.pkl','ALL':'datalowE.pkl'}
datafolder = './bokeh-app/data/'
@lru_cache()
def load_ticker(ticker):
    datafile = datafolder + data_dict[ticker]
    return pd.read_pickle(datafile)

@lru_cache()
def get_data(t1):
    data = load_ticker(t1)
    data = data.dropna()
    
    return data

# set up widgets

#stats = PreText(text='', width=800, height=500)
stats = PreText(text='',style={'font-size': '200%', 'color': 'blue'})

ticker1 = Select(value='IDM', options=DATA_TICKERS, width=400,height=80,default_size= 30, title='data set',background='lightblue')

# set up plots
source = ColumnDataSource(data=dict(x=[], y=[]))
source_static = ColumnDataSource(data=dict(x=[], y=[]))

def update_stats(data, t1):
#    stats.text = str(data[[t1]].describe())
    stats.text = str(data[["ene1","sigma","dll"]].describe())

# initialization
t1 = ticker1.value
data = get_data(t1)
source.data = source.from_df(data[['centerx', 'centery','ene1','sigma','figure']])
source_static.data = source.data
update_stats(data, t1)

    
tools = 'pan,wheel_zoom,xbox_select,reset,lasso_select'
TOOLTIPS = """
    <div>
        <div> 
            <img
                src="@figure" height="400" alt="@figure" width="600"
                style="float: left; margin: 0px 15px 15px 0px;"
                border="2"
            ></img>
        </div>
    </div>
"""

position = figure(plot_width=600, plot_height=600,tooltips=TOOLTIPS,
                  tools=tools)
position.circle('centerx', 'centery', size=5, source=source,
                selection_color="orange", alpha=0.8, nonselection_alpha=0.8, selection_alpha=0.8)

position.xaxis.axis_label = "X [pixel]"
position.yaxis.axis_label = "Y [1x100 pixel]"
position.xaxis.axis_label_text_font_size = "20pt"
position.yaxis.axis_label_text_font_size = "20pt"
position.yaxis.major_label_text_font_size = "20pt"
position.xaxis.major_label_text_font_size = "20pt"
position.xaxis[0].ticker.desired_num_ticks = 3

esigma = figure(plot_width=600, plot_height=600,tooltips=TOOLTIPS,
                tools=tools)
esigma.circle('ene1', 'sigma', size=5, source=source,
              selection_color="orange", alpha=0.8, nonselection_alpha=0.8, selection_alpha=0.8)
esigma.xaxis.axis_label = "Energy [keV]"
esigma.yaxis.axis_label = "depth [sigma]"
esigma.xaxis.axis_label_text_font_size = "20pt"
esigma.yaxis.axis_label_text_font_size = "20pt"
esigma.yaxis.major_label_text_font_size = "20pt"
esigma.xaxis.major_label_text_font_size = "20pt"
esigma.xaxis[0].ticker.desired_num_ticks = 3
################
### definition of histos for the projections
################
## energy histo:
hhist, hedges = np.histogram(source.data['ene1'], bins=20)
hzeros = np.zeros(len(hedges)-1)
hmax = max(hhist)*1.1
LINE_ARGS = dict(color="#3A5785", line_color=None)
ph = figure(toolbar_location=None, plot_width = esigma.plot_width, plot_height = 200,x_range = esigma.x_range,y_range=(-hmax, hmax), min_border=10, min_border_left=50, y_axis_location="right")
ph.xgrid.grid_line_color = None
ph.yaxis.major_label_orientation = np.pi/4
ph.background_fill_color = "#fafafa"
ph.quad(bottom=0, left=hedges[:-1], right=hedges[1:], top=hhist, color="white", line_color="#3A5785")
hh1 = ph.quad(bottom=0, left=hedges[:-1], right=hedges[1:], top=hzeros, alpha=0.5, **LINE_ARGS)
hh2 = ph.quad(bottom=0, left=hedges[:-1], right=hedges[1:], top=hzeros, alpha=0.1, **LINE_ARGS)

# create the vertical histogram                                                                    
vhist, vedges = np.histogram(source.data['sigma'], bins=20)
vzeros = np.zeros(len(vedges)-1)
vmax = max(vhist)*1.1

## sigma histo:
pv = figure(toolbar_location=None, plot_width=200, plot_height=esigma.plot_height, x_range=(-vmax, vmax), y_range=esigma.y_range, min_border=10, y_axis_location="right")
pv.ygrid.grid_line_color = None
pv.xaxis.major_label_orientation = np.pi/4
pv.background_fill_color = "#fafafa"
pv.quad(left=0, bottom=vedges[:-1], top=vedges[1:], right=vhist, color="white", line_color="#3A5785")
vh1 = pv.quad(left=0, bottom=vedges[:-1], top=vedges[1:], right=vzeros, alpha=0.5, **LINE_ARGS)
vh2 = pv.quad(left=0, bottom=vedges[:-1], top=vedges[1:], right=vzeros, alpha=0.1, **LINE_ARGS)

layout = gridplot([[esigma,pv], [ph, None]], merge_tools=False)

## x histo:
xhhist, xhedges = np.histogram(source.data['centerx'], bins=20)
xhzeros = np.zeros(len(xhedges)-1)
xhmax = max(xhhist)*1.1
LINE_ARGS = dict(color="#3A5785", line_color=None)
xph = figure(toolbar_location=None, plot_width = position.plot_width, plot_height = 200,x_range = position.x_range,y_range=(-xhmax, xhmax), min_border=10, min_border_left=50, y_axis_location="right")
xph.xgrid.grid_line_color = None
xph.yaxis.major_label_orientation = np.pi/4
xph.background_fill_color = "#fafafa"
xph.quad(bottom=0, left=xhedges[:-1], right=xhedges[1:], top=xhhist, color="white", line_color="#3A5785")
xhh1 = xph.quad(bottom=0, left=xhedges[:-1], right=xhedges[1:], top=xhzeros, alpha=0.5, **LINE_ARGS)
xhh2 = xph.quad(bottom=0, left=xhedges[:-1], right=xhedges[1:], top=xhzeros, alpha=0.1, **LINE_ARGS)

# create the vertical histogram                                                                    
yvhist, yvedges = np.histogram(source.data['centery'], bins=20)
yvzeros = np.zeros(len(yvedges)-1)
yvmax = max(yvhist)*1.1

## centery histo:
ypv = figure(toolbar_location=None, plot_width=200, plot_height=position.plot_height, x_range=(-yvmax, yvmax), y_range=position.y_range, min_border=10, y_axis_location="right")
ypv.ygrid.grid_line_color = None
ypv.xaxis.major_label_orientation = np.pi/4
ypv.background_fill_color = "#fafafa"
ypv.quad(left=0, bottom=yvedges[:-1], top=yvedges[1:], right=yvhist, color="white", line_color="#3A5785")
yvh1 = ypv.quad(left=0, bottom=yvedges[:-1], top=yvedges[1:], right=yvzeros, alpha=0.5, **LINE_ARGS)
yvh2 = ypv.quad(left=0, bottom=yvedges[:-1], top=yvedges[1:], right=yvzeros, alpha=0.1, **LINE_ARGS)

positionlayout = gridplot([[position,ypv], [xph, None]], merge_tools=False)

#def plot_hist(data):
# create the horizontal histogram                                                                  
    

# ts1 = figure(plot_width=900, plot_height=200, tools=tools, x_axis_type='datetime', active_drag="xbox_select")
# ts1.line('RUNID', '', source=source_static)
# ts1.circle('date', 't1', size=1, source=source, color=None, selection_color="orange")

# ts2 = figure(plot_width=900, plot_height=200, tools=tools, x_axis_type='datetime', active_drag="xbox_select")
# ts2.x_range = ts1.x_range
# ts2.line('date', 't2', source=source_static)
# ts2.circle('date', 't2', size=1, source=source, color=None, selection_color="orange")

# set up callbacks

def ticker1_change(attrname, old, new):
#    ticker2.options = nix(new, DEFAULT_TICKERS)
    update()

def ticker2_change(attrname, old, new):
#    ticker1.options = nix(new, DEFAULT_TICKERS)
    update()

def update(selected=None):
#    t1 = data_dict[ticker1.value]
    t1 = ticker1.value

    data = get_data(t1)
    source.data = source.from_df(data[['centerx', 'centery','ene1','sigma','figure']])
    source_static.data = source.data
    
    update_stats(data, t1)

#    corr.title.text = '%s returns vs. %s returns' % (t1, t2)
#    ts1.title.text, ts2.title.text = t1, t2


ticker1.on_change('value', ticker1_change)

def selection_change(attrname, old, new):
#    t1 = data_dict[ticker1.value]
    t1 = ticker1.value
    data = get_data(t1)
    selected = source.selected.indices
    if selected:
        data = data.iloc[selected, :]
    update_stats(data, t1)
#    plot_hist(data)

    inds = new
    if len(inds) == 0 or len(inds) == len(source.data['ene1']):
        hhist1, hhist2 = hzeros, hzeros
        vhist1, vhist2 = vzeros, vzeros
    else:
        neg_inds = np.ones_like(source.data['ene1'], dtype=np.bool)
        neg_inds[inds] = False
        hhist1, _ = np.histogram(source.data['ene1'][inds], bins=hedges)
        vhist1, _ = np.histogram(source.data['sigma'][inds], bins=vedges)
        hhist2, _ = np.histogram(source.data['ene1'][neg_inds], bins=hedges)
        vhist2, _ = np.histogram(source.data['sigma'][neg_inds], bins=vedges)
    hh1.data_source.data["top"]   =  hhist1
    hh2.data_source.data["top"]   = -hhist2
    vh1.data_source.data["right"] =  vhist1
    vh2.data_source.data["right"] = -vhist2

    if len(inds) == 0 or len(inds) == len(source.data['centerx']):
        xhhist1, xhhist2 = xhzeros, xhzeros
        yvhist1, yvhist2 = yvzeros, yvzeros
    else:
        neg_inds = np.ones_like(source.data['centerx'], dtype=np.bool)
        neg_inds[inds] = False
        xhhist1, _ = np.histogram(source.data['centerx'][inds], bins=xhedges)
        yvhist1, _ = np.histogram(source.data['centery'][inds], bins=yvedges)
        xhhist2, _ = np.histogram(source.data['centerx'][neg_inds], bins=xhedges)
        yvhist2, _ = np.histogram(source.data['centery'][neg_inds], bins=yvedges)


    xhh1.data_source.data["top"]   =  xhhist1
    xhh2.data_source.data["top"]   = -xhhist2
    yvh1.data_source.data["right"] =  yvhist1
    yvh2.data_source.data["right"] = -yvhist2


source.selected.on_change('indices', selection_change)

#set up layout
#widgets = column(ticker1, stats)
#main_row = row(widget,layout,positionlayout)
#series = column(ts1)
#layout = column(main_row)
plots = row(layout,positionlayout)
layout = column(ticker1, plots, stats)

# initialize
#update()

curdoc().add_root(layout)
curdoc().title = "low energy clusters"
