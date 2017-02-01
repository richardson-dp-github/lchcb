import research_questions_analysis
import pandas as pd
from graph_utility import return_filtered_dataframe as rfd
from research_questions_analysis import *


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
    x += r'\begin{table}' + '\n'
    x += latex_table_as_string

    x += '\caption{'+caption+'}' + '\n'
    x += '\label{table:' + label + '}' + '\n'
    x += '\end{table}' + '\n'

    xx += x
    return xx


def return_desired_summary_statistics_table(comparison_description, workload,
                                            csv_file='combined_results_revised.csv',
                                            measurement_of_interest = '[OVERALL] RunTime(ms)',
                                            d=None,
                                            wl='a',
                                            nn=1,
                                            nt='rp',
                                            nm='eth',
                                            ram='1GB'):

    table = {
        'vm_v_ref': summary_statistics_varying_RAM_for_1_3_and_6_node_configurations(wl=workload),
        'ram_v_ram': summary_statistics_varying_RAM_for_1_3_and_6_node_configurations(wl=workload),
        'rp_only': summary_statistics_rp_for_all_cluster_sizes(wl=workload),
        'rp_v_ref': summary_statistics_rp_for_1_3_and_6_node_configurations(wl=workload),
        'rp_v_vm': 'No summary statistics at this time',
        'wlan_only': 'No summary statistics at this time',
        'wlan_v_eth': 'No summary statistics at this time'
    }
    caption = 'Summary Statistics for Workload {workload} performed on {.  Except for count,' \
              'all values are in milliseconds.'.format(workload=workload.capitalize())
    return_summary_statistics_tabular(workload=wl,
                                    nt=nt,
                                    ram=ram,
                                    nm=nm,
                                    csv_file=csv_file,
                                    measurement_of_interest=measurement_of_interest)


    return table[comparison_description]


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
                 r'While it appears the varying the amount of memory has some effect on the results, there'
                 r'does not seem to be a predictable pattern across nodes. '
                 r'An ANOVA test will determine if there is an effect, and a linear regression will further test'
                 r'for an effect. ',
            'c': r'This section discusses testing and performance for memory sizes: 1GB, 2GB, and 4GB.  '
                 r'The results are displayed in Figure \ref{figures-wlc_fig4}. '
                 r'While it appears the varying the amount of memory has some effect on the results, there'
                 r'does not seem to be a predictable pattern across nodes. '
                 r'An ANOVA test will determine if there is an effect, and a linear regression will further test'
                 r'for an effect. ',
            'e': r'The results are displayed in Figure \ref{figures-wle_fig4}.  '
                 r'First of all, the performance for the a one-node cluster differs significantly between 1GB RAM and'
                 r'all other cases.  '
                 r'While this could be some kind of implementation error, it is best not to draw any conclusions from'
                 r'this. '
                 r'It would be best to run these tests again, possibly switching the order to eliminate the possible '
                 r'effect of interference or a mix-up of data. '
                 r'That one case aside, the amount of RAM seems to have had an effect on the results, but there does'
                 r'not seem to be any predictive relationship that holds true across cluster sizes. ',
            'i': r'The results are displayed in Figure \ref{figures-wli_fig4}. '
                 r'Here there is a visible trend of 4GB RAM implying better performance results '
                 r'than both 1GB RAM and 2GB RAM.  '
                 r'However, the relationship between 1GB RAM and 2GB RAM does not seem to be'
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

    caption_dict = {
        1: {
            'a': '',
            'c': '',
            'e': '',
            'i': ''
        },
        4: {
            'a': '',
            'c': '',
            'e': '',
            'i': ''
        },
        5: {
            'a': '',
            'c': '',
            'e': '',
            'i': ''
        },
        6: {
            'a': '',
            'c': '',
            'e': '',
            'i': ''
        },
        7: {
            'a': '',
            'c': '',
            'e': '',
            'i': ''
        },
        8: {
            'a': '',
            'c': '',
            'e': '',
            'i': ''
        },
        9: {
            'a': '',
            'c': '',
            'e': '',
            'i': ''
        },
        10: {
            'a': '',
            'c': '',
            'e': '',
            'i': ''
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

    for figure_id in figures_dict[comparison_type]:

        name_of_figure = 'figures-wl{workload}_fig{figure_id}.pdf'.format(workload=workload, figure_id=figure_id)
        label_for_figure = 'figures-wl{workload}_fig{figure_id}'.format(workload=workload, figure_id=figure_id)
        caption = get_caption(figure_id=figure_id, workload=workload)

        text += r'\begin{figure}[h]' + '\n' \
                r'\includegraphics[width=' + str(width) + r'in]{Figures/' + name_of_figure + r'}' + '\n' \
                r'\caption{' + caption + r'}' + '\n' \
                r'\label{' + label_for_figure + r'}' + '\n' \
                r'\end{figure}' + '\n' + '\n'

    return text


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
    s += speedup_analysis_tables(comparison_description=comparison_description,
                                 workload=workload,
                                 csv_file='combined_results_revised.csv')
    s += '\n'

    return s


def update_ordinal_statistics(comparison_type, workload):

    s = '\n'
    s += r'\subsubsection{Ordinal Statistics}'
    s += '\n'
    s += return_desired_summary_statistics_table(comparison_description=comparison_type, workload=workload)

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
    # for j in ['a', 'c', 'e', 'i']:
    for j in ['i']:
        s += return_single_results_section(j)

    return s


def save_results_section():

    f = open('doc/Chapters/Results-all.tex', 'w')
    f.write(return_entire_results_section())

