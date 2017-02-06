from scipy import stats
import numpy as np
import pandas as pd
from graph_utility import return_filtered_dataframe as rfd
from generate_conclusion import display_appropriate_interval_from_ms
from graph_utility import calculate_summary as cs




def map_reference_value(r,
                        desired_index=None,
                        cluster_sizes=None,
                        workloads=None,
                        database_sizes=None,
                        marker_for_reference_trial='unk',
                        level_for_trials=3):

    if not desired_index:
        desired_index = ['ref', 'unk', '2GB']

    if not cluster_sizes:
        cluster_sizes = [1, 3, 6]

    if not workloads:
        workloads = ['a', 'c', 'e']

    if not database_sizes:
        database_sizes = [1000]

    for nn in cluster_sizes:
        for wl in workloads:
            for db in database_sizes:

                r[desired_index[0],
                  desired_index[1],
                  desired_index[2]].loc[nn, wl, db] = r[desired_index[0],
                                                        desired_index[1],
                                                        desired_index[2]].loc[nn, wl, db, marker_for_reference_trial]

    r.drop(labels='unk', level=level_for_trials, inplace=True)

    return r

# Return df with a speedup column
def return_general_summary_table(main_csv_file='combined_results_revised.csv',
                                 reference_csv_file='abramova_results.csv',
                                 trial_list=None,
                                 measurement_of_interest='[OVERALL] RunTime(ms)',
                                 desired_index=None,
                                 desired_columns=None,
                                 desired_summary_function=np.median
                                 ):

    if not trial_list:
        trial_list = range(10, 30+1)

    if not desired_index:
        desired_index = ['nn', 'wl', 'dbs']

    if not desired_columns:
        desired_columns = ['nt', 'nm', 'ram']

    df = pd.read_csv(main_csv_file)

    df = rfd(df=df, d={'t': trial_list})

    if reference_csv_file:
        df = df.append(pd.read_csv(reference_csv_file))

    table = pd.pivot_table(df,
                           values=measurement_of_interest,
                           index=desired_index,
                           columns=desired_columns,
                           aggfunc=desired_summary_function)

    return table



def return_reference_data_frame():

    df_ref = pd.read_csv('abramova_results.csv')

    df_ref = df_ref.set_index(['nn', 'wl'])

    return df_ref


def get_summary_table(df,
                      label_for_new_column,
                      nn,
                      wl,
                      db=1000):

    if not nn:
        nn = [1, 3, 6]

    df_summary = df[label_for_new_column].loc[nn, wl, db]

    df_summary_for_individual_cluster_sizes = df_summary.unstack(level='nn')

    df_summary_stats_for_individual_cluster_sizes = df_summary_for_individual_cluster_sizes.describe()
    df_summary_stats_overall = df_summary.describe().rename('OVERALL')

    df_summary_stats = df_summary_stats_for_individual_cluster_sizes.join(pd.DataFrame(df_summary_stats_overall))

    return df_summary_stats


def get_observations_paragraph_for_reference(cluster_sizes=None,
                                             df_summary_of_differentials=None,
                                             df_ref=None,
                                             measurement_of_interest='[OVERALL] RunTime(ms)',
                                             workload='a'):

    s = ''

    if not cluster_sizes:
        cluster_sizes = [1, 3, 6]

    for cluster_size in cluster_sizes:
        nn = cluster_size
        wl = workload
        ref_val = df_ref[measurement_of_interest].loc[nn, wl]
        max_dif= df_summary_of_differentials[nn].loc['max']
        min_dif= df_summary_of_differentials[nn].loc['min']
        mean_dif= df_summary_of_differentials[nn].loc['mean']
        s += 'For a node cluster size of {cluster_size}, ' \
             'the experimental values fell within {max_dif} of the value reported, which was {ref_val}.  ' \
             ''.format(cluster_size=cluster_size,
                       max_dif=display_appropriate_interval_from_ms(max_dif),
                       ref_val=display_appropriate_interval_from_ms(ref_val, include_terminal_comma=False))

    nn = 'OVERALL'
    max_dif= df_summary_of_differentials[nn].loc['max']
    min_dif= df_summary_of_differentials[nn].loc['min']
    mean_dif= df_summary_of_differentials[nn].loc['mean']
    s += 'Overall, ' \
         'the experimental values fell within {max_dif} of the corresponding reference value.  \n' \
         ''.format(cluster_size=cluster_size,
                   max_dif=display_appropriate_interval_from_ms(max_dif),
                   ref_val=display_appropriate_interval_from_ms(ref_val, include_terminal_comma=False))

    return s


# Return df with a speedup column
def return_df_that_includes_speedup(main_csv_file='combined_results_revised.csv',
                                    reference_csv_file='abramova_results.csv',
                                    trial_list=None,
                                    measurement_of_interest='[OVERALL] RunTime(ms)',
                                    desired_index=None,
                                    desired_columns=None,
                                    filter_for_nominator=None,
                                    filter_for_denominator=None,
                                    label_for_new_column='su_rp_vm'):

    if not filter_for_denominator:
        filter_for_denominator = ['rp', 'eth', '1GB']

    if not filter_for_nominator:
        filter_for_nominator = ['vm', 'nodal', '1GB']

    table = return_general_summary_table(main_csv_file=main_csv_file,
                                         reference_csv_file=reference_csv_file,
                                         trial_list=trial_list,
                                         measurement_of_interest=measurement_of_interest,
                                         desired_index=desired_index,
                                         desired_columns=desired_columns,
                                         desired_summary_function=np.median
                                         )

    table[label_for_new_column] = table[filter_for_nominator[0],
                                        filter_for_nominator[1],
                                        filter_for_nominator[2]] / table[filter_for_denominator[0],
                                                                         filter_for_denominator[1],
                                                                         filter_for_denominator[2]]

    return table


# Return df with a speedup column
def return_df_that_includes_differences(main_csv_file='combined_results_revised.csv',
                                        reference_csv_file='abramova_results.csv',
                                        trial_list=None,
                                        measurement_of_interest='[OVERALL] RunTime(ms)',
                                        desired_index=None,
                                        desired_columns=None,
                                        filter_for_nominator=None,
                                        filter_for_denominator=None,
                                        label_for_new_column='su_rp_vm'):

    if not filter_for_denominator:
        filter_for_denominator = ['rp', 'eth', '1GB']

    if not filter_for_nominator:
        filter_for_nominator = ['vm', 'nodal', '1GB']

    desired_index=['nn', 'wl', 'dbs', 't']

    table = return_general_summary_table(main_csv_file=main_csv_file,
                                         reference_csv_file=reference_csv_file,
                                         trial_list=trial_list,
                                         measurement_of_interest=measurement_of_interest,
                                         desired_index=desired_index,
                                         desired_columns=desired_columns,
                                         desired_summary_function=np.median
                                         )

    table = map_reference_value(r=table)

    # Temporarily requires three

    table[label_for_new_column] = abs(table[filter_for_nominator[0],
                                        filter_for_nominator[1],
                                        filter_for_nominator[2]] - table[filter_for_denominator[0],
                                                                         filter_for_denominator[1],
                                                                         filter_for_denominator[2]])

    return table


# This is to support the conclusion that RAM (within a certain range) does not have an effect
#  on the overall performance of a distributed database such as Cassandra.
def anova_for_variation_in_ram(csv_file='combined_results_revised.csv',
                               measurement_of_interest = '[OVERALL] RunTime(ms)',
                               d=None,
                               wl='a',
                               nn=1):
    if not d:
        d={'nt': 'vm',
           'wl': wl,
           'nn': nn,
           't': range(10, 30+1)}

    df = pd.read_csv(csv_file)
    df_filtered = rfd(df, d=d)

    df_1gb = rfd(df_filtered, d={'ram': '1GB'})[measurement_of_interest]
    df_2gb = rfd(df_filtered, d={'ram': '2GB'})[measurement_of_interest]
    df_4gb = rfd(df_filtered, d={'ram': '4GB'})[measurement_of_interest]

    return return_embedded_latex_tables(latex_table_as_string=return_anova_summary_table(df_1gb, df_2gb, df_4gb),
                                        label='ram_variance_analysis_workload_'+wl+'_'+str(nn)+'_node',
                                        caption='ANOVA Summary Table for '
                                                'Workload {}, {} Node Cluster'.format(wl.capitalize(), nn)
                                        )


def return_max_min_range_for_all_levels_of_ram(csv_file='combined_results_revised.csv',
                                      measurement_of_interest = '[OVERALL] RunTime(ms)',
                                      d=None,
                                      wl='a',
                                      nn=1):

    if not d:
        d={'nt': 'vm',
           'wl': wl,
           'nn': nn,
           't': range(10, 30+1)}

    df = pd.read_csv(csv_file)
    df_filtered = rfd(df, d=d)

    df_Xgb = df_filtered[measurement_of_interest]

    s = df_Xgb.describe()

    for x in [s]:
        x['range'] = x['max'] - x['min']

    return s['max'], s['min'], s['range']


def return_summary_statistics_for_vms(csv_file='combined_results_revised.csv',
                                      measurement_of_interest = '[OVERALL] RunTime(ms)',
                                      d=None,
                                      wl='a',
                                      nn=1):

    if not d:
        d={'nt': 'vm',
           'wl': wl,
           'nn': nn,
           't': range(10, 30+1)}

    df = pd.read_csv(csv_file)
    df_filtered = rfd(df, d=d)

    df_1gb = rfd(df_filtered, d={'ram': '1GB'})[measurement_of_interest]
    df_2gb = rfd(df_filtered, d={'ram': '2GB'})[measurement_of_interest]
    df_4gb = rfd(df_filtered, d={'ram': '4GB'})[measurement_of_interest]

    s = df_1gb.describe()
    t = df_2gb.describe()
    u = df_4gb.describe()

    for x in [s, t, u]:
        x['range'] = x['max'] - x['min']

    v = pd.DataFrame(dict(ram1GB=s, ram2GB=t, ram4GB=u)).reset_index()

    return v.to_latex(index=False)



def return_summary_statistics_for_rp(csv_file='combined_results_revised.csv',
                                      measurement_of_interest = '[OVERALL] RunTime(ms)',
                                      d=None,
                                      wl='a',
                                      nn=1,
                                      nt='rp',
                                      nm='eth',
                                      cluster_sizes_of_choice={'1': 1, '3': 3, '6': 6}):

    if not d:
        d={'nm': nm,
           'nt': nt,
           'wl': wl,
           't': range(10, 30+1)}

    df = pd.read_csv(csv_file)
    df_filtered = rfd(df, d=d)

    df = {}
    s = {}
    for k, v in cluster_sizes_of_choice.iteritems():
        df[k] = rfd(df_filtered, d={'nn': v})[measurement_of_interest]
        s[k] = df[k].describe()

    for x in s.itervalues():
        x['range'] = x['max'] - x['min']

    v = pd.DataFrame(s).reset_index()
    set_display_format_for_floats(
        format_='{:.2g}'.format
    )
    return v.to_latex(index=False)


def summary_statistics_rp_for_1_3_and_6_node_configurations(wl='a'):
    set_display_format_for_floats(format_='{:.6g}'.format)
    x = ''

    caption = 'Summary for Raspberry Pi wired local area network'
    x += return_embedded_latex_tables(return_summary_statistics_for_rp(wl=wl,
                                                                       cluster_sizes_of_choice={'1': 1, '3': 3, '6': 6}),
                                          caption=caption,
                                          label='rp_wired_summary_statistics',
                                      )
    return x

def summary_statistics_rp_for_all_cluster_sizes(wl='a'):
    set_display_format_for_floats(format_='{:.6g}'.format)
    x = ''

    caption = 'Summary for Raspberry Pi wired local area network'
    x += return_embedded_latex_tables(return_summary_statistics_for_rp(wl=wl,
                                                                       cluster_sizes_of_choice={'1': 1,
                                                                                                '2': 2,
                                                                                                '3': 3,
                                                                                                '4': 4,
                                                                                                '5': 5,
                                                                                                '6': 6}),
                                          caption=caption,
                                          label='rp_wired_summary_statistics',
                                      )
    return x


# This function absorbs the responsibility of spacing out the tables
def return_embedded_latex_tables(latex_table_as_string='',
                                 label='',
                                 caption=''):
    xx = ''

    x = '\n\n'
    x += r'\begin{table}[H]' + '\n'
    x += r'\centering' + '\n'
    x += latex_table_as_string

    x += '\caption{'+caption+'}' + '\n'
    x += '\label{table:' + label + '}' + '\n'
    x += '\end{table}' + '\n\n'

    xx += x
    return xx

# This function absorbs the responsibility of spacing out the tables
def return_latex_tables_for_vm_summary_statistics(wl='a'):
    xx = ''
    for i in [1, 3, 6]:
        xx += return_embedded_latex_tables(latex_table_as_string=return_summary_statistics_for_vms(
                                               csv_file='combined_results_revised.csv',
                                               measurement_of_interest='[OVERALL] RunTime(ms)',
                                               d={'nt': 'vm',
                                                  'wl': wl,
                                                  'nn': i,
                                                  't': range(10, 30+1)
                                                  }
                                               ),
                                           caption='Summary Statistics for {}-Node Configuration. '
                                                   'All values represented fall between 5911.0 ms and '
                                                   '6891.0 ms, or rather within a span of 980.0 ms.'.format(i),
                                           label='table:summary_statistics_for_{}_config'.format(i)
        )




    return xx

def return_anova_summary_table(*args):

    string = ''

    index = 0
    ss = {}
    ss_wg = 0
    df_wg = 0
    for arg in args:
        s = pd.Series(arg)
        ss[index] = 0
        sum_of_squares = 0
        for key, val in s.iteritems():
            sum_of_squares += val**2
        ss[index] += sum_of_squares - s.sum()**2/s.count()  # from the text
        ss_wg += ss[index]
        df_wg += s.count() - 1
        index += 1

    # Now for the total
    first_iteration = True
    for arg in args:
        s = pd.Series(arg)
        if first_iteration:
            s_total = s
            first_iteration = False
        else:
            s_total = s_total.append(s)
    sum_of_squares = 0
    for key, val in s_total.iteritems():
        sum_of_squares += val**2
    ss_t = sum_of_squares - s_total.sum()**2/s_total.count()  # from the text

    ss_bg = ss_t - ss_wg

    df_bg = len(args) - 1
    df_t = df_bg + df_wg

    ms_bg = ss_bg / df_bg
    ms_wg = ss_wg / df_wg
    f_alternative = ms_bg / ms_wg

    f, p = stats.f_oneway(*args)

    #Make the summary table
    d = {'Source' : pd.Series(['between groups', 'within groups', 'total']),
         'SS' : pd.Series([ss_bg, ss_wg, ss_t]),
         'df' : pd.Series([df_bg, df_wg, df_t]),
         'MS' : pd.Series([ms_bg, ms_wg]),
         'F' : pd.Series([f_alternative]),
         'p' : pd.Series([p]),
         }

    df = pd.DataFrame(d)

    return df.to_latex(index=False, columns=['Source', 'SS', 'df', 'MS', 'F', 'p'])

# Display format
# Even though this is one line, it was written for convenience
def set_display_format_for_floats(format_='{:.2g}'.format):
    pd.options.display.float_format = format_
    return 0

def anova_for_variation_in_ram_1(csv_file='combined_results_revised.csv',
                                 measurement_of_interest='[OVERALL] RunTime(ms)',
                                 d=None):

    if not d:
        d={'nt': 'vm',
           'wl': 'a',
           'nn': 1}

    df = pd.read_csv(csv_file)
    df_filtered = rfd(df, d=d)

    df_1gb = rfd(df_filtered, d={'ram': '1GB'})[measurement_of_interest]
    df_2gb = rfd(df_filtered, d={'ram': '2GB'})[measurement_of_interest]
    df_4gb = rfd(df_filtered, d={'ram': '4GB'})[measurement_of_interest]

    results = return_anova_summary_table(df_1gb, df_2gb, df_4gb)

    return results

def ram_for_workload_a():
    set_display_format_for_floats(format_='{:.2g}'.format)

    print anova_for_variation_in_ram(nn=1)
    print anova_for_variation_in_ram(nn=3)
    print anova_for_variation_in_ram(nn=6)


def generate_bound_statement(max_,min_,ref,series):

    bound = max(abs(max_-ref),abs(min_-ref))
    s='For {}, the experimental values fell between {} ms and {} ms, inclusive, ' \
      'and all values fell within {} ms of the reference value of {} ms.  '.format(series, min_, max_, bound, ref)

    return s


def generate_bound_statements_rp_wired(
                                 csv_file='combined_results_revised.csv',
                                      measurement_of_interest = '[OVERALL] RunTime(ms)',
                                      d=None,
                                      wl='a',
                                      nn=1,
                                      nt='rp',
                                      nm='eth'):
    s = ''
    d=None
    if not d:
        d={'nm': nm,
           'nt': nt,
           'wl': wl,
           't': range(10, 30+1)}
    ref_values = {'a': {1: 58430, 3:65650, 6:87310},
                  'c': {1: 88000, 3:90210, 6:118090},
                  'e': {1: 223180, 3:330820, 6:404660}
                  }

    df = pd.read_csv(csv_file)
    df_filtered = rfd(df, d=d)
    for node in [1,3,6]:
        df = rfd(df_filtered, d={'nn': node})[measurement_of_interest]
        summary = df.describe()
        s += generate_bound_statement(max_=summary['max'], min_=summary['min'],
                                      series='a node network of {}'.format(node),
                                      ref=ref_values[wl][node])

    return s

def generate_bound_statements_rp_wired_and_wireless(
                                 csv_file='combined_results_revised.csv',
                                      measurement_of_interest = '[OVERALL] RunTime(ms)',
                                      d=None,
                                      wl='a',
                                      nn=1,
                                      nt='rp',
                                      nm='eth'):

    s = 'The median value of the corresponding wired experiment will serve as the reference in this paragraph. '

    d_wlan={'nm': 'wlan',
           'nt': nt,
           'wl': wl,
           't': range(10, 30+1)}

    d_eth={'nm': 'eth',
           'nt': nt,
           'wl': wl,
           't': range(10, 30+1)}


    ref_values = {'a': {1: 58430, 3:65650, 6:87310},
                  'c': {1: 88000, 3:90210, 6:118090},
                  'e': {1: 223180, 3:330820, 6:404660}
                  }

    df = pd.read_csv(csv_file)
    df_filtered_eth = rfd(df, d=d_eth)
    df_filtered_wlan = rfd(df, d=d_wlan)
    for node in [1, 3, 6]:
        df_eth = rfd(df_filtered_eth, d={'nn': node})[measurement_of_interest]
        df_wlan = rfd(df_filtered_wlan, d={'nn': node})[measurement_of_interest]
        summary_eth = df_eth.describe()
        summary_wlan = df_wlan.describe()
        s += generate_bound_statement(max_=summary_wlan['max'], min_=summary_wlan['min'],
                                      series='a node network of {}'.format(node),
                                      ref=summary_eth['50%'])

    return s

def summary_statistics_varying_RAM_for_1_3_and_6_node_configurations(wl='a'):
    set_display_format_for_floats(format_='{:.6g}'.format)
    x = ''

    for n in [1, 3, 6]:
        total_max, total_min, total_range = return_max_min_range_for_all_levels_of_ram(nn=n, wl=wl)
        caption = 'Summary Statistics for {}-Node Configuration. ' \
                  'All values represented fall between {} ms and {} ms, or rather within a span of {} ms.' \
                  ''.format(n, total_min, total_max, total_range)
        x += return_embedded_latex_tables(return_summary_statistics_for_vms(nn=n, wl=wl),
                                              caption=caption,
                                              label='summary_statistics_for_{}_config_varying_ram_wl{}'.format(n, wl))
    return x


def assign_contrast(val, thing_that_gets_assigned_0, thing_that_gets_assigned_1):
    if val == thing_that_gets_assigned_0:
        return 0
    elif val == thing_that_gets_assigned_1:
        return 1
    else:
        return -1

def assign_contrast_wired_v_wireless(val):
    return assign_contrast(val, 'eth', 'wlan')


def assign_contrast_rp_v_vm(val):
    return assign_contrast(val, 'vm', 'rp')


# There's a better way to do this with regular expressions, but for now this works.
# s will be between '1GB', '2GB', '4GB'
def convert_ram_text_to_gb(s):
    if s in ['1GB', '2GB', '4GB']:
        return int(s[0])
    else:
        return -999


def return_speedup_stats(x, y):

    speedup_stats = {

        'ratio_of_the_means': stats.nanmean(x) / stats.nanmean(y),
        'ratio_of_the_medians': stats.nanmedian(x) / stats.nanmedian(y),
        'ratio_of_the_stddevs': stats.nanstd(x) / stats.nanstd(y),
        'ratio_max_to_min': np.amax(x) / np.amin(y),
        'ratio_min_to_max': np.amin(x) / np.amax(y)

    }
    return speedup_stats


#
def return_entire_speedup_table(workload,
                                comparison_description,
                                measurement_of_interest='[OVERALL] RunTime(ms)',
                                csv_file=None):

    df = pd.read_csv(csv_file)

    dd = []

    d = [None, None]
    df_filtered = [None, None]

    speedup_dictionary = {}

    for cluster_size in range(1, 6 + 1) + [[1, 2, 3, 4, 5, 6]]:

        if comparison_description == 'rp_v_vm':
            nm = ['nodal', 'eth']
            nt = ['vm', 'rp']
        elif comparison_description == 'wlan_v_eth':
            nm = ['eth', 'wlan']
            nt = ['rp', 'rp']
        else:
            nm = 'error'
            nt = 'error'

        for i in [0, 1]:
            d[i] = {'nt': nt[i],
                    'wl': workload,
                    'ram': '1GB',
                    'nm': nm[i],
                    'nn': cluster_size,
                    't': range(10, 30+1)
                    }

            df_filtered[i] = rfd(df=df, d=d[i])

        x = df_filtered[0][measurement_of_interest]
        y = df_filtered[1][measurement_of_interest]

        speedup_dictionary = return_speedup_stats(x, y)

        if cluster_size == [1, 2, 3, 4, 5, 6]:
            speedup_dictionary['cluster_size'] = 'OVERALL'
        else:
            speedup_dictionary['cluster_size'] = cluster_size

        dd.append(speedup_dictionary)

    table_in_dataframe_format = pd.DataFrame(dd)

    table_in_dataframe_format = table_in_dataframe_format.transpose()

    return table_in_dataframe_format.to_latex()


# These are all linear regressions
def speedup_analysis_tables(csv_file, comparison_description, workload,
                            measurement_of_interest = '[OVERALL] RunTime(ms)'):

    s = ':::something went wrong generating the speedup analysis tables:::'

    df = pd.read_csv(csv_file)

    label='{}_{}'.format(comparison_description, workload)

    reference_statement = ''  # initialize

    if comparison_description == 'ram_v_ram':

        reference_statement = 'See Table \\ref{{{}}}.'.format('table:{}'.format(label))

        dd = {}

        dd['slope'] = []
        dd['intercept'] = []
        dd['r_value'] = []
        dd['p_value'] = []
        dd['std_err'] = []
        dd['cluster_size'] = []

        for cluster_size in range(1, 6 + 1):

            d={'nt': 'vm',
               'wl': workload,
               'nn': cluster_size,
               't': range(10, 30+1)}

            df_filtered = rfd(df=df, d=d)

            df_filtered['ram_in_gb'] = df_filtered['ram'].map(convert_ram_text_to_gb)

            if not df_filtered.empty:

                x = df_filtered['ram_in_gb']
                y = df_filtered[measurement_of_interest]
                slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

                dd['slope'].append(slope)
                dd['intercept'].append(intercept)
                dd['r_value'].append(r_value)
                dd['p_value'].append(p_value)
                dd['std_err'].append(std_err)
                dd['cluster_size'].append(cluster_size)

        dd = pd.DataFrame(dd)

        s = return_embedded_latex_tables(latex_table_as_string=dd.to_latex(index=False,
                                                                           columns=['cluster_size', 'slope',
                                                                                    'intercept', 'r_value',
                                                                                    'p_value', 'std_err']),
                                         caption='Linear Regression over amount of RAM',
                                         label=label)

    elif comparison_description in ['rp_only', 'wlan_only']:

        reference_statement = 'See Table \\ref{{{}}}.'.format('table:{}'.format(label))

        dd = {}

        dd['slope'] = []
        dd['intercept'] = []
        dd['r_value'] = []
        dd['p_value'] = []
        dd['std_err'] = []

        if comparison_description == 'rp_only':
            nm = 'eth'
        elif comparison_description == 'wlan_only':
            nm = 'wlan'
        else:
            nm = 'error'

        d={'nt': 'rp',
           'wl': workload,
           'ram': '1GB',
           'nm': nm,
           't': range(10, 30+1)}

        df_filtered = rfd(df=df, d=d)

        x = df_filtered['nn']
        y = df_filtered[measurement_of_interest]
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

        dd['slope'].append(slope)
        dd['intercept'].append(intercept)
        dd['r_value'].append(r_value)
        dd['p_value'].append(p_value)
        dd['std_err'].append(std_err)

        dd = pd.DataFrame(dd)

        s = return_embedded_latex_tables(latex_table_as_string=dd.to_latex(index=False,
                                                                           columns=['slope', 'intercept',
                                                                                    'r_value', 'p_value', 'std_err']),
                                         caption='Linear Regression over Cluster Size, Workload {}'.format(workload.capitalize()),
                                         label=label
                                         )


    elif comparison_description in ['rp_v_vm', 'wlan_v_eth']:

        dd = {}

        dd['slope'] = []
        dd['intercept'] = []
        dd['r_value'] = []
        dd['p_value'] = []
        dd['std_err'] = []
        dd['cluster_size'] = []

        for cluster_size in range(1, 6 + 1):

            d={'nt': ['vm', 'rp'],
               'wl': workload,
               'nn': cluster_size,
               'ram': '1GB',
               't': range(10, 30+1)}

            # Tune the filter
            if comparison_description in ['rp_v_vm']:
                d['nm'] = ['eth', 'nodal']
                d['nt'] = ['rp', 'vm']

            elif comparison_description in ['wlan_v_eth']:
                d['nm'] = ['eth', 'wlan']
                d['nt'] = 'rp'


            df_filtered = rfd(df=df, d=d)

            if comparison_description in ['rp_v_vm']:
                name_of_new_column = 'is_limited_hardware'
                df_filtered[name_of_new_column] = df_filtered['nt'].map(assign_contrast_rp_v_vm)
            elif comparison_description in ['wlan_v_eth']:
                name_of_new_column = 'is_wireless_lan'
                df_filtered[name_of_new_column] = df_filtered['nm'].map(assign_contrast_wired_v_wireless)
            else:
                name_of_new_column = 'error_occurred'

            x = df_filtered[name_of_new_column]
            y = df_filtered[measurement_of_interest]
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

            dd['slope'].append(slope)
            dd['intercept'].append(intercept)
            dd['r_value'].append(r_value)
            dd['p_value'].append(p_value)
            dd['std_err'].append(std_err)
            dd['cluster_size'].append(cluster_size)

        cluster_size = [1, 2, 3, 4, 5, 6]

        # -- Now append the Overall, over 1,2,3,4,5,6 -- #
        d['nn'] = cluster_size

        df_filtered = rfd(df=df, d=d)

        if comparison_description in ['rp_v_vm']:
            name_of_new_column = 'is_limited_hardware'
            df_filtered[name_of_new_column] = df_filtered['nt'].map(assign_contrast_rp_v_vm)
        elif comparison_description in ['wlan_v_eth']:
            name_of_new_column = 'is_wireless_lan'
            df_filtered[name_of_new_column] = df_filtered['nm'].map(assign_contrast_wired_v_wireless)

        x = df_filtered[name_of_new_column]
        y = df_filtered[measurement_of_interest]
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

        dd['slope'].append(slope)
        dd['intercept'].append(intercept)
        dd['r_value'].append(r_value)
        dd['p_value'].append(p_value)
        dd['std_err'].append(std_err)
        dd['cluster_size'].append('OVERALL')

        # --- Now convert to dataframe ---

        dd = pd.DataFrame(dd)

        if comparison_description in ['rp_v_vm']:
            caption = 'Linear Regression over the effect of limited hardware, Workload {}.  The designation (NaN) indicates that data was not collected for this cluster size.  r- values in the high nineties indicate that there is a pronounced effect.  Lower r-values indicate a less pronounced effect, likely attributed to high variance.'.format(workload.capitalize())
        elif comparison_description in ['wlan_v_eth']:
            caption = 'Linear Regression over the effect of 802.11 links, Workload {}.  The designation (NaN) indicates that data was not collected for this cluster size.   r-values in the high nineties indicate that there is a pronounced effect.  Lower r-values indicate a less pronounced effect, likely attributed to high variance.'.format(workload.capitalize())
        else:
            caption = 'Something went wrong with the caption assignment.'

        insert0 = return_embedded_latex_tables(latex_table_as_string=dd.to_latex(index=False,
                                                                           columns=['cluster_size', 'slope',
                                                                                    'intercept', 'r_value',
                                                                                    'p_value', 'std_err']),
                                         caption=caption,
                                         label=label)

        # -- Get the speedup statistics --

        if comparison_description in ['rp_v_vm']:
            caption_for_speedup = 'Speedup over the effect of limited hardware, Workload {}'.format(workload.capitalize())
        elif comparison_description in ['wlan_v_eth']:
            caption_for_speedup = 'Speedup over the effect of 802.11 links, Workload {}'.format(workload.capitalize())
        else:
            caption_for_speedup = 'Something went wrong with the caption assignment.'

        label_for_speedup = label + '_speedup'

        entire_speedup_table = return_entire_speedup_table(workload=workload,
                                comparison_description=comparison_description,
                                measurement_of_interest='[OVERALL] RunTime(ms)',
                                csv_file=csv_file)

        reference_statement = 'See Tables \\ref{{{}}} and \\ref{{{}}}.'.format('table:{}'.format(label), 'table:{}'.format(label_for_speedup))

        insert1 = return_embedded_latex_tables(latex_table_as_string=entire_speedup_table,
                                               caption=caption_for_speedup,
                                               label=label_for_speedup)

        s = '\n\n' + insert0 + '\n\n' + insert1 + '\n\n'

    elif comparison_description in ['rp_v_ref', 'vm_v_ref']:
        s = ''

    s = reference_statement + '\n\n' + s


    return s


def return_summary_statistics_tabular(workload='a',
                                    nt='vm',
                                    ram='1GB',
                                    nm='nodal',
                                    csv_file='combined_results_revised.csv',
                                    measurement_of_interest = '[OVERALL] RunTime(ms)'):



    ss = []

    for cluster_size in [1, 2, 3, 4, 5, 6, [1, 2, 3, 4, 5, 6]]:

        d = {'nt': nt,
             'wl': workload,
             'ram': ram,
             'nm': nm,
             'nn': cluster_size,
             't': range(10, 30+1)}

        df = pd.read_csv(csv_file)
        df_filtered = rfd(df, d=d)[measurement_of_interest]

        if not df_filtered.empty:

            s = df_filtered.describe()

            s['range'] = s['max'] - s['min']

            if cluster_size == [1, 2, 3, 4, 5, 6]:
                s['cluster_size'] = "Overall"
            else:
                s['cluster_size'] = cluster_size

            ss.append(s)

    v = pd.DataFrame(ss).reset_index()

    w = pd.pivot_table(v,
                           columns=['cluster_size'])

    return w.to_latex(index=True)




# -------------------------------------------------------------------------------------------
# For testing purposes only
# -------------------------------------------------------------------------------------------

# From http://vassarstats.net/textbook/ch14pt1.html
def return_example_dataframe_for_anova_test():

    df = pd.DataFrame(

        {
             'a': pd.Series([27.0, 26.2, 28.8, 33.5, 28.8]),
             'b': pd.Series([22.8, 23.1, 27.7, 27.6, 24.0]),
             'c': pd.Series([21.9, 23.4, 20.1, 27.8, 19.3]),
             'd': pd.Series([23.5, 19.6, 23.7, 20.8, 23.9])
        }

    )

    return df

