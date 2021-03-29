#!/usr/bin/env python3
import calendar, datetime
import unittest
import date_functions as dtfunc

# non leap years
MONTHDAYS_NONLEAP = [31,28,31,30,31,30,31,31,30,31,30,31]
def get_n_of_days_in_month_nonleapyears(p_date):
  '''
  For testing module calendar below
  :param p_date:
  :return:
  '''
  return MONTHDAYS_NONLEAP[p_date.month-1]

class TestDateFunctions(unittest.TestCase):

  def test_module_calendar(self):

    for i in range(1, 13):
      p_date = datetime.date(year=2019, month=i, day=1)
      days_in_month_via_calendar = calendar.monthrange(p_date.year, p_date.month)[1]
      domestic_days_in_month_via = get_n_of_days_in_month_nonleapyears(p_date)
      self.assertEqual(days_in_month_via_calendar, domestic_days_in_month_via)
    # with a leap year

    p_date = datetime.date(year=2000, month=2, day=1)
    days_in_month_via_calendar = calendar.monthrange(p_date.year, p_date.month)[1]
    domestic_days_in_month_via = get_n_of_days_in_month_nonleapyears(p_date) + 1
    self.assertEqual(days_in_month_via_calendar, domestic_days_in_month_via)

  def test_add_months(self):
    '''

    :return:
    '''
    ini_date = datetime.date(year=2019, month=11, day=11)
    n_months_to_add = 2
    expected_one_month_later_date = datetime.date(year=2020, month=1, day=11)
    returned_one_month_later_date = dtfunc.add_months(ini_date, n_months_to_add)
    self.assertEqual(expected_one_month_later_date, returned_one_month_later_date)

    ini_date = datetime.date(year=2019, month=11, day=11)
    n_months_to_add = -12
    expected_one_month_later_date = datetime.date(year=2018, month=11, day=11)
    returned_one_month_later_date = dtfunc.add_months(ini_date, n_months_to_add)
    self.assertEqual(expected_one_month_later_date, returned_one_month_later_date)

    ini_date = datetime.date(year=2019, month=11, day=11)
    added_n_months = -120
    expected_one_month_later_date = datetime.date(year=2009, month=11, day=11)
    returned_one_month_later_date = dtfunc.add_months(ini_date, added_n_months)
    self.assertEqual(expected_one_month_later_date, returned_one_month_later_date)

  def test_last_date_in_month(self):
    '''

    :return:
    '''
    ini_date = datetime.date(year=2019, month=11, day=11)
    expected_last_day_date = datetime.date(year=2019, month=11, day=30)
    returned_last_day_date = dtfunc.last_date_in_month(ini_date)
    self.assertEqual(expected_last_day_date, returned_last_day_date)

    ini_date = datetime.date(year=2019, month=2, day=11)
    expected_last_day_date = datetime.date(year=2019, month=2, day=28)
    returned_last_day_date = dtfunc.last_date_in_month(ini_date)
    self.assertEqual(expected_last_day_date, returned_last_day_date)

    ini_date = datetime.date(year=2016, month=2, day=11)
    expected_last_day_date = datetime.date(year=2016, month=2, day=29)
    returned_last_day_date = dtfunc.last_date_in_month(ini_date)
    self.assertEqual(expected_last_day_date, returned_last_day_date)

    ini_date = datetime.date(year=1900, month=2, day=11)
    expected_last_day_date = datetime.date(year=1900, month=2, day=28)
    returned_last_day_date = dtfunc.last_date_in_month(ini_date)
    self.assertEqual(expected_last_day_date, returned_last_day_date)

    ini_date = datetime.date(year=2000, month=2, day=11)
    expected_last_day_date = datetime.date(year=2000, month=2, day=29)
    returned_last_day_date = dtfunc.last_date_in_month(ini_date)
    self.assertEqual(expected_last_day_date, returned_last_day_date)

  def test_get_daysfraction_with_date(self):

    day_in_month = 11
    p_date = datetime.date(year=2019, month=11, day=day_in_month)
    days_in_month   = 30
    expected_days_fraction = day_in_month/days_in_month
    returned_days_fraction = dtfunc.get_daysfraction_with_date(p_date)
    self.assertEqual(expected_days_fraction, returned_days_fraction)

    # days fraction's complement to 1 (when day is last day, complement is 0)
    expected_remaining_days_fraction = (30-11)/30
    returned_remaining_days_fraction = dtfunc.get_remaining_daysfraction(p_date)
    self.assertEqual(expected_remaining_days_fraction, returned_remaining_days_fraction)
    returned_remaining_days_fraction = dtfunc.get_remaining_daysfraction_via_complement(p_date)
    self.assertEqual(expected_remaining_days_fraction, returned_remaining_days_fraction)

    # with previous day
    previous_day = 5
    expected_days_fraction = (day_in_month - previous_day) / days_in_month
    returned_days_fraction = dtfunc.get_daysfraction_with_date_n_previousday(p_date, previous_day)
    self.assertEqual(expected_days_fraction, returned_days_fraction)

    day_in_month = 30
    p_date = datetime.date(year=2019, month=11, day=day_in_month)
    days_in_month   = 30
    expected_days_fraction = day_in_month/days_in_month
    returned_days_fraction = dtfunc.get_daysfraction_with_date(p_date)
    self.assertEqual(expected_days_fraction, returned_days_fraction)

    # with previous day
    previous_day = 30
    expected_days_fraction = 0
    returned_days_fraction = dtfunc.get_daysfraction_with_date_n_previousday(p_date, previous_day)
    self.assertEqual(expected_days_fraction, returned_days_fraction)

    # days fraction's complement to 1 (when day is last day, complement is 0)
    expected_remaining_days_fraction = 0
    returned_remaining_days_fraction = dtfunc.get_remaining_daysfraction(p_date)
    self.assertEqual(expected_remaining_days_fraction, returned_remaining_days_fraction)
    returned_remaining_days_fraction = dtfunc.get_remaining_daysfraction_via_complement(p_date)
    self.assertEqual(expected_remaining_days_fraction, returned_remaining_days_fraction)
