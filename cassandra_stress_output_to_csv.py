import data
from analysis_forjp import compaction_type, compression_type, op_type, replication_factor, link_type
import csv
from extractdata import extract_data

# Copied and pasted from
# http://stackoverflow.com/questions/38987/how-to-merge-two-python-dictionaries-in-a-single-expression
def merge_two_dicts(x, y):
    """Given two dicts, merge them into a new dict as a shallow copy."""
    z = x.copy()
    z.update(y)
    return z


def get_field_names_from_keys(list_of_dictionaries):
    list_of_headers = []
    for d in list(list_of_dictionaries):
        for key in d.keys():
            if key not in list_of_headers:
                list_of_headers.append(key)
    return list_of_headers

def cassandra_stress_output_2_csv(csvfilename='oogabooga.csv',
                                  extract_from_html=False,
                                  html_file_from_which_to_extract='whateverwhatever.html'):

    # Perform extraction if desired.
    if extract_from_html:
        extract_data(html_file_from_which_to_extract)
    import data

    # Gather Data
    d = data
    list_of_dictionaries_analogue_to_convert_csv = []
    for r in d.stats['stats']:
        if 'revision' in r.keys():
            series_description = r['revision']  # This could also be 'command' or some combination

            d0 = {
                'compaction':   compaction_type(series_description),
                'compression':  compression_type(series_description),
                'op':           op_type(series_description),
                'network_type': link_type(series_description),
                'rf':           replication_factor(series_description)
            }

            # Here, create a list of dictionaries that can be inserted as rows...
            # r['intervals'] is a list of lists...
            keys = r['metrics']

            for interval in r['intervals']:  # These the actual points over time, not the total execution times
                values = interval
                d1 = dict(zip(keys, values))
                list_of_dictionaries_analogue_to_convert_csv.append(merge_two_dicts(d0, d1))

    fieldnames = merge_two_dicts(d0, d1).keys()

    with open(csvfilename, 'wb') as csvfile:

        spamwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        spamwriter.writeheader()
        spamwriter.writerows(list_of_dictionaries_analogue_to_convert_csv)

    return 0