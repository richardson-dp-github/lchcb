from scipy import stats
import pandas as pd
from graph_utility import return_filtered_dataframe as rfd
from graph_utility import calculate_summary as cs


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
                                        caption='ANOVA Summary Table for Workload '+wl.capitalize()+', '+str(nn)+' Node')


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
                                      nm='eth'):

    if not d:
        d={'nm': nm,
           'nt': nt,
           'wl': wl,
           't': range(10, 30+1)}

    df = pd.read_csv(csv_file)
    df_filtered = rfd(df, d=d)

    df = {}
    s = {}
    for k, v in {'1': 1, '3': 3, '6': 6}.iteritems():
        df[k] = rfd(df_filtered, d={'nn': v})[measurement_of_interest]
        s[k] = df[k].describe()

    for x in s.itervalues():
        x['range'] = x['max'] - x['min']

    v = pd.DataFrame(s).reset_index()
    set_display_format_for_floats(
        format_='{:.2g}'.format
    )
    return v.to_latex(index=False)


# This function absorbs the responsibility of spacing out the tables
def return_latex_tables_for_vm_summary_statistics(wl='a'):
    xx = ''
    for i in [1, 3, 6]:
        x = ''
        x += r'\begin{table}' + '\n'
        x += return_summary_statistics_for_vms(csv_file='combined_results_revised.csv',
                                               measurement_of_interest='[OVERALL] RunTime(ms)',
                                               d={'nt': 'vm',
                                                  'wl': wl,
                                                  'nn': i,
                                                  't': range(10, 30+1)
                                                  }
                                               )
        x += '\label{summary_statistics_execution_time_' + str(i) + '}' + '\n'
        x += '\caption{Summary statistics for case ' + str(i) + ' nodes}' + '\n'
        x += '\end{table}' + '\n'

        xx += x
    return xx


# This function absorbs the responsibility of spacing out the tables
def return_embedded_latex_tables(latex_table_as_string='',
                                 label='',
                                 caption=''):
    xx = ''

    x = ''
    x += r'\begin{table}' + '\n'
    x += latex_table_as_string
    x += '\label{table:' + label + '}' + '\n'
    x += '\caption{'+caption+'}' + '\n'
    x += '\end{table}' + '\n'

    xx += x
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

