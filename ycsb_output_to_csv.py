import csv
import glob
import re

main_filename = 'all.csv'


# This is written to match what will be in the tables.
def predefined_field_names():
    x = ['ram',
         'nm',
         'nt',
         'rf',
         'lt',
         'nn',
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

def get_record_parameter_portion(filename):

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
        return record


def get_field_names(directory='/home/daniel/grive/afit/thesis/lchcb/results/exp10*/*.txt',
                    verbose='True'):
    # field_names = []

    field_names = predefined_field_names()

    # Now, actually parse the file
    for filename in glob.iglob(directory):
        if verbose:
            print 'Parsing file for headers: ', filename
        with open(filename) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if is_row_of_data(row):
                    h = combine_headers_into_single_string(row[0], row[1])
                    if h not in field_names:
                        field_names.append(h)

    return field_names


# Returns an error if the filename is not properly formatted
# Returns a dictionary with the proper headers
# This assumes the operator is already under the impression that the filename fits this naming convention.
def get_record(filename):

    record = {}

    if is_valid_ycsb_output(filename):

        # Parse the filename in order to get the parameters of the test:
        x = filename.split('/')[-1]

        # These are all written individually to account for numeric and alphanumeric differences.
        record = get_record_parameter_portion(filename)

        # Now, actually parse the file
        with open(filename) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if is_row_of_data(row):
                    record[combine_headers_into_single_string(row[0], row[1])] = row[2]

    return record

def get_record_old_version(filename, ram='unk', nm='unk', nt='unk', rf='unk', lt='unk'):
    record = {
        'ram': ram,
        'nm': nm,
        'nt': nt,
        'rf': rf,
        'lt': lt,
        'n': 'unknown',
        't': 'unknown',
        'wl': 'unknown',
        'dbs': 'unknown'
    }
    # Parse the filename in order to get the parameters of the test:
    # x = filename.split('/')[-1].split("_")[0:5]
    x = filename.split('/')[-1]

    # These are all written individually to account for numeric and alphanumeric differences.
    record['dbs'] = re.search('(?<=_dbs)\d*(?=_)', x).group()
    record['n'] = re.search('(?<=n)\d*(?=_)', x).group()
    record['t'] = re.search('(?<=_t)\d*(?=_)', x).group()
    record['wl'] = re.search('(?<=_wl).(?=_)', x).group()

    if rf == 'unk':
        try:
            record['rf'] = re.search('(?<=_rf).(?=_)', x).group()
        except:
            record['rf'] = 'unk'

    if lt == 'unk':
        try:
            record['lt'] = re.search('(?<=_lt).(?=_)', x).group()
        except:
            record['lt'] = 'unk'

    temp = re.search('(?<=_ram)\w*(?=_)', x)
    if temp:
        record['ram'] = temp.group()
    else:
        record['ram'] = ram

    if '_ld_' in x:
        record['ld'] = True
    elif '_run_' in x:
        record['ld'] = False

    #Now, actually parse the file
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if ' RunTime(ms)' in row and '[OVERALL]' in row:
                record['RunTime(ms)'] = row[2]
            if '[OVERALL]' in row and ' Throughput(ops/sec)' in row:
                record['Throughput(ops/sec)'] = row[2]
            #if '[READ-MODIFY-WRITE]' in row and ' AverageLatency(us)' in row:
            #    record['[READ-MODIFY-WRITE]-AverageLatency(us)'] = row[2]

    try:
        record['RunTime(s)'] = float(record['RunTime(ms)']) / 1000
    except:
        print '---Error adding the RunTime in Seconds'

    return record


# This will start a new file and append records
# fieldnames is a list passed in
def start_new_file_and_append_records(directory, csvfilename='combined_results.csv',
                                      verbose=True):

    records=[]

    # get the fieldnames

    fieldnames = get_field_names(directory=directory)

    with open(csvfilename, 'wb') as csvfile:

        for filename in glob.iglob(directory):
            if verbose:
                print filename
            records.append(get_record(filename))  # this will append a dictionary

        spamwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        spamwriter.writeheader()
        spamwriter.writerows(records)


def start_new_file_and_append_records_old(directory, csvfilename, ram, nt='unk', nm='unk', rf='unk', lt='unk'):

    records=[]
    with open(csvfilename, 'wb') as csvfile:

        for filename in glob.iglob(directory):
            print filename
            records.append(get_record(filename, ram=ram, nt=nt, nm=nm, rf=rf, lt=lt))

        spamwriter = csv.DictWriter(csvfile, fieldnames=records[1].keys())
        spamwriter.writeheader()
        spamwriter.writerows(records)


def append_records(directory, csvfilename, ram='unk', nt='unk', nm='unk', rf='unk', lt='unk'):

    records=[]
    with open(csvfilename, 'ab') as csvfile:

        for filename in glob.iglob(directory):
            print filename
            records.append(get_record(filename, ram=ram, nt=nt, nm=nm, rf=rf, lt=lt))

        spamwriter = csv.DictWriter(csvfile, fieldnames=records[1].keys())
        spamwriter.writerows(records)


# This function will observe the results of the test and count the number of nodes
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


# This function will count all the nodes in a given directory
def count_nodes_in_all_reports(directory):
    for filename in glob.iglob(directory):
        print filename, count_nodes(filename, node_ips=['192.168.56.100', '192.168.56.101', '192.168.56.102',
                                                        '192.168.56.103', '192.168.56.104', '192.168.56.105'])


# This is a one-time operation that was desired by the author
def temp_1():
    start_new_file_and_append_records('/home/daniel/Documents/thesis/exp2/*.txt', main_filename, ram='2GB')
    append_records('/home/daniel/Documents/thesis/exp3/*.txt', main_filename, ram='1GB')


# This function is a way to test the count nodes function
def temp_2():
    count_nodes_in_all_reports('/home/daniel/Documents/thesis/exp2/*.txt')

# 2016-12-02
def temp_3_raspberry_pi_nodes():
    start_new_file_and_append_records('/home/daniel/Documents/thesis/exp4/*.txt', 'all_rp.csv', ram='1GB_rp')
    # append_records('/home/daniel/Documents/thesis/exp3/*.txt', main_filename, ram='1GB')

# 2016-12-02 This combines everything into all.csv
def temp_4():
    start_new_file_and_append_records('/home/daniel/Documents/thesis/exp2/*.txt', main_filename, ram='2GB', nt='vm', nm='nodal', rf=1, lt=1)
    append_records('/home/daniel/Documents/thesis/exp3/*.txt', main_filename, ram='1GB', nt='vm', nm='nodal', rf=1, lt=1)
    append_records('/home/daniel/Documents/thesis/exp4/*.txt', main_filename, ram='1GB', nt='rp', nm='eth', rf=1, lt=1)
    append_records('/home/daniel/Documents/thesis/exp7_makeup/*.txt', main_filename, ram='unk', nt='vm', nm='nodal', rf=1, lt=1)
    return 0


# append_records('/home/daniel/Documents/thesis/exp8*/*.txt', main_filename)

# filename='/home/daniel/grive/afit/thesis/lchcb/results/exp10_1rp1GB/_ntrp_nmeth_nn1_ram1GB_wla_dbs1000_rf1_t1_lt1_run_res.txt'
# print filename, get_record_parameter_portion(filename)

filename = 'combined_results_revised.csv'
directory='/home/daniel/grive/afit/thesis/lchcb/results/exp1[0,2,3]*/*.txt'
start_new_file_and_append_records(directory=directory,
                                  csvfilename=filename)
