#!/usr/bin/env python3
'''
payments_json_writer.py
'''
import func.db.json_tofrom.general_json_reader_writer as jsongen
import func.datefs.datebillfunctions as dtbill
import models.billing_items as bimod

json_filename = 'payments_realestaterentsystem.json'

# =====
# CDT01
# 2019
# =====

payments_dict = {}

refmonthdatestr = '2019-04-01'
contract_id     = 'CDT01'
payment_id = dtbill.join_strdate_n_contractid_into_billid(refmonthdatestr, contract_id)

# May 2019 => registro de pagamento dia 27 valor R$ 4.860,00
payments_dict[payment_id] = {
  'contract_id'    : contract_id,
  'refmonthdate': refmonthdatestr,  # refmonth is, in general, previous month
  'payments_dictlist': [{
    'itdatetime': '2019-05-27 12:00',
    'ittype': bimod.BillingItemTypes.K_PAYMENT,
    'description': bimod.BillingItemTypes.get_short_description(bimod.BillingItemTypes.K_PAYMENT),
    'itvalue': 4860,
    'itobs1': 'TEC Depósito no Itaú',
    'itobs2': None,
    'is_inmonth': False,
  },],
}

# Jun 2019 => registro de pagamento dia 24 valor R$ 4.860,00
refmonthdatestr = '2019-05-01'
contract_id     = 'CDT01'
payment_id = dtbill.join_strdate_n_contractid_into_billid(refmonthdatestr, contract_id)
payments_dict[payment_id] = {
  'contract_id'    : contract_id,
  'refmonthdate': refmonthdatestr,  # refmonth is, in general, previous month
  'payments_dictlist': [{
    'itdatetime' : '2019-06-24 12:00',
    'ittype'     : bimod.BillingItemTypes.K_PAYMENT,
    'description': bimod.BillingItemTypes.get_short_description(bimod.BillingItemTypes.K_PAYMENT),
    'itvalue': 4860,
    'itobs1' : 'TEC Depósito no Itaú',
    'itobs2': None,
    'is_inmonth': False,
  },],
}

# Jul 2019 => 3 registros de pagamento: dia 2 valor R$ 4.860,00; dia 9 valor R$ 3.000,00; dia 9 valor R$ 1.860,00
refmonthdatestr = '2019-06-01'
contract_id     = 'CDT01'
payment_id = dtbill.join_strdate_n_contractid_into_billid(refmonthdatestr, contract_id)
payments_dict[payment_id] = {
  'contract_id'    : contract_id,
  'refmonthdate': refmonthdatestr,  # refmonth is, in general, previous month
  'payments_dictlist': [{
    'itdatetime' : '2019-07-02 12:00',
    'ittype'     : bimod.BillingItemTypes.K_PAYMENT,
    'description': bimod.BillingItemTypes.get_short_description(bimod.BillingItemTypes.K_PAYMENT),
    'itvalue': 4860,
    'itobs1' : 'TEC Depósito no Itaú',
    'itobs2': None,
    'is_inmonth': False,
  },
  {
    'itdatetime' : '2019-07-09 12:00',
    'ittype'     : bimod.BillingItemTypes.K_PAYMENT,
    'description': bimod.BillingItemTypes.get_short_description(bimod.BillingItemTypes.K_PAYMENT),
    'itvalue'     : 3000,
    'itobs1' : 'TEC Depósito no Itaú',
    'itobs2' : None,
    'is_inmonth': False,
  },
  {
    'itdatetime' : '2019-07-09 12:01',
    'ittype'     : bimod.BillingItemTypes.K_PAYMENT,
    'description': bimod.BillingItemTypes.get_short_description(bimod.BillingItemTypes.K_PAYMENT),
    'itvalue'    : 1860,
    'itobs1' : 'TEC Depósito no Itaú',
    'itobs2' : None,
    'is_inmonth': False,
  },
  ],
}

# Aug 2019 => registro de pagamento dia 12 valor R$ 4.860,00
refmonthdatestr = '2019-07-01'
contract_id     = 'CDT01'
payment_id = dtbill.join_strdate_n_contractid_into_billid(refmonthdatestr, contract_id)
payments_dict[payment_id] = {
  'contract_id'    : contract_id,
  'refmonthdate': refmonthdatestr,  # refmonth is, in general, previous month
  'payments_dictlist': [{
    'itdatetime' : '2019-08-12 12:00',
    'ittype'     : bimod.BillingItemTypes.K_PAYMENT,
    'description': bimod.BillingItemTypes.get_short_description(bimod.BillingItemTypes.K_PAYMENT),
    'itvalue': 4860,
    'itobs1' : 'TEC Depósito no Itaú',
    'itobs2': None,
    'is_inmonth': False,
  },],
}

# Oct 2019 => registro de pagamento dia 15 valor R$ 4.860,00
refmonthdatestr = '2019-09-01'
contract_id     = 'CDT01'
payment_id = dtbill.join_strdate_n_contractid_into_billid(refmonthdatestr, contract_id)
payments_dict[payment_id] = {
  'contract_id'    : contract_id,
  'refmonthdate': refmonthdatestr,  # refmonth is, in general, previous month
  'payments_dictlist': [{
    'itdatetime' : '2019-10-15 12:00', # ok, checked with bank extract
    'ittype'     : bimod.BillingItemTypes.K_PAYMENT,
    'description': bimod.BillingItemTypes.get_short_description(bimod.BillingItemTypes.K_PAYMENT),
    'itvalue': 4860,
    'itobs1' : 'TEC Depósito no Itaú',
    'itobs2': None,
    'is_inmonth': False,
  },],
}

# Nov 2019 => registro de pagamento dia 15 valor R$ 4.860,00
refmonthdatestr = '2019-10-01'
contract_id     = 'CDT01'
payment_id = dtbill.join_strdate_n_contractid_into_billid(refmonthdatestr, contract_id)
payments_dict[payment_id] = {
  'contract_id'    : contract_id,
  'refmonthdate': refmonthdatestr,  # refmonth is, in general, previous month
  'payments_dictlist': [{
    'itdatetime' : '2019-11-30 12:00',
    'ittype'     : bimod.BillingItemTypes.K_PAYMENT,
    'description': bimod.BillingItemTypes.get_short_description(bimod.BillingItemTypes.K_PAYMENT),
    'itvalue': 5000,
    'itobs1' : 'TEC Depósito no Itaú',
    'itobs2' : None,
    'is_inmonth': False,
  },],
}

def print_payments():
  payment_ids = payments_dict.keys()
  sorted(payment_ids)
  total_dict = 0
  for pid in payment_ids:
    p = payments_dict[pid]
    total_dict = {}
    print(p)
    print ('Payment id', pid )
    contract_id = p['contract_id']
    total_dict[contract_id] = 0
    paydata_dictlist = p['payments_dictlist']
    for paydata_dict in paydata_dictlist:
      itvalue = paydata_dict['itvalue']
      total_dict[contract_id] += itvalue
      print('\tpayvalue :', itvalue)
      paydatetime = paydata_dict['itdatetime']
      print('\tpaydate :', paydatetime)
      pay_obs = paydata_dict['itobs1']
      print('\tpay_obs :', pay_obs)
      payauthstring = paydata_dict['itobs2']
      print('\tpayauthstring :', payauthstring)


def process():
  jsongen.write_pythondata_to_jsondbfolder(payments_dict, json_filename)
  print_payments()

if __name__ == '__main__':
  process()
