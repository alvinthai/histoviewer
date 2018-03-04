from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler
from bokeh.io import show, output_notebook
from bokeh.io.state import curstate
from bokeh.layouts import column, row, widgetbox
from bokeh.plotting import curdoc, figure
from bokeh.models import ColumnDataSource, Spacer
from bokeh.models.widgets import (Button, RadioButtonGroup,
                                  RangeSlider, Select,
                                  Slider, TextInput)

import math
import numpy as np
import pandas as pd


def histoviewer(df, default_col=None, serve='notebook'):
    '''
    Creates an interactive application of histograms and bar charts for a
    pandas DataFrame input.

    Histograms (continuous variables) have interactive inputs for:
        - rebinning histogram from 10-100 bins
        - rescaling minimum/maximum bounds of histogram
    Bar Charts (categorical variables) have interactive inputs for:
        - resorting by y-axis (descending) or x-axis (alphabetical)
        - reindexing x-axis to filter categories

    Default serve mode assumes jupyter notebook. Histoviewer application could
    also be served from a python script via:
        histoviewer(df, serve='shell')

    If running from shell, execute:
        bokeh serve {script_name}.py
    at your command prompt. Then navigate to the URL
        http://localhost:5006/{script_name}
    '''

    # ========================================================
    # Initialize Default Parameters
    # ========================================================

    cols = []

    for col in df.columns:
        if len(df[col].unique()) != len(df):
            if df[col].dtype in [int, float, bool, object]:
                cols.append(col)
            else:
                try:
                    if df[col].dtype == 'category':
                        cols.append(col)
                except TypeError:
                    # unsupported dtype for histoviewer
                    print 'plotting unavailable for {}'.format(col)
        else:
            # ignore plotting for identification columns
            print 'plotting ignored for {}'.format(col)

    if default_col is None:
        default_col = cols[0]

    default_min = ''
    default_max = ''
    default_bins = 50

    # ========================================================
    # Bokeh Application Setup
    # ========================================================

    def modify_doc(doc):
        def change_categorical():
            '''
            bokeh plot application for categorical variables
            '''
            def update_bars(attr, old, new):
                '''
                callback for reindexing x-axis with slider
                '''
                data = df[select.value].value_counts()

                if radio_button_group.active == 1:
                    data = data.sort_index()

                start = int(round(new[0], 0))
                end = int(round(new[1], 0)) + 1

                data = data.iloc[start:end]
                keys = data.keys().tolist()
                vals = data.values

                p.x_range.factors = keys
                datasource.data = {'x': keys, 'top': vals}

            def update_barsort(attr, old, new):
                '''
                callback for changing sort method of bars
                '''
                data = df[select.value].value_counts()
                range_slider.value = (range_slider.start, range_slider.end)

                if new == 1:
                    data = data.sort_index()

                keys = data.keys().tolist()
                vals = data.values

                p.x_range.factors = keys
                datasource.data = {'x': keys, 'top': vals}

            # ============================
            # Plot Setup (Categorical)
            # ============================

            # fetch data
            data = df[select.value].value_counts()
            categories = len(data) - 1
            keys = data.keys().tolist()
            vals = data.values
            datasource = ColumnDataSource({'x': keys, 'top': vals})

            # create plot
            p = figure(x_range=keys, plot_height=600, plot_width=680,
                       min_border_bottom=200, min_border_left=80)
            p.vbar(x='x', top='top', width=0.9, source=datasource)

            # format plot
            p.xaxis.major_label_orientation = math.pi/2
            p.yaxis.axis_label = 'count'
            p.title.text = 'Barchart of {}'.format(select.value)
            p.xgrid.visible = False

            # create interactive tools
            range_slider = RangeSlider(start=0, end=categories,
                                       value=(0, categories), step=1,
                                       title="Index Selector")
            radio_button_group = RadioButtonGroup(labels=["Sort by y-axis",
                                                          "Sort by x-axis"],
                                                  active=0)

            range_slider.on_change('value', update_bars)
            radio_button_group.on_change('active', update_barsort)

            # add to application
            root = column(row(column(widgetbox(radio_button_group),
                                     widgetbox(range_slider)),
                              Spacer(height=150)), p)
            doc.add_root(root)

            if len(doc.roots) == 3:
                # remove plots for previous column variable
                doc.remove_root(doc.roots[1])

        def change_numeric():
            '''
            bokeh plot application for numeric variables
            '''
            def make_title(label, minval, maxval):
                '''
                adds title to plot with minimum and maximum limits if specified
                '''
                title = 'Histogram'

                if label is not None:
                    title += ' of {}'.format(label)

                if minval != '':
                    title += '; Minimum={}'.format(minval)

                if maxval != '':
                    title += '; Maximum={}'.format(maxval)

                return title

            def update_data(low, high):
                '''
                recalculates histograms
                '''
                hist, edges = np.histogram(data[(data >= low) & (data <= high)],
                                           bins=bins.value)
                datasource.data = {'top': hist, 'left': edges[:-1],
                                   'right': edges[1:]}
                p.title.text = make_title(label, minval.value, maxval.value)

                if low > -1 * np.inf:
                    p.x_range.start = low

                if high < np.inf:
                    p.x_range.end = high

            def update_bins(attr, old, new):
                '''
                callback for changing number of bins
                '''
                if minval.value == '':
                    low = -1 * np.inf
                else:
                    low = float(minval.value)

                if maxval.value == '':
                    high = np.inf
                else:
                    high = float(maxval.value)

                update_data(low, high)

            def update_min(attr, old, new):
                '''
                callback for setting minimum value limit
                '''
                if new == '':
                    low = -1 * np.inf
                else:
                    low = float(new)

                if maxval.value == '':
                    high = np.inf
                else:
                    high = float(maxval.value)

                update_data(low, high)

            def update_max(attr, old, new):
                '''
                callback for setting maximum value limit
                '''
                if minval.value == '':
                    low = -1 * np.inf
                else:
                    low = float(minval.value)

                if new == '':
                    high = np.inf
                else:
                    high = float(new)

                update_data(low, high)

            # ============================
            # Plot Setup (Numeric)
            # ============================

            # fetch data
            label = select.value
            data = df[label]
            data = data[~data.isna()]
            datasource = ColumnDataSource({'top': [], 'left': [], 'right': []})

            # create plot
            p = figure(plot_height=600, plot_width=680,
                       min_border_bottom=200, min_border_left=80)
            p.quad(top='top', bottom=0, left='left', right='right', alpha=0.4,
                   source=datasource)

            # format plot
            p.xaxis.major_label_orientation = math.pi/2
            p.yaxis.axis_label = 'count'
            p.below[0].formatter.use_scientific = False

            # create interactive tools
            bins = Slider(start=10, end=100, value=default_bins, step=1,
                          title="Bins")
            minval = TextInput(value=default_min, title="Min Value:")
            maxval = TextInput(value=default_max, title="Max Value:")

            bins.on_change('value', update_bins)
            minval.on_change('value', update_min)
            maxval.on_change('value', update_max)

            update_bins(None, None, default_bins)

            # add to application
            root = column(row(column(bins, row(minval, maxval)),
                              Spacer(height=150)), p)
            doc.add_root(root)

            if len(doc.roots) == 3:
                # remove plots for previous column variable
                doc.remove_root(doc.roots[1])

        def update_column(attr, old, new):
            '''
            callback for changing data to column specified in dropdown
            '''
            if df[new].dtype in [int, float]:
                change_numeric()
            else:
                change_categorical()

        # crette interactive dropdown for column selection
        select = Select(title="Column:", value=default_col, options=cols)
        select.on_change('value', update_column)

        doc.add_root(widgetbox(select))
        doc.title = "Histoviewer"
        update_column(None, None, select.value)

    if serve == 'notebook':
        # serve application in jupyter notebook
        if not curstate().notebook:
            output_notebook(hide_banner=True)

        app = Application(FunctionHandler(modify_doc))
        show(app)

    elif serve == 'shell':
        # serve application from python script
        modify_doc(curdoc())
