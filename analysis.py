import plotly
from plotly.graph_objs import Scatter, Layout, Box

import data

def link_type(s):
    for i in ['wired', 'wireless']:
        if i in s:
            return i
    return 'none'

def op_type(s):
    for i in ['insert_1', 'simple1_1', 'insert_5_simple1_5']:
        if i in s:
            if i == 'insert_1':
                return 'writes_only'
            elif i == 'simple1_1':
                return 'reads_only'
            elif i == 'insert_5_simple1_5':
                return 'mixed_reads_and_writes'
            return i
    return 'none'

def compression_type(s):
    for i in ['DeflateCompressor', 'LZ4Compressor', 'SnappyCompressor']:
        if i in s:
            return i
    return 'none'

# Codes
type_ = 0
total_ops = 1
ops_p_s = 2
pk_p_s = 3
row_p_s = 4
latency_mean = 5
latency_median = 6
latency_95 = 7
latency_99 = 8
latency_999 = 9
latency_max = 10
std_err = 12
time_ = 11
errors = 13
gc = 14
gc_max_ms = 15
gc_sum_ms = 16
gc_sdv_ms = 17
gc_mb = 18


# configure the graph
interval = 0
x_code = time_
y_code = ops_p_s
series = 'revision'
run = 0

xx = data.stats
xx2 = data.stats['stats']

# xxx = data.stats['stats'][run]['intervals'][interval][x_code]

xxx = {}
yyy = {}
'''
for r in data.stats['stats']:
    if 'intervals' in r.keys():
        k = r[series]
        xxx[k] = []
        yyy[k] = []
        for interval in r['intervals']:
            t = interval[x_code]
            xxx[k].append(t)
            yyy[k].append(interval[y_code])
'''

kk = 'runs'
xxx[kk] = []
yyy[kk] = []
boxplot0={}

for r in data.stats['stats']:
    if 'intervals' in r.keys():
        k = r[series]
        # kk = op_type(r[series])+compression_type(r[series])
        kk = link_type(r[series])
        if 'mixed' not in op_type(k):
            for interval in r['intervals']:
                t = interval[x_code]
                try:
                    xxx[kk].append(compression_type(k)+'_'+op_type(k))
                    yyy[kk].append(interval[y_code])
                except:
                    xxx[kk] = []
                    yyy[kk] = []
                    xxx[kk].append(compression_type(k)+'_'+op_type(k))
                    yyy[kk].append(interval[y_code])
                try:
                    boxplot0[k].append(interval[y_code])
                except:
                    boxplot0[k] = []
                    boxplot0[k].append(interval[y_code])


print 'xxx', xxx
print 'yyy', yyy

trace0 = []
'''
for key, value in xxx.iteritems():
    trace0.append(Scatter(
        x = xxx[key],
        y = yyy[key],
        mode = 'markers',
        name = key
    )
    )
'''

print 'boxplot0', sorted(boxplot0)

'''
for key, value in sorted(boxplot0.iteritems()):
    if True:
        trace0.append(Box(
            #x = xxx[key],
            y = value,
            #mode = 'markers',
            name = key,
            boxmean = True,
            boxpoints = 'all'
        )
        )
'''

'''
for key, value in boxplot0.iteritems():
    if 'insert_1' in key and 'DeflateCompressor' in key:
        trace0.append(Box(
            x=op_type(key),
            y=value,
            #mode = 'markers',
            name=op_type(key) + '-' + compression_type(key) + '-' + link_type(key),
            boxmean='sd',
            boxpoints='all'
        )
        )
'''

# Grouped Plot
for key, value in xxx.iteritems():
    if True:
        trace0.append(Box(
            x=value,
            y=yyy[key],
            #mode = 'markers',
            name=key,
            boxmean='sd',
            boxpoints='all'
        )
        )


plotly.offline.plot({
    "data": sorted(trace0),
    "layout": Layout(title="Operations Per Second Sensitivity, Wired v. Wireless", yaxis=dict(title='operations per second'), boxmode='group')
})

# or plot with: plot_url = py.plot(data, filename='basic-line')




# d = data.stats





# print d