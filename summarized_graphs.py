import csv
import plotly.plotly as py
import plotly
import plotly.graph_objs as go
import scipy
import pandas as pd
import numpy as np

df = pd.read_csv('all.csv')
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
    for wl in ['a', 'c', 'e']:
        traceref[wl] = go.Scatter(
                                    x=[key for key in sorted(data_from_abramova_paper.keys()) if wl in key],
                                    y=[value for key, value in sorted(data_from_abramova_paper.items()) if wl in key],
                                    # mode='markers',
                                    name='Reference'
                                    )

        data1[wl] = []
        for n in [1, 3, 6]:
            dfa1 = df[(df.wl == wl) & (df.ld == False) & (df.n == n) & (df.dbs == 1000) & (df.ram == '2GB')]
            data1[wl].append(

             go.Scatter(
                x=dfa1['wl'] + "-" + dfa1['n'].map(str),
                y=dfa1['RunTime(s)'],
                mode='markers',
                name=wl + '-' + str(n)
                        )
            )

        data = data1[wl]
        data.append(traceref[wl])

        fig = go.Figure(data=data, layout=layout)

        plotly.offline.plot(fig, filename='analysis-6_scatter-' + wl + '.html')

    # print data

analysis6()