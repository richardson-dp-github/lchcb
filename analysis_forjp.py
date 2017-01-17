import plotly
from plotly.graph_objs import Scatter, Layout, Box
import numpy
import scipy.stats as stats

import data

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

def replication_factor(s):
    for i in ['replication_1', 'replication_2', 'replication_3']:
        if i in s:
            return i
    return 'none'

def link_type(s):
    for i in ['wired', 'wireless']:
        if i in s:
            return i
    return 'none'

def op_type(s):
    for i in ['insert1', 'simple', 'insert_5_simple1_5']:
        if i in s:
            if i == 'insert1':
                return 'writes_only'
            elif i == 'simple':
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

def compaction_type(s):
    for i in ['stcs-minsstable-0128', 'stcs-minsstable-0016', 'stcs-minsstable-0001', 'stcs-minsstable-0002',
              'stcs-minsstable-0004',
              'stcs-minsstable-0008',
              'stcs-minsstable-0032',
              'stcs-minsstable-0064',
              'lcs-minsstable-0001',
                'lcs-minsstable-0001',
                'lcs-minsstable-0002',
                'lcs-minsstable-0004',
                'lcs-minsstable-0008',
                'lcs-minsstable-0016',
                'lcs-minsstable-0032',
                'lcs-minsstable-0064',
                'lcs-minsstable-0128',
                'base-03600max-window-86400',
                'base-03600max-window-10000',
                'base-03600max-window-00100',
                'base-03600max-window-00010',
                'base-01800max-window-86400',
                'base-01800max-window-10000',
                'base-01800max-window-00100',
                'base-01800max-window-00010',
                'base-00900max-window-86400',
                'base-00900max-window-10000',
                'base-00900max-window-00100',
                'base-00900max-window-00010',
                'base-00450max-window-86400',
                'base-00450max-window-10000',
                'base-00450max-window-00100',
                'base-00450max-window-00010',
                'base-00225max-window-86400',
                'base-00225max-window-10000',
                'base-00225max-window-00100',
                'base-00225max-window-00010',
                'base-00100max-window-86400',
                'base-00100max-window-10000',
                'base-00100max-window-00100',
                'base-00100max-window-00010',
                'base-00050max-window-86400',
                'base-00050max-window-10000',
                'base-00050max-window-00100',
                'base-00050max-window-00010',
                'base-00020max-window-86400',
                'base-00020max-window-10000',
                'base-00020max-window-00100',
                'base-00020max-window-00010',
                'base-00005max-window-86400',
                'base-00005max-window-10000',
                'base-00005max-window-00100',
                'base-00005max-window-00010',
                      'dtcs', 'lcs', 'stcs']:
        if i in s:
            return i
    return 'none'

def graph_writes_only_graph_compression():
    kk = 'runs'
    xxx = {}
    yyy = {}
    xxx[kk] = []
    yyy[kk] = []
    boxplot0={}

    # Gather Data
    for r in data.stats['stats']:
        if 'intervals' in r.keys():
            k = r[series]
            # kk = op_type(r[series])+compression_type(r[series])
            kk = compression_type(r[series])+'_'+op_type(r[series])
            g = link_type(k)
            if 'writes_only' in op_type(k):
                for interval in r['intervals']:
                    try:
                        xxx[kk].append(g)
                        yyy[kk].append(interval[y_code])
                    except:
                        xxx[kk] = []
                        yyy[kk] = []
                        xxx[kk].append(g)
                        yyy[kk].append(interval[y_code])
                    try:
                        boxplot0[k].append(interval[y_code])
                    except:
                        boxplot0[k] = []
                        boxplot0[k].append(interval[y_code])
    trace0 = []
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
                            "layout": Layout(title="Compression Methods", yaxis=dict(title='operations per second'), boxmode='group')})

    return 0

def graph_reads_only_graph_compression():
    kk = 'runs'
    xxx = {}
    yyy = {}

    xxx[kk] = []
    yyy[kk] = []
    boxplot0={}

    # Gather Data
    for r in data.stats['stats']:
        if 'intervals' in r.keys():
            k = r[series]
            # kk = op_type(r[series])+compression_type(r[series])
            kk = compression_type(r[series])+'_'+op_type(r[series])
            g = link_type(k)
            if 'reads_only' in op_type(k):
                for interval in r['intervals']:
                    try:
                        xxx[kk].append(g)
                        yyy[kk].append(interval[y_code])
                    except:
                        xxx[kk] = []
                        yyy[kk] = []
                        xxx[kk].append(g)
                        yyy[kk].append(interval[y_code])
                    try:
                        boxplot0[k].append(interval[y_code])
                    except:
                        boxplot0[k] = []
                        boxplot0[k].append(interval[y_code])
    trace0 = []
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
                            "layout": Layout(title="Compression Methods", yaxis=dict(title='operations per second'), boxmode='group')})

    return 0

def graph_wired_only_compression():
    kk = 'runs'
    xxx = {}
    yyy = {}

    xxx[kk] = []
    yyy[kk] = []
    boxplot0={}

    # Gather Data
    for r in data.stats['stats']:
        if 'intervals' in r.keys():
            k = r[series]
            # kk = op_type(r[series])+compression_type(r[series])
            kk = compression_type(r[series])+'_'+op_type(r[series])
            g = compression_type(r[series])+'_'+op_type(r[series])
            if 'wired' in link_type(k) and 'mixed' not in op_type(k):
                for interval in r['intervals']:
                    try:
                        xxx[kk].append(g)
                        yyy[kk].append(interval[y_code])
                    except:
                        xxx[kk] = []
                        yyy[kk] = []
                        xxx[kk].append(g)
                        yyy[kk].append(interval[y_code])
                    try:
                        boxplot0[k].append(interval[y_code])
                    except:
                        boxplot0[k] = []
                        boxplot0[k].append(interval[y_code])
    trace0 = []
    # Grouped Plot
    for key, value in yyy.iteritems():
        if True:
            trace0.append(Box(
                # x=value,
                y=value,
                name=key,
                boxmean='sd',
                boxpoints='all'
            )
            )
    plotly.offline.plot({
                            "data": sorted(trace0, key=lambda m: numpy.mean(m.y), reverse=True),
                            "layout": Layout(title="Wired Only, Varying Compression for Reads/Writes", yaxis=dict(title='operations per second'), boxmode='group')})

    return 0

def graph_wireless_only_compression():
    kk = 'runs'
    xxx = {}
    yyy = {}

    xxx[kk] = []
    yyy[kk] = []
    boxplot0={}

    # Gather Data
    for r in data.stats['stats']:
        if 'intervals' in r.keys():
            k = r[series]
            kk = compression_type(r[series])+'_'+op_type(r[series])
            g = compression_type(r[series])+'_'+op_type(r[series])
            if 'wireless' in link_type(k) and 'mixed' not in op_type(k):
                for interval in r['intervals']:
                    try:
                        xxx[kk].append(g)
                        yyy[kk].append(interval[y_code])
                    except:
                        xxx[kk] = []
                        yyy[kk] = []
                        xxx[kk].append(g)
                        yyy[kk].append(interval[y_code])
                    try:
                        boxplot0[k].append(interval[y_code])
                    except:
                        boxplot0[k] = []
                        boxplot0[k].append(interval[y_code])
    trace0 = []
    # Grouped Plot
    for key, value in yyy.iteritems():
        if True:
            trace0.append(Box(
                # x=value,
                y=value,
                name=key,
                boxmean='sd',
                boxpoints='all'
            )
            )
    plotly.offline.plot({
                            "data": sorted(trace0, key=lambda m: numpy.mean(m.y), reverse=True),
                            "layout": Layout(title="Wireless Only, Varying Compression for Reads/Writes", yaxis=dict(title='operations per second'), boxmode='group')})

    return 0

def graph_writes_only_graph_compaction():
    kk = 'runs'
    xxx = {}
    yyy = {}
    xxx[kk] = []
    yyy[kk] = []
    boxplot0={}

    # Gather Data
    for r in data.stats['stats']:
        if 'intervals' in r.keys():
            k = r[series]
            # kk = op_type(r[series])+compression_type(r[series])
            kk = compaction_type(r[series])+'_'+op_type(r[series])
            g = link_type(k)
            if 'writes_only' in op_type(k):
                for interval in r['intervals']:
                    try:
                        xxx[kk].append(g)
                        yyy[kk].append(interval[y_code])
                    except:
                        xxx[kk] = []
                        yyy[kk] = []
                        xxx[kk].append(g)
                        yyy[kk].append(interval[y_code])
                    try:
                        boxplot0[k].append(interval[y_code])
                    except:
                        boxplot0[k] = []
                        boxplot0[k].append(interval[y_code])
    trace0 = []
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
                            "layout": Layout(title="Compaction Methods", yaxis=dict(title='operations per second'), boxmode='group')})

    return 0

def graph_reads_only_graph_compaction():
    kk = 'runs'
    xxx = {}
    yyy = {}

    xxx[kk] = []
    yyy[kk] = []
    boxplot0={}

    # Gather Data
    for r in data.stats['stats']:
        if 'intervals' in r.keys():
            k = r[series]
            # kk = op_type(r[series])+compression_type(r[series])
            kk = compaction_type(r[series])+'_'+op_type(r[series])
            g = link_type(k)
            if 'reads_only' in op_type(k):
                for interval in r['intervals']:
                    try:
                        xxx[kk].append(g)
                        yyy[kk].append(interval[y_code])
                    except:
                        xxx[kk] = []
                        yyy[kk] = []
                        xxx[kk].append(g)
                        yyy[kk].append(interval[y_code])
                    try:
                        boxplot0[k].append(interval[y_code])
                    except:
                        boxplot0[k] = []
                        boxplot0[k].append(interval[y_code])
    trace0 = []
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
                            "layout": Layout(title="Compaction Methods", yaxis=dict(title='operations per second'), boxmode='group')})

    return 0

def graph_wired_only_compaction():
    kk = 'runs'
    xxx = {}
    yyy = {}

    xxx[kk] = []
    yyy[kk] = []
    boxplot0={}

    # Gather Data
    for r in data.stats['stats']:
        if 'intervals' in r.keys():
            k = r[series]
            # kk = op_type(r[series])+compression_type(r[series])
            kk = compaction_type(r[series])+'_'+op_type(r[series])
            g = compaction_type(r[series])+'_'+op_type(r[series])
            if 'wired' in link_type(k) and 'mixed' not in op_type(k):
                for interval in r['intervals']:
                    try:
                        xxx[kk].append(g)
                        yyy[kk].append(interval[y_code])
                    except:
                        xxx[kk] = []
                        yyy[kk] = []
                        xxx[kk].append(g)
                        yyy[kk].append(interval[y_code])
                    try:
                        boxplot0[k].append(interval[y_code])
                    except:
                        boxplot0[k] = []
                        boxplot0[k].append(interval[y_code])
    trace0 = []
    # Grouped Plot
    for key, value in yyy.iteritems():
        if True:
            trace0.append(Box(
                # x=value,
                y=value,
                name=key,
                boxmean='sd',
                boxpoints='all'
            )
            )
    plotly.offline.plot({
                            "data": sorted(trace0, key=lambda m: numpy.mean(m.y), reverse=True),
                            "layout": Layout(title="Wired Only, Varying Compaction for Reads/Writes", yaxis=dict(title='operations per second'), boxmode='group')})

    return 0

def graph_wireless_only_compaction():
    kk = 'runs'
    xxx = {}
    yyy = {}

    xxx[kk] = []
    yyy[kk] = []
    boxplot0={}

    # Gather Data
    for r in data.stats['stats']:
        if 'intervals' in r.keys():
            k = r[series]
            kk = compaction_type(r[series])+'_'+op_type(r[series])
            g = compaction_type(r[series])+'_'+op_type(r[series])
            if 'wireless' in link_type(k) and 'mixed' not in op_type(k):
                for interval in r['intervals']:
                    try:
                        xxx[kk].append(g)
                        yyy[kk].append(interval[y_code])
                    except:
                        xxx[kk] = []
                        yyy[kk] = []
                        xxx[kk].append(g)
                        yyy[kk].append(interval[y_code])
                    try:
                        boxplot0[k].append(interval[y_code])
                    except:
                        boxplot0[k] = []
                        boxplot0[k].append(interval[y_code])
    trace0 = []
    # Grouped Plot
    for key, value in yyy.iteritems():
        if True:
            trace0.append(Box(
                # x=value,
                y=value,
                name=key,
                boxmean='sd',
                boxpoints='all'
            )
            )
    plotly.offline.plot({
                            "data": sorted(trace0, key=lambda m: numpy.mean(m.y), reverse=True),
                            "layout": Layout(title="Wireless Only, Varying Compaction for Reads/Writes", yaxis=dict(title='operations per second'), boxmode='group')})

    return 0

def anova_dtcs():
    kk = 'runs'
    xxx = {}
    yyy = {}

    xxx[kk] = []
    yyy[kk] = []
    boxplot0={}

    # Gather Data
    for r in data.stats['stats']:
        if 'intervals' in r.keys():
            k = r[series]
            # print 'k=', k
            kk = k  # compaction_type(r[series])+'_'+op_type(r[series])
            g = compaction_type(r[series])+'_'+op_type(r[series])
            if True:
                for interval in r['intervals']:
                    try:
                        xxx[kk].append(g)
                        yyy[kk].append(interval[y_code])
                    except:
                        xxx[kk] = []
                        yyy[kk] = []
                        xxx[kk].append(g)
                        yyy[kk].append(interval[y_code])
                    try:
                        boxplot0[k].append(interval[y_code])
                    except:
                        boxplot0[k] = []
                        boxplot0[k].append(interval[y_code])
    print xxx
    print yyy
    print boxplot0
    # print kk


    print 1, yyy['wired_cqlstress-compaction-lcs-minsstable-0001yamlops_simple1_1__']
    print 2, yyy['wired_cqlstress-compaction-lcs-minsstable-0002yamlops_simple1_1__']
    print 4, yyy['wired_cqlstress-compaction-lcs-minsstable-0004yamlops_simple1_1__']
    print 8, yyy['wired_cqlstress-compaction-lcs-minsstable-0008yamlops_simple1_1__']
    print 16, yyy['wired_cqlstress-compaction-lcs-minsstable-0016yamlops_simple1_1__']
    print 32, yyy['wired_cqlstress-compaction-lcs-minsstable-0032yamlops_simple1_1__']
    print 64, yyy['wired_cqlstress-compaction-lcs-minsstable-0064yamlops_simple1_1__']

    print stats.f_oneway(

        yyy['wired_cqlstress-compaction-lcs-minsstable-0001yamlops_simple1_1__'],
        yyy['wired_cqlstress-compaction-lcs-minsstable-0002yamlops_simple1_1__'],
        yyy['wired_cqlstress-compaction-lcs-minsstable-0004yamlops_simple1_1__'],
        yyy['wired_cqlstress-compaction-lcs-minsstable-0008yamlops_simple1_1__'],
        yyy['wired_cqlstress-compaction-lcs-minsstable-0016yamlops_simple1_1__'],
        yyy['wired_cqlstress-compaction-lcs-minsstable-0032yamlops_simple1_1__'],
        yyy['wired_cqlstress-compaction-lcs-minsstable-0064yamlops_simple1_1__']

    )

    print stats.levene(

        yyy['wired_cqlstress-compaction-lcs-minsstable-0001yamlops_simple1_1__'],
        yyy['wired_cqlstress-compaction-lcs-minsstable-0002yamlops_simple1_1__'],
        yyy['wired_cqlstress-compaction-lcs-minsstable-0004yamlops_simple1_1__'],
        yyy['wired_cqlstress-compaction-lcs-minsstable-0008yamlops_simple1_1__'],
        yyy['wired_cqlstress-compaction-lcs-minsstable-0016yamlops_simple1_1__'],
        yyy['wired_cqlstress-compaction-lcs-minsstable-0032yamlops_simple1_1__'],
        yyy['wired_cqlstress-compaction-lcs-minsstable-0064yamlops_simple1_1__']

    )

    print stats.f_oneway(

        yyy['wired_cqlstress-compaction-lcs-minsstable-0001yamlops_insert_1__'],
        yyy['wired_cqlstress-compaction-lcs-minsstable-0002yamlops_insert_1__'],
        yyy['wired_cqlstress-compaction-lcs-minsstable-0004yamlops_insert_1__'],
        yyy['wired_cqlstress-compaction-lcs-minsstable-0008yamlops_insert_1__'],
        yyy['wired_cqlstress-compaction-lcs-minsstable-0016yamlops_insert_1__'],
        yyy['wired_cqlstress-compaction-lcs-minsstable-0032yamlops_insert_1__'],
        yyy['wired_cqlstress-compaction-lcs-minsstable-0064yamlops_insert_1__']

    )

    print stats.levene(

        yyy['wired_cqlstress-compaction-lcs-minsstable-0001yamlops_insert_1__'],
        yyy['wired_cqlstress-compaction-lcs-minsstable-0002yamlops_insert_1__'],
        yyy['wired_cqlstress-compaction-lcs-minsstable-0004yamlops_insert_1__'],
        yyy['wired_cqlstress-compaction-lcs-minsstable-0008yamlops_insert_1__'],
        yyy['wired_cqlstress-compaction-lcs-minsstable-0016yamlops_insert_1__'],
        yyy['wired_cqlstress-compaction-lcs-minsstable-0032yamlops_insert_1__'],
        yyy['wired_cqlstress-compaction-lcs-minsstable-0064yamlops_insert_1__']

    )


def graphs_dtcs():
    kk = 'runs'
    xxx = {}
    yyy = {}

    xxx[kk] = []
    yyy[kk] = []
    boxplot0={}

    # Gather Data
    for r in data.stats['stats']:
        if 'intervals' in r.keys():
            k = r[series]
            # print 'k=', k
            kk = k  # compaction_type(r[series])+'_'+op_type(r[series])
            g = compaction_type(r[series])+'_'+op_type(r[series])
            if True:
                for interval in r['intervals']:
                    try:
                        xxx[kk].append(g)
                        yyy[kk].append(interval[y_code])
                    except:
                        xxx[kk] = []
                        yyy[kk] = []
                        xxx[kk].append(g)
                        yyy[kk].append(interval[y_code])
                    try:
                        boxplot0[k].append(interval[y_code])
                    except:
                        boxplot0[k] = []
                        boxplot0[k].append(interval[y_code])
    trace0 = []
    # Grouped Plot
    for key, value in sorted(yyy.iteritems()):
        if 'lcs-minsstable' in key and 'insert' in key:
            trace0.append(Box(
                # x=value,
                y=value,
                name=key,
                boxmean='sd',
                boxpoints='all'
            )
            )
    plotly.offline.plot({
                            # "data": sorted(trace0, key=lambda m: numpy.mean(m.y), reverse=True),
                            "data": sorted(trace0),
                            "layout": Layout(title="Wireless Only, Varying Compaction for Reads/Writes", yaxis=dict(title='operations per second'), boxmode='group')})



def graph_wired_only_replication_factor():
    kk = 'runs'
    xxx = {}
    yyy = {}

    xxx[kk] = []
    yyy[kk] = []
    boxplot0={}

    # Gather Data
    for r in data.stats['stats']:
        if 'intervals' in r.keys():
            k = r[series]
            # kk = op_type(r[series])+compression_type(r[series])
            kk = replication_factor(r[series])+'_'+op_type(r[series])
            print 'k', k, 'kk', kk
            g = replication_factor(r[series])+'_'+op_type(r[series])
            if 'wired' in link_type(k) and 'mixed' not in op_type(k) and 'replication' in k:
                for interval in r['intervals']:
                    try:
                        xxx[kk].append(g)
                        yyy[kk].append(interval[y_code])
                    except:
                        xxx[kk] = []
                        yyy[kk] = []
                        xxx[kk].append(g)
                        yyy[kk].append(interval[y_code])
                    try:
                        boxplot0[k].append(interval[y_code])
                    except:
                        boxplot0[k] = []
                        boxplot0[k].append(interval[y_code])
    trace0 = []
    # Grouped Plot
    for key, value in yyy.iteritems():
        if True:
            trace0.append(Box(
                # x=value,
                y=value,
                name=key,
                boxmean='sd',
                boxpoints='all'
            )
            )
    plotly.offline.plot({
                            "data": sorted(trace0, key=lambda m: numpy.mean(m.y), reverse=True),
                            "layout": Layout(title="Wired Only, Varying Replication Factor", yaxis=dict(title='operations per second'), boxmode='group')})

    return 0





# configure the graph
interval = 0
x_code = time_
y_code = ops_p_s
series = 'revision'
run = 0


# anova_dtcs()
# graphs_dtcs()

'''
graph_writes_only_graph_compaction()
graph_reads_only_graph_compaction()
graph_wired_only_compaction()
graph_wireless_only_compaction()
'''
