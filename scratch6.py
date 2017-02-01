import subprocess
import time
import datetime   # this works despite the red underline
import sys
import cassandra
from cassandra.cluster import Cluster
import os.path
import csv
import pandas as pd
import csv
import glob
import re
import shutil
import ycsb_output_to_csv
import research_questions_figure_generation
import itertools
import numpy as np
import research_questions_analysis as rqa
import research_questions_figure_generation as rqfg
import graph_utility as gu
import generate_results as gr


# Return df with speedup
def return_df_that_includes_speedup():
    df = pd.read_csv('combined_results_revised.csv')

    df = gu.return_filtered_dataframe(df=df, d={'t': range(10, 30+1)})

    df = df.append(pd.read_csv('abramova_results.csv'))

    table = pd.pivot_table(df,
                           values='[OVERALL] RunTime(ms)',
                           index=['nn','wl','dbs'],
                           columns=['nt','nm','ram'],
                           aggfunc=np.median)

    table['su_rp_vm'] = table['vm', 'nodal', '1GB'] / table['rp', 'eth', '1GB']
    table['su_rp_ref'] = table['ref', 'unk', '2GB'] / table['rp', 'eth', '1GB']
    table['su_wlan_eth'] = table['rp', 'eth', '1GB'] / table['rp', 'wlan', '1GB']

    return table


gr.save_results_section()


# rqfg.research_question_4_figure_8()

# gu.convert_all_svgs_to_pdf()