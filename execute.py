# Cassandra-stress method
# This has been more or less deprecated in favor of using the YCSB

import config
import extractdata
import analysis_forjp
from subprocess import call
import time
import datetime   # this works despite the red underline
import sys

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

