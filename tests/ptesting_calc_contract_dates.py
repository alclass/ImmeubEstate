#!/usr/bin/env python3

import func.datefs.date_functions as dt

def call_for_test(inidatestr, n_years=1):
  print('-'*50)
  print(inidatestr, n_years)
  print('-'*50)
  inidate = dt.transform_datestr_to_date(inidatestr)
  inidate_findate_tuple = dt.return_inifindates_tuple_from_inidate(inidate, n_years)
  print(inidate_findate_tuple)
  inidate_findate_tuple = dt.return_inifindates_tuple_from_strinidate(inidatestr, n_years)
  print(inidate_findate_tuple)
  strinidate_findate_tuple = dt.return_strinifindates_tuple_from_strinidate(inidatestr, n_years)
  print(strinidate_findate_tuple)
  strinidate_findate_tuple = dt.return_strinifindates_tuple_from_inidate(inidate, n_years)
  print(strinidate_findate_tuple)


def ptest_tuple_year_round_inidate_findate():
  inidatestr = '2017-04-01'; n_years = 1
  call_for_test(inidatestr)
  inidatestr = '2013-05-15'
  call_for_test(inidatestr)
  n_years = 2
  call_for_test(inidatestr, n_years)
  n_years = 3
  call_for_test(inidatestr, n_years)
  n_years = -1
  call_for_test(inidatestr, n_years)
  n_years = 0
  call_for_test(inidatestr, n_years)

if __name__ == '__main__':
  ptest_tuple_year_round_inidate_findate()
