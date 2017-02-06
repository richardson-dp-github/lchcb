from research_questions_analysis import *





'''
def comparing_existing_work_vm_versus_ref_val(section, workload):

    measurement_of_interest='[OVERALL] RunTime(ms)'
    label_for_new_column='dif_from_ref'

    s = '\n\n'
    # First report initial observations
    #  except that there is no appropriate graph...

    # Here, we'll have to call both the graph and the table.
    df = return_df_that_includes_differences(main_csv_file='combined_results_revised.csv',
                                             reference_csv_file='abramova_results.csv',
                                             trial_list=None,
                                             measurement_of_interest=measurement_of_interest,
                                             desired_index=None,
                                             desired_columns=None,
                                             filter_for_nominator=['vm', 'nodal', '2GB'],
                                             filter_for_denominator=['ref', 'unk', '2GB'],
                                             label_for_new_column=label_for_new_column)


    #df_ref = pd.read_csv('abramova_results.csv')

    #df_ref = df_ref.set_index(['nn', 'wl'])

    df_ref = return_reference_data_frame()

    # Include and generate the table to insert here...

    # nn = [1, 3, 6]
    # wl = workload
    # db = 1000



    # df_summary = df[label_for_new_column].loc[nn, wl, db]

    # df_summary_for_individual_cluster_sizes = df_summary.unstack(level='nn')

    # df_summary_stats_for_individual_cluster_sizes = df_summary_for_individual_cluster_sizes.describe()
    # df_summary_stats_overall = df_summary.describe().rename('OVERALL')

    # df_summary_stats=df_summary_stats_for_individual_cluster_sizes.join(pd.DataFrame(df_summary_stats_overall))

    df_summary_stats = get_summary_table(df=df,
                                         label_for_new_column=label_for_new_column,
                                         nn=[1, 3, 6],
                                         wl=workload
                                         )

    label_for_assignment = 'abs_diffs_wl{}'.format(workload)
    label_for_reference = '\\ref{{{}}}'.format('table:{}'.format(label_for_assignment))
    reference_to_paper = r'\cite{Abramova2014TestingCassandra}'

    insert_table = return_embedded_latex_tables(latex_table_as_string=df_summary_stats.to_latex(),
                                                label=label_for_assignment,
                                                caption='Summary of the differences between the empirical execution'
                                                        ' time and the corresponding execution time reported in {}'
                                                        ''.format(reference_to_paper))


    # Second, calculate differences and do a linear regression




    s += 'Here, as depicted in Figure {fig}, one can see that the virtual machine configured to represent the network' \
         ' in {reference_to_paper} appears to perform at a significantly shorter execution time ' \
         'compared to {reference_to_paper}.  ' \
         'This is probably due to the fact that the network in the virtual ' \
         ' environment was a node and did not experience any kind of significant propagation delay nor ' \
         ' the delays . ' \
         'Table {table_ref} displays these results.  ' \
         '' \
         ''.format(
                   reference_to_paper=reference_to_paper,
                   fig='\\ref{{{}}}'.format('figures-wl{}_fig5'.format(workload)),
                   table_ref=label_for_reference)

    for i in [1, 3, 6]:
        nn = i
        wl = workload
        db = 1000
        ref_val = df_ref[measurement_of_interest].loc[nn, wl]
        max_dif = df_summary_stats[nn].loc['max']
        min_dif = df_summary_stats[nn].loc['min']
        mean_dif = df_summary_stats[nn].loc['mean']
        max_point = df['vm', 'nodal', '2GB'].loc[nn, wl].describe()['max']
        min_point = df['vm', 'nodal', '2GB'].loc[nn, wl].describe()['min']
        s += 'For a cluster size of {node_size}, the configuration in {reference_to_paper} reported ' \
             'a total execution time of {ref}' \
             'The maximum point, {max_point}, fell {max_dif} away from the reference point of {ref}.  ' \
             'The minimum point, {min_point}, fell {min_dif} away from the reference point.  ' \
             'The mean distance from the reference was calculated to be {mean_dif}.  ' \
             ''.format(node_size=i,
                       ref=ref_val,
                       reference_to_paper=reference_to_paper,
                       max_point=max_point,
                       min_point=min_point,
                       max_dif=max_dif,
                       min_dif=min_dif,
                       mean_dif=mean_dif)

    max_dif= df_summary_stats[nn].loc['max']
    min_dif= df_summary_stats[nn].loc['min']
    mean_dif= df_summary_stats[nn].loc['mean']
    s += 'Overall, for all node cluster sizes' \
         ', the maximum deviation from the reference was {max_dif}, and the minimum deviation from the ' \
         'reference was {min_dif}, and the mean deviation from the reference was {mean_dif}.' \
         ''.format(max_dif=max_dif,
                   min_dif=min_dif,
                   mean_dif=mean_dif)


    # Third, calculate speedup and do a linear regression

    # Calculate the speedup now...

    df_speedup = return_df_that_includes_speedup(main_csv_file='combined_results_revised.csv',
                                                 reference_csv_file='abramova_results.csv',
                                                 trial_list=None,
                                                 measurement_of_interest='[OVERALL] RunTime(ms)',
                                                 desired_index=None,
                                                 desired_columns=None,
                                                 filter_for_nominator=None,
                                                 filter_for_denominator=None,
                                                 label_for_new_column='su_vm_ref')

    s += 'There is also interest in calculating the speedup, the ratio of the virtual machine ' \
         'performance to the execution time reported in {reference_to_paper}.' \
         '  ' \
         '' \
         ''.format(
                   reference_to_paper=reference_to_paper,
                   fig='figures-wl{}_fig5.pdf'.format(workload),
                   table_ref=label_for_reference)

    for i in [1, 3, 6]:
        nn = i
        wl = workload
        db = 1000
        ref_val = df_ref[measurement_of_interest].loc[nn, wl]
        max_dif= df_summary_stats[nn].loc['max']
        min_dif= df_summary_stats[nn].loc['min']
        mean_dif= df_summary_stats[nn].loc['mean']
        max_point = df['vm', 'nodal', '2GB'].loc[nn, wl].describe()['max']
        min_point = df['vm', 'nodal', '2GB'].loc[nn, wl].describe()['min']
        s += 'For a cluster size of {node_size}, the configuration in {reference_to_paper} reported ' \
             'a total execution time of {ref}' \
             'The maximum point, {max_point}, fell {max_dif} away from the reference point of {ref}.  ' \
             'The minimum point, {min_point}, fell {min_dif} away from the reference point.  ' \
             'The mean distance from the reference was calculated to be {mean_dif}.  ' \
             ''.format(node_size=i,
                       ref=ref_val,
                       reference_to_paper=reference_to_paper,
                       max_point=max_point,
                       min_point=min_point,
                       max_dif=max_dif,
                       min_dif=min_dif,
                       mean_dif=mean_dif)

    max_dif= df_summary_stats[nn].loc['max']
    min_dif= df_summary_stats[nn].loc['min']
    mean_dif= df_summary_stats[nn].loc['mean']
    s += 'Overall, for all node cluster sizes' \
         ', the maximum deviation from the reference was {max_dif}, and the minimum deviation from the ' \
         'reference was {min_dif}, and the mean deviation from the reference was {mean_dif}.' \
         ''.format(max_dif=max_dif,
                   min_dif=min_dif,
                   mean_dif=mean_dif)


    return s
'''









def raspberry_pi_versus_virtual_machine(workload):
    s = '' \
        ''
    return s





def wireless_links_versus_wired(workload):

    s = '\n'

    s += 'In this section, ' \
         'the median value of the corresponding wired experiment will serve as the reference for the purposes ' \
         'of evaluating the wireless links. '

    #for cluster_size in [1, 3, 6]:
    #    s += 'For a node network of {cluster_size}, ' \
    #         'the experimental values fell between {} and {}, inclusive, and all values fell ' \
    #         'within {} of the reference value {}.  ' \
    #         ''.format(cluster_size=cluster_size)

    s += 'Figure 38 depicts the two experiments using Raspberry Pis: ' \
         'a wireless LAN (wlan) and an Ethernet LAN (eth). ' \
         'In Figure 38, as well as previous graphs, one can observe that the Ethernet LAN effects about ' \
         '50 seconds of execution time for 10,000 operations.  ' \
         ''

    return s




