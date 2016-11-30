import csv
import glob

main_filename = 'all.csv'

def get_record(filename, ram):
    record = {
        'ram': ram,
        'n': 'unknown',
        't': 'unknown',
        'wl': 'unknown',
        'dbs': 'unknown'
    }
    # Parse the filename in order to get the parameters of the test:
    x = filename.split('/')[-1].split("_")[0:5]
    for i in x[0:4]:
        for j in record.keys():
            if j in i and '/home/' not in i:
                record[j] = i.translate(None, j)
    if 'ld' in x[4]:
        record['ld'] = True
    else:
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

def start_new_file_and_append_records(directory, csvfilename, ram):

    records=[]
    with open(csvfilename, 'wb') as csvfile:

        for filename in glob.iglob(directory):
            print filename
            records.append(get_record(filename, ram='2GB'))

        spamwriter = csv.DictWriter(csvfile, fieldnames=records[1].keys())
        spamwriter.writeheader()
        spamwriter.writerows(records)



def append_records(directory, csvfilename, ram):

    records=[]
    with open(csvfilename, 'ab') as csvfile:

        for filename in glob.iglob(directory):
            print filename
            records.append(get_record(filename, ram=ram))

        spamwriter = csv.DictWriter(csvfile, fieldnames=records[1].keys())
        spamwriter.writerows(records)



start_new_file_and_append_records('/home/daniel/Documents/thesis/exp2/*.txt', main_filename, ram='2GB')
append_records('/home/daniel/Documents/thesis/exp3/*.txt', main_filename, ram='1GB')

# print get_record('/home/daniel/Documents/thesis/exp3/n1_t5_wlf_dbs1000_run_res.txt', '2GB')