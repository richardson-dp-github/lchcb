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




# rqa.set_display_format_for_floats(format_='{:.6g}'.format)
'''
x= rqa.return_embedded_latex_tables(latex_table_as_string=rqa.return_summary_statistics_for_rp(),
                                       label='rp_summary',
                                       caption='These are the summary statistics for Workload A '
                                               'executed on the Raspberry Pi wired local area network')
'''



# summary_statistics_varying_RAM_for_1_3_and_6_node_configurations(wl='c')

# print rqa.anova_for_variation_in_ram(wl='c', nn=1)
# print rqa.anova_for_variation_in_ram(wl='c', nn=3)
# print rqa.anova_for_variation_in_ram(wl='c', nn=6)
# print rqa.summary_statistics_rp_for_1_3_and_6_node_configurations(wl='c')

# send_to_clipboard(x)

# The whole clipboard thing was from this http://stackoverflow.com/questions/579687/how-do-i-copy-a-string-to-the-clipboard-on-windows-using-python

