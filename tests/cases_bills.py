#!/usr/bin/env python3

import datetime
from contracts import Contract
import functions_lib as funclib
from bills import Bill
from bills_month_closer import BillMonthCloser

billitem_ntuple_constr = funclib.billitem_ntuple_constr  # collections.namedtuple('BillItemNamedTuple', 'itdate, ittype, itvalue, itobs, itformula')
closer = None

def get_1_billingitem_namedtuplelist():
  billingitem_namedtuplelist = []
  refmonthdate = datetime.date(year=2019, month=10, day=1)
  billingitem_namedtuple = billitem_ntuple_constr(
    itdate=refmonthdate,
    ittype=funclib.KItemTypes.TK_IBALANCE,
    itvalue=3000,
    itobs=None,
    itformula=None,
  )
  billingitem_namedtuplelist.append(billingitem_namedtuple)

  billingitem_namedtuple = billitem_ntuple_constr(
    itdate=refmonthdate,
    ittype=funclib.KItemTypes.TK_RENTVAL,
    itvalue=2300,
    itobs=None,
    itformula=None,
  )
  billingitem_namedtuplelist.append(billingitem_namedtuple)

  billingitem_namedtuple = billitem_ntuple_constr(
    itdate=refmonthdate,
    ittype=funclib.KItemTypes.TK_CONDFEE,
    itvalue=800,
    itobs=None,
    itformula=None,
  )
  billingitem_namedtuplelist.append(billingitem_namedtuple)

  billingitem_namedtuple = billitem_ntuple_constr(
    itdate=refmonthdate,
    ittype=funclib.KItemTypes.TK_PROPTAX,
    itvalue=400,
    itobs=None,
    itformula=None,
  )
  billingitem_namedtuplelist.append(billingitem_namedtuple)

  return billingitem_namedtuplelist

def get_1_payment_n_date_namedtuplelist():

  payment_n_date_namedtuplelist = []
  # item 1
  paydate = datetime.date(year=2019, month=10, day=11)
  itemtype = Bill.KItemTypes.TK_PAYMENT
  value = 4000
  payment_n_date_namedtuple = billitem_ntuple_constr(
    itdate=paydate,
    ittype=itemtype,
    itvalue=value,
    itobs=None,
    itformula=None
  )
  payment_n_date_namedtuplelist.append(payment_n_date_namedtuple)

  return payment_n_date_namedtuplelist

def case_2():

  contract = Contract('CDUTRA')
  billingitem_namedtuplelist = get_1_billingitem_namedtuplelist()
  bill = Bill(contract, billingitem_namedtuplelist)
  print('='*80)
  print(bill)

  paidamount_n_paydate_namedtuplelist = get_1_payment_n_date_namedtuplelist()
  bill2 = BillMonthCloser(bill, paidamount_n_paydate_namedtuplelist)

  print('='*80)

  print(bill2)

def case_4():
  # instantiate one element

  contract = Contract('CDUTRA')
  billingitem_namedtuplelist = get_1_billingitem_namedtuplelist()
  bill = Bill(contract, billingitem_namedtuplelist)

  payment_n_date_namedtuplelist = get_1_payment_n_date_namedtuplelist()

  print('='*80)
  print('Case 4')
  print('='*80)
  bill = BillMonthCloser(bill, payment_n_date_namedtuplelist)

  bill.close_month()

  print(bill.generate_bill_as_text())
  print('Same', '='*80)
  print (bill)

def process():
  case_2()
  case_4()

if __name__ == '__main__':
  process()
