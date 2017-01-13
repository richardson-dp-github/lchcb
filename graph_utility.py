# ----------------------------------------------------------------------------------------------
# GRAPH UTILITY FUNCTIONS
# ----------------------------------------------------------------------------------------------
# These should make it easier and more intuitive for graphing


import plotly
import plotly.graph_objs as go
import pandas as pd
import credentials


# Given a figure, produce the graph
# There are several options here:
#   The file can be saved locally as an image file (.png)
#    -saving the image locally requires calling the online
#   The file can be saved locally as an html file (.html)
#    -the option of storing an image is not explored in this particular option
#    -it results in an obnoxious browser prompt asking one to save
def produce_graph(fig,
                  html_filename='scatterplot.html',
                  image_filename='plot-image.png',
                  save_image_locally_as_png_=False,
                  save_image_as_html=True,
                  save_image_as_svg=False,
                  save_image_as_pdf=False):

    if save_image_locally_as_png_:
        save_image_locally_as_png(fig,
                                  save_online=True,
                                  filename=image_filename)


    if save_image_as_html:
        plotly.offline.plot(fig, filename=html_filename)

    if save_image_as_svg:
        plotly.offline.plot(fig, filename=html_filename, image_filename=image_filename, image='svg')
    elif save_image_as_pdf:
        plotly.offline.plot(fig, filename=html_filename, image_filename=image_filename, image='pdf')


# This is a utility function designed specifically for ordering the traces in ascending order of name
def trace_name(t):
    return t.name

# This function creates a scatter plot of interest
def create_scatter(df,
                   x_column='',
                   y_column='',
                   s_column=None,
                   marker_size=15,
                   title='Generic Title',
                   mode='markers',
                   series_name='series_name',
                   filename='genericfilename.html',
                   image_filename='plot-image',
                   save_image_locally_as_png_=False,
                   save_image_locally_as_svg_=False,
                   show_zero_line_on_y_axis=False):

    # sort because otherwise the connecting lines are all scattered
    if not s_column:
        df.sort_values(by=[x_column], inplace=True)
    else:
        df.sort_values(by=[s_column, x_column], inplace=True)

    if s_column:
        data = []
        for s in list(set(df[s_column])):

            # df_of_interest = df[(df[s_column] == s)]
            df_of_interest = return_filtered_dataframe(df, {s_column: s})

            x = df_of_interest[x_column]
            y = df_of_interest[y_column]

            data.append(go.Scatter(
                            x=x,
                            y=y,
                            mode=mode,
                            marker=dict(
                                    size=marker_size,
                                    # color = 'rgba(152, 0, 0, .8)',
                                    line=dict(
                                        width=2,
                                        # color = 'rgb(0, 0, 0)'
                                    )),
                            name=s
                                    )
            )
        data.sort(key=trace_name)


    else:
        x = df[x_column]
        y = df[y_column]

        g = go.Scatter(
                            x=x,
                            y=y,
                            mode=mode,
                            marker= dict(
                                    size=marker_size,
                                    # color = 'rgba(152, 0, 0, .8)',
                                    line=dict(
                                        width=2,
                                        # color = 'rgb(0, 0, 0)'
                                    )),
                            name=series_name
                                    )
        data = [g]


    layout = go.Layout(
            title=title,
            yaxis=dict(title=y_column),
            xaxis=dict(title=x_column),
            font=dict(family='Courier New, monospace', size=24, color='#7f7f7f')
        )

    if show_zero_line_on_y_axis: # Override
        layout = go.Layout(
            title=title,
            yaxis=dict(title=y_column, rangemode='tozero'),
            xaxis=dict(title=x_column),
            font=dict(family='Courier New, monospace', size=24, color='#7f7f7f')
        )

    fig = go.Figure(data=data, layout=layout)

    produce_graph(fig,
                  save_image_locally_as_png_=save_image_locally_as_png_,
                  save_image_as_svg=save_image_locally_as_svg_,
                  html_filename=filename,
                  image_filename=image_filename)

    return 0


# This function creates a scatter plot of interest
def create_boxplot(df,
                   x_column='',
                   y_column='',
                   s_column=None,
                   marker_size=15,
                   title='Generic Title',
                   mode='markers',
                   series_name='series_name',
                   filename='genericfilename.html',
                   image_filename='plot-image',
                   save_image_locally_as_png_=False,
                   show_zero_line_on_y_axis=False):

    # sort because otherwise the connecting lines are all scattered
    if not s_column:
        df.sort_values(by=[x_column], inplace=True)
    else:
        df.sort_values(by=[s_column, x_column], inplace=True)

    if s_column:
        data=[]
        for s in list(set(df[s_column])):

            # df_of_interest = df[(df[s_column] == s)]
            df_of_interest = return_filtered_dataframe(df, {s_column: s})

            x = df_of_interest[x_column]
            y = df_of_interest[y_column]

            data.append(go.Box(
                            x=x,
                            y=y,
                            #mode=mode,
                            name=s
                                    )
            )
        data.sort(key=trace_name)

        layout = go.Layout(
            title=title,
            yaxis=dict(title=y_column),
            xaxis=dict(title=x_column),
            font=dict(family='Courier New, monospace', size=24, color='#7f7f7f'),
            boxmode='group'
        )

        if show_zero_line_on_y_axis:  # Override
            layout = go.Layout(
                title=title,
                yaxis=dict(title=y_column, rangemode='tozero'),
                xaxis=dict(title=x_column),
                font=dict(family='Courier New, monospace', size=24, color='#7f7f7f')
            )


    else:
        x = df[x_column]
        y = df[y_column]

        g = go.Box(
                            x=x,
                            y=y,
                            #mode=mode,
                            name=series_name
                                    )
        data = [g]


        layout = go.Layout(
                title=title,
                yaxis=dict(title=y_column),
                xaxis=dict(title=x_column),
                font=dict(family='Courier New, monospace', size=24, color='#7f7f7f'))

        if show_zero_line_on_y_axis:  # Override
            layout = go.Layout(
                title=title,
                yaxis=dict(title=y_column, rangemode='tozero'),
                xaxis=dict(title=x_column),
                font=dict(family='Courier New, monospace', size=24, color='#7f7f7f')
            )


    fig = go.Figure(data=data, layout=layout)

    produce_graph(fig, save_image_locally_as_png_=save_image_locally_as_png_,
                  html_filename=filename,
                  image_filename=image_filename)

    return 0

# This function creates a scatter plot of interest
def create_barchart(df,
                    x_column='',
                    y_column='',
                    s_column=None,
                    marker_size=15,
                    title='Generic Title',
                    mode='markers',
                    series_name='series_name',
                    filename='genericfilename.html',
                    image_filename='plot-image',
                    save_image_locally_as_png_=False):

    # sort because otherwise the connecting lines are all scattered
    if not s_column:
        df.sort_values(by=[x_column], inplace=True)
    else:
        df.sort_values(by=[s_column, x_column], inplace=True)

    if s_column:
        data=[]
        for s in list(set(df[s_column])):

            # df_of_interest = df[(df[s_column] == s)]
            df_of_interest = return_filtered_dataframe(df, {s_column: s})

            x = df_of_interest[x_column]
            y = df_of_interest[y_column]

            data.append(go.Bar(
                            x=x,
                            y=y,
                            #mode=mode,
                            name=s
                                    )
            )
        data.sort(key=trace_name)


    else:
        x = df[x_column]
        y = df[y_column]

        g = go.Bar(
                            x=x,
                            y=y,
                            #mode=mode,
                            name=series_name
                                    )
        data = [g]


    layout = go.Layout(
            title=title,
            yaxis=dict(title=y_column),
            xaxis=dict(title=x_column),
            font=dict(family='Courier New, monospace', size=24, color='#7f7f7f')
        )

    fig = go.Figure(data=data, layout=layout)

    produce_graph(fig, save_image_locally_as_png_=save_image_locally_as_png_,
                  html_filename=filename,
                  image_filename=image_filename)

    return 0

# From http://stackoverflow.com/questions/4843173/how-to-check-if-type-of-a-variable-is-string
def isstring(s):
    # if we use Python 3
    #if (sys.version_info[0] >= 3):
    #    return isinstance(s, str)
    # we use Python 2
    return isinstance(s, basestring)


# Checks to see if the variable is a numeric value
def isval(v):
    return str(type(v))=="<type 'int'>" or str(type(v))=="<type 'float'>"

# Checks to see if the variable is a list
def islist(l):
    return str(type(l)) == "<type 'list'>"

# Filters the data frame
def return_filtered_dataframe(df, d):
    for key, val in d.iteritems():
        if isstring(val) or isval(val):
            df = df[(df[key] == val)]
        elif islist(val):
            df = df[df[key].isin(val)]

    return df

def generate_filtered_graph(df=None,
                            read_from_csv=True,
                            csv_with_main_results='combined_results.csv',
                            d=None,
                            x_column='t',
                            y_column='[OVERALL] RunTime(ms)',
                            s_column='ram',
                            title='Execution Time for 10k operations',
                            mode='markers',
                            filename='figures/rq1_fig6.html',
                            image_filename='figures/untitled',
                            image_type='png',
                            type='scatter',
                            show_zero_line_on_y_axis=False):

    # Import the csv if no dataframe specified
    if read_from_csv:
        df = pd.read_csv(csv_with_main_results)

    if d:
        df = return_filtered_dataframe(df, d)

    print df.head(10)
    if type == 'scatter':
        create_scatter(df,
                   x_column=x_column,
                   y_column=y_column,
                   s_column=s_column,
                   title=title,
                   mode=mode,
                   filename=filename,
                   image_filename=image_filename,
                   save_image_locally_as_png_=isstring(image_filename),
                   show_zero_line_on_y_axis=show_zero_line_on_y_axis)
    elif type == 'boxplot':
        create_boxplot(df,
                   x_column=x_column,
                   y_column=y_column,
                   s_column=s_column,
                   marker_size=15,
                   title=title,
                   mode=mode,
                   series_name='series_name',
                   filename=filename,
                   image_filename=image_filename,
                   save_image_locally_as_png_=isstring(image_filename),
                   show_zero_line_on_y_axis=show_zero_line_on_y_axis)
    elif type == 'bar':
        create_barchart(df,
                   x_column=x_column,
                   y_column=y_column,
                   s_column=s_column,
                   marker_size=15,
                   title=title,
                   mode=mode,
                   series_name='series_name',
                   filename=filename,
                   image_filename=image_filename,
                   save_image_locally_as_png_=isstring(image_filename))
    else:
        print "Invalid Chart Type, choose scatter, boxplot, or bar"


# Takes dataframe df and plots a histogram
def create_histogram(df,
                     title="Execution Time for 10,000 Operations",
                     y_axis_label='frequency',
                     x_axis_label='seconds',
                     opacity=0.75,
                     column_of_interest='RunTime(s)',
                     data_series_name='2GB RAM',
                     barmode='overlay',
                     font_name='Courier New, monospace',
                     font_size=24,
                     font_color='#7f7f7f'
                     ):

    data = []

    data.append(go.Histogram(
        x=df[column_of_interest],
        opacity=opacity,
        name=data_series_name
    ))

    layout = go.Layout(
        title=title,
        barmode=barmode,
        yaxis=dict(title=y_axis_label),
        xaxis=dict(title=x_axis_label),
        font=dict(family=font_name, size=font_size, color=font_color)
    )

    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename='analysis-2_scatter.html')

# Return a data frame that will show the medians, like one had just done a summary groupby query
def calculate_summary(input_csv_file_name='combined_results.csv',
                      read_from_csv=True,
                      dataframe=None,
                      measurement_of_interest='[OVERALL] RunTime(ms)',
                      series_to_group_by=['ram', 'nm', 'nt', 'rf', 'wl'],
                      return_series_not_data_frame=False,
                      reset_index_before_returning_data_frame=True,
                      summary_statistic_of_interest='median'
                      ):

    # ==PROCESS INPUT====================

    # The user can either read in from a
    if read_from_csv:
        df = pd.read_csv(input_csv_file_name)
    elif dataframe:
        df = dataframe
    else:
        df = None

    # Set the index.  It's assumed the df has no index
    df.set_index(keys=series_to_group_by, inplace=True)  # combine extraneous characteristics, like trials or subtrials

    # ==CALCULATE==========================

    if summary_statistic_of_interest == 'median':
        s = df.median(level=series_to_group_by)[measurement_of_interest]  # This will replace the median
    elif summary_statistic_of_interest == 'variance':
        s = df.var(level=series_to_group_by)[measurement_of_interest]  # This will put the variance in
    elif summary_statistic_of_interest == 'stdev':
        s = df.std(level=series_to_group_by)[measurement_of_interest]
    else:
        s = df.median(level=series_to_group_by)[measurement_of_interest]  # Let median be the default calculation

    # ==PROCESS OUTPUT=====================

    # User decides whether to return a series or data frame, whether or not data frame is indexed
    if return_series_not_data_frame:
        return s
    else: # return data frame
        d = s.to_frame()       # convert to a frame
        if reset_index_before_returning_data_frame:
            d = d.reset_index()
        return d


# Saves the image locally
def save_image_locally_as_png(fig,
                              save_online=False,
                              filename='a-simple-plot.png'):

    # This saves file online, assuming a plotly account
    if '.png' in filename:
        if save_online:
            plotly_username = credentials.plotly_credentials['username']
            plotly_api_code = credentials.plotly_credentials['api_key']

            plotly.plotly.sign_in(plotly_username, plotly_api_code)

            plotly.plotly.image.save_as(fig, filename=filename)
    else:
        print 'invalid filename'
