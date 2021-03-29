#!/usr/bin/env python3
import datetime
import date_functions as dtfunc
# from functions_lib import print_bookkeeping

from bills import Bill

def initialize_bill_with_contract_n_month():

  bill = Bill()

  # item 1
  paydate = datetime.date(year=2019, month=11, day=1)
  itemtype = Bill.KItemTypes.TK_INIDEBT
  value = 4000
  billitem = Bill.BillItemNamedTuple(itdate=paydate, ittype=itemtype, itvalue=value, itobs=None, itformula=None)
  bill[paydate] = billitem

  # item 2
  paydate = datetime.date(year=2019, month=11, day=1)
  itemtype = Bill.KItemTypes.TK_RENTVAL
  value = 2500
  billitem = Bill.BillItemNamedTuple(itdate=paydate, ittype=itemtype, itvalue=value, itobs=None, itformula=None)
  bill[paydate] = billitem

  # item 3
  paydate = datetime.date(year=2019, month=11, day=1)
  itemtype = Bill.KItemTypes.TK_CONDFEE
  value = 800
  billitem = Bill.BillItemNamedTuple(itdate=paydate, ittype=itemtype, itvalue=value, itobs=None, itformula=None)
  bill[paydate] = billitem

  # item 4
  paydate = datetime.date(year=2019, month=11, day=1)
  itemtype = Bill.KItemTypes.TK_PROPTAX
  value = 300
  billitem = Bill.BillItemNamedTuple(itdate=paydate, ittype=itemtype, itvalue=value, itobs=None, itformula=None)
  bill[paydate] = billitem

  print(bill.generate_bill_as_text())

  '''
  # item 5
  paydate = datetime.date(year=2019, month=11, day=11)
  itemtype = Bill.KItemTypes.TK_INCFINE
  value = 250
  billitem = Bill.BillItemNamedTuple(itdate=paydate,ittype=itemtype,itvalue=value,itobs=None,itformula='2000*0,1')
  bill[paydate] = billitem



  # item 5
  paydate = datetime.datetime(year=2019, month=11, day=13)
  itemtype = Bill.KItemTypes.TK_PAYMENT
  value = 3000
  billitem = Bill.BillItemNamedTuple(itdate=paydate,ittype=itemtype,itvalue=value,itobs=None,itformula='2000*0,1')
  bill[paydate] = billitem

  # item 6
  paydate = datetime.datetime(year=2019, month=11, day=13)
  itemtype = Bill.KItemTypes.TK_INTMCORR
  value = 30
  billitem = Bill.BillItemNamedTuple(itdate=paydate,ittype=itemtype,itvalue=value,itobs=None,itformula='payment*corrmonet*fraction')
  bill[paydate] = billitem

  # item 7
  paydate = datetime.datetime(year=2019, month=11, day=13)
  itemtype = Bill.KItemTypes.TK_INTMCORR
  value = 30
  billitem = Bill.BillItemNamedTuple(itdate=paydate,ittype=itemtype,itvalue=value,itobs='Fechamento',itformula='balance*corrmonet')
  bill[paydate] = billitem
  '''

  print (bill)


def process():
  initialize_bill_with_contract_n_month()
  return


  b = Bill({Bill.KItems.TK_RENTVAL:10, Bill.KItems.TK_CONDFEE:16, Bill.KItems.TK_PROPTAX:20,})
  tot = b.totalize()
  print ('Bill =>')
  print(b)
  print ('total =>', tot)

if __name__ == '__main__':
  process()
