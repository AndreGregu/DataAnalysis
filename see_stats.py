import pstats

p = pstats.Stats('prof_char.prof')
p.strip_dirs().sort_stats('time').print_stats(10)