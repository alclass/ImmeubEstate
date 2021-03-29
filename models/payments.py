#!/usr/bin/env python3

# import unittest
# from .BillMod import Bill
import func.db.json_tofrom.jsonreaders as paymread

class Payment:
  '''
  '''

  def __init__(self, payid):
    '''

    payid is composed of date8char and contract5letter (eg 20191001CDT01)

    When more than one payment is done on a single day, the Payment object is integrated.
    However, individual payments are registered inside a JSON field. This field is attribute 'bankrecordsjson'.

    This json is strutured as follows:
      {'paydate':<date>, 'paid_amount':<value>, 'bankaccount_id':<bid>,
       'seqorder_onday': <seq>, 'bankdocline': <banksdocstring>,
       'payeesname': <name>, 'paytype': <transfer|dep-money|dep-cheque>}
      */

    There is no need for 'contract_id' in the above JSON, because contract_id belongs to self, below.
    '''
    self.payid = payid

  @classmethod
  def create_instance_from_jsondict_by_id(cls, payid):
    paydict = paymread.get_payment_by_id_from_json(payid)
    payobj = cls(payid)
    if paydict is None:
      return None
    for k in paydict:
      setattr(payobj, k, paydict[k])
    return payobj

  @staticmethod
  def check_paydates_order_n_raise_exception_if_inconsistent(payments):
    if len(payments) == 0:
      return
    previouspay = payments[0]
    for nextpay in payments[1:]:
      if previouspay.paydate > nextpay.paydate:
        error_msg = 'nextpay.paydate (%s) > previouspay.paydate (%s)' %(str(nextpay.paydate), str(previouspay.paydate))
        raise ValueError(error_msg)
      previouspay = nextpay

  @staticmethod
  def order_payments_in_date_ascending_order_if_needed(payments):
    '''
    TO-DO
    :param payments:
    :return:
    '''
    return payments

  @staticmethod
  def are_there_more_than_one_payment_in_a_day(payments):
    if payments is None or len(payments) == 0:
      return False
    previouspay = payments[0]
    for nextpay in payments[1:]:
      if previouspay.paydate == nextpay.paydate:
        return True
      previouspay = nextpay
    return False


  @staticmethod
  def consolidate_days_when_there_are_more_than_one_payment_in_a_day(payments):
    if payments is None or len(payments) == 0:
      return
    consolidated_paymentlists = []
    previouspay = payments[0]
    del payments[0]
    consolidated_paymentlists.append(previouspay)
    while len(payments) > 0:
      nextpay = payments[0]
      del payments[0]
      if previouspay.paydate         == nextpay.paydate and \
          previouspay.monthrefdate   == nextpay.monthrefdate and \
          previouspay.monthseqnumber == nextpay.monthseqnumber and \
          previouspay.contract_id    == nextpay.contract_id:

        previouspay.paid_amount += nextpay.paid_amount
      else:
        consolidated_paymentlists.append(nextpay)
        previouspay = nextpay

    return consolidated_paymentlists

  # def get_ittype_description(self, ittype):

  def str_as_lines(self):
    lines = []
    line = 'payid=%s on %s' %(str(self.payid), str(self.refmonthdate))
    lines.append(line)
    for pdict in self.payments_dictlist:
      line = '%(itdatetime)s | %(ittype)d | %(description)s | %(itvalue)f obs %(obs1)s' %{
        'itdatetime' : pdict['itdatetime'],
        'ittype': pdict['ittype'],
        'description': pdict['description'],
        'itvalue': pdict['itvalue'],
        'obs1': pdict['itobs1'],
      }
      lines.append(line)
    return lines


  def __str__(self):
    return '\n'.join(self.str_as_lines())

def adhoctest():
  payid = '20190701CDT01'
  payobj = Payment.create_instance_from_jsondict_by_id(payid)
  if payobj is None:
    print('payobj is None')
    return
  print (payobj)

if __name__ == '__main__':
  adhoctest()
