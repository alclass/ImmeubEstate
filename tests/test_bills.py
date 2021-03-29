#!/usr/bin/env python3
# test_bills
import datetime
import unittest
# instantiate one element
from bills_month_closer import Closer
from contracts import MoraParams
from bills import Bill

class TestBill(unittest.TestCase):

  def instantiate_bill(self):

    self.bill = Bill()

    # item 1
    paydate = datetime.date(year=2019, month=11, day=1)
    itemtype = Bill.KItemTypes.TK_IBALANCE
    value = 4000
    billitem = Bill.billitem_ntuple_constr(itdate=paydate, ittype=itemtype, itvalue=value, itobs=None, itformula=None)
    self.bill[paydate] = billitem

    # item 2
    paydate = datetime.date(year=2019, month=11, day=1)
    itemtype = Bill.KItemTypes.TK_RENTVAL
    value = 2500
    billitem = Bill.billitem_ntuple_constr(itdate=paydate, ittype=itemtype, itvalue=value, itobs=None, itformula=None)
    self.bill[paydate] = billitem

    # item 3
    paydate = datetime.date(year=2019, month=11, day=1)
    itemtype = Bill.KItemTypes.TK_CONDFEE
    value = 800
    billitem = Bill.billitem_ntuple_constr(itdate=paydate, ittype=itemtype, itvalue=value, itobs=None, itformula=None)
    self.bill[paydate] = billitem

    # item 4
    paydate = datetime.date(year=2019, month=11, day=1)
    itemtype = Bill.KItemTypes.TK_PROPTAX
    value = 300
    billitem = Bill.billitem_ntuple_constr(itdate=paydate, ittype=itemtype, itvalue=value, itobs=None, itformula=None)
    self.bill[paydate] = billitem

    # print(bill.generate_bill_as_text())

  def test_1(self):
    '''
    Simple possible testcase:
      a) inmonth_amount is 50
      b) payment on date is 50
      c) closed balance is 0

    :return:
    '''
    self.instantiate_bill()
    expected_inmonth_amount = 2500 + 800 + 300
    returned_inmonth_amount = self.bill.inmonth_amount
    self.assertEqual(returned_inmonth_amount, expected_inmonth_amount)
