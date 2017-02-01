from research_questions_analysis import set_display_format_for_floats
from scipy import stats
import pandas as pd
from graph_utility import return_filtered_dataframe as rfd
import graph_utility as sg


def return_summary_statistics(csv_file='results/exp0_cstress/cassandra_stress_results_compression_strategy.csv',
                              measurement_of_interest='op/s',
                              op='reads_only',
                              d=None,
                              compression_strategy='LZ4Compressor',
                              network_type='wired'):

    if not d:
        d={'compression': compression_strategy,
           'op': op,
           'network_type': network_type
        }

    df = pd.read_csv(csv_file)
    df_filtered = rfd(df, d=d)

    # df = {}
    # s = {}

    # df = rfd(df_filtered, d={'nn': v})[measurement_of_interest]

    s = df_filtered[measurement_of_interest].describe()

    for x in [s]:
        x['range'] = x['max'] - x['min']

    v = pd.DataFrame(s).reset_index()
    set_display_format_for_floats(
        format_='{:.5g}'.format
    )

    return v.to_latex(index=False)


def generate_cassandra_stress_graphs(graph_of_choice='none'):

    if graph_of_choice == '1':
        sg.generate_filtered_graph(df=None,
                            read_from_csv=True,
                            csv_with_main_results='results/exp0_cstress/cassandra_stress_results_compression_strategy.csv',
                            d={'op': 'writes_only'},
                            x_column='network_type',
                            y_column='op/s',
                            s_column='compression',
                            title='Operations Per Second - Writes Only',
                            mode='markers',
                            boxmean='sd',
                            boxpoints='all',
                            filename='figures/cs1_fig1.html',
                            image_filename='figures/cs1_fig1',
                            image_type='svg',
                            type='boxplot',
                            show_zero_line_on_y_axis=False,
                            verbose=True,
                            html_filename='cs1_fig1.html',
                            save_image_locally_as_png_=False,
                            save_image_as_html=True,
                            save_image_as_svg=True,
                            save_image_as_pdf=False)
    elif graph_of_choice == '2':
        sg.generate_filtered_graph(df=None,
                            read_from_csv=True,
                            csv_with_main_results='results/exp0_cstress/cassandra_stress_results_compression_strategy.csv',
                            d={'op': 'reads_only'},
                            x_column='network_type',
                            y_column='op/s',
                            s_column='compression',
                            title='Operations Per Second - Reads Only',
                            mode='markers',
                            boxmean='sd',
                            boxpoints='all',
                            filename='figures/cs1_fig2.html',
                            image_filename='figures/cs1_fig2',
                            image_type='svg',
                            type='boxplot',
                            show_zero_line_on_y_axis=False,
                            verbose=True,
                            html_filename='cs1_fig1.html',
                            save_image_locally_as_png_=False,
                            save_image_as_html=True,
                            save_image_as_svg=True,
                            save_image_as_pdf=False)
    elif graph_of_choice == '3':
        csv_file='results/exp0_cstress/cassandra_stress_results_compression_strategy.csv'

        df = pd.read_csv(csv_file)
        new_column_name = 'Compression-Operations'
        df[new_column_name] = df['compression'].map(str) + '-' + df['op']  # add column

        sg.generate_filtered_graph(df=df,
                            read_from_csv=False,
                            csv_with_main_results=csv_file,
                            d={'network_type': 'wired'},
                            x_column=new_column_name,
                            y_column='op/s',
                            s_column=None,
                            title='Operations Per Second',
                            mode='markers',
                            boxmean='sd',
                            boxpoints='all',
                            filename='figures/cs1_fig3.html',
                            image_filename='figures/cs1_fig3',
                            image_type='svg',
                            type='boxplot',
                            show_zero_line_on_y_axis=False,
                            verbose=True,
                            html_filename='cs1_fig1.html',
                            save_image_locally_as_png_=False,
                            save_image_as_html=True,
                            save_image_as_svg=True,
                            save_image_as_pdf=False,
                            sort_by_means=True)
    elif graph_of_choice == '4':
        csv_file='results/exp0_cstress/cassandra_stress_results_compression_strategy.csv'

        df = pd.read_csv(csv_file)
        new_column_name = 'Compression-Operations'
        df[new_column_name] = df['compression'].map(str) + '-' + df['op']  # add column
        sg.generate_filtered_graph(df=df,
                            read_from_csv=False,
                            csv_with_main_results='results/exp0_cstress/cassandra_stress_results_compression_strategy.csv',
                            d={'network_type': 'wireless'},
                            x_column=new_column_name,
                            y_column='op/s',
                            s_column='compression',
                            title='Operations Per Second',
                            mode='markers',
                            boxmean='sd',
                            boxpoints='all',
                            filename='figures/cs1_fig4.html',
                            image_filename='figures/cs1_fig4',
                            image_type='svg',
                            type='boxplot',
                            show_zero_line_on_y_axis=False,
                            verbose=True,
                            html_filename='cs1_fig1.html',
                            save_image_locally_as_png_=False,
                            save_image_as_html=True,
                            save_image_as_svg=True,
                            save_image_as_pdf=False,
                            sort_by_means=True)
