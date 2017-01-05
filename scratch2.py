import numpy as np
import graph_utility as sg
import pandas as pd
import research_questions_figure_generation as rqfg
import run_ycsb


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


# test_generate_filtered_graph()
# test_generate_filtered_graph()
# rqfg.research_question_1_figure_1()
# rqfg.research_question_1_figure_2()
# rqfg.research_question_1_figure_3()
# rqfg.research_question_1_figure_4()
# rqfg.research_question_1_figure_5()
# rqfg.research_question_1_figure_6()
rqfg.research_question_1_figure_7()

# run_ycsb.begin_cassandra_cluster(run_ycsb.select_cluster(network_type='rp_wired_cluster')[0])
# run_ycsb.create_ycsb_database(s=run_ycsb.session, rf=1)
# run_ycsb.load_ycsb_usertable(num_records=1000000, start_empty=True, cluster_base_node_of_choice='192.168.1.130')
# run_ycsb.workloads_from_abramova_paper()



