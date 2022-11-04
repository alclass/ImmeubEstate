#!/usr/bin/env python3
import calendar, copy, datetime
from dateutil.relativedelta import relativedelta #, MO
'''
docs
'''

def get_payment_id_from_contrid_n_refmonth(contract_id, refmonthdatestr):
  refmonthdatestr = refmonthdatestr.replace('-','')
  return refmonthdatestr + contract_id

def check_n_filter_p_date(p_date):
  if p_date is None:
    p_date = datetime.date.today()
    return p_date
  if type(p_date) in [datetime.date, datetime.datetime]:
    return p_date
  try:
    p_date = datetime.datetime.strptime(p_date, '%Y-%m-%d')
    return p_date
  except Exception:
    p_date = datetime.date.today()
  return p_date

def add_months(p_date, n=1):
  p_date = check_n_filter_p_date(p_date)
  return p_date + relativedelta(months=n)

def get_n_of_days_in_month(p_date=None):
  '''
  days_in_month = calendar.monthrange(p_date.year, p_date.month)[1]
  :param p_date:
  :return:
  '''
  p_date = check_n_filter_p_date(p_date)
  days_in_month = calendar.monthrange(p_date.year, p_date.month)[1]
  return days_in_month

def last_date_in_month(p_date=None):
  p_date = check_n_filter_p_date(p_date)
  last_day = get_n_of_days_in_month(p_date)
  return datetime.date(year=p_date.year, month=p_date.month, day=last_day)

def transform_date_to_8char(pdate):
  try:
    outstr = '%(year)s%(month)s%(day)s' %{
      'year' : str(pdate.year).zfill(4),
      'month': str(pdate.month).zfill(2),
      'day'  : str(pdate.day).zfill(2),
    }
    return outstr
  except AttributeError:
    pass
  return None

def transform_datestr_to_date(datestr):
  # 1st try (split by -)
  try:
    pp = datestr.split('-')
    year, month, day = int(pp[0]) , int(pp[1]) , int(pp[2])
    pdate = datetime.date(year, month, day)
    return pdate
  except (IndexError, ValueError):
    pass
  # 2nd try (split by /)
  try:
    pp = datestr.split('/')
    year, month, day = int(pp[0]) , int(pp[1]) , int(pp[2])
    pdate = datetime.date(year, month, day)
    return pdate
  except (IndexError, ValueError):
    pass
  # 3rd try (split by .)
  try:
    pp = datestr.split('.')
    year, month, day = int(pp[0]) , int(pp[1]) , int(pp[2])
    pdate = datetime.date(year, month, day)
    return pdate
  except (IndexError, ValueError):
    pass
  # 4th try (no split, but sliced)
  try:
    year  = int(datestr[:4])
    month = int(datestr[4:6])
    day   = int(datestr[6:])
    pdate = datetime.date(year, month, day)
    return pdate
  except (KeyError, ValueError):
    pass
  return None

def return_inifindates_tuple_from_inidate(inidate, n_years=1):
  if type(inidate) not in [datetime.date, datetime.datetime]:
    return (None, None)
  n_days = 1
  if n_years < 1:
    n_days = - 1
  findate = inidate + relativedelta(years=n_years) - datetime.timedelta(days=n_days)
  # order output, ie, lesser date comes first
  if findate > inidate:
    return (inidate, findate)
  else:
    return (findate, inidate)

def return_inifindates_tuple_from_strinidate(inidatestr, n_years=1):
  inidate = transform_datestr_to_date(inidatestr)
  return return_inifindates_tuple_from_inidate(inidate, n_years)

def return_strinifindates_tuple_from_strinidate(inidatestr, n_years=1):
  inifindates_tuple = return_inifindates_tuple_from_strinidate(inidatestr, n_years)
  if None in inifindates_tuple:
    return t
  inidatestr = str(inifindates_tuple[0]); findatestr = str(inifindates_tuple[1])
  return (inidatestr, findatestr)

def return_strinifindates_tuple_from_inidate(inidate, n_years=1):
  inifindates_tuple = return_inifindates_tuple_from_inidate(inidate, n_years)
  if None in inifindates_tuple:
    return t
  inidatestr = str(inifindates_tuple[0]); findatestr = str(inifindates_tuple[1])
  return (inidatestr, findatestr)

def are_same_year_n_same_month(date1, date2):
  if date1.year == date2.year and date1.month == date2.month:
    return True
  return False

def get_daysfraction_with_date(p_date):
  p_date = check_n_filter_p_date(p_date)
  n_of_day_in_month = p_date.day
  days_in_month = get_n_of_days_in_month(p_date)
  return n_of_day_in_month / days_in_month

def get_daysfraction_with_date_n_previousday(p_date, previous_day=0):
  if type(p_date) != datetime.date:
    error_msg = 'type(p_date = %s) != datetime.date' % str(p_date)
    raise TypeError(error_msg)
  days_in_month = get_n_of_days_in_month(p_date)
  if previous_day is None or previous_day < 1:
    return p_date.day / days_in_month
  elif previous_day > p_date.day:  # this never happens after 'or': or previous_day > days_in_month:
    return 0
  return (p_date.day - previous_day) / days_in_month

def get_remaining_daysfraction(p_date):
  n_of_day_in_month = p_date.day
  days_in_month = get_n_of_days_in_month(p_date)
  n_of_days = days_in_month - n_of_day_in_month
  remaining_daysfraction = n_of_days / days_in_month
  return remaining_daysfraction

def get_remaining_daysfraction_via_complement(p_date):
  return 1 - get_daysfraction_with_date(p_date)

def process():
  pass

if __name__ == '__main__':
  process()
