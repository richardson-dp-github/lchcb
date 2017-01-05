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
                               title='RQ 1 Fig 1: Execution Time for 10k operations, Workload A, Abramova Paper',
                               mode='line')


# ram,nm,nt,rf,lt,nn,t,wl,dbs are possible columns
def research_question_1_figure_2_3_utility_fn(csv_file, title,
                                              d={'nm': 'nodal',
                                                 'nt': 'vm',
                                                 'nn': 1,
                                                 'wl': 'a'}):
    for i in ['a']:
        for j in [1]:
            gu.generate_filtered_graph(csv_with_main_results=csv_file,
                                       d=d,
                                       x_column='t',
                                       y_column='[OVERALL] RunTime(ms)',
                                       s_column='ram',
                                       title=title,
                                       mode='line')


def research_question_1_figure_2():
    research_question_1_figure_2_3_utility_fn(csv_file='experiment_11_magnify_cash_effect',
                                              title='RQ 1 Fig 2: Execution Time for 1k operations: {} Nodes, Workload {}'.format(1, 'A'))


def research_question_1_figure_3():
    research_question_1_figure_2_3_utility_fn(csv_file='combined_results.csv',
                                              title='RQ 1 Fig 3: Execution Time for 10k operations: {} Nodes, Workload {}'.format(1, 'A'),
                                              d={'nm': 'nodal',
                                                 'nt': 'vm',
                                                 'nn': 1,
                                                 'wl': 'a',
                                                 't': range(10,31)})
    return 0


def research_question_1_figure_4():
    csv_file='combined_results.csv',
    title='Res. Q. 1 Fig 4: Execution Time for 10k operations: {} Nodes, Workload {}'.format(1, 'A')

    for i in ['a']:
        for j in [1]:
            gu.generate_filtered_graph(csv_with_main_results=csv_file,
                                       d={'nm': 'nodal',
                                          'nt': 'vm',
                                          'nn': j,
                                          'wl': i,
                                          't': range(10, 31)},
                                       x_column='t',
                                       y_column='[OVERALL] RunTime(ms)',
                                       s_column='ram',
                                       title=title,
                                       mode='line')
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
                                   d={'wl': i,'nt-ram': ['vm-4GB', 'ref-2GB', 'rp-1GB']},
                                   x_column='nn',
                                   y_column='[OVERALL] RunTime(ms)',
                                   s_column='nt-ram',
                                   title='Research Question 1 Fig 5: Median Execution Time for 10k operations: Workload {}'.format(i),
                                   mode='marker')

    return 0


def research_question_1_figure_6():
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
                                   d={'wl': i, 'nt-ram': ['vm-4GB', 'ref-2GB', 'rp-1GB']},
                                   x_column='nn',
                                   y_column='[OVERALL] RunTime(ms)',
                                   s_column='nt-ram',
                                   title='Research Question 1 Figure 6: Median Execution Time for 10k operations: Workload {}'.format(i),
                                   mode='marker',
                                   filename='figures/rq1_fig6.html',
                                   image_filename='figures/rq1_fig6',
                                   image_type='png')



    return 0


# This is waiting on the wireless experiments
def research_question_1_figure_7():

    df = gu.calculate_summary(input_csv_file_name='experiment_12_wireless_tests',
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
                                   csv_with_main_results='experiment_12_wireless_tests',
                                   read_from_csv=False,
                                   d={'wl': i},
                                   x_column='nn',
                                   y_column='[OVERALL] RunTime(ms)',
                                   s_column='',
                                   title='Research Question 1 Figure 7: Median Execution Time for 10k operations, Wireless: Workload {}'.format(i),
                                   mode='marker',
                                   filename='figures/rq1_fig7.html',
                                   image_filename='figures/rq1_fig7',
                                   image_type='png')
    return 0
