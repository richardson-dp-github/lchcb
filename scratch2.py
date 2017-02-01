import numpy as np
import graph_utility as sg
import pandas as pd
import research_questions_figure_generation as rqfg
import research_questions_analysis as rqa
import analysis_forjp as a4jp
import cassandra_stress_output_to_csv as cso2csv
import cassandra_stress_analysis as csa
import glob
from run_ycsb import run_command
# import run_ycsb
import os.path


def test_return_filtered_dataframe():

    data2 = [{'a': 1, 'b': 2, 'c': 1, 'd': 2},  {'a': 5, 'b': 10, 'c': 20, 'd': 500},
             {'a': 1, 'b': 4, 'c': 11, 'd': 8}, {'a': 4, 'b': 2, 'c': 9, 'd': 23}]


    df = pd.DataFrame(data2)

    print 'original data frame...'
    print df

    print '---'
    print 'filtered data frame ...'
    print sg.return_filtered_dataframe(df=df,
                                       d={'a': 1, 'b': 4})

    return 0


def test_generate_filtered_graph():


    sg.generate_filtered_graph(csv_with_main_results='test_data.csv',
                               d=None,
                               x_column='Year',
                               y_column='UFOSightings',
                               s_column='City',
                               title='UFO Sightings in Various Cities',
                               mode='line',
                               image_filename='results/ufosightings.png')

# run_ycsb.begin_cassandra_cluster(run_ycsb.select_cluster(network_type='rp_wired_cluster')[0])
def archive_20170108():
    run_ycsb.create_ycsb_database(s=run_ycsb.session, rf=1)
    run_ycsb.load_ycsb_usertable(num_records=1000000, start_empty=True, cluster_base_node_of_choice='192.168.1.100')
    run_ycsb.workloads_from_abramova_paper(ram='1GB',
                                      experiment='13',
                                      nodes='2',
                                      node_type='rp',
                                      link_type='eth',
                                      num_trials=30,
                                      do_workloads_a_and_c=True,
                                      do_workload_e=True,
                                      cluster_base_node_of_choice='192.168.1.100',
                                      verbose=True)

# test_generate_filtered_graph()
# test_generate_filtered_graph()
# rqfg.research_question_1_figure_1()
# rqfg.research_question_1_figure_2()
# rqfg.research_question_1_figure_3()
# rqfg.research_question_1_figure_4()
# rqfg.research_question_1_figure_5()
# rqfg.research_question_1_figure_6()
# rqfg.research_question_1_figure_6a()
# rqfg.research_question_1_figure_6b()
# rqfg.research_question_1_figure_7()
# rqfg.research_question_1_figure_8()


def run_all_graphs_for_workload_a():
    rqfg.research_question_1_figure_1()
    rqfg.research_question_1_figure_2()
    rqfg.research_question_1_figure_3()
    rqfg.research_question_1_figure_4()
    rqfg.research_question_1_figure_5()
    rqfg.research_question_1_figure_6()
    rqfg.research_question_1_figure_7()
    rqfg.research_question_1_figure_8()
    rqfg.research_question_1_figure_9()
    rqfg.research_question_1_figure_10()


def run_all_graphs_for_workload_c():
    rqfg.research_question_2_figure_1()
    rqfg.research_question_2_figure_4()
    rqfg.research_question_2_figure_5()
    rqfg.research_question_2_figure_6()
    rqfg.research_question_2_figure_7()
    rqfg.research_question_2_figure_8()
    rqfg.research_question_2_figure_9()
    rqfg.research_question_2_figure_10()



def run_all_graphs_for_workload_e():
    rqfg.research_question_3_figure_1()
    rqfg.research_question_3_figure_4()
    rqfg.research_question_3_figure_5()
    rqfg.research_question_3_figure_6()
    rqfg.research_question_3_figure_7()
    rqfg.research_question_3_figure_8()
    rqfg.research_question_3_figure_9()
    rqfg.research_question_3_figure_10()


def return_convert_cmd(filename_without_extension):
    return 'rsvg-convert -f pdf -o {}.pdf {}.svg'.format(filename_without_extension, filename_without_extension)


# doesn't like parentheses, and I totally don't care.  Filenames shouldn't have parentheses in them.
def convert_all_svgs_to_pdf(directory='figures/*.svg'):
    filenames = glob.iglob(directory)
    for filename in filenames:
        filename_without_extension = filename.split('/')[-1].replace('.svg', '')
        if not os.path.exists('{}.pdf'.format(filename_without_extension)):
            cmd = return_convert_cmd(filename_without_extension=filename_without_extension)
            run_command(cmd=cmd, cwd=os.path.dirname(filename))



'''
for i in ['3','4']:
    generate_cassandra_stress_graphs(graph_of_choice=i)
'''



'''
run_all_graphs_for_workload_c()
run_all_graphs_for_workload_e()

rqfg.research_question_1_figure_9()
rqfg.research_question_2_figure_9()
rqfg.research_question_3_figure_9()
'''
'''
cso2csv.cassandra_stress_output_2_csv(csvfilename='results/exp0_cstress/cassandra_stress_results_compression_strategy.csv',
                                      html_file_from_which_to_extract='old/test_compression_ops.html',
                                      extract_from_html=True)
'''
'''
cso2csv.cassandra_stress_output_2_csv(csvfilename='results/exp0_cstress/cassandra_stress_results_compression_strategy.csv')


print csa.return_summary_statistics()
'''

'''
run_all_graphs_for_workload_a()
run_all_graphs_for_workload_c()
run_all_graphs_for_workload_e()
'''
#rqfg.research_question_1_figure_1()
#rqfg.research_question_2_figure_1()
#rqfg.research_question_3_figure_1()

# rqfg.research_question_1_figure_2()
#rqfg.research_question_1_figure_10()
#rqfg.research_question_2_figure_10()
#rqfg.research_question_3_figure_10()

#for i in ['2', '3', '4']:
#    csa.generate_cassandra_stress_graphs(i)

#convert_all_svgs_to_pdf()

'''
workload = 'e'
print rqa.summary_statistics_varying_RAM_for_1_3_and_6_node_configurations(wl=workload)
print rqa.anova_for_variation_in_ram(wl=workload, nn=1)
print rqa.anova_for_variation_in_ram(wl=workload, nn=3)
print rqa.anova_for_variation_in_ram(wl=workload, nn=6)
print rqa.summary_statistics_rp_for_1_3_and_6_node_configurations(wl=workload)
print rqa.generate_bound_statements_rp_wired(wl=workload)
print rqa.generate_bound_statements_rp_wired_and_wireless(wl=workload)
'''


