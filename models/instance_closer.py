#!/usr/bin/env python3

import datetime
import unittest
# instantiate one element
from bills_month_closer import Closer
from bills import Bill
from contracts import Contract
from contracts import MoraParams

def instantiate_closer(
    refmonthdate,
    ini_balance,
    rent_value,
    cond_fee,
    prop_tax,
    dueday,
    incidence_fine_fraction,
    fix_monthly_interest,
    monet_corr_fraction,
    payment_n_date_namedtuplelist,
):

  mora_params = MoraParams(
    incidence_fine_fraction=incidence_fine_fraction,
    fix_monthly_interest=fix_monthly_interest,
    monet_corr_fraction=monet_corr_fraction
  )
  contract = Contract(due_day_in_month=dueday, mora_params=mora_params)
  bill = Bill(contract)
  # billitem_ntuple_constr  # collections.namedtuple('BillItemNamedTuple', 'itdate, ittype, itvalue, itobs, itformula')
  value = Bill.billitem_ntuple_constr(itdate=refmonthdate, ittype=Bill.KItemTypes.TK_IBALANCE, itvalue=ini_balance, itobs=None, itformula=None)
  bill[1] = value
  value = Bill.billitem_ntuple_constr(itdate=refmonthdate, ittype=Bill.KItemTypes.TK_RENTVAL, itvalue=rent_value, itobs=None, itformula=None)
  bill[1] = value
  value = Bill.billitem_ntuple_constr(itdate=refmonthdate, ittype=Bill.KItemTypes.TK_CONDFEE, itvalue=cond_fee, itobs=None, itformula=None)
  bill[1] = value
  value = Bill.billitem_ntuple_constr(itdate=refmonthdate, ittype=Bill.KItemTypes.TK_PROPTAX, itvalue=prop_tax, itobs=None, itformula=None)
  bill[1] = value

  Bill.billitem_ntuple_constr(itdate=refmonthdate, ittype=Bill.KItemTypes.TK_IBALANCE, itvalue=ini_balance, itobs=None, itformula=None)
  bill[1] = value

  closer   = Closer(bill, contract, payment_n_date_namedtuplelist)
  return closer