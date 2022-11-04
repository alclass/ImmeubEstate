#!/usr/bin/env python3
import datetime

'''
json_ipca_indices_reader.py
'''
import fs.db.json_tofrom.general_json_reader_writer as jsongen
json_filename = 'ipca_indices_realestaterentsystem.json'

def read_all():
  '''
  Calling genread(json_filename) will return Python's data structure from the JSON data
  genread() will join the package's directory and json_filename, so that other packages may work with these modules
  '''
  return jsongen.readjson_n_return_python_data(json_filename)

def print_all():
  print('='*80)
  print ('json_data_reader from file [', json_filename, ']')
  print('='*80)
  pdict = read_all()
  for k in pdict:
    print(k, pdict[k])

def get_ipca_index_by_refmonthdate(refmonthdate):
  ipca_dict = read_all()
  year = refmonthdate.year
  month = refmonthdate.month
  try:
    year_str = str(year)
    ipca_year_months = ipca_dict[year_str]
    i = month - 1
    ipca_index = ipca_year_months[i]
    return ipca_index
  except KeyError:
    pass
  return None

def ptest():
  ipca_dict = read_all()
  for year in ipca_dict:
    print('-'*50)
    ipca_year_months = ipca_dict[year]
    print(year, '=>', ipca_year_months)

def ptest2():
  refmonthdate = datetime.date(2018, 10, 1)
  index = get_ipca_index_by_refmonthdate(refmonthdate)
  print (refmonthdate, '=>', index)
  refmonthdate = datetime.date(2004, 2, 1)
  index = get_ipca_index_by_refmonthdate(refmonthdate)
  print (refmonthdate, '=>', index)

def process():
  ptest()
  ptest2()

if __name__ == '__main__':
  process()
