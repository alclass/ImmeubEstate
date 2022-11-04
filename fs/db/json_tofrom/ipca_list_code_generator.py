#!/usr/bin/env python3
# import json
import datetime
from dateutil.relativedelta import relativedelta #, MO
'''
json_data_ipca_mounter.py
'''
json_file_data = []
json_filename = 'json_writer_ipca_indices.json'

ipca_reversed_2019out_2004jan = '''
0.1
-0.04
0.11
0.19
0.01
0.13
0.57
0.75
0.43
0.32
0.15
-0.21
0.45
0.48
-0.09
0.33
1.26
0.4
0.22
0.09
0.32
0.29
0.44
0.28
0.42
0.16
0.19
0.24
-0.23
0.31
0.14
0.25
0.33
0.38
0.3
0.18
0.26
0.08
0.44
0.52
0.35
0.78
0.61
0.43
0.9
1.27
0.96
1.01
0.82
0.54
0.22
0.62
0.79
0.74
0.71
1.32
1.22
1.24
0.78
0.51
0.42
0.57
0.25
0.01
0.4
0.46
0.67
0.92
0.69
0.55
0.92
0.54
0.57
0.35
0.24
0.03
0.26
0.37
0.55
0.47
0.6
0.86
0.79
0.6
0.59
0.57
0.41
0.43
0.08
0.36
0.64
0.21
0.45
0.56
0.5
0.52
0.43
0.53
0.37
0.16
0.15
0.47
0.77
0.79
0.8
0.83
0.63
0.83
0.75
0.45
0.04
0.01
0
0.43
0.57
0.52
0.78
0.75
0.37
0.41
0.28
0.24
0.15
0.24
0.36
0.47
0.48
0.2
0.55
0.48
0.28
0.36
0.45
0.26
0.28
0.53
0.74
0.79
0.55
0.48
0.49
0.54
0.74
0.38
0.3
0.18
0.47
0.24
0.28
0.28
0.25
0.37
0.44
0.44
0.48
0.31
0.33
0.21
0.05
0.19
-0.21
0.1
0.21
0.43
0.41
0.59
0.36
0.55
0.75
0.35
0.17
0.25
-0.02
0.49
0.87
0.61
0.59
0.58
0.86
0.69
0.44
0.33
0.69
0.91
0.71
0.51
0.37
0.47
0.61
0.76
'''
monthly_ipcas = ipca_reversed_2019out_2004jan.split('\n')
flambda = lambda x : not x == ''
monthly_ipcas = list(filter(flambda, monthly_ipcas))
monthly_ipcas.reverse() # (not used) pop is already reversed, no need to use a reverse()
ini_refmonthdate = datetime.date(year=2004, month=1, day=1)
ini_year = 2004
refmonthdate = datetime.date(year=ini_year, month=1, day=1)
tuplelist = []
for ipca_months_index in monthly_ipcas:
  datum = (refmonthdate, ipca_months_index)
  tuplelist.append(datum)
  refmonthdate = refmonthdate + relativedelta(months=+1)

#for tupl in tuplelist:
  #print (tupl)
ongoing_year = ini_year
year_line = 'monthly_ipca_by_year_dict[%s] = [ '
ongoing_line = year_line %ini_year
lines = []; idate = None
for tupl in tuplelist:
  idate = tupl[0]; index = tupl[1]
  if idate.year == ongoing_year:
    ongoing_line += '%s, ' %index
  else:
    ongoing_line = ongoing_line[ :-2]
    ongoing_line += ']'
    lines.append(ongoing_line)
    ongoing_year += 1
    ongoing_line = year_line %ongoing_year
    ongoing_line += '%s, ' %index

if idate is not None and idate.month < 12:
  if len(ongoing_line) > 3:
    ongoing_line = ongoing_line[:-2]
  ongoing_line += ']'
  lines.append(ongoing_line)

for line in lines:
  print (line)



