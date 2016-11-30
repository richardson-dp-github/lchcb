# from subprocess import call
import subprocess
import time
import datetime   # this works despite the red underline
import sys
import cassandra
from cassandra.cluster import Cluster
import os.path

# ---------------------------------------------------

rp_wired_cluster_base_node = '192.168.1.100'

vm_cluster = ['192.168.56.100']
rp_wired_cluster = ['192.168.1.100']

# ---------------------------------------------------

cluster_of_choice = rp_wired_cluster
cluster_base_node_of_choice = rp_wired_cluster_base_node
num_nodes = 1  # This only affects the naming convention

# ---------------------------------------------------
cluster = Cluster(cluster_of_choice)

session = cluster.connect()





absolute_path_ycsb = '/home/daniel/Documents/thesis/YCSB/bin/ycsb'
absolute_path_results = '/home/daniel/Documents/thesis/exp4/'
absolute_path_workload = '/home/daniel/Documents/thesis/YCSB/workloads/workload'



workloads = ['a', 'c', 'f']
db_sizes = [500000, 800000, 1000000]
trials = [1, 2, 3, 4, 5]
mv_cmd = ['mvn -DskipTests package dependency:build=classpath']
cd_cmd = ['cd /home/daniel/Documents/thesis/YCSB/']

# print mv_cmd
# call(mv_cmd, shell=True)
for t in trials:
    for s in db_sizes:
        for w in workloads:
            filename_prefix = 'n' + str(num_nodes) + '_t' + str(t) + '_wl' + w + '_dbs' + str(s/1000)
            load_file = absolute_path_results + filename_prefix + '_ld_res.txt'
            read_file = absolute_path_results + filename_prefix + '_run_res.txt'
            if not os.path.isfile(load_file):
                cmd_ld0 = absolute_path_ycsb + ' load cassandra-cql ' \
                     '-p hosts="' + cluster_base_node_of_choice + '" ' \
                     '-P ' + absolute_path_workload + w +  \
                     ' -s ' \
                     '-p recordcount=' + str(s) + ' > ' + \
                     absolute_path_results + filename_prefix + '_ld_res.txt'
                cmd_run0 = absolute_path_ycsb + ' run  cassandra-cql ' \
                          '-threads 1  ' \
                          '-p hosts="' + cluster_base_node_of_choice + '" ' \
                          '-P ' + absolute_path_workload + w + \
                          ' -s ' \
                          '-p operationcount=10000 ' \
                          ' > ' + absolute_path_results + filename_prefix + '_run_res.txt'
                cmd_ld = [cmd_ld0]
                cmd_run = [cmd_run0]
                session.execute("TRUNCATE ycsb.usertable")
                for cmd in [cmd_ld, cmd_run]:
                    print cmd
                    p=subprocess.Popen(cmd, shell=True, cwd='/home/daniel/Documents/thesis/YCSB/')
                    p.wait()
            else:
                print load_file, 'already exists'




'''
absolute_path_cassandra_stress = '/home/daniel/Documents/thesis/apache-cassandra-3.9/tools/bin/'

# Calculate duration of test
total_duration_of_test_seconds = 0

total_duration_of_test_seconds += config.trial_duration_in_seconds * \
                                config.num_trials * len(config.config_files)\
                                * len(config.ops_vals)

print 'This test is estimated to last ....', datetime.timedelta(seconds=total_duration_of_test_seconds)

time.sleep(5.5)
try:
    for trial in range(1, config.num_trials+1):  # This staggers the trials to mitigate interference effects
        for cf in config.config_files:
            for interval in config.intervals_of_interest:
                for o in config.ops_vals:
                    cmd = [absolute_path_cassandra_stress + 'cassandra-stress ' +
                           ' user '
                           ' profile=' + cf +
                           ' duration=' + str(config.trial_duration_in_seconds) + 's ' +
                           o +
                           ' no-warmup ' +
                           config.graph_command_prefix + config.return_filename_appropriate_string(cf+o) + ' '
                           ' -node ' + config.seed_wired_lan + ' '
                           ' -rate threads=200 '
                           ' -log interval=' + str(interval) + 's '
                           ]
                    print cmd
                    print 'Trial', str(trial), 'of', str(config.num_trials)
                    call(cmd, shell=True)
except:
    print 'error, could not run trials'
    sys.exit(1)

# finally, extract the data to a python file
extractdata.extract_data(file0=config.graph_filename)

# then run the analysis, graphs, etc. that are specified
analysis_forjp.graph_wired_only_compaction()
'''
