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

# from local files

import run_ycsb
# import ycsb_output_to_csv
# import summarized_graphs


# This actually runs the command in the terminal
#   This is a separate function for convenience so one doesn't have to remember to put the wait down every time.
def run_command(cmd, verbose=True, cwd='/home/daniel/Documents/thesis/YCSB/'):
    if verbose:
        print cmd
    p = subprocess.Popen(cmd, shell=True, cwd=cwd)
    p.wait()


def return_clone_command(new_machine_name):
    clone_command = 'VBoxManage clonevm ' \
                    ' "c0" ' \
                    '--options link ' \
                    '--name "' + new_machine_name + '" ' \
                    '--register '

    return clone_command


def change_ram_for_one_machine(machine_name, memory_size):
    clone_command = 'VBoxManage modifyvm ' \
                    ' "' + machine_name + '" ' \
                    '--memory ' + str(memory_size)

    return clone_command


def change_ram_for_all_machines(memory_size):
    for i in range(0, 8):
        cmd = change_ram_for_one_machine('c' + str(i), memory_size)
        run_command(cmd)

def clone_vms():
    for i in ['a', 'b', 'd']:
        for j in [0,1,2,3,4,5,6]:
            name_of_new_machine = i + str(j)
            x = return_clone_command(name_of_new_machine)
            run_command(cmd=x, cwd='.')
    print "Execution finished"


def determine_if_test_is_already_done(csvfilename='all.csv', num_nodes=0, t=9999, w='_UNK_', ld=False, s=0,
                                      lt=9999, rf=0, ram='0GB', node_type='unknown', lan_type='unknown'):
    df = pd.read_csv(csvfilename)


    x = any(
        (df.ld == ld) &
        (df.wl == w) &
        (df.ram == ram) &
        (df.n == num_nodes) &
        (df.t == t) &
        (df.dbs == s) &
        (df.rf == rf) &
        (df['lt'] == lt) &
        (df.nt == node_type) &
        (df.nm == lan_type)
    )

    return x

def test_determine_if_test_is_already_done():
    print 'This should be false:', determine_if_test_is_already_done()

    # I know that these exist
    # ram,wl,RunTime(s),dbs,ld,nm,Throughput(ops/sec),RunTime(ms),lt,n,rf,t,nt
    # 2GB,c,778.69,1000,True,nodal, 1284.2080930794025, 778690.0,1,3,1,3,vm
    # 2GB,c,19.909,800,False,nodal, 502.2853985634638, 19909.0,1,1,1,4,vm
    ram,wl,dbs,ld,nm,lt,n,rf,t,nt = '2GB','c',1000,True,'nodal',1,3,1,3,'vm'

    print 'This should be true:'
    print determine_if_test_is_already_done(csvfilename='all.csv', num_nodes=n, t=t, w=wl, ld=ld, s=dbs,
                                      lt=lt, rf=1, ram=ram, node_type=nt, lan_type=nm)


# This function will rename files from a previous name and additional inputs
#  This function will then use the proper naming function
def return_proper_file_name(fname, path, num_nodes=0, t=9999, w='_UNK_', ld=False, s=0, lt=9999, rf=0, nt='unk', nm='unk',
                           ram='unk'):

    filename = fname

    # Parse the filename in order to get the parameters of the test:
    # x = filename.split('/')[-1].split("_")[0:5]
    x = filename.split('/')[-1]

    temp = re.search('(?<=_dbs)\d*(?=_)', x)
    if temp:
        try:
            s = temp.group()
        except:
            s = 'unk'

    temp = re.search('(?<=n)\d*(?=_)', x)
    if temp:
        try:
            num_nodes = temp.group()
        except:
            num_nodes = 'unk'

    temp = re.search('(?<=_t)\d*(?=_)', x)
    if temp:
        try:
            t = temp.group()
        except:
            t = 'unk'

    temp = re.search('(?<=_wl)\w*?(?=_)', x)
    if temp:
        try:
            wl = temp.group()
        except:
            wl = 'unk'

    temp = re.search('(?<=_rf)\d*(?=_)', x)
    if temp:
        try:
            rf = temp.group()
        except:
            rf = 'unk'

    temp = re.search('(?<=_lt)\d*(?=_)', x)
    if temp:
        try:
            lt = temp.group()
        except:
            lt = 'unk'

    temp = re.search('(?<=_ram)\w*(?=_)', x)
    if temp:
        ram = temp.group()
    else:
        ram = ram

    if '_ld_' in x:
        ld = True
    elif '_run_' in x:
        ld = False

    filename_prefix = '_nt' + str(nt) + \
                      '_nm' + str(nm) + \
                      '_n' + str(num_nodes) + \
                      '_ram' + str(ram) + \
                      '_wl' + str(w) + \
                      '_dbs' + str(int(s)) + \
                      '_rf' + str(rf) + \
                      '_t' + str(t) + \
                      '_lt' + str(lt)

    # There is no need to divide s by 1000 this time...that was only if saving from the original
    #  service.

    full_filename = path + filename_prefix
    if ld:
        full_filename += '_ld_'
    else:
        full_filename += '_run_'
    full_filename += 'res.txt'
    return full_filename


# Finish the end of the
def temp0():

    fname = 'n1_t5_wlf_dbs1000_run_res.txt'
    path = '/home/daniel/Documents/thesis/exp3/'
    directory = path + '*.txt'

    # Now do everything in the exp3 directory
    # exp3 was the 1GB RAM Virtual Machine (vm)
    for filename in glob.iglob(directory):
        fname = filename
        new_fname = return_proper_file_name(fname, path, num_nodes=0, t=9999, w='_UNK_', ld=False, s=0, lt=1, rf=0, nt='unk', nm='unk',
                               ram='unk')
        print fname, new_fname
    return 0


def bring_file_in(file_to_retrive, local_filename, username='pi', host_name='192.168.1.100', local_directory='/config/'):
    cmd = 'scp ' + username + '@' + host_name + ' ' +  ' /config/local/directory'
    run_command(cmd,cwd='.')
    return 0

def send_file_out(local_filename, out_filename):

    return 0


def print_cmd_copy_cassandra_config_files_from_main_node_to_other_nodes(list_of_nodes=['192.168.1.101', '192.168.1.102'], main_node='192.168.1.100'):
    for host in list_of_nodes:

        cmd = "scp pi@192.168.1.100:cassandra/apache-cassandra-3.9/conf/cassandra.yaml pi@" + host + ":cassandra/apache-cassandra-3.9/conf/"
        print cmd
        # run_command(cmd, cwd='.')

    return 0

def print_cmd_copy_cassandra_config_files_from_laptop_to_other_nodes(list_of_nodes=['192.168.1.100',
                                                                                    '192.168.1.101',
                                                                                    '192.168.1.102',
                                                                                    '192.168.1.103',
                                                                                    '192.168.1.104'],
                                                                     laptop_directory='grive/afit/thesis/lchcb/config/',
                                                                     config_filename='cassandra_config_files/rp_wireless/cassandra.yaml',
                                                                     verbose=True):
    if verbose:
        print "These can be copied into the terminal...then enter the password...."


    for host in list_of_nodes:

        cmd = "scp " + laptop_directory + config_filename + " pi@" + host + ":cassandra/apache-cassandra-3.9/conf/"
        print cmd
        print ''
        # run_command(cmd, cwd='.')

    return 0

# This is written to match what will be in the tables.
def predefined_field_names():
    x = ['ram',
         'nm',
         'nt',
         'rf',
         'lt',
         'n',
         't',
         'wl',
         'dbs']
    return x


def is_valid_ycsb_output(filename):
    # Begins with the assumption of validity
    is_valid = True
    for x in predefined_field_names():
        if x not in filename:
            is_valid = False
    return is_valid


def is_row_of_data(row):
    return len(row) == 3


# This is to standardize the headers throughout the program, so that they match.
def combine_headers_into_single_string(header_1, header_2):
    return header_1 + header_2

def get_record_parameter_portion(filename, ram='unk', nm='unk', nt='unk', rf='unk', lt='unk'):

    if is_valid_ycsb_output(filename):
        record = {}

        # Parse the filename in order to get the parameters of the test:
        x = filename.split('/')[-1]

        p = predefined_field_names()

        # These are all written individually to account for numeric and alphanumeric differences.
        for i in p:
            ii = re.search('(?<=_'+i+')\w*?(?=_)', x)
            if ii:
                record[i] = ii.group()
            else:
                print i, ' not found in ', x
        print record



def temp_change_file_names_old(i='n',
                           newi='nn',
                           directory='/home/daniel/grive/afit/thesis/lchcb/results/exp10*/*.txt',
                           time_to_sleep=0,
                           verbose=True):

    # directory='/home/daniel/grive/afit/thesis/lchcb/results/exp10*/*.txt'
    for filename in glob.iglob(directory):
        x = filename
        ii = re.search('(?<=_'+i+')\d*?(?=_)', x)
        if ii:
            iii = i + ii.group()
            iiii = newi + ii.group()
            xx = x.replace(iii, iiii)

            if verbose:

                print 'Replace existing file', x
                print '        with new file', xx
                print ''

                time.sleep(time_to_sleep)

                shutil.copy(x, xx)

    return 0


def temp_change_file_names(i='_ram1GB_',
                           newi='_ram2GB_',
                           directory='/home/daniel/grive/afit/thesis/lchcb/results/exp10_1vm2048/*.txt',
                           time_to_sleep=0,
                           verbose=True):

    # directory='/home/daniel/grive/afit/thesis/lchcb/results/exp10*/*.txt'
    for filename in glob.iglob(directory):
        x = filename
        xx = filename.replace(i, newi)

        if verbose:

            print 'Replace existing file', x
            print '        with new file', xx
            print ''

            time.sleep(time_to_sleep)

        if not (x==xx):
            shutil.copy(x, xx)


    return 0


# I need to rename some of the files; one-time bookkeeping
def archive_201612181814():
    temp_change_file_names(i='exp10_5rp1GB_',
                           newi='_',
                           directory='/home/daniel/grive/afit/thesis/lchcb/results/exp10_5rp1GB/*.txt',)

    temp_change_file_names(i='_ram1GB_',
                           newi='_ram2GB_',
                           directory='/home/daniel/grive/afit/thesis/lchcb/results/exp10_1vm2048/*.txt',)

    temp_change_file_names(i='_nn3_',
                           newi='_nn6_',
                           directory='/home/daniel/grive/afit/thesis/lchcb/results/exp10_6rp1GB/*.txt',)
    temp_change_file_names(i='_dbs0_',
                           newi='_dbs1000_',
                           directory='/home/daniel/grive/afit/thesis/lchcb/results/exp10_*/*.txt',)


def archive_201612181949():
    temp_change_file_names(i='_dbs0_',
                           newi='_dbs1000_',
                           directory='/home/daniel/grive/afit/thesis/lchcb/results/exp10_6rp1GB/*.txt',)



def archive_201612181927():
    temp_change_file_names(i='_nn3_',
                           newi='_nn5_',
                           directory='/home/daniel/grive/afit/thesis/lchcb/results/exp10_5rp1GB/*.txt',)
    temp_change_file_names(i='_dbs0_',
                           newi='_dbs1000_',
                           directory='/home/daniel/grive/afit/thesis/lchcb/results/exp10_5rp1GB/*.txt',)

def archive_201612181923():
    temp_change_file_names(i='_ram1GB_',
                       newi='_ram4GB_',
                       directory='/home/daniel/grive/afit/thesis/lchcb/results/exp10_1vm4096/*.txt',)




def archive_201612181906():
    temp_change_file_names(i='_ram1GB_',
                       newi='_ram2GB_',
                       directory='/home/daniel/grive/afit/thesis/lchcb/results/exp10_1vm2048/*.txt',)


# print_cmd_copy_cassandra_config_files_from_laptop_to_other_nodes()

def archive_201701090233():
    print_cmd_copy_cassandra_config_files_from_laptop_to_other_nodes(list_of_nodes=['192.168.1.100',
                                                                                        '192.168.1.101',
                                                                                        '192.168.1.102',
                                                                                        '192.168.1.103',
                                                                                        '192.168.1.104',
                                                                                        '192.168.1.109'],
                                                                         laptop_directory='grive/afit/thesis/lchcb/config/',
                                                                         config_filename='cassandra_config_files/rp_wired/cassandra.yaml',
                                                                         verbose=True)


def archive_201701090237():
    temp_change_file_names(i='_nn0_',
                           newi='_nn1_',
                           directory='/home/daniel/grive/afit/thesis/lchcb/results/exp13_1rp1GB/*.txt')

    temp_change_file_names(i='_nn0_',
                           newi='_nn2_',
                           directory='/home/daniel/grive/afit/thesis/lchcb/results/exp13_2rp1GB/*.txt')


def archive_201701091824():
    temp_change_file_names(i='_nn0_',
                           newi='_nn6_',
                           directory='/home/daniel/grive/afit/thesis/lchcb/results/exp12_6rp1GB/*.txt')


# import plotly.plotly as py
# fig = {'data': [{'x': [1, 2, 3], 'y': [3, 1, 5], 'type': 'bar'}]}
# py.image.save_as(figure_or_data=fig, filename='my_image.png', format='png')
# py.image.save_as(figure_or_data=fig, filename='my_image.jpeg', format='jpeg')
# py.image.save_as(figure_or_data=fig, filename='my_image.pdf', format='pdf')
# py.image.save_as(figure_or_data=fig, filename='my_image.svg', format='svg')

# from plotly.offline import plot
# import plotly.graph_objs as go

# plot([go.Scatter(x=[1, 2, 3], y=[3, 2, 6])], filename='my-graph.html')
# We can also download an image of the plot by setting the image parameter
# to the image format we want
# plot([go.Scatter(x=[1, 2, 3], y=[3, 2, 6])], filename='my-graph.html', image='svg', image_filename='my-graph')

def archive_201701231259():
    run_ycsb.experiment14_workloadi_utility_fn(ram='1GB',
                                                  experiment='16',
                                                  nodes='6',
                                                  node_type='rp',
                                                  link_type='wlan',
                                                  num_trials=30,
                                                  cluster_base_node_of_choice='192.168.1.130',
                                                  cluster_of_choice=['192.168.1.130',
                                                                     '192.168.1.131',
                                                                     '192.168.1.132',
                                                                     '192.168.1.133',
                                                                     '192.168.1.134',
                                                                     '192.168.1.139',],
                                                  cluster_description='rp_wireless_cluster',
                                                  verbose=True)


def archive_201701252204():
    filename = 'combined_results_revised.csv'
    directory='/home/daniel/grive/afit/thesis/lchcb/results/exp1[0,2,3,4,5,6]*/*.txt'
    ycsb_output_to_csv.start_new_file_and_append_records(directory=directory,
                                      csvfilename=filename)


def archive_201701260828():
    for j in [15, 16]:
        for k in [1,2,3,4,5,6]:
            temp_change_file_names(i='_nn0_',
                                   newi='_nn{}_'.format(k),
                                   directory='/home/daniel/grive/afit/thesis/lchcb/results/exp{}_{}rp1GB/*.txt'.format(j, k),
                                   time_to_sleep=1)


def archive_201701260848():
    research_questions_figure_generation.research_question_4_figure_4()
    research_questions_figure_generation.research_question_4_figure_5()
    research_questions_figure_generation.research_question_4_figure_6()
    research_questions_figure_generation.research_question_4_figure_7()
    research_questions_figure_generation.research_question_4_figure_8()
    research_questions_figure_generation.research_question_4_figure_9()
    research_questions_figure_generation.research_question_4_figure_10()


def archive_201701261128():
    run_ycsb.experiment14_workloadi_utility_fn(ram='2GB',
                                                  experiment='14',
                                                  nodes='6',
                                                  node_type='vm',
                                                  link_type='nodal',
                                                  num_trials=30,
                                                  cluster_base_node_of_choice='192.168.56.100',
                                                  cluster_of_choice=['192.168.56.100',
                                                                     '192.168.56.101',
                                                                     '192.168.56.102',
                                                                     '192.168.56.103',
                                                                     '192.168.56.104',
                                                                     '192.168.56.105',],
                                                  cluster_description='vm_cluster',
                                                  verbose=True)


def archive_201701261131():
    change_ram_for_all_machines(2048)


def archive_201701261216():
    run_ycsb.experiment14_workloadi_utility_fn(ram='2GB',
                                                  experiment='14',
                                                  nodes='5',
                                                  node_type='vm',
                                                  link_type='nodal',
                                                  num_trials=30,
                                                  cluster_base_node_of_choice='192.168.56.100',
                                                  cluster_of_choice=['192.168.56.100',
                                                                     '192.168.56.101',
                                                                     '192.168.56.102',
                                                                     '192.168.56.103',
                                                                     '192.168.56.104',
                                                                     '192.168.56.105',],
                                                  cluster_description='vm_cluster',
                                                  verbose=True)


def archive_201701261216():
    run_ycsb.experiment14_workloadi_utility_fn(ram='2GB',
                                                  experiment='14',
                                                  nodes='4',
                                                  node_type='vm',
                                                  link_type='nodal',
                                                  num_trials=30,
                                                  cluster_base_node_of_choice='192.168.56.100',
                                                  cluster_of_choice=['192.168.56.100',
                                                                     '192.168.56.101',
                                                                     '192.168.56.102',
                                                                     '192.168.56.103',
                                                                     '192.168.56.104',
                                                                     '192.168.56.105',],
                                                  cluster_description='vm_cluster',
                                                  verbose=True)

def archive_201701261306():
    run_ycsb.experiment14_workloadi_utility_fn(ram='2GB',
                                                  experiment='14',
                                                  nodes='3',
                                                  node_type='vm',
                                                  link_type='nodal',
                                                  num_trials=30,
                                                  cluster_base_node_of_choice='192.168.56.100',
                                                  cluster_of_choice=['192.168.56.100',
                                                                     '192.168.56.101',
                                                                     '192.168.56.102',
                                                                     '192.168.56.103',
                                                                     '192.168.56.104',
                                                                     '192.168.56.105',],
                                                  cluster_description='vm_cluster',
                                                  verbose=True)


def archive_201701261332():
    run_ycsb.experiment14_workloadi_utility_fn(ram='2GB',
                                                  experiment='14',
                                                  nodes='2',
                                                  node_type='vm',
                                                  link_type='nodal',
                                                  num_trials=30,
                                                  cluster_base_node_of_choice='192.168.56.100',
                                                  cluster_of_choice=['192.168.56.100',
                                                                     '192.168.56.101',
                                                                     '192.168.56.102',
                                                                     '192.168.56.103',
                                                                     '192.168.56.104',
                                                                     '192.168.56.105',],
                                                  cluster_description='vm_cluster',
                                                  verbose=True)

def archive_201701261401():
    run_ycsb.experiment14_workloadi_utility_fn(ram='2GB',
                                                  experiment='14',
                                                  nodes='1',
                                                  node_type='vm',
                                                  link_type='nodal',
                                                  num_trials=30,
                                                  cluster_base_node_of_choice='192.168.56.100',
                                                  cluster_of_choice=['192.168.56.100',
                                                                     '192.168.56.101',
                                                                     '192.168.56.102',
                                                                     '192.168.56.103',
                                                                     '192.168.56.104',
                                                                     '192.168.56.105',],
                                                  cluster_description='vm_cluster',
                                                  verbose=True)


def archive_201701261425():
    change_ram_for_all_machines(4096)


def archive_201701261426():
    run_ycsb.experiment14_workloadi_utility_fn(ram='4GB',
                                                  experiment='14',
                                                  nodes='1',
                                                  node_type='vm',
                                                  link_type='nodal',
                                                  num_trials=30,
                                                  cluster_base_node_of_choice='192.168.56.100',
                                                  cluster_of_choice=['192.168.56.100',
                                                                     '192.168.56.101',
                                                                     '192.168.56.102',
                                                                     '192.168.56.103',
                                                                     '192.168.56.104',
                                                                     '192.168.56.105',],
                                                  cluster_description='vm_cluster',
                                                  verbose=True)

def archive_201701261538():
    run_ycsb.experiment14_workloadi_utility_fn(ram='4GB',
                                                  experiment='14',
                                                  nodes='2',
                                                  node_type='vm',
                                                  link_type='nodal',
                                                  num_trials=30,
                                                  cluster_base_node_of_choice='192.168.56.100',
                                                  cluster_of_choice=['192.168.56.100',
                                                                     '192.168.56.101',
                                                                     '192.168.56.102',
                                                                     '192.168.56.103',
                                                                     '192.168.56.104',
                                                                     '192.168.56.105',],
                                                  cluster_description='vm_cluster',
                                                  verbose=True)

def archive_201701261555():
    run_ycsb.experiment14_workloadi_utility_fn(ram='4GB',
                                                  experiment='14',
                                                  nodes='3',
                                                  node_type='vm',
                                                  link_type='nodal',
                                                  num_trials=30,
                                                  cluster_base_node_of_choice='192.168.56.100',
                                                  cluster_of_choice=['192.168.56.100',
                                                                     '192.168.56.101',
                                                                     '192.168.56.102',
                                                                     '192.168.56.103',
                                                                     '192.168.56.104',
                                                                     '192.168.56.105',],
                                                  cluster_description='vm_cluster',
                                                  verbose=True)


def archive_201701261614():
    run_ycsb.experiment14_workloadi_utility_fn(ram='4GB',
                                                  experiment='14',
                                                  nodes='4',
                                                  node_type='vm',
                                                  link_type='nodal',
                                                  num_trials=30,
                                                  cluster_base_node_of_choice='192.168.56.100',
                                                  cluster_of_choice=['192.168.56.100',
                                                                     '192.168.56.101',
                                                                     '192.168.56.102',
                                                                     '192.168.56.103',
                                                                     '192.168.56.104',
                                                                     '192.168.56.105',],
                                                  cluster_description='vm_cluster',
                                                  verbose=True)

def archive_201701261644():
    run_ycsb.experiment14_workloadi_utility_fn(ram='4GB',
                                                  experiment='14',
                                                  nodes='5',
                                                  node_type='vm',
                                                  link_type='nodal',
                                                  num_trials=30,
                                                  cluster_base_node_of_choice='192.168.56.100',
                                                  cluster_of_choice=['192.168.56.100',
                                                                     '192.168.56.101',
                                                                     '192.168.56.102',
                                                                     '192.168.56.103',
                                                                     '192.168.56.104',
                                                                     '192.168.56.105',],
                                                  cluster_description='vm_cluster',
                                                  verbose=True)



def archive_201701261723():
    run_ycsb.experiment14_workloadi_utility_fn(ram='4GB',
                                                  experiment='14',
                                                  nodes='6',
                                                  node_type='vm',
                                                  link_type='nodal',
                                                  num_trials=30,
                                                  cluster_base_node_of_choice='192.168.56.100',
                                                  cluster_of_choice=['192.168.56.100',
                                                                     '192.168.56.101',
                                                                     '192.168.56.102',
                                                                     '192.168.56.103',
                                                                     '192.168.56.104',
                                                                     '192.168.56.105',],
                                                  cluster_description='vm_cluster',
                                                  verbose=True)


def archive_201701292228():
    run_ycsb.load_ycsb_usertable(num_records=None,
                        start_empty=False,
                        filename='temp_ld_res.txt',
                        cluster_base_node_of_choice='192.168.1.130',
                        cluster_of_choice=None,
                        workload='e',
                        verbose=True,
                        core_workload_insertion_retry_limit=15,
                        core_workload_insertion_retry_interval=15,
                        session=None,
                        threads=2)
    run_ycsb.workloads_from_abramova_paper(ram='1GB',
                                           experiment='12',
                                           nodes='6',
                                           node_type='rp',
                                           link_type='wlan',
                                           num_trials=30,
                                           do_workloads_a_and_c=False,
                                           do_workload_e=True,
                                           cluster_base_node_of_choice='192.168.1.130',
                                           verbose=True)

def archive_201701311436():
    run_ycsb.experiment10_workload_utility_fn_makeup(ram='1GB',
                                      experiment='10',
                                      nodes='5',
                                      node_type='vm',
                                      link_type='nodal',
                                      num_trials=30,
                                      cluster_base_node_of_choice='192.168.56.100',
                                      cluster_of_choice=None,
                                      cluster_description='vm_cluster',
                                      verbose=True,
                                      workloads=None)


def archive_201702020358():
    research_questions_figure_generation.research_question_1_figure_1()
    research_questions_figure_generation.research_question_1_figure_4()
    research_questions_figure_generation.research_question_1_figure_5()
    research_questions_figure_generation.research_question_1_figure_6()
    research_questions_figure_generation.research_question_1_figure_7()
    research_questions_figure_generation.research_question_1_figure_8()
    research_questions_figure_generation.research_question_1_figure_9()
    research_questions_figure_generation.research_question_1_figure_10()
    research_questions_figure_generation.research_question_2_figure_1()
    research_questions_figure_generation.research_question_2_figure_4()
    research_questions_figure_generation.research_question_2_figure_5()
    research_questions_figure_generation.research_question_2_figure_6()
    research_questions_figure_generation.research_question_2_figure_7()
    research_questions_figure_generation.research_question_2_figure_8()
    research_questions_figure_generation.research_question_2_figure_9()
    research_questions_figure_generation.research_question_2_figure_10()
    research_questions_figure_generation.research_question_3_figure_1()
    research_questions_figure_generation.research_question_3_figure_4()
    research_questions_figure_generation.research_question_3_figure_5()
    research_questions_figure_generation.research_question_3_figure_6()
    research_questions_figure_generation.research_question_3_figure_7()
    research_questions_figure_generation.research_question_3_figure_8()
    research_questions_figure_generation.research_question_3_figure_9()
    research_questions_figure_generation.research_question_3_figure_10()
    research_questions_figure_generation.research_question_4_figure_4()
    research_questions_figure_generation.research_question_4_figure_5()
    research_questions_figure_generation.research_question_4_figure_6()
    research_questions_figure_generation.research_question_4_figure_7()
    research_questions_figure_generation.research_question_4_figure_8()
    research_questions_figure_generation.research_question_4_figure_9()
    research_questions_figure_generation.research_question_4_figure_10()
    research_questions_figure_generation.research_question_1_figure_2()
    research_questions_figure_generation.research_question_1_figure_3()

archive_201702020358()