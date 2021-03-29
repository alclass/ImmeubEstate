#!/usr/bin/env python3

import datetime
import sys
from bills_month_closer import Closer
from functions_lib import print_bookkeeping
import instance_closer as ic

closer = None

def case_1():
  # instantiate one element

  expected_refmonthdate = datetime.date(year=2019, month=10, day=1)
  ini_balance = 0
  rent_value = 350
  cond_fee = 120
  prop_tax = 50
  dueday = 10
  incidence_fine_fraction = 0.1
  fix_monthly_interest = 0.01
  monet_corr_fraction = 0.003

  payment_n_date_namedtuplelist = []

  paid_amount = 50
  paydate = datetime.date(year=2019, month=10, day=10)
  payment_n_date_namedtuple = Closer.payment_n_date_tuple_constr(paid_amount=paid_amount, paydate=paydate)

  payment_n_date_namedtuplelist.append(payment_n_date_namedtuple)

  closer = ic.instantiate_closer(
    refmonthdate=expected_refmonthdate,
    ini_balance=ini_balance,
    rent_value=rent_value,
    cond_fee=cond_fee,
    prop_tax=prop_tax,
    dueday=dueday,
    incidence_fine_fraction=incidence_fine_fraction,
    fix_monthly_interest=fix_monthly_interest,
    monet_corr_fraction=monet_corr_fraction,
    payment_n_date_namedtuplelist=payment_n_date_namedtuplelist,
  )


  # Increases
  # 1) 4000 must be corrected on day 8
  # calculation: balance: b = 1500+3500 + 1500*(0.01+0.002)*(8/31)- 4000
  # b = 1004.6451612903229
  # 2) though paid on time 4000, balance 1004.6451612903229 is within inmonth_amount,
  # so that amount in balance is subjected to incidence fine and correcting
  # incidence fine is 100.46451612903229
  # calculation: b = b * ( 1 + 0.1)
  # incidence calls for a full correction up to the 11th day
  # (because of that, the boolean variable will be the following:
  # h1) if incidence happens, closing acts from the 11th to the last day in month;
  # h2) if incidence does not happen, closing acts from the 1st to the last day in month;
  # b = 1105.1096774193552
  # calculation: b = b + b *(0.01+0.002)*(11/31)
  # b = 1109.8153057232053
  # 3) closing happens on the 31st
  # b = b + b *(0.01+0.002)*((31-11)/31)
  # FINAL calculation: b = 1118.4074242191268

  closer.close_month()
  print (closer)

def case_2_2():
  refmonthdate = datetime.date(year=2019, month=10, day=1)
  carried_debt = 100
  inmonth_amount = 50
  duedate = datetime.date(year=2019, month=10, day=10)
  payment_n_dates_tuplelist = []
  paid_amount = 150
  paydate = datetime.date(year=2019, month=10, day=10)
  payment_n_dates_tuplelist.append((paid_amount, paydate))
  incidence_fine = 0.1
  fix_monthly_interest = 0.01
  monet_corr_fraction = 0.003
  mora_params = MoraParams(incidence_fine, fix_monthly_interest, monet_corr_fraction)
  closer = Closer(
    refmonthdate, inmonth_amount, carried_debt, duedate,
    payment_n_dates_tuplelist, mora_params
  )
  closer.close_month()
  print (closer)

def case_7():
  print ('CASE 1 ======================')
  refmonthdate = datetime.date(year=2019, month=10, day=1)
  carried_debt = 0;
  inmonth_amount = 50
  duedate = datetime.date(year=2019, month=10, day=10)
  payment_n_dates_tuplelist = []
  paid_amount = 50
  paydate = datetime.date(year=2019, month=10, day=10)
  payment_n_dates_tuplelist.append((paid_amount, paydate))
  incidence_fine = 0.1
  fix_monthly_interest = 0.01
  monet_corr_fraction = 0.003
  mora_params = MoraParams(incidence_fine, fix_monthly_interest, monet_corr_fraction)
  closer = Closer(
    refmonthdate, inmonth_amount, carried_debt, duedate,
    payment_n_dates_tuplelist, mora_params
  )
  closer.close_month()
  print(closer)

def case_2():
  print ('CASE 2 ======================')
  refmonthdate = datetime.date(year=2019, month=10, day=1)
  carried_debt = 100
  inmonth_amount = 50
  duedate = datetime.date(year=2019, month=10, day=10)
  payment_n_dates_tuplelist = []
  paid_amount = 150
  paydate = datetime.date(year=2019, month=10, day=10)
  payment_n_dates_tuplelist.append((paid_amount, paydate))
  incidence_fine = 0.1
  fix_monthly_interest = 0.01
  monet_corr_fraction = 0.003
  mora_params = MoraParams(incidence_fine, fix_monthly_interest, monet_corr_fraction)
  closer = Closer(
    refmonthdate, inmonth_amount, carried_debt, duedate,
    payment_n_dates_tuplelist, mora_params
  )
  closer.close_month()
  print(closer)

def case_3():
  print ('CASE 3 ======================')
  refmonthdate = datetime.date(year=2019, month=10, day=1)
  carried_debt = 15000
  inmonth_amount = 3500
  duedate = datetime.date(year=2019, month=10, day=10)
  payment_n_dates_tuplelist = []
  paid_amount = 3000
  paydate = datetime.date(year=2019, month=10, day=15)
  payment_n_dates_tuplelist.append((paid_amount, paydate))
  incidence_fine = 0.1
  fix_monthly_interest = 0.01
  monet_corr_fraction = 0.003
  mora_params = MoraParams(incidence_fine, fix_monthly_interest, monet_corr_fraction)
  closer = Closer(
    refmonthdate, inmonth_amount, carried_debt, duedate,
    payment_n_dates_tuplelist, mora_params
  )
  closer.close_month()
  print(closer)

def case_4():
  print ('CASE 4 ======================')
  refmonthdate = datetime.date(year=2019, month=10, day=1)
  carried_debt = 0
  inmonth_amount = 3500
  duedate = datetime.date(year=2019, month=10, day=10)
  payment_n_dates_tuplelist = []
  incidence_fine = 0.1
  fix_monthly_interest = 0.01
  monet_corr_fraction = 0.003
  mora_params = MoraParams(incidence_fine, fix_monthly_interest, monet_corr_fraction)
  closer = Closer(
    refmonthdate, inmonth_amount, carried_debt, duedate,
    payment_n_dates_tuplelist, mora_params
  )
  closer.close_month()
  print(closer)


def case_5():
  print ('CASE 5 ======================')
  refmonthdate = datetime.date(year=2019, month=6, day=1)
  carried_debt = 15000
  inmonth_amount = 3500
  duedate = datetime.date(year=2019, month=6, day=10)
  payment_n_dates_tuplelist = []
  incidence_fine = 0.1
  fix_monthly_interest = 0.01
  monet_corr_fraction = 0.003
  mora_params = MoraParams(incidence_fine, fix_monthly_interest, monet_corr_fraction)

  closer = Closer(
    refmonthdate, inmonth_amount, carried_debt, duedate,
    payment_n_dates_tuplelist, mora_params
  )

  inmonth_amount = 3500
  closer.inmonth_amount = inmonth_amount
  carried_debt = 15000
  closer.carried_debt = carried_debt

  payment_n_dates_tuplelist = []
  # class Closer will sort paydates ascendingly
  # 5
  paid_amount = 2500
  paydate = datetime.date(year=2019, month=6, day=30)
  payment_n_dates_tuplelist.append((paid_amount, paydate))
  # 4
  paid_amount = 4000
  paydate = datetime.date(year=2019, month=6, day=27)
  payment_n_dates_tuplelist.append((paid_amount, paydate))
  # 3
  paid_amount = 3500
  paydate = datetime.date(year=2019, month=6, day=11)
  payment_n_dates_tuplelist.append((paid_amount, paydate))
  # 2
  paid_amount = 3500
  paydate = datetime.date(year=2019, month=6, day=10)
  payment_n_dates_tuplelist.append((paid_amount, paydate))
  # 1
  paid_amount = 1000
  paydate = datetime.date(year=2019, month=6, day=1)
  payment_n_dates_tuplelist.append((paid_amount, paydate))

  closer._payment_n_date_namedtuplelist = payment_n_dates_tuplelist
  closer.check_payment_n_date_tuplelist()
  closer.duedate = datetime.date(year=2019, month=6, day=10)
  closer.mora_params.monet_corr_fraction = monet_corr_fraction
  closer.revert_calculations()
  closer.close_month()
  print(closer)


def process():
  case_1()
  '''
  case_2()
  case_3()
  case_4()
  case_5()
  '''

if __name__ == '__main__':
  process()
