import pandas as pd
from graph_utility import return_filtered_dataframe as rfd


def display_appropriate_interval_from_ms(ms=1000,
                                         include_terminal_comma=True):

    s = ms, 'milliseconds'

    milliseconds_in_a_second = 1000
    seconds_in_a_minute = 60
    minutes_in_an_hour = 60
    hours_in_a_day = 24
    days_in_a_week = 7

    second_threshold = milliseconds_in_a_second
    minute_threshold = second_threshold * seconds_in_a_minute
    hour_threshold = minute_threshold * minutes_in_an_hour
    day_threshold = hour_threshold * hours_in_a_day
    week_threshold = day_threshold * days_in_a_week

    if -1 < ms < second_threshold:
        s = s
    elif second_threshold <= ms < minute_threshold:
        s = ms / milliseconds_in_a_second, 'second(s)'
    elif minute_threshold <= ms < hour_threshold:
        s = ms / (milliseconds_in_a_second * seconds_in_a_minute), 'minute(s)'
    elif hour_threshold <= ms < day_threshold:
        s = ms / (milliseconds_in_a_second * seconds_in_a_minute * minutes_in_an_hour), 'hour(s)'
    elif day_threshold <= ms < week_threshold:
        s = ms / (milliseconds_in_a_second * seconds_in_a_minute * minutes_in_an_hour * hours_in_a_day), 'day(s)'
    else:
        s = ms / (milliseconds_in_a_second *
                  seconds_in_a_minute *
                  minutes_in_an_hour * hours_in_a_day * days_in_a_week), 'week(s)'

    if include_terminal_comma:
        comma = ','
    else:
        comma = ''
    phrase = ''
    if ms == 1:
        phrase = '1 millisecond'
    elif ms == s[0]:
        phrase = '{} milliseconds'.format(ms)
    else:
        phrase = '{} milliseconds, or about {:.2g} {}{}'.format(ms, s[0], s[1], comma)


    return phrase




# given the workload, this will give the maximum absolute deviation from the mean
def get_max_absolute_deviation_from_ref(
        csv_file='combined_results_revised.csv',
        wl='a',
        list_of_number_of_nodes=None,
        csv_reference_data_file='abramova_results.csv',
        measurement_of_interest = '[OVERALL] RunTime(ms)',
        d=None,
        d_ref=None,
        t_range=None,
        node_type='rp',
        nm='eth'
                                                   ):

    # Initialize Variables----------------------------
    if not list_of_number_of_nodes:
        list_of_number_of_nodes = [1, 3, 6]

    if not t_range:
        t_range=range(10, 30+1)

    if not d:
        d={'nt': node_type,
           'wl': wl,
           'nn': 1,
           't': t_range,
           'nm': nm}

    if not d_ref:
        d_ref = d
    # ------------------------------------------------

    # Read from CSV File -----------------------------

    df = pd.read_csv(csv_file)
    df_ref = pd.read_csv(csv_reference_data_file)

    # ------------------------------------------------

    #  For each node, get the max's and min's
    bound_dict = {}
    for node_count in list_of_number_of_nodes:
        d['nn'] = node_count  # adjust the filter(s)
        d_ref['nn'] = node_count

        df_flt = rfd(df, d)
        df_ref_flt = rfd(df_ref, d_ref)

        df_summary = df_flt.describe()
        df_ref_summary = df_ref_flt.describe()

        max_ = df_summary[measurement_of_interest]['max']
        min_ = df_summary[measurement_of_interest]['min']

        max_ref = df_ref_summary[measurement_of_interest]['max']
        min_ref = df_ref_summary[measurement_of_interest]['min']

        bound_dict[node_count] = max(abs(max_-min_ref), abs(min_-max_ref))  # assumes one mean is always greater

    bound = max(bound_dict.values())

    return bound


def generate_paragraph_for_workload(wl='a'):

    filter_reference ={'nm': 'unk',
                        'nt': 'ref',
                        'wl': wl,
                        }

    filter_rp_eth_lan ={'nm': 'eth',
                        'nt': 'rp',
                        'wl': wl,
                        't': range(10, 30+1)
                        }

    filter_rp_w_lan ={'nm': 'wlan',
                        'nt': 'rp',
                        'wl': wl,
                        't': range(10, 30+1)
                        }

    count_of_trials = len(filter_rp_eth_lan['t'])

    max_absolute_deviation_from_ref = get_max_absolute_deviation_from_ref(
                                                            csv_file='combined_results_revised.csv',
                                                            wl=wl,
                                                            list_of_number_of_nodes=[1, 3, 6],
                                                            csv_reference_data_file='abramova_results.csv',
                                                            measurement_of_interest = '[OVERALL] RunTime(ms)',
                                                            t_range=None,
                                                            d=filter_rp_eth_lan,
                                                            d_ref=filter_reference,
                                                            node_type='rp',
                                                            nm='eth',

                                                   )
    standard_deviation_from_ref = 0
    max_absolute_deviation_between_wired_and_wireless = get_max_absolute_deviation_from_ref(
                                                            csv_file='combined_results_revised.csv',
                                                            wl=wl,
                                                            csv_reference_data_file='combined_results_revised.csv',
                                                            measurement_of_interest = '[OVERALL] RunTime(ms)',
                                                            d=filter_rp_w_lan,
                                                            d_ref=filter_rp_eth_lan,
                                                            t_range=None,
                                                            node_type='rp',
                                                            nm='eth',
                                                            list_of_number_of_nodes=[1, 2, 3, 4, 5, 6]
                                                   )
    standard_deviation_between_wired_and_wireless = 0

    header = '\paragraph{Research Question ' + str(associated_research_question(wl)) + '}'
    s = header + '\n\n' + \
        'For {} trials, each consisting of 10,000 operations of workload {} ({}) ' \
        ' and performed over 1, 3, and 6-node configurations, ' \
        'the greatest absolute deviation from the reference to the Raspberry Pi configuration was found to be {}. ' \
        'Second, for 10,000 operations of this workload and' \
        ' over 1, 2, 3, 4, 5, and 6-node configurations, the greatest absolute deviation from any given ' \
        ' trial in the wired configuration to an analogous trial using wireless configuration was found to be {}. ' \
        'Third, using this workload and the one-way ANOVA test, ' \
        'it was determined with 95 percent confidence that varying the memory of a device does not necessarily ' \
        'imply a differential in performance.' \
        ''.format(count_of_trials,
                  wl.capitalize(), ycsb_workload_description(wl),
                  display_appropriate_interval_from_ms(max_absolute_deviation_from_ref),
                  display_appropriate_interval_from_ms(max_absolute_deviation_between_wired_and_wireless))

    return s

def ycsb_workload_description(workload):
    d = {'a': '50 percent reads and 50 percent updates',
         'c': '100 percent reads',
         'e': '100 percent scans',
         'i': '99 percent inserts, 1 percent reads'}
    return d[workload]

def associated_research_question(workload):
    d = {'a': 1,
         'c': 2,
         'e': 3,
         'i': 4}
    return d[workload]

def generate_all_paragraphs():
    x = ''
    for i in ['a', 'c', 'e', 'i']:
        x += generate_paragraph_for_workload(wl=i)
        x += '\n\n'

    return x

def string_to_latex(s):
    ss = s.replace('%', '\%')
    return ss
