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
def research_question_1_figure_1_utility_function(wl='a'):
    gu.generate_filtered_graph(csv_with_main_results='abramova_results.csv',
                               d={
                                  'wl': wl
                                           },
                               x_column='nn',
                               y_column='[OVERALL] RunTime(ms)',
                               s_column=None,
                               title='Execution Time, Workload {}'.format(wl.capitalize()),
                               mode='markers',
                               filename='figures/wl{}_fig1.html'.format(wl),
                               image_filename='figures/wl{}_fig1'.format(wl),
                               image_type='svg',
                               save_image_as_svg=True,
                               type='bar')


def research_question_1_figure_1():
    research_question_1_figure_1_utility_function(wl='a')


def research_question_2_figure_1():
    research_question_1_figure_1_utility_function(wl='c')


def research_question_3_figure_1():
    research_question_1_figure_1_utility_function(wl='e')


# ram,nm,nt,rf,lt,nn,t,wl,dbs are possible columns
def research_question_1_figure_2_3_utility_fn(csv_file, title,
                                              d={'nm': 'nodal',
                                                 'nt': 'vm',
                                                 'nn': 1,
                                                 'wl': 'a'},
                                              filename='figures/wl{}_fig23.html'.format('a'),
                                              image_filename='figures/wla_fig23',
                                              image_type='svg',
                                              save_image_as_svg=True):
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
                                       save_image_as_svg=save_image_as_svg,
                                       image_type=image_type)


# Experiment to see how the varying the number of operations per trial affects the results.
def research_question_1_figure_2():
    research_question_1_figure_2_3_utility_fn(csv_file='experiment_11_magnify_cash_effect',
                                              title='Execution Time',
                                              filename='figures/wl{}_fig2.html'.format('a'),
                                              image_filename='figures/wl{}_fig2'.format('a'),
                                              save_image_as_svg=True,
                                              image_type='svg')


def research_question_1_figure_3():
    research_question_1_figure_2_3_utility_fn(csv_file='combined_results.csv',
                                              title='Execution Time',
                                              d={'nm': 'nodal',
                                                 'nt': 'vm',
                                                 'nn': 1,
                                                 'wl': 'a',
                                                 't': range(10, 31)},
                                              filename='figures/wl{}_fig3.html'.format('a'),
                                              image_filename='figures/wl{}_fig3'.format('a'),
                                              image_type='svg',
                                              save_image_as_svg=True)
    return 0


# This does a box plot comparing the VMs performance based on 1GB, 2GB, 4GB RAM
def research_question_figure_4_utility_function(workload='a',
                                                ):
    csv_file='combined_results_revised.csv'
    title='Execution Time, Workload {}'.format(workload.capitalize())

    df = pd.read_csv(csv_file)
    new_column_name = 'NumberOfNodes'
    df[new_column_name] = df['nn'].map(str) + ' Nodes'  # add column

    for i in [workload]:
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
                                       filename='figures/wl{}_fig4.html'.format(i),
                                       image_filename='figures/wl{}_fig4'.format(i),
                                       image_type='svg',
                                       save_image_as_svg=True,
                                       boxmean=True)
    return 0


def research_question_1_figure_4():
    research_question_figure_4_utility_function(workload='a',
                                                )
    return 0


def research_question_2_figure_4():
    research_question_figure_4_utility_function(workload='c',
                                                )
    return 0


def research_question_3_figure_4():
    research_question_figure_4_utility_function(workload='e',
                                                )
    return 0


def research_question_4_figure_4():
    research_question_figure_4_utility_function(workload='i',
                                                )
    return 0


# This is the comparison against the Abramova paper
def research_question_1_figure_5_utility_function(wl='a'):
    df = gu.calculate_summary(input_csv_file_name='combined_results_revised.csv',
                              read_from_csv=True,
                              dataframe=None,
                              measurement_of_interest='[OVERALL] RunTime(ms)',
                              series_to_group_by=['ram', 'nm', 'nt', 'rf', 'wl', 'nn'],
                              return_series_not_data_frame=False,
                              reset_index_before_returning_data_frame=True,
                              summary_statistic_of_interest='median'
                              )

    df_ref = pd.read_csv('abramova_results.csv')
    df_ref = gu.return_filtered_dataframe(df_ref, {'wl': wl})

    df = df.append(df_ref, ignore_index=True)

    df['nt-ram'] = df['nt'].map(str) + '-' + df['ram'].map(str)  # for the series name

    for i in [wl]:
        gu.generate_filtered_graph(df=df,
                                   csv_with_main_results='combined_results.csv',
                                   read_from_csv=False,
                                   d={'wl': i,'nt-ram': ['vm-2GB', 'ref-2GB']},
                                   x_column='nn',
                                   y_column='[OVERALL] RunTime(ms)',
                                   s_column='nt-ram',
                                   title='Execution Time, Workload {}'.format(i.capitalize()),
                                   mode='marker',
                                   filename='figures/wl{}_fig5.html'.format(wl),
                                   image_filename='figures/wl{}_fig5'.format(wl),
                                   image_type='svg',
                                   show_zero_line_on_y_axis=True,
                                   save_image_as_svg=True)

    return 0


def research_question_1_figure_5():
    research_question_1_figure_5_utility_function(wl='a')
    return 0


def research_question_2_figure_5():
    research_question_1_figure_5_utility_function(wl='c')
    return 0


def research_question_3_figure_5():
    research_question_1_figure_5_utility_function(wl='e')
    return 0


def research_question_4_figure_5():
    research_question_1_figure_5_utility_function(wl='i',
                                                )
    return 0


# This compares the virtual machine performance against the raspberry pi hardware
def research_question_1_figure_6_utility_function(wl='a'):
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
    df_ref = gu.return_filtered_dataframe(df_ref, {'wl': wl})

    df = df.append(df_ref, ignore_index=True)

    df['nt-ram'] = df['nt'].map(str) + '-' + df['ram'].map(str)  # for the series name

    for i in [wl]:
        gu.generate_filtered_graph(df=df,
                                   read_from_csv=False,
                                   d={'wl': i, 'nt-ram': ['vm-1GB', 'ref-2GB', 'rp-1GB'], 'nm': ['eth','nodal','unk']},
                                   x_column='nn',
                                   y_column='[OVERALL] RunTime(ms)',
                                   s_column='nt-ram',
                                   title='Execution Time, Workload {}'.format(i.capitalize()),
                                   mode='marker',
                                   filename='figures/wl{}_fig6.html'.format(wl),
                                   image_filename='figures/wl{}_fig6'.format(wl),
                                   image_type='svg',
                                   save_image_as_svg=True)

    return 0


def research_question_1_figure_6():
    research_question_1_figure_6_utility_function(wl='a')
    return 0


def research_question_2_figure_6():
    research_question_1_figure_6_utility_function(wl='c')
    return 0


def research_question_3_figure_6():
    research_question_1_figure_6_utility_function(wl='e')
    return 0


def research_question_4_figure_6():
    research_question_1_figure_6_utility_function(wl='i')
    return 0


# Compare the medians between the 2GB Virtual Machine and the Raspberry Pi Hardware
def research_question_1_figure_7_utility_function(wl='a'):

    df = gu.calculate_summary(input_csv_file_name='combined_results_revised.csv',
                              read_from_csv=True,
                              dataframe=None,
                              measurement_of_interest='[OVERALL] RunTime(ms)',
                              series_to_group_by=['ram', 'nm', 'nt', 'rf', 'wl', 'nn'],
                              return_series_not_data_frame=False,
                              reset_index_before_returning_data_frame=True,
                              summary_statistic_of_interest='median'
                              )

    for i in [wl]:
        gu.generate_filtered_graph(df=df,
                                   read_from_csv=False,
                                   d={'wl': i, 'nt': 'rp'},
                                   x_column='nn',
                                   y_column='[OVERALL] RunTime(ms)',
                                   s_column='nm',
                                   title='Execution Time, Workload {}'.format(i.capitalize()),
                                   mode='marker',
                                   show_zero_line_on_y_axis=True,
                                   filename='figures/wl{}_fig7.html'.format(wl),
                                   image_filename='figures/wl{}_fig7'.format(wl),
                                   image_type='svg',
                                   save_image_as_svg=True)
    return 0


def research_question_1_figure_7():
    research_question_1_figure_7_utility_function(wl='a')
    return 0


def research_question_2_figure_7():
    research_question_1_figure_7_utility_function(wl='c')
    return 0


def research_question_3_figure_7():
    research_question_1_figure_7_utility_function(wl='e')
    return 0


def research_question_4_figure_7():
    research_question_1_figure_7_utility_function(wl='i')
    return 0


# Boxplot for the wireless experiments
def research_question_1_figure_8_utility_function(wl='a'):

    df = pd.read_csv('combined_results_revised.csv')

    for i in [wl]:
        gu.generate_filtered_graph(df=df,
                                   read_from_csv=False,
                                   d={'wl': i,
                                      'nm': 'wlan'},
                                   x_column='nn',
                                   y_column='[OVERALL] RunTime(ms)',
                                   s_column=None,
                                   show_zero_line_on_y_axis=True,
                                   title='Execution Time, Workload {}'.format(i),
                                   filename='figures/wl{}_fig8.html'.format(wl),
                                   image_filename='figures/wl{}_fig8'.format(wl),
                                   image_type='svg',
                                   type='boxplot',
                                   save_image_as_svg=True)
    return 0


def research_question_1_figure_8():
    research_question_1_figure_8_utility_function(wl='a')
    return 0


def research_question_2_figure_8():
    research_question_1_figure_8_utility_function(wl='c')
    return 0


def research_question_3_figure_8():
    research_question_1_figure_8_utility_function(wl='e')
    return 0


def research_question_4_figure_8():
    research_question_1_figure_8_utility_function(wl='i')
    return 0


# This is waiting on the wireless experiments
def research_question_1_figure_9_utility_fn(workload='a',
                                            research_question='1'):

    df = gu.calculate_summary(input_csv_file_name='combined_results_revised.csv',
                              read_from_csv=True,
                              dataframe=None,
                              measurement_of_interest='[OVERALL] RunTime(ms)',
                              series_to_group_by=['ram', 'nm', 'nt', 'rf', 'wl', 'nn'],
                              return_series_not_data_frame=False,
                              reset_index_before_returning_data_frame=True,
                              summary_statistic_of_interest='stdev'
                              )


    for i in [workload]:
        gu.generate_filtered_graph(df=df,
                                   read_from_csv=False,
                                   d={'wl': i, 'nt': 'rp'},
                                   x_column='nm',
                                   y_column='[OVERALL] RunTime(ms)',
                                   s_column='nn',
                                   title='Workload {} Execution Time'.format(workload.capitalize()),
                                   mode='marker',
                                   show_zero_line_on_y_axis=True,
                                   filename='figures/wl{}_fig9.html'.format(i),
                                   image_filename='figures/wl{}_fig9'.format(i),
                                   type='bar',
                                   save_image_as_pdf=False,
                                   save_image_locally_as_png_=False,
                                   save_image_as_svg=True)
    return 0


def research_question_1_figure_9():
    research_question_1_figure_9_utility_fn()
    return 0


def research_question_2_figure_9():
    research_question_1_figure_9_utility_fn(workload='c',
                                            research_question='2')
    return 0


def research_question_3_figure_9():
    research_question_1_figure_9_utility_fn(workload='e',
                                            research_question='3')
    return 0


def research_question_4_figure_9():
    research_question_1_figure_9_utility_fn(workload='i',
                                            research_question='4')
    return 0

# Boxplot for the wired experiments
def research_question_1_figure_10_utility_function(wl='a'):

    # df = gu.calculate_summary(input_csv_file_name='experiment_12_wireless_tests',
    #                          read_from_csv=True,
    #                          dataframe=None,
    #                          measurement_of_interest='[OVERALL] RunTime(ms)',
    #                          series_to_group_by=['ram', 'nm', 'nt', 'rf', 'wl', 'nn'],
    #                          return_series_not_data_frame=False,
    #                          reset_index_before_returning_data_frame=True,
    #                          summary_statistic_of_interest='median'
    #                          )

    df = pd.read_csv('combined_results_revised.csv')

    for i in [wl]:
        gu.generate_filtered_graph(df=df,
                                   csv_with_main_results='combined_results_revised.csv',
                                   read_from_csv=False,
                                   d={'wl': i, 'nt': 'rp'},
                                   x_column='nn',
                                   y_column='[OVERALL] RunTime(ms)',
                                   s_column=None,
                                   show_zero_line_on_y_axis=True,
                                   title='Execution Time, Workload {}'.format(i),
                                   filename='figures/wl{}_fig10.html'.format(wl),
                                   image_filename='figures/wl{}_fig10'.format(wl),
                                   image_type='svg',
                                   type='boxplot',
                                   save_image_as_svg=True)
    return 0


def research_question_1_figure_10():
    research_question_1_figure_10_utility_function(wl='a')
    return 0


def research_question_2_figure_10():
    research_question_1_figure_10_utility_function(wl='c')
    return 0


def research_question_3_figure_10():
    research_question_1_figure_10_utility_function(wl='e')
    return 0


def research_question_4_figure_10():
    research_question_1_figure_10_utility_function(wl='i')
    return 0


# This will create the references on top of the boxplot.  This will not be valid for workload I.
def research_question_1_figure_11_utility_function(wl='a'):

    # df = gu.calculate_summary(input_csv_file_name='experiment_12_wireless_tests',
    #                          read_from_csv=True,
    #                          dataframe=None,
    #                          measurement_of_interest='[OVERALL] RunTime(ms)',
    #                          series_to_group_by=['ram', 'nm', 'nt', 'rf', 'wl', 'nn'],
    #                          return_series_not_data_frame=False,
    #                          reset_index_before_returning_data_frame=True,
    #                          summary_statistic_of_interest='median'
    #                          )

    df = pd.read_csv('combined_results_revised.csv')

    for i in [wl]:
        gu.generate_filtered_graph(df=df,
                                   csv_with_main_results='combined_results_revised.csv',
                                   read_from_csv=False,
                                   d={'wl': i, 'nt': 'rp'},
                                   x_column='nn',
                                   y_column='[OVERALL] RunTime(ms)',
                                   s_column=None,
                                   show_zero_line_on_y_axis=True,
                                   title='Execution Time, Workload {}'.format(i),
                                   filename='figures/wl{}_fig11.html'.format(wl),
                                   image_filename='figures/wl{}_fig11'.format(wl),
                                   image_type='svg',
                                   type='boxplot',
                                   save_image_as_svg=True)
    return 0

def research_question_1_figure_12_utility_function(wl='a'):



    return 0