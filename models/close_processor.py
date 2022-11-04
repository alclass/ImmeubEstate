#!/usr/bin/env python3
import fs.datefs.datebillfunctions as dtbill
# import fs.textfs as funclib
import models.bills
import fs.db.json_tofrom.jsonreaders as paymread
import fs.db.json_tofrom.bills_json_reader as billread



class CloseProcessor:

  def __init__(self, bill_id):

    self.bill_id = bill_id
    self.bill = models.bills.bills.Bill.fetch_bill_by_id_from_json(self.bill_id)
    if self.bill is None:
      error_msg = 'bill_id %s does not exist in db' %self.bill_id
      raise ValueError(error_msg)
    if self.bill.is_closed:
      error_msg = 'Error: bill (%s) is closed' %self.bill_id
      raise ValueError(error_msg)

    self.close_process()

  def close_process(self):
    '''

"20181101CDT01":
{'payment_id': '20190501CDT01', 'contract_id': 'CDT01', 'refmonthdate': '2019-05-01',
'paydata_dictlist': [{'payvalue': 4860, 'paydatetime': '2019-05-27 12:00', 'payauthstring': '', 'pay_obs': 'TEC Depósito no Itaú'}]}
    :return:
    '''

    payment_id = self.bill_id # payment id is the same as bill_id
    self.payobj = paymread.get_payment_by_id(payment_id)
    if self.payobj is None:
      return None
    print ('bill', self.bill)
    print ('pay', self.payobj)
    self.fuse_bill_with_payment()

  def fuse_bill_with_payment(self):
    pass

def sort_bills(pdict):
  '''
   # Note that it will sort in lexicographical order
   # For mathematical way, change it to float
   print(sorted(key_value.items(), key =
               lambda kv:(kv[1], kv[0])))
  :return:
  '''
  bidictlist = pdict['billing_items_dictlist']
  bidictlist2 = sorted(bidictlist, key=lambda k : (k['itdate'],k['ittype']))
  for pdict in bidictlist:
    print (pdict)
  print ('-'*50)
  print(pdict.items())
  # pdict = sorted(pdict)
  for pdict in bidictlist2:
    print (pdict)
  print ('-'*50)

def adhoc_close_process():
  print ('CloseProcessor()')
  strdate = '20190701'; contract5char = 'CDT01'
  bill_id = dtbill.join_strdate_n_contractid_into_billid(strdate, contract5char)
  CloseProcessor(bill_id)

def adhoc_test_sort():
  bill_id = '20190701CDT01'
  billdict = billread.get_bill_dict_by_id_from_json(bill_id)
  sort_bills(billdict)
  payrecdict = paymread.get_payment_by_id_from_json(bill_id)
  print(payrecdict)


def process():
  adhoc_test_sort()


if __name__ == '__main__':
  process()
