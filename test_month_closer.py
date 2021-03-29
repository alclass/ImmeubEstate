#!/usr/bin/env python3
import datetime
import unittest
# instantiate one element
from month_closer import Closer
from month_closer import MoraParams

class Test_Closer(unittest.TestCase):

  def instantiate_closer(self):
    nextrefmonth   = datetime.date(year=2019, month=11, day=1)
    carried_debt = 100
    inmonth_amount = 50
    duedate        = datetime.date(year=2019, month=10, day=10)
    payment_n_dates_tuplelist = []
    paid_amount    = 150
    paydate = datetime.date(year=2019, month=10, day=10)
    payment_n_dates_tuplelist.append((paid_amount, paydate))
    incidence_fine = 0.1
    fix_monthly_interest = 0.01
    monet_corr_fraction  = 0.003
    mora_params = MoraParams(incidence_fine, fix_monthly_interest, monet_corr_fraction)
    self.closer = Closer(
      nextrefmonth, inmonth_amount, carried_debt, duedate,
      payment_n_dates_tuplelist, mora_params
    )

  def test_1(self):
    '''
    Simple possible testcase:
      a) inmonth_amount is 50
      b) payment on date is 50
      c) closed balance is 0

    :return:
    '''
    self.instantiate_closer()
    carried_debt   =   0; self.closer.carried_debt   = carried_debt
    inmonth_amount =  50; self.closer.inmonth_amount = inmonth_amount
    payment_n_dates_tuplelist = []
    paid_amount = 50
    paydate = datetime.date(year=2019, month=10, day=10)
    payment_n_dates_tuplelist.append((paid_amount, paydate))
    self.closer.payment_n_dates_tuplelist = payment_n_dates_tuplelist
    # incidence_fine = 0.1; fix_monthly_interest = 0.01; monet_corr_fraction = 0.003
    self.closer.revert_calculations()
    self.assertFalse(self.closer.STEP_1_HAS_BEEN_CALLED)
    self.assertFalse(self.closer.STEP_2_HAS_BEEN_CALLED)
    self.closer.step_1_loop_over_payments()
    self.assertAlmostEqual(self.closer.balance, 0)
    self.closer.apply_once_incidence_fine_if_needed()
    self.assertAlmostEqual(self.closer.balance, 0)
    self.closer.step_2_close_month()
    self.assertAlmostEqual(self.closer.balance, 0)
    self.assertAlmostEqual(self.closer.total_interest_n_monetcorr, 0)
    self.assertAlmostEqual(self.closer.total_mora, 0)
    self.assertTrue(self.closer.STEP_1_HAS_BEEN_CALLED)
    self.assertTrue(self.closer.STEP_2_HAS_BEEN_CALLED)

  def test_2(self):
    '''
    A more complicate example.
    Though payment covers carried_debt and inmount_amount,
      carried_debt corrects, generates incidence fine which in turns generates correction.

    nextrefmonth is 11/2019
    carried_debt   = 100
    inmonth_amount = 50
    duedate is 10/10/2019
    paid_amount    = 150
    paydate is 10/10/2019
    incidence_fine = 0.1; fix_monthly_interest = 0.01; monet_corr_fraction  = 0.003

    :return:
    '''
    self.instantiate_closer()
    self.closer.revert_calculations()
    self.assertFalse(self.closer.STEP_1_HAS_BEEN_CALLED)
    self.assertFalse(self.closer.STEP_2_HAS_BEEN_CALLED)
    self.closer.step_1_loop_over_payments()
    carried_debt   = 100
    inmonth_amount = 50
    # local variable here that coincides to the value in closer.tuplelist object
    paid_amount    = 150
    incidence_fine = 0.1; fix_monthly_interest = 0.01; monet_corr_fraction  = 0.003
    total_interest_n_monetcorr = 0
    balance  = carried_debt + inmonth_amount
    increase = carried_debt * (fix_monthly_interest+monet_corr_fraction)*(10/31)
    total_interest_n_monetcorr += increase
    balance = balance + increase - paid_amount
    self.assertAlmostEqual(self.closer.balance, balance)
    # balance (saldo) at this moment (step 2 has not yet run)
    self.closer.apply_once_incidence_fine_if_needed()
    incidence_fine_value = balance * incidence_fine
    self.assertAlmostEqual(self.closer.incidence_fine_value, incidence_fine_value)
    balance += incidence_fine_value
    increase = balance * (fix_monthly_interest+monet_corr_fraction)*(11/31)
    balance += increase
    total_interest_n_monetcorr += increase
    self.assertAlmostEqual(self.closer.balance, balance)
    self.assertTrue(self.closer.STEP_1_HAS_BEEN_CALLED)
    self.assertFalse(self.closer.STEP_2_HAS_BEEN_CALLED)
    # on the 31st, month is closed
    self.closer.step_2_close_month()
    daysfraction = 20/31
    increase = balance * (fix_monthly_interest+monet_corr_fraction)*daysfraction
    balance += increase
    total_interest_n_monetcorr += increase
    self.assertAlmostEqual(self.closer.balance, balance)
    self.assertAlmostEqual(self.closer.total_interest_n_monetcorr, total_interest_n_monetcorr)
    total_mora = total_interest_n_monetcorr + incidence_fine_value
    self.assertAlmostEqual(self.closer.total_mora, total_mora)
    self.assertTrue(self.closer.STEP_1_HAS_BEEN_CALLED)
    self.assertTrue(self.closer.STEP_2_HAS_BEEN_CALLED)

  def test_3(self):
    '''
    As tests increase in number, they become a little more complex.
    This testcase here envolves a relatively large carried_debt and
      a late payment that is smaller than inmonth_amount.

    :return:
    '''
    self.instantiate_closer()
    inmonth_amount = 3500
    self.closer.inmonth_amount = inmonth_amount
    carried_debt   = 15000
    self.closer.carried_debt   = carried_debt
    self.closer.duedate        = datetime.date(year=2019, month=10, day=10)
    payment_n_dates_tuplelist = []
    paid_amount    = 3000
    paydate = datetime.date(year=2019, month=10, day=15)
    payment_n_dates_tuplelist.append((paid_amount, paydate))
    self.closer.payment_n_dates_tuplelist = payment_n_dates_tuplelist
    self.closer.revert_calculations()
    self.assertFalse(self.closer.STEP_1_HAS_BEEN_CALLED)
    self.assertFalse(self.closer.STEP_2_HAS_BEEN_CALLED)
    self.closer.close_month()
    self.assertTrue(self.closer.STEP_1_HAS_BEEN_CALLED)
    self.assertTrue(self.closer.STEP_2_HAS_BEEN_CALLED)
    # logical explicit calculations
    total_interest_n_monetcorr = 0
    balance = carried_debt + inmonth_amount
    # first increase is incidence fine
    self.assertAlmostEqual(self.closer.value_subjected_to_incidence_fine, inmonth_amount)
    incidence_fine_fraction = self.closer.mora_params.incidence_fine_fraction
    incidence_fine_value = inmonth_amount * incidence_fine_fraction
    self.assertAlmostEqual(self.closer.incidence_fine_value, incidence_fine_value)
    balance += incidence_fine_value
    # second increase on day 11 interest and monet corr
    fix_monthly_interest = self.closer.mora_params.fix_monthly_interest
    monet_corr_fraction  = self.closer.mora_params.monet_corr_fraction
    daysfraction = 11/31
    increase = balance * (fix_monthly_interest+monet_corr_fraction)*daysfraction
    balance += increase
    total_interest_n_monetcorr += increase
    # payment is on the 15th
    daysfraction = (15-11)/31
    increase = paid_amount * (fix_monthly_interest+monet_corr_fraction)*daysfraction
    balance += increase
    total_interest_n_monetcorr += increase
    balance -= paid_amount
    # closing happens on the 31st
    daysfraction = (31-11)/31
    increase = balance * (fix_monthly_interest+monet_corr_fraction)*daysfraction
    total_interest_n_monetcorr += increase
    balance += increase
    self.assertAlmostEqual(self.closer.balance, balance)
    self.assertAlmostEqual(self.closer.total_interest_n_monetcorr, total_interest_n_monetcorr)
    total_mora = total_interest_n_monetcorr + incidence_fine_value
    self.assertAlmostEqual(self.closer.total_mora, total_mora)

  def test_4(self):
    '''
    Here no payments happen
    :return:
    '''
    self.instantiate_closer()
    inmonth_plus_debt = 3500
    self.closer.inmonth_amount = inmonth_plus_debt
    carried_debt = 0
    self.closer.carried_debt   = carried_debt
    self.closer.duedate        = datetime.date(year=2019, month=10, day=10)

    payment_n_dates_tuplelist = []
    #paid_amount    = 3500
    #paydate = datetime.date(year=2019, month=10, day=10)
    #payment_n_dates_tuplelist.append((paid_amount, paydate))
    self.closer.payment_n_dates_tuplelist = payment_n_dates_tuplelist

    self.closer.revert_calculations()
    self.assertFalse(self.closer.STEP_1_HAS_BEEN_CALLED)
    self.assertFalse(self.closer.STEP_2_HAS_BEEN_CALLED)
    self.closer.close_month()
    self.assertTrue(self.closer.STEP_1_HAS_BEEN_CALLED)
    self.assertTrue(self.closer.STEP_2_HAS_BEEN_CALLED)
    # logical explicit calculations
    balance = carried_debt + inmonth_plus_debt
    total_interest_n_monetcorr = 0
    fix_monthly_interest    = self.closer.mora_params.fix_monthly_interest
    monet_corr_fraction     = self.closer.mora_params.monet_corr_fraction
    incidence_fine_fraction = self.closer.mora_params.incidence_fine_fraction
    incidence_fine_value = inmonth_plus_debt * incidence_fine_fraction
    self.assertAlmostEqual(self.closer.incidence_fine_value, incidence_fine_value)
    balance += incidence_fine_value
    increase = balance * (fix_monthly_interest+monet_corr_fraction) * (11/31)
    balance += increase
    total_interest_n_monetcorr += increase
    # closing month
    increase = balance * (fix_monthly_interest+monet_corr_fraction) * ((31-11)/31)
    balance += increase
    total_interest_n_monetcorr += increase
    self.assertAlmostEqual(self.closer.balance, balance)
    self.assertAlmostEqual(self.closer.total_interest_n_monetcorr, total_interest_n_monetcorr)
    total_mora = total_interest_n_monetcorr + incidence_fine_value
    self.assertAlmostEqual(self.closer.total_mora, total_mora)

  def test_5(self):
    '''
    Here, 5 payments happen:
     1) one on the 1st,
     2) one on the 10th,
     3) one on the 11th
     3) one on the 27th
     4) one on the last day of month (if it's February, it's on 28th)

    :return:
    '''
    self.instantiate_closer()
    self.closer.nextrefmonth   = datetime.date(year=2019, month=7, day=1)
    inmonth_amount = 3500
    self.closer.inmonth_amount = inmonth_amount
    carried_debt = 15000
    self.closer.carried_debt = carried_debt

    payment_n_dates_tuplelist = []
    # 1
    paid_amount    = 1000
    paydate = datetime.date(year=2019, month=6, day=1)
    payment_n_dates_tuplelist.append((paid_amount, paydate))
    # 2
    paid_amount    = 3500
    paydate = datetime.date(year=2019, month=6, day=10)
    payment_n_dates_tuplelist.append((paid_amount, paydate))
    # 3
    paid_amount    = 3500
    paydate = datetime.date(year=2019, month=6, day=11)
    payment_n_dates_tuplelist.append((paid_amount, paydate))
    # 4
    paid_amount    = 4000
    paydate = datetime.date(year=2019, month=6, day=27)
    payment_n_dates_tuplelist.append((paid_amount, paydate))
    # 5
    paid_amount    = 2500
    paydate = datetime.date(year=2019, month=6, day=30)
    payment_n_dates_tuplelist.append((paid_amount, paydate))
    self.closer.payment_n_dates_tuplelist = payment_n_dates_tuplelist

    self.closer.duedate = datetime.date(year=2019, month=6, day=10)
    monet_corr_fraction = 0.002
    self.closer.mora_params.monet_corr_fraction  = monet_corr_fraction
    fix_monthly_interest = self.closer.mora_params.fix_monthly_interest
    incidence_fine_fraction = fix_monthly_interest = self.closer.mora_params.incidence_fine_fraction
    self.closer.revert_calculations()
    self.assertFalse(self.closer.STEP_1_HAS_BEEN_CALLED)
    self.assertFalse(self.closer.STEP_2_HAS_BEEN_CALLED)
    self.closer.close_month()
    self.assertTrue(self.closer.STEP_1_HAS_BEEN_CALLED)
    self.assertTrue(self.closer.STEP_2_HAS_BEEN_CALLED)

    # logical explicit calculations
    balance = carried_debt + inmonth_amount
    total_interest_n_monetcorr = 0

    # 1 update first 1000 on the 1st
    paid_amount = payment_n_dates_tuplelist[0][0]
    paydate = payment_n_dates_tuplelist[0][1]
    daysfraction = paydate.day / 30
    increase = paid_amount * (fix_monthly_interest+monet_corr_fraction) * (daysfraction)
    balance += increase
    total_interest_n_monetcorr += increase

    # 2 update next 3500 on the 10th
    paid_amount = payment_n_dates_tuplelist[1][0]
    paydate = payment_n_dates_tuplelist[1][1]
    daysfraction = paydate.day / 30
    increase = paid_amount * (fix_monthly_interest+monet_corr_fraction) * (daysfraction)
    balance += increase
    total_interest_n_monetcorr += increase

    # 3 apply incidence on the 11th
    incidence_fine_value = inmonth_amount * incidence_fine_fraction
    self.assertAlmostEqual(self.closer.incidence_fine_value, incidence_fine_value)
    balance += incidence_fine_value
    total_interest_n_monetcorr += increase

    # 4 update next incidence point on the 11th
    increase = balance * (fix_monthly_interest+monet_corr_fraction) * (11/30)
    balance += increase
    total_interest_n_monetcorr += increase

    # 5 update next 3500 (pay 3) on the 11th
    paid_amount = payment_n_dates_tuplelist[2][0]
    paydate = payment_n_dates_tuplelist[2][1]
    daysfraction = paydate.day / 30
    increase = 0 # because incidence happened on same day
    balance += increase
    total_interest_n_monetcorr += increase

    # 6 update next 4000 (pay 4) on the 27th
    paid_amount = payment_n_dates_tuplelist[3][0]
    paydate = payment_n_dates_tuplelist[3][1]
    daysfraction = paydate.day / 30
    increase = paid_amount * (fix_monthly_interest+monet_corr_fraction) * ((27-11)/30)
    balance += increase
    total_interest_n_monetcorr += increase

    # 7 update next 2500 (pay 4) on the 30th
    paid_amount = payment_n_dates_tuplelist[4][0]
    paydate = payment_n_dates_tuplelist[4][1]
    daysfraction = paydate.day / 30
    increase = paid_amount * (fix_monthly_interest+monet_corr_fraction) * ((30-11)/30)
    balance += increase
    total_interest_n_monetcorr += increase

    # 8 close month on the 30th
    increase = balance * (fix_monthly_interest+monet_corr_fraction) * ((30-11)/30)
    balance += increase
    total_interest_n_monetcorr += increase
    #self.assertAlmostEqual(self.closer.balance, balance)

    #self.assertAlmostEqual(self.closer.total_interest_n_monetcorr, total_interest_n_monetcorr)
    total_mora = total_interest_n_monetcorr + incidence_fine_value
    #self.assertAlmostEqual(self.closer.total_mora, total_mora)
