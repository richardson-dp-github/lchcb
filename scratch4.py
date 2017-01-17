import research_questions_analysis as rqa
from Tkinter import Tk
from time import sleep

def send_to_clipboard(x):
    r = Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(x) # Debug and place pause marker after this line
    '''
    print "Text has been appended."
    for i in range(30,0,-5):
        sleep(5)
        print i, 'seconds remaining'
    '''
    r.destroy()
    print x


def summary_statistics_varying_RAM_for_1_3_and_6_node_configurations():
    rqa.set_display_format_for_floats(format_='{:.6g}'.format)
    x = ''

    for n in [1, 3, 6]:
        total_max, total_min, total_range = rqa.return_max_min_range_for_all_levels_of_ram(nn=n)
        caption = 'Summary Statistics for {}-Node Configuration. ' \
                  'All values represented fall between {} ms and {} ms, or rather within a span of {} ms.' \
                  ''.format(n, total_min, total_max, total_range)
        x += rqa.return_embedded_latex_tables(rqa.return_summary_statistics_for_vms(nn=n),
                                              caption=caption,
                                              label='summary_statistics_for_{}_config'.format(n))
    send_to_clipboard(x=x)

# rqa.set_display_format_for_floats(format_='{:.6g}'.format)
print rqa.return_summary_statistics_for_rp()



# The whole clipboard thing was from this http://stackoverflow.com/questions/579687/how-do-i-copy-a-string-to-the-clipboard-on-windows-using-python