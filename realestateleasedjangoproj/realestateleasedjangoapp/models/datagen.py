#!/usr/bin/env python3
from datetime import date


REFTYPE_KEY = 'reftype'


def create_billingitems_list_for_invoicebill():
  '''
    # data
    DEBI stands for 'Debt Immediate' and means that non-paid billing in the previous month
    billing_item = {'typeref':'DEBI', 'value':1900+600+200}
    billing_items.append(billing_item)
    DEBC stands for 'Debt Carried-on' and means that older non-paid amount carried to the previous month

  :return:
  '''
  billingitems = []
  billingitem = {REFTYPE_KEY:'ALUG', 'value': 1900}
  billingitems.append(billingitem)
  billingitem = {REFTYPE_KEY: 'COND', 'value': 600}
  billingitems.append(billingitem)
  billingitem = {REFTYPE_KEY: 'IPTU', 'value': 200}
  billingitems.append(billingitem)
  billingitem = {REFTYPE_KEY: 'CARR', 'value': 800}
  billingitems.append(billingitem)
  return billingitems

def create_payments():
  payments = []
  payment_obj = Payment(paid_amount=1000, paydate=date(2018,2,10))
  payments.append(payment_obj)
  payment_obj = Payment(paid_amount=500, paydate=date(2018,2,25))
  payments.append(payment_obj)
  return payments



class PreviousBill:

  nonpaid_months_amount = 0
  carriedup_debt_amount = 0

  @staticmethod
  def fetch_nonpaid_months_amount():
    return PreviousBill.nonpaid_months_amount

  @staticmethod
  def fetch_carriedup_debt_amount():
    return PreviousBill.carriedup_debt_amount

