# from subprocess import call
import subprocess
import time
import datetime   # this works despite the red underline
import sys
import cassandra
from cassandra.cluster import Cluster
import os.path
import glob
import pandas as pd
import csv

# ----constants--------------------------------------

rp_wired_cluster_base_node = '192.168.1.100'

vm_cluster_base_node = '192.168.56.100'

vm_cluster = ['192.168.56.100', '192.168.56.101', '192.168.56.102',
              '192.168.56.103', '192.168.56.104', '192.168.56.105']
rp_wired_cluster = ['192.168.1.100', '192.168.1.101', '192.168.1.102']

# -------configuration-------------------------------

cluster_of_choice = vm_cluster
cluster_base_node_of_choice = vm_cluster_base_node

num_nodes = 1  # This only affects the naming convention

sensitivity_testing = True

workloads_default = ['a', 'c', 'f']
db_sizes_default = [500000, 800000, 1000000]
trials_default = [1, 2, 3, 4, 5]


absolute_path_ycsb = '/home/daniel/Documents/thesis/YCSB/bin/ycsb'

absolute_path_workload = '/home/daniel/Documents/thesis/YCSB/workloads/workload'

absolute_path_here = '/home/daniel/grive/afit/thesis/lchcb/'
# ---------------------------------------------------

# Connect to the cluster
cluster = Cluster(cluster_of_choice)
session = cluster.connect()

# Sensitivity Testing Involves Changing Something
cd_cmd = ['cd /home/daniel/Documents/thesis/YCSB/']


# connect to the cluster
def begin_cassandra_cluster(cluster_of_choice):
    cluster = Cluster(cluster_of_choice)
    session = cluster.connect()

    return cluster, session


# based on the configuration
def select_cluster(network_type=None):
    rp_wired_cluster_base_node = '192.168.1.100'
    rp_wired_cluster = ['192.168.1.100', '192.168.1.101', '192.168.1.102']

    vm_cluster_base_node = '192.168.56.100'
    vm_cluster = ['192.168.56.100', '192.168.56.101', '192.168.56.102',
                  '192.168.56.103', '192.168.56.104', '192.168.56.105']

    rp_wireless_cluster_base_node = '192.168.1.100'
    rp_wireless_cluster = ['192.168.1.100', '192.168.1.101', '192.168.1.102']

    cluster = None
    cluster_base_node = None

    if network_type=='vm_cluster':
        cluster = vm_cluster
        cluster_base_node = vm_cluster_base_node
    elif network_type=='rp_wireless_cluster':
        cluster = rp_wireless_cluster
        cluster_base_node = rp_wireless_cluster_base_node
    elif network_type=='rp_wired_cluster':
        cluster = rp_wired_cluster
        cluster_base_node = rp_wired_cluster_base_node

    return cluster, cluster_base_node


# This function will observe the results of the test and count the number of nodes
# The point of this function is so that one does not have to pre-coordinate the number of nodes prior to running the
#   script.  The output should report.
# I was unable to find
def count_nodes(original_output_file, node_ips):
    filename = original_output_file
    count = 0
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            for item in row:
                for ip in node_ips:
                    if ip in item:
                        count += 1
    return count


# This function will assign a standardized name according to various parameters
def standardized_file_name(path, num_nodes=0, t=9999, w='_UNK_', ld=False, s=0, lt=9999, rf=0, nt='unk', nm='unk',
                           ram='unk'):
    filename_prefix = '_nt' + nt + \
                      '_nm' + nm + \
                      '_nn' + str(num_nodes) + \
                      '_ram' + str(ram) + \
                      '_wl' + w + \
                      '_dbs' + str(s/1000) + \
                      '_rf' + str(rf) + \
                      '_t' + str(t) + \
                      '_lt' + str(lt)

    full_filename = path + filename_prefix
    if ld:
        full_filename += '_ld_'
    else:
        full_filename += '_run_'
    full_filename += 'res.txt'
    return full_filename


# This function assumes the user wants to overwrite any existing YCSB database
def create_ycsb_database(c=cluster, s=session, rf=3, time_to_sleep=1):
    cmd_drop_keyspace = "drop keyspace if exists ycsb"
    cmd_create_keyspace = "create keyspace if not exists ycsb " \
                          "WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor': " + str(rf) + " }"
    create_table_cmd = "create table if not exists ycsb.usertable (" \
                       "y_id varchar primary key," \
                       "field0 varchar," \
                       "field1 varchar," \
                       "field2 varchar," \
                       "field3 varchar," \
                       "field4 varchar," \
                       "field5 varchar," \
                       "field6 varchar," \
                       "field7 varchar," \
                       "field8 varchar," \
                       "field9 varchar);"
    print "Executing Command", cmd_drop_keyspace
    time.sleep(time_to_sleep)
    msg0 = s.execute(cmd_drop_keyspace)
    print "Executing Command", cmd_create_keyspace
    time.sleep(time_to_sleep)
    msg1 = s.execute(cmd_create_keyspace)
    time.sleep(time_to_sleep)
    print "Executing Command", create_table_cmd, '...'
    time.sleep(time_to_sleep)
    msg2 = s.execute(create_table_cmd)


# Taken from http://stackoverflow.com/questions/273192/how-to-check-if-a-directory-exists-and-create-it-if-necessary
def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)


# Prerequisites: The YCSB keyspace and ycsb.usertable already need to be created
def load_ycsb_usertable(num_records=10,
                        start_empty=False,
                        absolute_path_ycsb=absolute_path_ycsb,
                        absolute_path_results=absolute_path_here+'results/',
                        filename='temp_ld_res.txt',
                        verbose=True):
    ensure_dir(absolute_path_results)
    s = num_records
    core_workload_insertion_retry_limit=15
    core_workload_insertion_retry_interval=15
    w = 'a'    # for loading, it doesn't matter, one of workload a through f just has to be selected

    if start_empty:
        if verbose:
            print "Truncating table usertable in keyspace ycsb..."
        session.execute("TRUNCATE ycsb.usertable")  # start off empty

    output_file = absolute_path_results + filename

    cmd_ld0 = absolute_path_ycsb + \
              ' load cassandra-cql ' \
              ' -p hosts="' + cluster_base_node_of_choice + '" ' \
              ' -p core_workload_insertion_retry_limit=' + str(core_workload_insertion_retry_limit) + ' ' \
              ' -p core_workload_insertion_retry_interval=' + str(core_workload_insertion_retry_interval) + ' ' \
              ' -P ' + absolute_path_workload + w +  \
              ' -s ' \
              ' -p recordcount=' + str(s) + ' > ' + \
              output_file

    cmd_ld = [cmd_ld0]

    run_command(cmd_ld, verbose=True)

    return output_file   # so it can be renamed


# Run trials
def run_trials(trials=trials_default, db_sizes=db_sizes_default, workloads=workloads_default, trials_per_load=1,
               predicted_number_of_nodes=0,
               absolute_path_results='/home/daniel/Documents/thesis/experimental_results/',
               replication_factor_for_filename=0,
               ram_for_filename='unk',
               node_type_for_filename='unk',
               lan_type_for_filename='unk',
               reload_once_per_trial=False,
               time_to_sleep=2,
               table_is_already_loaded=True,
               num_ops_per_trial=10000,
               verbose=True):

    ensure_dir(absolute_path_results)

    for s in db_sizes:
        if not table_is_already_loaded:
            if verbose:
                print "Program has been passed parameter table_is_already_loaded as", table_is_already_loaded
                print "Executing initial load..."
                print "Initial load is set to truncate table usertable in keyspace ycsb prior to loading..."
            load_ycsb_usertable(num_records=s, start_empty=True)
        for t in trials:
            if verbose:
                print "************************************************************************************"
                print "************************ STARTING TRIAL " + str(t) + " ******************************"
                print "************************************************************************************"
            time.sleep(time_to_sleep)
            for w in workloads:
                if verbose:
                    print "    ****************************************************************************"
                    print "    **** STARTING TRIAL " + str(t) + "  WORKLOAD " + str(w) + " **************************"
                    print "    ****************************************************************************"
                time.sleep(time_to_sleep)
                if reload_once_per_trial:

                    if verbose:
                        print 'User has selected reload_once_per_trial to be set to ', \
                              reload_once_per_trial, \
                              '...performing reload before moving on to read operations...'
                        time.sleep(time_to_sleep)

                    # Run the load operation
                    output_file = load_ycsb_usertable(num_records=s, start_empty=True)

                    # Now rename the files
                    #   Rename the load file
                    count_of_nodes = count_nodes(output_file, cluster_of_choice)
                    os.rename(output_file,
                              standardized_file_name(
                                  absolute_path_results,
                                  count_of_nodes, t, w, ld=True, s=s,
                                  rf=replication_factor_for_filename,
                                  nt=node_type_for_filename, nm=lan_type_for_filename, lt=1,
                                  ram=ram_for_filename)
                              )

                else:
                    if verbose:
                        print 'reload_once_per_trial is set to ', reload_once_per_trial, '...skipping reload' \
                                                                                         ' and moving on to' \
                                                                                         ' read operations...'

                # sub-trials : read operations
                for tl in range(1, trials_per_load + 1):
                    time.sleep(time_to_sleep)

                    read_file = standardized_file_name(absolute_path_results,
                                                       predicted_number_of_nodes, t, w, ld=False, s=s,
                                                       rf=replication_factor_for_filename,
                                                       nt=node_type_for_filename, nm=lan_type_for_filename, lt=tl,
                                                       ram=ram_for_filename)

                    temp_run_file = absolute_path_results + 'temp_' + str(tl) + '_run_res.txt'

                    cmd_run0 = absolute_path_ycsb + ' run  cassandra-cql ' \
                              '-threads 1  ' \
                              '-p hosts="' + cluster_base_node_of_choice + '" ' \
                              '-P ' + absolute_path_workload + w + \
                              ' -s ' \
                              '-p operationcount=' + str(num_ops_per_trial) + ' ' \
                              ' > ' + temp_run_file

                    cmd_run = [cmd_run0]

                    run_command(cmd_run, verbose=True)

                    count_of_nodes = count_nodes(temp_run_file, cluster_of_choice)

                    os.rename(temp_run_file, standardized_file_name(absolute_path_results,
                                                                    count_of_nodes, t, w, ld=False, s=s,
                                                                    rf=replication_factor_for_filename,
                                                                    nt=node_type_for_filename,
                                                                    nm=lan_type_for_filename, lt=tl,
                                                                    ram=ram_for_filename))


# This actually runs the command in the terminal
#   This is a separate function for convenience so one doesn't have to remember to put the wait down every time.
def run_command(cmd, verbose=True):
    if verbose:
        print cmd
    p = subprocess.Popen(cmd, shell=True, cwd='/home/daniel/Documents/thesis/YCSB/')
    p.wait()


def test_run_trials():
    run_trials(trials=[1], db_sizes=[10000], workloads=['a'], trials_per_load=2,
               predicted_number_of_nodes=0, absolute_path_results='/home/daniel/Documents/thesis/exp6_testonly/')


def test_is_already_done(csvfilename='all.csv', num_nodes=0, t=9999, w='_UNK_', ld=False, s=0,
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



def vary_replication():
    for i in [1]:
        try:
            print 'Creating the test ycsb database...'
            create_ycsb_database(s=session, rf=i)
        except:
            try:
                x = 5
                print "Second attempt at creating database...sleeping for " + str(x) + " seconds"
                time.sleep(x)
                create_ycsb_database(s=session, rf=i)
            except:
                try:
                    print "Third attempt at creating database...sleeping for " + str(x*x) + " seconds"
                    time.sleep(x*x)
                    create_ycsb_database(s=session, rf=i)
                except:
                    print "Tried sleeping twice...not working"

        run_trials(trials=range(1, 31),    # arbitrarily chosen, need a good number to compare replication
               db_sizes=[1000000],     # seems like a fair number, no need to vary too much, just has to be big
                                      #    enough, this will be the operations for the load
               workloads=['a', 'c', 'e'],  # to possible compare against others
               trials_per_load=1,    # may throw 9 away if there is a significant cache effect into 10 trials
               predicted_number_of_nodes=3,
               absolute_path_results='/home/daniel/grive/afit/thesis/lchcb/results/exp9_3rps_2dtry/',
               replication_factor_for_filename=i,
               node_type_for_filename='rp',
               lan_type_for_filename='eth',
               ram_for_filename='1GB',
            )


# This will run the workloads.
# The actual nature of the cluster (what type of nodes, etc.) must be controlled outside of this function
def workloads_from_abramova_paper(verbose=True):

    ram = '1GB'
    experiment = '10'
    nodes = '1'
    node_type = 'vm'
    link_type = 'nodal'
    pathname = '/home/daniel/grive/afit/thesis/lchcb/results/exp' + experiment + '_' + nodes + node_type + ram + '/'
    num_trials = 30
    # Workload e adds records, so the timing is different
    do_workloads_a_and_c = False
    do_workload_e = True
    if verbose:
        print "Running..."
        print "Results will be saved in directory", pathname
        time.sleep(10)

    if do_workloads_a_and_c:

        run_trials(trials=range(1, num_trials + 1),    # arbitrarily chosen, need a good number to compare replication
                   db_sizes=[1000000],     # this is just for naming
                   workloads=['a', 'c'],  # to possible compare against others
                   trials_per_load=1,    # may throw 9 away if there is a significant cache effect into 10 trials
                   predicted_number_of_nodes=int(nodes),
                   absolute_path_results=pathname,
                   replication_factor_for_filename=1,
                   node_type_for_filename=node_type,
                   lan_type_for_filename=link_type,
                   ram_for_filename=ram,

                   )

    if do_workload_e:

        run_trials(trials=range(1, num_trials + 1),    # arbitrarily chosen, need a good number to compare replication
                   db_sizes=[1000000],     # seems like a fair number, no need to vary too much, just has to be big
                                          #    enough, this will be the operations for the load
                   workloads=['e'],  # to possible compare against others
                   trials_per_load=1,    # may throw 9 away if there is a significant cache effect into 10 trials
                   predicted_number_of_nodes=1,
                   absolute_path_results=pathname,
                   replication_factor_for_filename=1,
                   node_type_for_filename=node_type,
                   lan_type_for_filename=link_type,
                   ram_for_filename=ram,
                   reload_once_per_trial=False,

                   )

    return 0

def experiment_11_cache_effect():


    verbose = True
    ram = '1GB'
    experiment = '11'
    nodes = '6'
    node_type = 'vm'
    link_type = 'nodal'
    pathname = '/home/daniel/grive/afit/thesis/lchcb/results/exp' + experiment + '_' + nodes + node_type + ram + '/'
    # Workload e adds records, so the timing is different
    do_load = True
    do_workloads_a_and_c = True
    do_workload_e = True
    num_trials = 120
    num_ops_per_trial = 1000


    if verbose:
        print "Running Experiment 11: Exploring Cache Effect"

    if do_load:
        load_ycsb_usertable(num_records=1000000, start_empty=True, filename='load_file_' + datetime.datetime.now().strftime("%y%m%d%I%M"))


    if verbose:
        print "Running..."
        print "Results will be saved in directory", pathname
        time.sleep(10)

    if do_workloads_a_and_c:

        run_trials(trials=range(1, num_trials + 1),    # arbitrarily chosen, need a good number to compare replication
                   db_sizes=[1000000],     # this is just for naming
                   workloads=['a', 'c'],  # to possible compare against others
                   trials_per_load=1,    # may throw 9 away if there is a significant cache effect into 10 trials
                   predicted_number_of_nodes=int(nodes),
                   absolute_path_results=pathname,
                   replication_factor_for_filename=1,
                   node_type_for_filename=node_type,
                   lan_type_for_filename=link_type,
                   ram_for_filename=ram,
                   num_ops_per_trial=num_ops_per_trial
                   )

    if do_workload_e:

        run_trials(trials=range(1, num_trials + 1),    # arbitrarily chosen, need a good number to compare replication
                   db_sizes=[1000000],     # seems like a fair number, no need to vary too much, just has to be big
                                          #    enough, this will be the operations for the load
                   workloads=['e'],  # to possible compare against others
                   trials_per_load=1,    # may throw 9 away if there is a significant cache effect into 10 trials
                   predicted_number_of_nodes=int(nodes),
                   absolute_path_results=pathname,
                   replication_factor_for_filename=1,
                   node_type_for_filename=node_type,
                   lan_type_for_filename=link_type,
                   ram_for_filename=ram,
                   reload_once_per_trial=False,
                   num_ops_per_trial=num_ops_per_trial
                   )

    return 0



experiment_11_cache_effect()

