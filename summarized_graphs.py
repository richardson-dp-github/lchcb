import csv
import plotly.plotly as py
import plotly
import plotly.graph_objs as go
import scipy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# df = pd.read_csv('all.csv')
# dfrp = pd.read_csv('all_rp.csv')
def exp5():
    # df1 = df.groupby(by=['wl', 'n']).mean()
    df1 = df[(df.wl == 'a') & (df.ld == False) & (df.n == 1) & (df.dbs == 1000)]
    df2 = df[(df.wl == 'c') & (df.ld == False) & (df.n == 1) & (df.dbs == 1000)]
    df3 = df[(df.wl == 'f') & (df.ld == False) & (df.n == 1) & (df.dbs == 1000)]

    df4 = df1.groupby(['ram']).mean()
    df5 = df2.groupby(['ram']).mean()
    df6 = df3.groupby(['ram']).mean()

    print 'Types'
    print type(df1), type(df2), type(df3), type(df4), type(df5), type(df6)
    print '-----'

    print df4
    print df5
    print df6


    print df1.index.tolist()
    print df4.index.tolist()

    # print df1
    # print '===mean===', df.groupby(['ram', 'dbs']).mean()

    trace1 = go.Bar(
        x=df4.index.tolist(),
        y=df4['RunTime(ms)'],
        # mode='markers',
        name='1 Node, Workload A'
    )
    trace2 = go.Bar(
        x=df5.index.tolist(),
        y=df5['RunTime(ms)'],
        # mode='markers',
        name='1 Node, Workload C'
    )
    trace3 = go.Bar(
        x=df5.index.tolist(),
        y=df5['RunTime(ms)'],
        # mode='markers',
        name='1 Node, Workload F'
    )


    data = [trace1, trace2, trace3]






    layout = go.Layout(
        title="Mean Execution Time, 5 Trials",
        yaxis=dict(title='execution time for 10000 operations (milliseconds)'),
        xaxis=dict(title='total available RAM on node')
    )

    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename='bar.html')

    # average execution time

def exp6():
    trace1 = go.Box(
        x=df['ram'],
        y=df['RunTime(ms)'],
        # mode='markers',
        name='-----'
    )
    data = [trace1]

    layout = go.Layout(
        title="Mean Execution Time",
        yaxis=dict(title='execution time for 10000 operations (milliseconds)'),
        xaxis=dict(title='total available RAM on node')
    )

    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename='boxplot-exp6.html')

# Initial Comparison with Abramova Paper
def analysis1():


    data = []

    for wl in ['a', 'c']:
        for n in [1, 3, 6]:
            dfa1 = df[(df.wl == wl) & (df.ld == False) & (df.n == n) & (df.dbs == 1000) & (df.ram == '2GB')]
            data.append(go.Scatter(
                x=dfa1['wl'] + "-" + dfa1['n'].map(str),
                y=dfa1['RunTime(s)'],
                mode='markers',
                name=wl + '-' + str(n)
            )
            )


    traceref = go.Scatter(
        x=['a-1', 'a-3', 'a-6', 'c-1', 'c-3', 'c-6',
           ],
        # transcribed from the Abramova paper
        y=[58.43, 65.65, 87.31,
           88, 90.21, 118.09,
           223.18, 330.82, 404.66],
        # mode='markers',
        name='Reference'
    )

    data.append(traceref)

    print data

    layout = go.Layout(
        title="Execution Time for 10,000 Operations",
        yaxis=dict(title='seconds'),
        xaxis=dict(title='Workload-Number of Nodes'),
        font=dict(family='Courier New, monospace', size=24, color='#7f7f7f')
    )

    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename='analysis-1_scatter.html')


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


def analysis2():

    data = []

    df_2gb = df[(df.ld == False) & (df.ram == '2GB')]
    df_1gb = df[(df.ld == False) & (df.ram == '1GB')]

    data.append(go.Scatter(
        x=df_2gb['ram'],
        y=df_2gb['RunTime(s)'],
        mode='markers',
        name='2GB'
    )
    )

    data.append(go.Scatter(
        x=df_1gb['ram'],
        y=df_1gb['RunTime(s)'],
        mode='markers',
        name='1GB'
    )
    )

    data = []

    data.append(go.Histogram(
        x=df_2gb['RunTime(s)'],
        opacity=0.75,
        name='2GB RAM'
    )
    )

    data.append(go.Histogram(
        x=df_1gb['RunTime(s)'],
        opacity=0.75,
        name='1GB RAM'
    )
    )

    layout = go.Layout(
        title="Execution Time for 10,000 Operations",
        barmode='overlay',
        yaxis=dict(title='frequency'),
        xaxis=dict(title='seconds'),
        font=dict(family='Courier New, monospace', size=24, color='#7f7f7f')
    )

    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename='analysis-2_scatter.html')

# This is the t-test evaluating workloads A and C
def analysis3():
    df_2gb = df[(df.wl.isin(['a','c'])) & (df.ld == False) & (df.n.isin([1, 3, 6])) & (df.dbs.isin([500, 800, 1000])) &
                (df.ram == '2GB')].sort_values(by=['wl', 'n', 'dbs', 't'])
    df_1gb = df[(df.wl.isin(['a','c'])) & (df.ld == False) & (df.n.isin([1, 3, 6])) & (df.dbs.isin([500, 800, 1000])) &
                (df.ram == '1GB')].sort_values(by=['wl', 'n', 'dbs', 't'])

    # print df_2gb.head()
    # print df_1gb.head()

    a = df_2gb['RunTime(s)']
    b = df_1gb['RunTime(s)']

    total = a.append(b)

    print a.describe()
    print b.describe()
    print total.describe()

    print scipy.stats.ttest_rel(a, b)

    return 0

# Writes
def analysis4():


    data = []

    df_2gb = df[(df.ld == True) & (df.ram == '2GB') & (df.dbs == 1000)]
    df_1gb = df[(df.ld == True) & (df.ram == '1GB') & (df.dbs == 1000)]

    data = []

    data.append(go.Box(
        x=df_2gb['RunTime(s)'],
        # opacity=0.65,
        name='2GB'
    )
    )

    data.append(go.Box(
        x=df_1gb['RunTime(s)'],
        # opacity=0.65,
        name='1GB'
    )
    )

    layout = go.Layout(
        title="Execution Time for 1 Million Writes",
        yaxis=dict(title='RAM on Node'),
        xaxis=dict(title='seconds'),
        font=dict(family='Courier New, monospace', size=24, color='#7f7f7f')
    )

    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename='analysis-4_histogram.html')

    return 0

def analysis5():
    df_2gb = df[(df.wl.isin(['a', 'c'])) & (df.ld == True) & (df.n.isin([1, 3, 6])) & (df.dbs.isin([1000])) &
                (df.ram == '2GB')].sort_values(by=['wl', 'n', 'dbs', 't'])
    df_1gb = df[(df.wl.isin(['a', 'c'])) & (df.ld == True) & (df.n.isin([1, 3, 6])) & (df.dbs.isin([1000])) &
                (df.ram == '1GB')].sort_values(by=['wl', 'n', 'dbs', 't'])

    a = df_2gb['RunTime(s)']
    b = df_1gb['RunTime(s)']

    print scipy.stats.ttest_rel(a, b, nan_policy='omit')
    print a.mean(), a.std()
    print b.mean(), b.std()

    print a.describe()
    print b.describe()

    total = a.append(b)

    print total.describe()

    return 0

# This will provide the three (3) graphs that John Pecarina is looking for.
# This was adapted from analysis 1

def analysis6():

    make_boxplot = False
    make_scatter = True

    data = []
    data1 = {}
    traceref = {}

    data_from_abramova_paper = {
        'a-1': 58.43,
        'a-3': 65.65,
        'a-6': 87.31,
        'c-1': 88,
        'c-3': 90.21,
        'c-6': 118.09,
        'e-1': 223.18,
        'e-3': 330.82,
        'e-6': 404.66
    }

    layout = go.Layout(
        title="Execution Time for 10,000 Operations",
        yaxis=dict(title='seconds'),
        xaxis=dict(title='Workload-Number of Nodes'),
        font=dict(family='Courier New, monospace', size=24, color='#7f7f7f')
    )



    # This will create the scatter graphs from the collected data
    for wl in ['a','c','e']:
        traceref[wl] = go.Scatter(
                                    x=[key for key in sorted(data_from_abramova_paper.keys()) if wl in key],
                                    y=[value for key, value in sorted(data_from_abramova_paper.items()) if wl in key],
                                    # mode='markers',
                                    name='Reference'
                                    )

        data1[wl] = []
        for n in [0]: # [1, 3, 6]: Loop is inconsequential
            for ram in ['1GB', '2GB']:
                dfa1 = df[(df.wl == wl) & (df.ld == False) & (df.n.isin([1, 3, 6])) & (df.dbs == 1000) & (df.ram == ram)]
                if make_scatter:
                    data1[wl].append(

                     go.Scatter(
                        x=dfa1['wl'] + "-" + dfa1['n'].map(str),
                        y=dfa1['RunTime(s)'],
                        mode='markers',
                         #marker = dict(
                           # size = 10,
                           # color = 'rgba(152, 0, 0, .8)',
                           # line = dict(
                           #     width = 2,
                           #     color = 'rgb(0, 0, 0)'
                           # )),
                        name=wl + '-' + str(ram)
                                )
                    )
                if make_boxplot:
                    data1[wl].append(

                     go.Box(
                        x=dfa1['wl'] + "-" + dfa1['n'].map(str),
                        y=dfa1['RunTime(s)'],
                        # mode='markers',
                        name=wl + '-' + str(n) + '-' + str(ram)
                                )
                    )

        data = data1[wl]
        data.append(traceref[wl])

        fig = go.Figure(data=data, layout=layout)

        plotly.offline.plot(fig, filename='analysis-6-'+str(wl)+'withoutRP.html')


        # From the Raspberry Pi
        data2 = {}
        data2[wl] = []
        for n in [0]: # loop is inconsequential
            ram = '1GB_rp'
            dfa1 = dfrp[(dfrp.wl == wl) & (dfrp.ld == False) & (df.n.isin([1, 3, 6])) & (dfrp.dbs == 1000) & (dfrp.ram == ram)]
            if make_scatter:
                data2[wl].append(

                 go.Scatter(
                    x=dfa1['wl'] + "-" + dfa1['n'].map(str),
                    y=dfa1['RunTime(s)'],
                    mode='markers',
                    marker= dict(
                            size = 30,
                            # color = 'rgba(152, 0, 0, .8)',
                            line=dict(
                                width=2,
                                # color = 'rgb(0, 0, 0)'
                            )),
                    name=wl + '-' + str(ram)
                            )
                )
            if make_boxplot:
                data2[wl].append(

                 go.Box(
                    x=dfa1['wl'] + "-" + dfa1['n'].map(str),
                    y=dfa1['RunTime(s)'],
                    # mode='markers',
                    name=wl + '-' + str(n) + '-' + str(ram)
                            )
                )

        data.extend(data2[wl])

        fig = go.Figure(data=data, layout=layout)

        plotly.offline.plot(fig, filename='analysis-6-'+str(wl)+'withRP.html')


    # print data

def analysis7(csv_file_name='combined_results.csv',
              verbose=True):

    plot_multiple_series(include_reference=True, apply_filter={'wl': 'a'})
    plot_multiple_series(include_reference=True, apply_filter={'wl': 'c'})
    plot_multiple_series(include_reference=True, apply_filter={'wl': 'e'})


    return 0


def plot_multiple_series(csv_file_name='combined_results.csv',
                         y_column='[OVERALL] RunTime(ms)',
                         series=['ram', 'nm', 'nt', 'rf', 'wl'],
                         apply_filter=None,
                         x_column='nn',
                         include_reference=False,
                         ref_csv_filename='abramova_results.csv',
                         output_filename='multiple-series-plot.html',
                         title="Execution Time for 10,000 Operations",
                         verbose=True):

    # =============================

    df = pd.read_csv(csv_file_name)

    if verbose:
        print "Data frame has been imported...header shown below..."
        print df

    levels_of_interest = series + [x_column]

    # Import and Plot the Reference Data ====
    if include_reference:

        df_ref = pd.read_csv(ref_csv_filename)
        df = df.append(df_ref, ignore_index=True)


    # ==============================

    df.set_index(keys=levels_of_interest, inplace=True)  # combine extraneous characteristics, like trials

    s = df.median(level=levels_of_interest)[y_column]  # This will replace the median



    # ===>Do I need to do both

    df_median = s.to_frame()  # convert back to data frame type; it'll be easier to deconstruct and plot with plotly

    # df_median_unstacked = df_median.reset_index()  # reset the index so that the x values are attainable

    if apply_filter:
        for key, val in apply_filter.items():
            df_median = df_median.xs(val, level=key, drop_level=False)

    data = []

    for i, j in df_median.groupby(level=series):

        df_median_unstacked = j.reset_index()

        x = df_median_unstacked[x_column]
        y = df_median_unstacked[y_column]  # pre-select the x and y values here; renders easier debugging process

        if verbose:
            print i
            print j


        layout = go.Layout(
            title=title,
            yaxis=dict(title=y_column),
            xaxis=dict(title=x_column),
            font=dict(family='Courier New, monospace', size=24, color='#7f7f7f')
        )

        g = go.Scatter(
                        x=x,
                        y=y,
                        # mode='markers',
                        marker= dict(
                                size=15,
                                # color = 'rgba(152, 0, 0, .8)',
                                line=dict(
                                    width=2,
                                    # color = 'rgb(0, 0, 0)'
                                )),
                        name=str(i)
                                )

        if g:
            data.append(g)



    fig = go.Figure(data=data, layout=layout)

    plotly.offline.plot(fig, filename=output_filename)
    return 0


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

def test_calculate_summary():
    return 0


# Speedup
def analysis8():

    # set parameters
    levels_of_interest = ['ram', 'nm', 'nt', 'rf', 'wl', 'nn']
    csv_with_main_results = 'combined_results.csv'
    value_of_interest = '[OVERALL] RunTime(ms)'
    ref_csv_filename='abramova_results.csv'
    calculated_value='RelativeRunTime'


    # Process the data file to get the median values as defined by the multi-level index
    df = pd.read_csv(csv_with_main_results)
    df_ref = pd.read_csv(ref_csv_filename)
    df = df.append(df_ref, ignore_index=True)
    df.set_index(keys=levels_of_interest, inplace=True)
    s = df.median(level=levels_of_interest)[value_of_interest]  # This will replace the median
    df_median = s.to_frame()  # convert back to data frame type; it'll be easier to deconstruct and plot with plotly

    # print df_median

    # df_median[calculated_value] = df_median[['wl','nn']]

    # levels_for_lookup = ['ram', 'nm', 'nt', 'rf', 'wl', 'nn']

    # df1 = df_median.unstack(level=['ram','nt','nm','rf'])

    # df_median[calculated_value] = df_median.loc[df_median["'"+ram+"'"]]

    df_median['newcol'] = 0

    print 'Printing itertuples...'
    for i in df_median.itertuples():
        print i
        df_median['newcol'] = df_median.loc[i.Index[0], 'unk', 'ref', 'unk', i.Index[4], i.Index[5]][value_of_interest]
        print ''

    print 'Printing iterrows()'
    for j in df_median.iterrows():
        print j
        print ''

    # print df_median


    return 0

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
                   filename='genericfilename.html'):

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



    fig = go.Figure(data=data, layout=layout)

    plotly.offline.plot(fig, filename=filename)

    return 0

def analysis9():
    csv_with_main_results = 'combined_results.csv'
    df = pd.read_csv(csv_with_main_results)

    df_of_interest = df[
                         (df['ram'] == '2GB') &
                         (df['nm'] == 'nodal') &
                         (df['nt'] == 'vm') &
                         (df['rf'] == 1) &
                         (df['lt'] == 1) &
                         (df['nn'] == 1) &
                         (df['wl'] == 'a') &
                         (df['dbs'] == 1000)
                     ]

    print df_of_interest.head(31)

    create_histogram(df_of_interest,
                     column_of_interest='[OVERALL] RunTime(ms)')



    # 4GB,nodal,vm,1,1,3,4,c,1000,

    return 0

# From http://stackoverflow.com/questions/4843173/how-to-check-if-type-of-a-variable-is-string
def isstring(s):
    # if we use Python 3
    #if (sys.version_info[0] >= 3):
    #    return isinstance(s, str)
    # we use Python 2
    return isinstance(s, basestring)

def isval(v):
    return str(type(v))=="<type 'int'>" or str(type(v))=="<type 'float'>"

def islist(l):
    return str(type(l)) == "<type 'list'>"

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
                            mode='markers'):

    # Import the csv if no dataframe specified
    if read_from_csv:
        df = pd.read_csv(csv_with_main_results)

    if d:
        df = return_filtered_dataframe(df, d)

    print df.head(10)

    create_scatter(df,
                   x_column=x_column,
                   y_column=y_column,
                   s_column=s_column,
                   title=title,
                   mode=mode)


def analysis10():
    csv_with_main_results = 'combined_results.csv'
    df = pd.read_csv(csv_with_main_results)

    for i in []:

        df_of_interest = df[
                         (df['ram'] == '4GB') &
                         (df['nm'] == 'nodal') &
                         (df['nt'] == 'vm') &
                         (df['rf'] == 1) &
                         (df['lt'] == 1) &
                         (df['nn'] == 1) &
                         (df['wl'] == 'a') &
                         (df['dbs'] == 1000)
                     ]

    print df_of_interest.head(31)

    create_scatter(df_of_interest,
                   x_column='t',
                   y_column='[OVERALL] RunTime(ms)',
                   title='Execution Time for 10k operations',
                   mode='markers')




    # 4GB,nodal,vm,1,1,3,4,c,1000,

    return 0

def analysis11():
    for i in ['a', 'c', 'e']:
        for j in [1, 3, 6]:
            generate_filtered_graph(csv_with_main_results='experiment_11_magnify_cash_effect',
                                    d={'nm': 'nodal',
                                       'nt': 'vm',
                                       'rf': 1,
                                       'lt': 1,
                                       'nn': j,
                                       'wl': i,
                                       'dbs': 1000},
                                    x_column='t',
                                    y_column='[OVERALL] RunTime(ms)',
                                    s_column='ram',
                                    title='Execution Time for 10k operations: '+str(i)+str(j),
                                    mode='markers')

# This is the reference data from the paper only, Workload A only
def research_question_1_figure_1():
    generate_filtered_graph(csv_with_main_results='abramova_results.csv',
                                    d={
                                       'wl': 'a',
                                       },
                                    x_column='nn',
                                    y_column='[OVERALL] RunTime(ms)',
                                    s_column=None,
                                    title='Execution Time for 10k operations, Workload A, Abramova Paper',
                                    mode='markers')

# ram,nm,nt,rf,lt,nn,t,wl,dbs are possible columns
def research_question_1_figure_2_3_utility_fn(csv_file, title):
    for i in ['a']:
        for j in [1]:
            generate_filtered_graph(csv_with_main_results=csv_file,
                                    d={'nm': 'nodal',
                                       'nt': 'vm',
                                       'nn': j,
                                       'wl': i},
                                    x_column='t',
                                    y_column='[OVERALL] RunTime(ms)',
                                    s_column='ram',
                                    title=title,
                                    mode='line')


def research_question_1_figure_2():
    research_question_1_figure_2_3_utility_fn(csv_file='experiment_11_magnify_cash_effect',
                                              title='Execution Time for 1k operations: {} Nodes, Workload {}'.format(1, 'A'))

def research_question_1_figure_3():
    research_question_1_figure_2_3_utility_fn(csv_file='combined_results.csv',
                                              title='Execution Time for 10k operations: {} Nodes, Workload {}'.format(1, 'A'))
    return 0


def research_question_1_figure_4_5():
    df = calculate_summary(input_csv_file_name='combined_results.csv',
                           read_from_csv=True,
                           dataframe=None,
                           measurement_of_interest='[OVERALL] RunTime(ms)',
                           series_to_group_by=['ram', 'nm', 'nt', 'rf', 'wl', 'nn'],
                           return_series_not_data_frame=False,
                           reset_index_before_returning_data_frame=True,
                           summary_statistic_of_interest='median'
                           )

    df_ref = pd.read_csv('abramova_results.csv')
    df_ref = return_filtered_dataframe(df_ref, {'wl': 'a'})

    df = df.append(df_ref, ignore_index=True)

    df['nt-ram'] = df['nt'].map(str) + '-' + df['ram'].map(str)  # for the series name

    for i in ['a']:
        generate_filtered_graph(df=df,
                                csv_with_main_results='combined_results.csv',
                                read_from_csv=False,
                                d={'wl': i,'nt': ['vm','ref']},
                                x_column='nn',
                                y_column='[OVERALL] RunTime(ms)',
                                s_column='nt-ram',
                                title='Median Execution Time for 10k operations: Workload {}'.format(i),
                                mode='marker')

    return 0

def research_question_1_figure_6():
    df = calculate_summary(input_csv_file_name='combined_results.csv',
                           read_from_csv=True,
                           dataframe=None,
                           measurement_of_interest='[OVERALL] RunTime(ms)',
                           series_to_group_by=['ram', 'nm', 'nt', 'rf', 'wl', 'nn'],
                           return_series_not_data_frame=False,
                           reset_index_before_returning_data_frame=True,
                           summary_statistic_of_interest='median'
                           )

    df_ref = pd.read_csv('abramova_results.csv')
    df_ref = return_filtered_dataframe(df_ref, {'wl': 'a'})

    df = df.append(df_ref, ignore_index=True)

    df['nt-ram'] = df['nt'].map(str) + '-' + df['ram'].map(str)  # for the series name

    for i in ['a']:
        generate_filtered_graph(df=df,
                                csv_with_main_results='combined_results.csv',
                                read_from_csv=False,
                                d={'wl': i},
                                x_column='nn',
                                y_column='[OVERALL] RunTime(ms)',
                                s_column='nt-ram',
                                title='Median Execution Time for 10k operations: Workload {}'.format(i),
                                mode='marker')

    return 0