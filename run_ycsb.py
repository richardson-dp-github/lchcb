# from subprocess import call
import subprocess
import time
import datetime   # this works despite the red underline
import sys
import cassandra
from cassandra.cluster import Cluster
import os.path
import csv

# ----constants--------------------------------------

rp_wired_cluster_base_node = '192.168.1.100'

vm_cluster_base_node = '192.168.56.100'

vm_cluster = ['192.168.56.100', '192.168.56.101', '192.168.56.102',
              '192.168.56.103', '192.168.56.104', '192.168.56.105']
rp_wired_cluster = ['192.168.1.100']

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
# ---------------------------------------------------

# Connect to the cluster
cluster = Cluster(cluster_of_choice)
session = cluster.connect()

# Sensitivity Testing Involves Changing Something
cd_cmd = ['cd /home/daniel/Documents/thesis/YCSB/']

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


# This function will assign a standardized name according to various paramters
def standardized_file_name(path, num_nodes=0, t=9999, w='_UNK_', ld=False, s=0, lt=9999):
    filename_prefix = 'n' + str(num_nodes) + '_t' + str(t) + '_lt' + str(lt) + '_wl' + w + '_dbs' + str(s/1000)
    full_filename = path + filename_prefix
    if ld:
        full_filename += '_ld_'
    else:
        full_filename += '_run_'
    full_filename += 'res.txt'
    return full_filename


# This function assumes the user wants to overwrite any existing YCSB database
def create_ycsb_database(c=cluster, s=session, rf=3):
    s.execute("drop keyspace if exists ycsb")
    s.execute("create keyspace ycsb"
              "WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor': " + str(rf) + " }")
    s.execute("use ycsb")
    s.execute("create table usertable ("
              "y_id varchar primary key,"
              "field0 varchar,"
              "field1 varchar,"
              "field2 varchar,"
              "field3 varchar,"
              "field4 varchar,"
              "field5 varchar,"
              "field6 varchar,"
              "field7 varchar,"
              "field8 varchar,"
              "field9 varchar);")


# Taken from http://stackoverflow.com/questions/273192/how-to-check-if-a-directory-exists-and-create-it-if-necessary
def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)


# Run trials
def run_trials(trials=trials_default, db_sizes=db_sizes_default, workloads=workloads_default, trials_per_load=1,
               predicted_number_of_nodes=0,
               absolute_path_results='/home/daniel/Documents/thesis/experimental_results/'):
    ensure_dir(absolute_path_results)
    for t in trials:
        for s in db_sizes:
            for w in workloads:
                temp_load_file = absolute_path_results + 'temp_ld_res.txt'
                load_file = standardized_file_name(absolute_path_results,
                                                   predicted_number_of_nodes, t, w, ld=True, s=s)
                read_file = standardized_file_name(absolute_path_results,
                                                   predicted_number_of_nodes, t, w, ld=False, s=s)
                # This will run the experiment as long as the corresponding file does not already exist
                if not os.path.isfile(load_file):
                    session.execute("TRUNCATE ycsb.usertable")  # start off empty
                    cmd_ld0 = absolute_path_ycsb + ' load cassandra-cql ' \
                         '-p hosts="' + cluster_base_node_of_choice + '" ' \
                         '-P ' + absolute_path_workload + w +  \
                         ' -s ' \
                         '-p recordcount=' + str(s) + ' > ' + \
                         absolute_path_results + 'temp_ld_res.txt'
                    cmd_ld = [cmd_ld0]
                    run_command(cmd_ld, verbose=True)
                    temp_run_files = []
                    for tl in range(0, trials_per_load):
                        temp_run_file = absolute_path_results + 'temp_' + str(tl) + '_run_res.txt'
                        # temp_run_files.append(temp_run_file) # not used right now
                        cmd_run0 = absolute_path_ycsb + ' run  cassandra-cql ' \
                                  '-threads 1  ' \
                                  '-p hosts="' + cluster_base_node_of_choice + '" ' \
                                  '-P ' + absolute_path_workload + w + \
                                  ' -s ' \
                                  '-p operationcount=10000 ' \
                                  ' > ' + temp_run_file
                        cmd_run = [cmd_run0]
                        run_command(cmd_run, verbose=True)
                        count_of_nodes = count_nodes(temp_run_file, cluster_of_choice)
                        os.rename(temp_run_file, standardized_file_name(absolute_path_results,
                                                                        count_of_nodes, t, w, ld=False, s=s,
                                                                        lt=tl))
                    session.execute("TRUNCATE ycsb.usertable")  # clear for the next iteration

                    # Now rename the files
                    #   Rename the load file
                    count_of_nodes = count_nodes(temp_load_file, cluster_of_choice)
                    os.rename(temp_load_file, standardized_file_name(absolute_path_results,
                                                                     count_of_nodes, t, w, ld=True, s=s, lt=0))
                    #   The run files have already been renamed
                else:
                    print load_file, 'already exists'


# This actually runs the command in the terminal
#   This is a separate function for convenience so one doesn't have to remember to put the wait down every time.
def run_command(cmd, verbose=True):
    if verbose:
        print cmd
    p = subprocess.Popen(cmd, shell=True, cwd='/home/daniel/Documents/thesis/YCSB/')
    p.wait()


def test_run_trials():
    run_trials(trials=[1], db_sizes=[10000], workloads=['a', 'c', 'e'], trials_per_load=3,
               predicted_number_of_nodes=0, absolute_path_results='/home/daniel/Documents/thesis/exp6_testonly/')

test_run_trials()