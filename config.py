import re
import time

is_wireless_test = False
vary_compaction = True
vary_compression = True
vary_bloom_filter = True
quick_test = True


##################################################################
##################################################################
##################################################################

if is_wireless_test:
    link_type = 'wireless'
else:
    link_type = 'wired'

def return_filename_appropriate_string(s):
    return re.sub(r'\W+', '', s)

def set_parameter_in_new_config_file(template_file, output_file, look_for, replace_with):
    with open(output_file, "wt") as fout:
        with open(template_file, "rt") as fin:
            for line in fin:
                fout.write(line.replace(look_for, replace_with))

# -----------------------------------------------------------------
# Parameters related to the current environment
# -----------------------------------------------------------------
absolute_path_cassandra_stress = '/home/daniel/Documents/thesis/apache-cassandra-3.9/tools/bin/'
# -----------------------------------------------------------------

# -----------------------------------------------------------------
# How the cluster is defined
# -----------------------------------------------------------------
seed_wireless_lan = '192.168.1.109'
seed_wired_lan = '192.168.1.100'
# -----------------------------------------------------------------

# -----------------------------------------------------------------
# Parameters related to sampling
# -----------------------------------------------------------------

intervals_of_interest = [4]

trial_duration_in_seconds = 30

num_trials = 5

ops_vals = [
    'ops\(simple1=1\)',
    'ops\(insert=1\)',
    # 'ops\(insert=5,simple1=5\)'
    ]

# output
graph_filename = 'test_5nodes_' + time.strftime('%Y%m%d%H%M') + '.html'
graph_title = '5 nodes '
graph_series_prefix = link_type + '_'
#  add the suffix within the trial
graph_command_prefix = '-graph file=' + graph_filename + ' ' + 'revision=' + graph_series_prefix

# -----------------------------------------------------------------

# -----------------------------------------------------------------
# Tunable Parameters
#   configurable in the YAML configuration file
# -----------------------------------------------------------------
bloom_filter_values = [0.05,
                       0.1,
                       0.15,
                       0.2,
                       0.25,
                       0.3,
                       0.35,
                       0.4,
                       0.45,
                       0.5,
                       0.55,
                       0.6,
                       0.65,
                       0.7,
                       0.75,
                       0.8,
                       0.85,
                       0.9,
                       0.95]

consistency_levels = ['one', 'two', 'three', 'quorum', 'local quorum', 'each quorum', 'all']
compression_values = ['', 'LZ4Compressor', 'SnappyCompressor', 'DeflateCompressor']

# Sub-parameters for compaction
min_sstable_size_values = [1, 2, 4, 8, 16, 32, 64, 128]
base_time_seconds_values = [3600, 1800, 900, 450, 225, 100, 50, 20, 5]        # default 1 hour
max_window_size_seconds_values = [86400, 10000, 1000, 100, 10]                # default 1 day

# -----------------------------------------------------------------


# -----------------------------------------------------------------
# Tunable Parameters
#   applicable to Cassandra running on the node
#   configurable in the Cassandra.yaml file, executes on initiation
#    of Cassandra
# -----------------------------------------------------------------
num_tokens = 256
# -----------------------------------------------------------------

####################################################################################################
# Write the configuration files ####################################################################
####################################################################################################

if quick_test:
    config_files = ['cqlstress-example.yaml']
else:
    config_files = []

    for i in min_sstable_size_values:
        out = 'cqlstress-compaction-stcs-minsstable-' + str(i).zfill(4) + '.yaml'
        set_parameter_in_new_config_file(template_file='cqlstress-compaction-stcs.yaml',output_file=out, look_for="'min_sstable_size' : 1", replace_with="'min_sstable_size' : " + str(i))
        config_files.append(out)

    for i in min_sstable_size_values:
        out = 'cqlstress-compaction-lcs-minsstable-' + str(i).zfill(4) + '.yaml'
        set_parameter_in_new_config_file(template_file='cqlstress-compaction-lcs.yaml',output_file=out, look_for="'sstable_size_in_mb' : 1", replace_with="'sstable_size_in_mb' : " + str(i))
        config_files.append(out)

    for i in base_time_seconds_values:
        for j in max_window_size_seconds_values:
            out = 'cqlstress-compaction-dtcs-base-' + str(i).zfill(5) + 'max-window-' + str(j).zfill(5) + '.yaml'
            set_parameter_in_new_config_file(template_file='cqlstress-compaction-dtcs.yaml',output_file=out, look_for="'base_time_seconds' : 20, 'max_window_size_seconds' : 120", replace_with="'base_time_seconds' : " + str(i) + ", 'max_window_size_seconds' : " + str(j))
            config_files.append(out)

config_files.append('cqlstress-replication_1.yaml')
config_files.append('cqlstress-replication_2.yaml')
config_files.append('cqlstress-replication_3.yaml')
####################################################################################################

####################################################################################################
# ARCHIVE ##########################################################################################
####################################################################################################

# Here are the raw commands
'''
cmd = [absolute_path_cassandra_stress + 'cassandra-stress ' \
      'write ' \
      'n=500000 ' \
      'no-warmup ' \
      '-node 192.168.1.105 ' \
      '-schema "replication(strategy=NetworkTopologyStrategy, existing=2)" ' \
      '-graph file=test.html title=test revision=test1 ']
'''

# Command Line: read, write, mixed
'''
for pop in [' -pop dist=UNIFORM\(1..10000\) ', ' -pop dist=EXP\(1..10\) ']:
    for schema in [' ']:
        for operation in ['write']:
            for node_option in config.node_option_list:
                for dist in ['']:
                    revision_name = (dist+node_option+pop+schema+operation).replace('-', '').replace(' ', '')
                    cmd = [absolute_path_cassandra_stress + 'cassandra-stress ' +
                           operation +
                           ' n=5000 '
                           ' no-warmup ' +
                           dist +
                           pop +
                           node_option +
                           schema +
                           '-graph file=test.html title=test revision=r_' +
                           revision_name]
                    print cmd
                    call(cmd, shell=True)
'''

'''
# User Option
# with the user option, you use ops and profile options, and the profile options has a number of options

cmd = [absolute_path_cassandra_stress + 'cassandra-stress ' +
       ' user '
       ' profile=cqlstress-example.yaml '
       ' duration=30s '
       ' ops\(insert=1\) '
       ' no-warmup '
       ' cl=QUORUM '
       ' -graph file=test2.html title=test revision=profile1 '
       ' -node 192.168.1.105 '
       ' -rate threads=200 '
       ' -log interval=1s '
       #' -sample report=15 '
       ]
print cmd
for trials in range(1, 50):
    cmd[0] = cmd[0].replace('profile1', 'trial' + str(trials))
    call(cmd, shell=True)

'''
'''
# create configuration files
config_files = []


compression_values = ['LZ4Compressor', 'SnappyCompressor', 'DeflateCompressor']

ops_vals = ['ops\(simple1=1\)',
            'ops\(insert=1\)']


# schema_option_list = ['-schema "replication(strategy=NetworkTopologyStrategy, existing=2)" ', ' ']
# The schema can be defined in the YAML configuration file.

options = {'command': '',
           'cl': '',
           'clustering': '',
           'duration': '',
           'err<': '',
           'n>': '',
           'n<': '',
           'n': '',
           'no-warmup': False,
           'ops': '',
           'profile': '',
           'truncate': '',
           'pop': {'seq': 1,
                   'no-wrap': False,
                   'read-lookback': 'DIST(?)',
                   'contents': ''},
           'insert': {
               'revisit': 'DIST(?)',
               'visits': 'DIST(?)',
               'partitions': 'DIST(?)',
               'batchtype': '?',
               'select-ratio': 'DIST(?)'
           },
           'col': {
               'n': 'DIST(?)',
               'slice': True,
               'super': '?',
               'comparator': '?',
               'size': 'DIST(?)',
               'timestamp': '?'
           },
           'rate': {
               'threads': 1,
               'thread_inclusive_min': 1,
               'thread_inclusive_max': 1,
               'limit': '?',
               'auto': True
           },
           'mode': {
               'thrift': {
                   'smart': False,
                   'user': '',
                   'password': ''
               },
               'native': {
                   'unprepared': '',
                   'cql3': '',
                   'compression': '',
                   'port': '',
                   'user': '',
                   'password': '',
                   'auth-provider': '',
                   'maxPending': '',
                   'connectionsPerHost': ''

               },
               'simplenative': {
                   'prepared': True,
                   'cql3': True,
                   'port': ''
               }
           },
           'errors': {
               'retries': '',
               'ignore': ''
           },
           'sample': {
               'history': '',
               'live': '',
               'report': ''
           },
           'schema': {
               'replication': '',
               'keyspace': '',
               'compaction': '',
               'compression': ''
           },
           'transport': {
               'factory': '',
               'truststore': '',
               'truststore-password': '',
               'ssl-protocol': '',
               'ssl-alg': '',
               'store-type': '',
               'ssl-ciphers': ''
           },
           'graph': {
               'file': '',
               'title': '',
               'revision': '',
           }
           }

def report_degrees_of_freedom():
    return 'This function has not been written yet.'

# Return the string for the Cassandra stress command based on options
def cassandra_stress_command(cassandra_stress_path):
    s = cassandra_stress_path + 'cassandra-stress '
    return s

'''