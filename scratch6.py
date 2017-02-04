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


def return_arguments_from_list(x):

    return str(x).replace(']', '').replace('[', '')




gr.save_results_section()

# print rqa.return_df_that_includes_differences()

#r['ref', 'unk', '2GB'] = r['ref', 'unk', '2GB']



# print r

# rqfg.research_question_4_figure_8()

# gu.convert_all_svgs_to_pdf()