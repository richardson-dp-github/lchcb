import plotly.plotly as py
import plotly
import plotly.graph_objs as go

trace1 = go.Bar(
    x=['500K', '800K', '1M'],
    y=[19582.0, 18908.0, 38754.0],
    name='1 Node'
)
trace2 = go.Bar(
    x=['500K', '800K', '1M'],
    y=[39118.0, 35712.0, 22802.0],
    name='3 Nodes'
)
trace3 = go.Bar(
    x=['500K', '800K', '1M'],
    y=[19937.0, 23547.0, 29217.0],
    name='6 Nodes'
)

data = [trace1, trace2, trace3]
layout = go.Layout(
    barmode='group',
    title="Execution Time of workload C",
    yaxis=dict(title='execution time for 10000 operations (milliseconds)'),
    xaxis=dict(title='size of database')
)

fig = go.Figure(data=data, layout=layout)
plotly.offline.plot(fig, filename='grouped-bar.html')
