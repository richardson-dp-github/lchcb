import csv
import plotly.plotly as py
import plotly
import plotly.graph_objs as go
import scipy
import pandas as pd
import graph_utility as gu
import numpy as np
import matplotlib.pyplot as plt


# This is the reference data from the paper only, Workload A only
def research_question_1_figure_1():
    gu.generate_filtered_graph(csv_with_main_results='abramova_results.csv',
                               d={
                                  'wl': 'a'
                                           },
                               x_column='nn',
                               y_column='[OVERALL] RunTime(ms)',
                               s_column=None,
                               title='Execution Time for 10k operations, Workload A',
                               mode='markers',
                               filename='figures/rq1_fig1.html',
                               image_filename='figures/rq1_fig1',
                               image_type='png',
                               type='bar')


# ram,nm,nt,rf,lt,nn,t,wl,dbs are possible columns
def research_question_1_figure_2_3_utility_fn(csv_file, title,
                                              d={'nm': 'nodal',
                                                 'nt': 'vm',
                                                 'nn': 1,
                                                 'wl': 'a'},
                                              filename='figures/rq1_fig23.html',
                                              image_filename='figures/rq1_fig23',
                                              image_type='png'):
    for i in ['a']:
        for j in [1]:
            gu.generate_filtered_graph(csv_with_main_results=csv_file,
                                       d=d,
                                       x_column='t',
                                       y_column='[OVERALL] RunTime(ms)',
                                       s_column='ram',
                                       title=title,
                                       mode='line',
                                       filename=filename,
                                       image_filename=image_filename,
                                       image_type=image_type)


# Experiment to see how the varying the number of operations per trial affects the results.
def research_question_1_figure_2():
    research_question_1_figure_2_3_utility_fn(csv_file='experiment_11_magnify_cash_effect',
                                              title='Execution Time for 1k operations: {} Nodes, Workload {}'.format(1, 'A'),
                                              filename='figures/rq1_fig2.html',
                                              image_filename='figures/rq1_fig2',
                                              image_type='png')


def research_question_1_figure_3():
    research_question_1_figure_2_3_utility_fn(csv_file='combined_results.csv',
                                              title='RQ 1 Fig 3: Execution Time for 10k operations: {} Nodes, Workload {}'.format(1, 'A'),
                                              d={'nm': 'nodal',
                                                 'nt': 'vm',
                                                 'nn': 1,
                                                 'wl': 'a',
                                                 't': range(10,31)},
                                              filename='figures/rq1_fig3.html',
                                              image_filename='figures/rq1_fig3',
                                              image_type='png')
    return 0


def research_question_2_figure_3():
    research_question_1_figure_2_3_utility_fn(csv_file='combined_results.csv',
                                              title='RQ 2 Fig 3: Execution Time for 10k operations: {} Nodes, Workload {}'.format(1, 'C'),
                                              d={'nm': 'nodal',
                                                 'nt': 'vm',
                                                 'nn': 1,
                                                 'wl': 'c',
                                                 't': range(10, 31)})


def research_question_3_figure_3():
    research_question_1_figure_2_3_utility_fn(csv_file='combined_results.csv',
                                              title='RQ 3 Fig 3: Execution Time for 10k operations: {} Nodes, Workload {}'.format(1, 'E'),
                                              d={'nm': 'nodal',
                                                 'nt': 'vm',
                                                 'nn': 1,
                                                 'wl': 'e',
                                                 't': range(10, 31)},
                                              filename='figures/rq1_fig3.html',
                                              image_filename='figures/rq1_fig3',
                                              image_type='png',)


# Ignoring the first 10 trials
# This compares the various
def research_question_1_figure_4():
    csv_file='combined_results.csv'
    title='Execution Time for 10k operations: Workload {}'.format('A')

    df = pd.read_csv(csv_file)
    new_column_name = 'NumberOfNodes'
    df[new_column_name] = df['nn'].map(str) + ' Nodes'  # add column

    for i in ['a']:
        for j in [1]:
            gu.generate_filtered_graph(df,
                                       d={'nm': 'nodal',
                                          'nt': 'vm',
                                          'wl': i,
                                          't': range(10, 31)},
                                       x_column=new_column_name,
                                       y_column='[OVERALL] RunTime(ms)',
                                       s_column='ram',
                                       title=title,
                                       type='boxplot',
                                       read_from_csv=False,
                                       filename='figures/rq1_fig4.html',
                                       image_filename='figures/rq1_fig4',
                                       image_type='png',)
    return 0


def research_question_1_figure_5():
    df = gu.calculate_summary(input_csv_file_name='combined_results.csv',
                              read_from_csv=True,
                              dataframe=None,
                              measurement_of_interest='[OVERALL] RunTime(ms)',
                              series_to_group_by=['ram', 'nm', 'nt', 'rf', 'wl', 'nn'],
                              return_series_not_data_frame=False,
                              reset_index_before_returning_data_frame=True,
                              summary_statistic_of_interest='median'
                              )

    df_ref = pd.read_csv('abramova_results.csv')
    df_ref = gu.return_filtered_dataframe(df_ref, {'wl': 'a'})

    df = df.append(df_ref, ignore_index=True)

    df['nt-ram'] = df['nt'].map(str) + '-' + df['ram'].map(str)  # for the series name

    for i in ['a']:
        gu.generate_filtered_graph(df=df,
                                   csv_with_main_results='combined_results.csv',
                                   read_from_csv=False,
                                   d={'wl': i,'nt-ram': ['vm-2GB', 'ref-2GB']},
                                   x_column='nn',
                                   y_column='[OVERALL] RunTime(ms)',
                                   s_column='nt-ram',
                                   title='YCSB Workload A, 10k operations, Comparison Against Existing Work',
                                   mode='marker',
                                   filename='figures/rq1_fig5.html',
                                   image_filename='figures/rq1_fig5',
                                   image_type='png',
                                   show_zero_line_on_y_axis=True)

    return 0


def research_question_1_figure_6():
    df = gu.calculate_summary(input_csv_file_name='combined_results_revised.csv',
                              read_from_csv=True,
                              dataframe=None,
                              measurement_of_interest='[OVERALL] RunTime(ms)',
                              series_to_group_by=['ram', 'nm', 'nt', 'rf', 'wl', 'nn'],
                              return_series_not_data_frame=False,
                              reset_index_before_returning_data_frame=True,
                              summary_statistic_of_interest='median',

                              )

    df_ref = pd.read_csv('abramova_results.csv')
    df_ref = gu.return_filtered_dataframe(df_ref, {'wl': 'a'})

    df = df.append(df_ref, ignore_index=True)

    df['nt-ram'] = df['nt'].map(str) + '-' + df['ram'].map(str)  # for the series name

    for i in ['a']:
        gu.generate_filtered_graph(df=df,
                                   read_from_csv=False,
                                   d={'wl': i, 'nt-ram': ['vm-4GB', 'ref-2GB', 'rp-1GB'], 'nm': ['eth','nodal','unk']},
                                   x_column='nn',
                                   y_column='[OVERALL] RunTime(ms)',
                                   s_column='nt-ram',
                                   title='Median Execution Time for 10k operations: Workload {}'.format(i),
                                   mode='marker',
                                   filename='figures/rq1_fig6.html',
                                   image_filename='figures/rq1_fig6',
                                   image_type='png')



    return 0

def research_question_1_figure_6a():
    df = gu.calculate_summary(input_csv_file_name='combined_results.csv',
                              read_from_csv=True,
                              dataframe=None,
                              measurement_of_interest='[OVERALL] RunTime(ms)',
                              series_to_group_by=['ram', 'nm', 'nt', 'rf', 'wl', 'nn'],
                              return_series_not_data_frame=False,
                              reset_index_before_returning_data_frame=True,
                              summary_statistic_of_interest='median'
                              )

    df_ref = pd.read_csv('abramova_results.csv')
    df_ref = gu.return_filtered_dataframe(df_ref, {'wl': 'a'})

    df = df.append(df_ref, ignore_index=True)

    df['nt-ram'] = df['nt'].map(str) + '-' + df['ram'].map(str)  # for the series name

    for i in ['a']:
        gu.generate_filtered_graph(df=df,
                                   csv_with_main_results='combined_results.csv',
                                   read_from_csv=False,
                                   d={'wl': i, 'nt': ['vm']},
                                   x_column='nn',
                                   y_column='[OVERALL] RunTime(ms)',
                                   s_column='nt-ram',
                                   title='Research Question 1 Figure 6a Median Execution Time for 10k operations: Workload {}'.format(i),
                                   mode='marker',
                                   filename='figures/rq1_fig6a.html',
                                   image_filename='figures/rq1_fig6a',
                                   image_type='png')



    return 0

def research_question_1_figure_6b():
    df = gu.calculate_summary(input_csv_file_name='combined_results.csv',
                              read_from_csv=True,
                              dataframe=None,
                              measurement_of_interest='[OVERALL] RunTime(ms)',
                              series_to_group_by=['ram', 'nm', 'nt', 'rf', 'wl', 'nn'],
                              return_series_not_data_frame=False,
                              reset_index_before_returning_data_frame=True,
                              summary_statistic_of_interest='median'
                              )

    df_ref = pd.read_csv('abramova_results.csv')
    df_ref = gu.return_filtered_dataframe(df_ref, {'wl': 'a'})

    df = df.append(df_ref, ignore_index=True)

    # df['nt-ram'] = df['nt'].map(str) + '-' + df['ram'].map(str)  # for the series name

    for i in ['a']:
        gu.generate_filtered_graph(df=df,
                                   csv_with_main_results='combined_results.csv',
                                   read_from_csv=False,
                                   d={'wl': i, 'nt': ['vm']},
                                   x_column='ram',
                                   y_column='[OVERALL] RunTime(ms)',
                                   s_column='nn',
                                   title='Research Question 1 Figure 6b Median Execution Time for 10k operations: Workload {}'.format(i),
                                   mode='marker',
                                   filename='figures/rq1_fig6b.html',
                                   image_filename='figures/rq1_fig6b',
                                   image_type='png')



    return 0

# This is waiting on the wireless experiments
def research_question_1_figure_7():

    df = gu.calculate_summary(input_csv_file_name='combined_results_revised.csv',
                              read_from_csv=True,
                              dataframe=None,
                              measurement_of_interest='[OVERALL] RunTime(ms)',
                              series_to_group_by=['ram', 'nm', 'nt', 'rf', 'wl', 'nn'],
                              return_series_not_data_frame=False,
                              reset_index_before_returning_data_frame=True,
                              summary_statistic_of_interest='median'
                              )


    for i in ['a']:
        gu.generate_filtered_graph(df=df,
                                   read_from_csv=False,
                                   d={'wl': i, 'nt': 'rp'},
                                   x_column='nn',
                                   y_column='[OVERALL] RunTime(ms)',
                                   s_column='nm',
                                   title='Workload A on Ethernet and Wireless: Median Execution Time for 10k operations',
                                   mode='marker',
                                   show_zero_line_on_y_axis=True,
                                   filename='figures/rq1_fig7.html',
                                   image_filename='figures/rq1_fig7',
                                   image_type='png')
    return 0


# Boxplot for the wireless experiments
def research_question_1_figure_8():

    # df = gu.calculate_summary(input_csv_file_name='experiment_12_wireless_tests',
    #                          read_from_csv=True,
    #                          dataframe=None,
    #                          measurement_of_interest='[OVERALL] RunTime(ms)',
    #                          series_to_group_by=['ram', 'nm', 'nt', 'rf', 'wl', 'nn'],
    #                          return_series_not_data_frame=False,
    #                          reset_index_before_returning_data_frame=True,
    #                          summary_statistic_of_interest='median'
    #                          )

    df = pd.read_csv('experiment_12_wireless_tests')

    for i in ['a']:
        gu.generate_filtered_graph(df=df,
                                   csv_with_main_results='experiment_12_wireless_tests',
                                   read_from_csv=False,
                                   d={'wl': i},
                                   x_column='nn',
                                   y_column='[OVERALL] RunTime(ms)',
                                   s_column=None,
                                   show_zero_line_on_y_axis=True,
                                   title='Execution Time for 10k operations, Wireless LAN: Workload {}'.format(i),
                                   filename='figures/rq1_fig8.html',
                                   image_filename='figures/rq1_fig8',
                                   image_type='png',
                                   type='boxplot')
    return 0

# This is waiting on the wireless experiments
def research_question_1_figure_9():

    df = gu.calculate_summary(input_csv_file_name='combined_results_revised.csv',
                              read_from_csv=True,
                              dataframe=None,
                              measurement_of_interest='[OVERALL] RunTime(ms)',
                              series_to_group_by=['ram', 'nm', 'nt', 'rf', 'wl', 'nn'],
                              return_series_not_data_frame=False,
                              reset_index_before_returning_data_frame=True,
                              summary_statistic_of_interest='variance'
                              )


    for i in ['a']:
        gu.generate_filtered_graph(df=df,
                                   read_from_csv=False,
                                   d={'wl': i, 'nt': 'rp'},
                                   x_column='nm',
                                   y_column='[OVERALL] RunTime(ms)',
                                   s_column='nn',
                                   title='Workload A on Ethernet and Wireless: Variance in Execution Time for 10k operations',
                                   mode='marker',
                                   show_zero_line_on_y_axis=True,
                                   filename='figures/rq1_fig9.html',
                                   image_filename='figures/rq1_fig9',
                                   image_type='png',
                                   type='bar')
    return 0