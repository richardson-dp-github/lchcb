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


def copy_cassandra_config_files_from_main_node_to_other_nodes(list_of_nodes=['192.168.1.101', '192.168.1.102'], main_node='192.168.1.100'):
    for host in list_of_nodes:

        cmd = "scp pi@192.168.1.100:cassandra/apache-cassandra-3.9/conf/cassandra.yaml pi@" + host + ":cassandra/apache-cassandra-3.9/conf/"
        print cmd
        run_command(cmd, cwd='.')

    return 0



copy_cassandra_config_files_from_main_node_to_other_nodes()
