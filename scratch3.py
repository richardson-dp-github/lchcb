import research_questions_analysis as rqa


for i in [1,3,6]:
    x = rqa.anova_for_variation_in_ram(csv_file='combined_results_revised.csv',
                                       measurement_of_interest = '[OVERALL] RunTime(ms)',
                                       d={'nt': 'vm',
                                          'wl': 'a',
                                          'nn': i})
    print i, x

x = rqa.anova_for_variation_in_ram(csv_file='combined_results_revised.csv',
                                   measurement_of_interest = '[OVERALL] RunTime(ms)',
                                   d={'nt': 'vm',
                                      'wl': 'a'
                                      })
print 's', x

print 'Last 20 Trials'

trials_of_interest = range(10, 30+1)

for i in [1,3,6]:
    x = rqa.anova_for_variation_in_ram(csv_file='combined_results_revised.csv',
                                       measurement_of_interest = '[OVERALL] RunTime(ms)',
                                       d={'nt': 'vm',
                                          'wl': 'a',
                                          'nn': i,
                                          't': trials_of_interest})
    print i, x

x = rqa.anova_for_variation_in_ram(csv_file='combined_results_revised.csv',
                                   measurement_of_interest = '[OVERALL] RunTime(ms)',
                                   d={'nt': 'vm',
                                      'wl': 'a',
                                      't': trials_of_interest})
print 's', x