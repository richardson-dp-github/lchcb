import research_questions_analysis
import pandas as pd
from graph_utility import return_filtered_dataframe as rfd
from research_questions_analysis import *
from scratch5 import ram_vs_ram, \
    raspberry_pi_versus_virtual_machine, wireless_links_only, \
    wireless_links_versus_wired


def return_standardized_label(figure_id=0,
                              workload='a'):

    return 'figures-wl{workload}_fig{figure_id}'.format(workload=workload, figure_id=figure_id)


def latex_reference(label):
    return r'\ref{' + label + '}'


def decode_abbreviation_from_data_for_narrative(code):
    d = {
        'rp': 'limited hardware, Raspberry Pi',
        'vm': 'virtual machine',
        'eth': 'Ethernet',
        'wlan': '802.11a/b/g/n',
        'nodal': 'nodal'
    }

    return d[code]



def there_exists_comparison_data(workload):
    if workload in ['a', 'c', 'e']:
        return True
    else:
        return False


# Display format
# Even though this is one line, it was written for convenience
def set_display_format_for_floats(format_='{:.2g}'.format):
    pd.options.display.float_format = format_
    return 0


# This function absorbs the responsibility of spacing out the tables
def return_embedded_latex_tables(latex_table_as_string='',
                                 label='',
                                 caption=''):
    xx = ''

    x = ''
    x += r'\begin{table}[h!]' + '\n'
    x += latex_table_as_string

    x += '\caption{' + caption + '}' + '\n'
    x += '\label{table:' + label + '}' + '\n'
    x += '\end{table}' + '\n'

    xx += x
    return xx




def return_desired_summary_statistics_table(
                                            csv_file='combined_results_revised.csv',
                                            measurement_of_interest = '[OVERALL] RunTime(ms)',
                                            wl='a',
                                            nt='rp',
                                            nm='eth',
                                            ram='1GB'):

    caption = 'Summary Statistics for Workload {workload} performed on a {ram} {nt} node over a(n)' \
              '{nm} network.  Except for count, ' \
              'all values are in milliseconds.' \
              ''.format(workload=wl.capitalize(),
                        nt=decode_abbreviation_from_data_for_narrative(nt),
                        nm=decode_abbreviation_from_data_for_narrative(nm),
                        ram=ram)

    label = 'summary_table_{wl}_{ram}_{nt}_{nm}'.format(wl=wl,
                                                        ram=ram,
                                                        nt=nt,
                                                        nm=nm)

    x = return_summary_statistics_tabular(workload=wl,
                                          nt=nt,
                                          ram=ram,
                                          nm=nm,
                                          csv_file=csv_file,
                                          measurement_of_interest=measurement_of_interest)

    xx = return_embedded_latex_tables(latex_table_as_string=x,
                                      label=label,
                                      caption=caption)

    return xx


def insert_summary_statistics_table(comparison_description, workload):

    rest_of_vms = ''

    if workload in ['i']:
        x = ['1GB', '2GB', '4GB']
    else:
        x = ['1GB', '4GB']

    for i in x:
        rest_of_vms += return_desired_summary_statistics_table(
                                            csv_file='combined_results_revised.csv',
                                            measurement_of_interest = '[OVERALL] RunTime(ms)',
                                            wl=workload,
                                            nt='vm',
                                            nm='nodal',
                                            ram=i)
        rest_of_vms += '\n'

    d = {
        'vm_v_ref': return_desired_summary_statistics_table(
                                            csv_file='combined_results_revised.csv',
                                            measurement_of_interest = '[OVERALL] RunTime(ms)',
                                            wl=workload,
                                            nt='vm',
                                            nm='nodal',
                                            ram='2GB'),
        'ram_v_ram': rest_of_vms,
        'rp_only': return_desired_summary_statistics_table(
                                            csv_file='combined_results_revised.csv',
                                            measurement_of_interest = '[OVERALL] RunTime(ms)',
                                            wl=workload,
                                            nt='rp',
                                            nm='eth',
                                            ram='1GB'),
        'wlan_only': return_desired_summary_statistics_table(
                                            csv_file='combined_results_revised.csv',
                                            measurement_of_interest = '[OVERALL] RunTime(ms)',
                                            wl=workload,
                                            nt='rp',
                                            nm='wlan',
                                            ram='1GB'),
        'rp_v_ref': '',
        'rp_v_vm': '',
        'wlan_v_eth': ''
    }

    return d[comparison_description]


# This will be just a dictionary with the text of all initial observations.
def initial_observations_text(comparison_description, workload):

    initial_observations_dict = {
        'vm_v_ref': {
            'a': r'The result medians are displayed in Figure \ref{figures-wla_fig5}.  '
                 r'As expected, the virtual machine results imply much, much less execution time '
                 r'compared to the reference value, presumably accounting for diminished network '
                 r'latency. '
                 r'Such network latency seems to have an increasing effect on the reference as the cluster '
                 r'size goes up, '
                 r'but further analysis would be required to even make this claim. ',
            'c': r'The result medians are displayed in Figure \ref{figures-wlc_fig5}.  '
                 r'As expected, the virtual machine results imply much, much less execution time '
                 r'compared to the reference value, presumably accounting for diminished network '
                 r'latency. '
                 r'Such network latency seems to have an increasing effect on the reference as the cluster '
                 r'size goes up, '
                 r'but further analysis would be required to even make this claim. ',
            'e': r'The result medians are displayed in Figure \ref{figures-wle_fig5}.  '
                 r'As expected, the virtual machine results imply much, much less execution time '
                 r'compared to the reference value, presumably accounting for diminished network '
                 r'latency. '
                 r'For the reference value, it seems a higher cluster size seems to imply a cost, but a cost that '
                 r'decreases as the cluster size increases. '
                 r'However,  further analysis would be required to see if this is not just the product of '
                 r'normal variation.  '
                 r'Because of the high contrast, it difficult to reach any initial predictions for virtual machine.  '
                 r'The flat curve may just be an illusion, a minimization of the differences due to the scale of the '
                 r'graph.  ',
            'i': r'Because workload I was conceived in this paper, there is no outside reference at this time.  '
        },
        'ram_v_ram': {
            'a': r'This section discusses testing and performance for memory sizes: 1GB, 2GB, and 4GB.  '
                 r'The results are displayed in Figure \ref{figures-wla_fig4}. '
                 r'While it appears the varying the amount of memory has some effect on the results, there '
                 r'does not seem to be a predictable pattern across nodes. '
                 r'An ANOVA test will determine if there is an effect, and a linear regression will further test'
                 r'for an effect. ',
            'c': r'This section discusses testing and performance for memory sizes: 1GB, 2GB, and 4GB.  '
                 r'The results are displayed in Figure \ref{figures-wlc_fig4}. '
                 r'While it appears the varying the amount of memory has some effect on the results, there '
                 r'does not seem to be a predictable pattern across nodes. '
                 r'An ANOVA test will determine if there is an effect, and a linear regression will further test '
                 r'for an effect. ',
            'e': r'The results are displayed in Figure \ref{figures-wle_fig4}.  '
                 r'First of all, the performance for the a one-node cluster differs significantly between 1GB RAM and '
                 r'all other cases.  '
                 r'While this could be some kind of implementation error, it is best not to draw any conclusions from '
                 r'this. '
                 r'It would be best to run these tests again, possibly switching the order to eliminate the possible '
                 r'effect of interference or a mix-up of data. '
                 r'That one case aside, the amount of RAM seems to have had an effect on the results, but there does '
                 r'not seem to be any predictive relationship that holds true across cluster sizes. ',
            'i': r'The results are displayed in Figure \ref{figures-wli_fig4}. '
                 r'Here there is a visible trend of 4GB RAM implying better performance results '
                 r'than both 1GB RAM and 2GB RAM.  '
                 r'However, the relationship between 1GB RAM and 2GB RAM does not seem to be '
                 r' predictable across cluster node sizes. '
        },
        'rp_only': {
            'a': r'The results are displayed in Figure \ref{figures-wla_fig10}.  ',
            'c': r'The results are displayed in Figure \ref{figures-wlc_fig10}.  ',
            'e': r'The results are displayed in Figure \ref{figures-wle_fig10}.  ',
            'i': r'The results are displayed in Figure \ref{figures-wli_fig10}.  '
        },
        'rp_v_ref': {
            'a': r'The results are displayed in Figure \ref{figures-wla_fig6}.  '
                 r'The performance of the limited hardware, the Raspberry Pi, seems comparable with the '
                 r'results from the more appropriate in the other paper.  '
                 r'In addition, there is no reason to suspect a significant differential in the overall pattern '
                 r'with respect to scalability: performance over cluster size. ',
            'c': r'The results are displayed in Figure \ref{figures-wlc_fig6}.  '
                 r'The performance of the limited hardware, the Raspberry Pi, seems comparable with the '
                 r'results from the more appropriate in the other paper. '
                 r'In addition, there is no reason to suspect a significant differential in the overall pattern '
                 r'with respect to scalability: performance over cluster size. ',
            'e': r'The results are displayed in Figure \ref{figures-wle_fig6}.  '
                 r'These medians seem to indicate, that for this workload, any effect of the Raspberry Pi is '
                 r'exacerbated with this particular workload. ',
            'i': r'Because workload I was conceived in this paper, there is no outside reference at this time.  '
        },
        'rp_v_vm': {
            'a': r'The results are displayed in Figure \ref{figures-wla_fig6}.  '
                 r'As expected, there is a significant differential between the limited hardware, the Raspberry Pi '
                 r'configuration and the virtual machine.  However, it is not clear if this is linear across cluster '
                 r'size. '
                 r'',
            'c': r'The results are displayed in Figure \ref{figures-wlc_fig6}.  '
                 r'As expected, there is a significant differential between the limited hardware, the Raspberry Pi '
                 r'configuration and the virtual machine.  However, it is not clear if this is linear across cluster '
                 r'size. '
                 r'',
            'e': r'The results are displayed in Figure \ref{figures-wle_fig6}.  '
                 r'As expected, there is a significant differential between the limited hardware, the Raspberry Pi '
                 r'configuration and the virtual machine.  However, it is not clear if this is linear across cluster '
                 r'size. '
                 r'',
            'i': r'The results are displayed in Figure \ref{figures-wli_fig6}.  '
                 r'As expected, there is a significant differential between the limited hardware, the Raspberry Pi '
                 r'configuration and the virtual machine.  However, it is not clear if this is linear across cluster '
                 r'size. '
                 r''
        },
        'wlan_only': {
            'a': r'The results are displayed in Figure \ref{figures-wla_fig8}.  '
                 r'Although there is a general trend of increased execution time over cluster size,'
                 r' the oscillation that occurs between odd and '
                 r'even node cluster sizes is hard to miss. '
                 r'This may be result of the collision avoidance strategy, but further experiments would be '
                 r'needed to determine a more specific explanation. ',
            'c': r'The results are displayed in Figure \ref{figures-wlc_fig8}.  '
                 r'Although there is a general trend of increased execution time over cluster size,'
                 r' the oscillation that occurs between odd and '
                 r'even node cluster sizes is hard to miss. '
                 r'This may be result of the collision avoidance strategy, but further experiments would be '
                 r'needed to determine a more specific explanation. ',
            'e': r'The results are displayed in Figure \ref{figures-wle_fig8}.  '
                 r'Although there is a general trend of increased execution time over cluster size,'
                 r' the oscillation that occurs between odd and '
                 r'even node cluster sizes is hard to miss. '
                 r'This may be result of the collision avoidance strategy, but further experiments would be '
                 r'needed to determine a more specific explanation. ',
            'i': r'The results are displayed in Figure \ref{figures-wli_fig8}.  '
                 r'There does not seem to be the oscillation that there was in the other workloads, which seems to '
                 r'suggest that somehow the reads and scans that dominate the other workloads are somehow correlated '
                 r'with the oscillation previously observed. '
                 r'Furthermore, this would seem to suggest that Workload I or any similar workload could be used as '
                 r'a control in such an experiment to further investigate the source of the oscillation observed in'
                 r' other, more read-heavy workloads.   '
                 r'As far as the general trend, the results depicted here seem to suggest that at from 3-node clusters '
                 r'on, there seems to be an diminishing increase in execution time as the node cluster increases.  '
        },
        'wlan_v_eth': {
            'a': r'The results are displayed in Figures \ref{figures-wla_fig7} and \ref{figures-wla_fig9}.  '
                 r'For 1, 2, and 3-node clusters, despite the expected  disparity in execution time, '
                 r'the wired and wireless trends seem to follow each other.  '
                 r'However, from 3 nodes up through 6 nodes, the execution times starts to diverge, suggesting that '
                 r'the wireless has a increasing effect as the number of nodes increases. ',
            'c': r'The results are displayed in Figures \ref{figures-wlc_fig7} and \ref{figures-wlc_fig9}.  '
                 r'For 1, 2, and 3-node clusters, despite the expected  disparity in execution time, '
                 r'the wired and wireless trends seem to follow each other.  '
                 r'However, from 3 nodes up through 6 nodes, the execution times starts to diverge, suggesting that '
                 r'the wireless has a increasing effect as the number of nodes increases. ',
            'e': r'The results are displayed in Figures \ref{figures-wle_fig7} and \ref{figures-wle_fig9}.  '
                 r'For 1, 2, and 3-node clusters, despite the expected  disparity in execution time, '
                 r'the wired and wireless trends seem to follow each other.  '
                 r'However, from 3 nodes up through 6 nodes, the execution times starts to diverge, suggesting that '
                 r'the wireless has a increasing effect as the number of nodes increases. ',
            'i': r'The results are displayed in Figures \ref{figures-wli_fig7} and \ref{figures-wli_fig9}.  '
                 r'For 1, 2, and 3-node clusters, despite the expected  disparity in execution time, '
                 r'the wired and wireless trends seem to follow each other.  '
                 r'However, from 3 nodes up through 6 nodes, the execution times starts to diverge, suggesting that '
                 r'the wireless has a increasing effect as the number of nodes increases. '
        }

    }

    return initial_observations_dict[comparison_description][workload]


# This will be just a dictionary with the text of all initial observations.
def get_caption(figure_id, workload):

    figure_1_caption = r'This scatterplot compares the values from \cite{Abramova2014TestingCassandra} to the median result of the workload executed on the virtual machine.'
    figure_4_caption = r'Execution time for virtual machines with 1GB, 2GB, and 4GB of \gls{ram}.  The first 9 trials have been removed in order to filter out the trials representing cache effect and thus represents the steady state.'
    figure_5_caption = r'This compares the 2GB virtual machine with the corresponding value from \cite{Abramova2014TestingCassandra}.'
    figure_9_caption = r'Standard deviation of execution time in milliseconds.  There is a significant increase when going from the wired to the wireless configuration.'
    figure_6_caption = r'Comparison among the Raspberry Pi nodes (rp-1GB), the results reported in \cite{Abramova2014TestingCassandra}, and the virtual nodes with 1GB of \gls{ram}.'
    figure_7_caption = r'Comparison between links: Ethernet wired versus 802.11 wireless.  As the cluster sizes increase, these show a tendency to diverge.'
    figure_8_caption = r'Results of wireless testing.  There seems to be a steady climb in execution time as the cluster size increases.  Any oscillation cannot be explained with current analysis and would require additional experimentation.'
    figure_10_caption = r'Results of limited hardware, the Raspberry Pi, on an Ethernet \gls{lan}.  Execution time is plotted over cluster size.'

    caption_dict = {
        1: {
            'a': figure_1_caption,
            'c': figure_1_caption,
            'e': figure_1_caption,
            'i': figure_1_caption
        },
        4: {
            'a': figure_4_caption,
            'c': figure_4_caption,
            'e': figure_4_caption,
            'i': figure_4_caption
        },
        5: {
            'a': figure_5_caption,
            'c': figure_5_caption,
            'e': figure_5_caption,
            'i': figure_5_caption
        },
        6: {
            'a': figure_6_caption,
            'c': figure_6_caption,
            'e': figure_6_caption,
            'i': figure_6_caption
        },
        7: {
            'a': figure_7_caption,
            'c': figure_7_caption,
            'e': figure_7_caption,
            'i': figure_7_caption
        },
        8: {
            'a': figure_8_caption,
            'c': figure_8_caption,
            'e': figure_8_caption,
            'i': figure_8_caption
        },
        9: {
            'a': figure_9_caption,
            'c': figure_9_caption,
            'e': figure_9_caption,
            'i': figure_9_caption
        },
        10: {
            'a': figure_10_caption,
            'c': figure_10_caption,
            'e': figure_10_caption,
            'i': figure_10_caption
        }

    }

    return caption_dict[figure_id][workload]


def ordinal_analysis_text(comparison_type):

    s = []

    if 'ref' in comparison_type:

        s[0] = 'For {} out of {} node cases, the reference value value from \cite{} falls within the range of the values. '
        s[1] = 'For those that did fall, they fell within the 75/25 percentile range. '
        s[2] = 'This seems to suggest that the operation of the Raspberry Pi in this context is similar to that of a more' \
               'capable node. '



    return s


def averages_and_variances_analysis():

    s = []

    return s


def get_titles(comparison_type):
    titles_dict = {
        'vm_v_ref': 'Comparing Existing Work: Virtual Machine vs the Reference Value',
        'ram_v_ram': '1GB RAM vs 2GB RAM vs 4GB RAM',
        'rp_only': 'Implementation on Raspberry Pi',
        'rp_v_ref': 'Raspberry Pi vs Reference Value',
        'rp_v_vm': 'Raspberry Pi vs Virtual Machine',
        'wlan_only': 'Wireless Links Only',
        'wlan_v_eth': 'Wireless Links vs Wired Links'
    }

    return titles_dict[comparison_type]


# Assume the figures are already generated, this generates the text that points to them.
def insert_figures(comparison_type, workload, width=5.5):
    figures_dict = {
        'vm_v_ref': [1, 5],
        'ram_v_ram': [4],
        'rp_only': [10],
        'rp_v_ref': [6],
        'rp_v_vm': [],
        'wlan_only': [8],
        'wlan_v_eth': [7, 9]
    }

    text = ''

    reference_labels = []

    for figure_id in figures_dict[comparison_type]:

        name_of_figure = 'figures-wl{workload}_fig{figure_id}.pdf'.format(workload=workload, figure_id=figure_id)
        label_for_figure = 'figures-wl{workload}_fig{figure_id}'.format(workload=workload, figure_id=figure_id)
        caption = get_caption(figure_id=figure_id, workload=workload)

        text += r'\begin{figure}[h!]' + '\n' \
                r'\includegraphics[width=' + str(width) + r'in]{Figures/' + name_of_figure + r'}' + '\n' \
                r'\caption{' + caption + r'}' + '\n' \
                r'\label{' + label_for_figure + r'}' + '\n' \
                r'\end{figure}' + '\n' + '\n'

        reference_labels.append(label_for_figure)

    return text


# This function returns the sentences that refer to the tables.  It is important that they be standardized and without
# flaws in every instantiation.  They will be repeated often, so it is best just to insert them as a function.
def get_sentences_to_refer_to_appropriate_summary_tables(comparison_description, workload):
    s = '\n'
    if 'vm' in comparison_description or 'ram' in comparison_description:
        s += 'The summary statistics for Workload {workload} performed on the virtual machines ' \
             'are in Tables {ref_1gb}, {ref_2gb}, and {ref_4gb}.' \
             ''.format(workload=workload.capitalize(),
                       ref_1gb='\\ref{{{}}}'.format('table:summary_table_{wl}_{ram}_{nt}_{nm}'.format(wl=workload,
                                                                                               ram='1GB',
                                                                                               nt='vm',
                                                                                               nm='nodal')),
                       ref_2gb='\\ref{{{}}}'.format('table:summary_table_{wl}_{ram}_{nt}_{nm}'.format(wl=workload,
                                                                                               ram='2GB',
                                                                                               nt='vm',
                                                                                               nm='nodal')),
                       ref_4gb='\\ref{{{}}}'.format('table:summary_table_{wl}_{ram}_{nt}_{nm}'.format(wl=workload,
                                                                                               ram='4GB',
                                                                                               nt='vm',
                                                                                               nm='nodal'))
                       )
        s += '\n'
    if 'rp' in comparison_description or 'eth' in comparison_description:
        s += 'The summary statistics for Workload {workload} performed on the limited hardware, ' \
             'Raspberry Pi, on the Ethernet local area network ' \
             'are in Table {ref_rp_eth}.' \
             ''.format(workload=workload.capitalize(),
                       ref_rp_eth='\\ref{{{}}}'.format('table:summary_table_{wl}_{ram}_{nt}_{nm}'.format(wl=workload,
                                                                                    ram='1GB',
                                                                                    nt='rp',
                                                                                    nm='eth')))
        s += '\n'
    if 'wlan' in comparison_description:
        s += 'The summary statistics for Workload {workload} performed on the limited hardware, ' \
             'Raspberry Pi, on the Ethernet local area network ' \
             'are in Table {ref_wlan}.' \
             ''.format(workload=workload.capitalize(),
                       ref_wlan='\\ref{{{}}}'.format('table:summary_table_{wl}_{ram}_{nt}_{nm}'.format(wl=workload,
                                                                                                ram='1GB',
                                                                                                nt='rp',
                                                                                                nm='wlan')))
        s += '\n'

    return s


def get_observations_paragraph_for_individual(cluster_sizes=None,
                                              df_summary=None,
                                              df_ref=None,
                                              measurement_of_interest='[OVERALL] RunTime(ms)',
                                              workload='a'):

    s = ''

    if not cluster_sizes:
        cluster_sizes = [1, 3, 6]

    for cluster_size in cluster_sizes:
        nn = cluster_size
        wl = workload
        max_dif= df_summary[nn].loc['max']
        min_dif= df_summary[nn].loc['min']
        med_dif= df_summary[nn].loc['50%']
        s += 'For a node cluster size of {cluster_size}, ' \
             'the median execution time was {med_dif}, and ' \
             'all execution times fell within {min_dif} and {max_dif}, inclusive.  ' \
             ''.format(cluster_size=cluster_size,
                       max_dif=display_appropriate_interval_from_ms(max_dif, include_terminal_comma=False),
                       min_dif=display_appropriate_interval_from_ms(min_dif),
                       med_dif=display_appropriate_interval_from_ms(med_dif, include_terminal_comma=False))

    nn = 'OVERALL'
    max_dif= df_summary[nn].loc['max']
    min_dif= df_summary[nn].loc['min']
    med_dif= df_summary[nn].loc['50%']
    s += 'Overall, ' \
         'the median execution time was {med_dif}, and all execution times fell within {min_dif} and {max_dif}.  \n' \
         ''.format(cluster_size=cluster_size,
                       max_dif=display_appropriate_interval_from_ms(max_dif, include_terminal_comma=False),
                       min_dif=display_appropriate_interval_from_ms(min_dif),
                       med_dif=display_appropriate_interval_from_ms(med_dif, include_terminal_comma=False))

    return s


def implementation_on_raspberry_pi(workload):

    s = '\n'

    # s += 'In a similar fashion, the tests were run on the Raspberry Pi to observe performance. ' \
    #     'The spread of each of the tests can be seen in Figure 23 and Table 17. ' \
    #     'The results can be seen in Figure 37. ' \
    #     '\n\n' \
    #     'As can be seen from Figure 37, the Raspberry Pi configuration takes considerably more execution time ' \
    #     'than its virtual machine analogy, which is probably due to the physical nature of the links, and the ' \
    #     'router acting as an intermediary as well as the limitations of the Raspberry Pi hardware. ' \
    #     'However, it is worth noting that its analogy in [?] exhibits similar performance. ' \
    #     '\n\n'

    s = '\n\n'

    figure_insert = insert_figures(comparison_type='rp_only', workload=workload)

    s += figure_insert
    s += 'This section summarizes the results from running Workload {workload} on Raspberry Pi clusters networked ' \
         'via an Ethernet LAN.  ' \
         ''.format(workload=workload)
    ref_to_figure = 'The results are depicted in Figure {}. '.format(latex_reference(return_standardized_label(
        figure_id=10,
        workload=workload)))

    s += ref_to_figure

    label_for_assignment = 'rp_only_wl{}'.format(workload)
    label_for_reference = '\\ref{{{}}}'.format('table:{}'.format(label_for_assignment))
    reference_to_paper = r'\cite{Abramova2014TestingCassandra}'
    desired_index=['nn', 'wl', 'dbs', 't']
    measurement_of_interest='[OVERALL] RunTime(ms)'
    label_for_new_column='rp_on_eth'
    df = return_df_that_includes_differences(main_csv_file='combined_results_revised.csv',
                                             reference_csv_file='abramova_results.csv',
                                             trial_list=None,
                                             measurement_of_interest=measurement_of_interest,
                                             desired_index=None,
                                             desired_columns=None,
                                             filter_for_nominator=['rp', 'eth', '1GB'],
                                             filter_for_denominator=['ref', 'unk', '2GB'],
                                             label_for_new_column=label_for_new_column)

    df = return_general_summary_table(desired_index=desired_index,
                                      reference_csv_file=None)

    df = pd.DataFrame(df['rp', 'eth', '1GB'].rename(label_for_new_column))

    df = get_summary_table(df=df,
                           label_for_new_column=label_for_new_column,
                           nn=[1, 2, 3, 4, 5, 6],
                           wl=workload)

    s += get_observations_paragraph_for_individual(cluster_sizes=[1, 2, 3, 4, 5, 6],
                                                  df_summary=df,
                                                  df_ref=return_reference_data_frame(),
                                                  measurement_of_interest='[OVERALL] RunTime(ms)',
                                                  workload=workload)

    insert_table = return_embedded_latex_tables(latex_table_as_string=df.to_latex(),
                                                label=label_for_assignment,
                                                caption='Summary of Workload {workload} '
                                                        'executed on Raspberry Pi clusters on an Ethernet LAN '
                                                        ''
                                                        ''.format(workload=workload))

    s += insert_table

    s += 'The full summary of the differences are reported in Table {}.  '.format(label_for_reference)




    s += '\n\n'




    # for cluster_size in [1, 3, 6]:
    #     s += 'For a node network of {cluster_size}, ' \
    #         'the experimental values fell between {} and {}, inclusive, and all values fell ' \
    #         'within {} of the reference value {}.  ' \
    #         ''.format(cluster_size=cluster_size)

    return s


def raspberry_pi_versus_reference_value(workload):
    s = '\n\n'

    figure_insert = insert_figures(comparison_type='rp_v_ref', workload=workload)

    s += figure_insert

    ref_to_figure = 'The results are depicted in Figure {}. '.format(latex_reference(return_standardized_label(
        figure_id=6,
        workload=workload)))

    s += 'It is of interest to compare the performance of the Raspberry Pi to that of the reported value. '

    s += ref_to_figure

    label_for_assignment = 'abs_diffs_rp_ref_wl{}'.format(workload)
    label_for_reference = '\\ref{{{}}}'.format('table:{}'.format(label_for_assignment))
    reference_to_paper = r'\cite{Abramova2014TestingCassandra}'

    measurement_of_interest='[OVERALL] RunTime(ms)'
    label_for_new_column='dif_from_ref'
    df = return_df_that_includes_differences(main_csv_file='combined_results_revised.csv',
                                             reference_csv_file='abramova_results.csv',
                                             trial_list=None,
                                             measurement_of_interest=measurement_of_interest,
                                             desired_index=None,
                                             desired_columns=None,
                                             filter_for_nominator=['rp', 'eth', '1GB'],
                                             filter_for_denominator=['ref', 'unk', '2GB'],
                                             label_for_new_column=label_for_new_column)

    df = get_summary_table(df=df,
                           label_for_new_column=label_for_new_column,
                           nn=[1, 3, 6],
                           wl=workload)

    s += get_observations_paragraph_for_reference(cluster_sizes=[1, 3, 6],
                                                  df_summary_of_differentials=df,
                                                  df_ref=return_reference_data_frame(),
                                                  measurement_of_interest='[OVERALL] RunTime(ms)',
                                                  workload=workload)

    insert_table = return_embedded_latex_tables(latex_table_as_string=df.to_latex(),
                                                label=label_for_assignment,
                                                caption='Summary of the absolute value of the differences '
                                                        'between the empirical execution'
                                                        ' time on the Raspberry Pi clusters '
                                                        'and the corresponding execution time reported in {}'
                                                        ''.format(reference_to_paper))

    s += insert_table

    s += 'The full summary of the differences are reported in Table {}.  '.format(label_for_reference)




    s += '\n\n'



    return s

def comparing_existing_work_vm_versus_ref_val(workload):
    s = '\n\n'

    figure_insert = insert_figures(comparison_type='vm_v_ref', workload=workload)

    s += figure_insert

    ref_to_figure = 'The results are depicted in Figure {}. '.format(latex_reference(return_standardized_label(
        figure_id=5,
        workload=workload)))

    s += 'It is of interest to compare the performance of the virtual machine to that of the reported value. '

    s += ref_to_figure

    label_for_assignment = 'abs_diffs_vm_ref_wl{}'.format(workload)
    label_for_reference = '\\ref{{{}}}'.format('table:{}'.format(label_for_assignment))
    reference_to_paper = r'\cite{Abramova2014TestingCassandra}'

    measurement_of_interest='[OVERALL] RunTime(ms)'
    label_for_new_column='dif_from_ref'
    df = return_df_that_includes_differences(main_csv_file='combined_results_revised.csv',
                                             reference_csv_file='abramova_results.csv',
                                             trial_list=None,
                                             measurement_of_interest=measurement_of_interest,
                                             desired_index=None,
                                             desired_columns=None,
                                             filter_for_nominator=['vm', 'nodal', '2GB'],
                                             filter_for_denominator=['ref', 'unk', '2GB'],
                                             label_for_new_column=label_for_new_column)

    df = get_summary_table(df=df,
                           label_for_new_column=label_for_new_column,
                           nn=[1, 3, 6],
                           wl=workload)

    s += get_observations_paragraph_for_reference(cluster_sizes=[1, 3, 6],
                                                  df_summary_of_differentials=df,
                                                  df_ref=return_reference_data_frame(),
                                                  measurement_of_interest='[OVERALL] RunTime(ms)',
                                                  workload=workload)

    insert_table = return_embedded_latex_tables(latex_table_as_string=df.to_latex(),
                                                label=label_for_assignment,
                                                caption='Summary of the absolute value of the differences '
                                                        'between the empirical execution'
                                                        ' time on the Virtual Machine clusters '
                                                        'and the corresponding execution time reported in {}'
                                                        ''.format(reference_to_paper))

    s += insert_table

    s += 'The full summary of the differences are reported in Table {}.  '.format(label_for_reference)




    s += '\n\n'



    return s

def update_initial_observation(comparison_type, workload):
    s = '\n'
    s += r'\subsubsection{Initial Observations}'
    s += '\n'
    s += initial_observations_text(comparison_type, workload)
    s += insert_figures(comparison_type=comparison_type, workload=workload)

    return s


def update_analysis(comparison_description, workload):

    s = '\n'
    s += r'\subsubsection{Analysis}'
    s += '\n'
    s += 'This section will take a more in-depth look at the data.'
    s += '\n'
    s += speedup_analysis_tables(comparison_description=comparison_description,
                                 workload=workload,
                                 csv_file='combined_results_revised.csv')
    s += '\n'

    if 'ref' in comparison_description:
        s = '\n\n'

    return s


def update_ordinal_statistics(comparison_type, workload):

    s = '\n'
    s += r'\subsubsection{Ordinal Statistics}'
    s += '\n'
    s += r'This section will describe some of the summary statistics that describe the data.  '
    s += '\n'
    s += get_sentences_to_refer_to_appropriate_summary_tables(comparison_description=comparison_type, workload=workload)
    s += insert_summary_statistics_table(comparison_description=comparison_type, workload=workload)

    s += '\n'

    return s


def return_single_results_section(workload):

    s = r'\section{Results for Workload ' + '{}'.format(workload.capitalize()) + r'}'
    s += '\n'
    if there_exists_comparison_data(workload=workload):
        subsections = ['vm_v_ref','ram_v_ram','rp_only','rp_v_ref','rp_v_vm','wlan_only','wlan_v_eth']
    else:
        subsections = ['ram_v_ram','rp_only','rp_v_vm','wlan_only','wlan_v_eth']
    for i in subsections:
        s += r'\subsection{' + get_titles(comparison_type=i) + '}'
        if i in ['vm_v_ref']:
            s += comparing_existing_work_vm_versus_ref_val(workload=workload)
        elif i in ['rp_only']:
            s += implementation_on_raspberry_pi(workload=workload)
        elif i in ['wlan_v_eth']:
            s += wireless_links_versus_wired(workload=workload)
        elif i in ['ram_v_ram']:
            s += ram_vs_ram(workload=workload)
        elif i in ['rp_v_vm']:
            s += raspberry_pi_versus_virtual_machine(workload=workload)
        elif i in ['rp_v_ref']:
            s += raspberry_pi_versus_reference_value(workload=workload)
        elif i in ['wlan_only']:
            s += wireless_links_only(workload=workload)

        else:
            s += update_initial_observation(workload=workload, comparison_type=i)
            s += '\n'
            s += update_ordinal_statistics(comparison_type=i, workload=workload)
            s += '\n'
            s += update_analysis(comparison_description=i, workload=workload)
            s += '\n'


    return s


def return_entire_results_section():

    s = '\n\n'
    s += r'\chapter{Results and Evaluation}'
    s += '\n'
    s += r'\label{results}'
    s += '\n\n'
    s += r'\section{Introduction and Overview}'
    s += '\n'
    s += r'This section will report and display the results from the resulting ' \
         r'experiments described in \ref{Methodology}' \
         r' For standard workloads A, C, an E, as well as custom workload I, the results will be displayed in both ' \
         r'graph and table format.  First, the results of the virtual machine will be compared to its analogy in ' \
         r'\cite{Abramova2014TestingCassandra}.  Second, the results among the varying \gls{ram} will be compared. ' \
         r'Third, the results of implementing the workload on the Raspberry Pi will be reported.  ' \
         r'Fourth, the Raspberry ' \
         r'Pi results will be compared against the system in \cite{Abramova2014TestingCassandra}.  ' \
         r'Fifth, the Raspberry ' \
         r'Pi results will be compared against the corresponding virtual machine.  ' \
         r'Sixth, the results from the wireless ' \
         r'network, using the Raspberry Pi nodes, will be explored.  Finally, seventh, the wired and wireless results ' \
         r'will be compared.  '
    s += '\n'
    for j in ['a', 'c', 'e', 'i']:
    # for j in ['i']:
        s += return_single_results_section(j)

    return s


def save_results_section():
    set_display_format_for_floats()
    f = open('doc/Chapters/Results-all.tex', 'w')
    f.write(return_entire_results_section())

