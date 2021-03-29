#!/usr/bin/env python3
import datetime
import unittest
# instantiate one element
from bills_month_closer import Closer
from bills import Bill
from contracts import Contract
from contracts import MoraParams
import instance_closer as ic




class Test_Closer(unittest.TestCase):

  def test_1(self):
    '''
    Simple possible testcase:
      a) inmonth_amount is 50
      b) payment on date is 50
      c) closed balance is 0

    :return:
    '''

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
      expected_refmonthdate,
      ini_balance,
      rent_value,
      cond_fee,
      prop_tax,
      dueday,
      incidence_fine_fraction,
      fix_monthly_interest,
      monet_corr_fraction,
      payment_n_date_namedtuplelist,
    )




    self.closer.payment_n_dates_tuplelist = payment_n_dates_tuplelist
    # incidence_fine = 0.1; fix_monthly_interest_fraction = 0.01; apply_monthly_monet_corr = 0.003
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

