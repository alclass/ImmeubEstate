#!/usr/bin/env python3
'''
payments_json_writer.py
'''
import func.datefs.date_functions as dtfunc
import func.db.json_tofrom.general_json_reader_writer as jsongen

json_filename = 'payments_realestaterentsystem2.json'


# =====
# HLB01
# 2018
# =====

payment_id = '20181201HLB01'
payments_dict[payment_id] = {
  'payment_id'  : payment_id,
  'contract_id' : 'HLB01',
  'refmonthdate': '2018-12-01',
  'paydata_dictlist' : [{
    'payvalue'     : 2812.70,
    'paydatetime'  : '2019-01-10',
    'payauthstring': '',
    'pay_obs'      : 'Transferência via BB',
  },],
}

# =====
# HLB01
# 2019
# =====

payment_id = '20190101HLB01'
payments_dict[payment_id] = {
  'payment_id'  : payment_id,
  'contract_id' : 'HLB01',
  'refmonthdate': '2019-01-01',
  'paydata_dictlist' : [{
    'payvalue'     : 2823.71,
    'paydatetime'  : '2019-02-10',
    'payauthstring': '',
    'pay_obs'      : 'Transferência via BB',
  },],
}

payment_id = '20190201HLB01'
payments_dict[payment_id] = {
  'payment_id'  : payment_id,
  'contract_id'    : 'HLB01',
  'refmonthdate'   : '2019-02-01',
  'paydata_dictlist' : [{
    'payvalue' : 2918.28,
    'paydatetime'  : '2019-03-10',
    'payauthstring': '',
    'pay_obs'      : 'Transferência via BB',
  },],
}

payment_id = '20190301HLB01'
payments_dict[payment_id] = {
  'payment_id'  : payment_id,
  'contract_id'    : 'HLB01',
  'refmonthdate'   : '2019-03-01',
  'paydata_dictlist' : [{
    'payvalue' : 2909.47,
    'paydatetime'  : '2019-04-10',
    'payauthstring': '',
    'pay_obs': 'Transferência via BB',
  },],
}

payment_id = '20190401HLB01'
payments_dict[payment_id] = {
  'payment_id'  : payment_id,
  'contract_id'    : 'HLB01',
  'refmonthdate'   : '2019-04-01',
  'paydata_dictlist' : [{
    'payvalue' : 2909.47,
    'paydatetime'  : '2019-05-10',
    'payauthstring': '',
    'pay_obs': 'Transferência via BB',
  },],
}

payment_id = '20190501HLB01'
payments_dict[payment_id] = {
  'payment_id'  : payment_id,
  'contract_id'    : 'HLB01',
  'refmonthdate'   : '2019-05-01',
  'paydata_dictlist' : [{
    'payvalue' : 3072.78,
    'paydatetime'  : '2019-06-10',
    'payauthstring': '',
    'pay_obs': 'Transferência via BB',
  },],
}

payment_id = '20190601HLB01'
payments_dict[payment_id] = {
  'payment_id'  : payment_id,
  'contract_id'    : 'HLB01',
  'refmonthdate'   : '2019-06-01',
  'paydata_dictlist' : [{
    'payvalue' : 2920.48,
    'paydatetime'  : '2019-07-10',
    'payauthstring': '',
    'pay_obs': 'Transferência via BB',
  },],
}

payment_id = '20190701HLB01'
payments_dict[payment_id] = {
  'payment_id'  : payment_id,
  'contract_id'    : 'HLB01',
  'refmonthdate'   : '2019-07-01',
  'paydata_dictlist' : [{
    'payvalue' : 2910.57,
    'paydatetime'  : '2019-08-10',
    'payauthstring': '',
    'pay_obs': 'Transferência via BB',
  },],
}

payment_id = '20190801HLB01'
payments_dict[payment_id] = {
  'payment_id'  : payment_id,
  'contract_id'    : 'HLB01',
  'refmonthdate'   : '2019-08-01',
  'paydata_dictlist' : [{
    'payvalue' : 2922.24,
    'paydatetime'  : '2019-09-10',
    'payauthstring': '',
    'pay_obs': 'Transferência via BB',
  },],
}

payment_id = '20190901HLB01'
payments_dict[payment_id] = {
  'payment_id'  : payment_id,
  'contract_id'    : 'HLB01',
  'refmonthdate'   : '2019-09-01',
  'paydata_dictlist' : [{
    'payvalue' : 2919.38,
    'paydatetime'  : '2019-10-10',
    'payauthstring': '',
    'pay_obs': 'Transferência via BB',
  },],
}

payment_id = '20191001HLB01'
payments_dict[payment_id] = {
  'payment_id'  : payment_id,
  'contract_id' : 'HLB01',
  'refmonthdate': '2019-10-01',
  'paydata_dictlist' : [{
    'payvalue'     : 2923.79,
    'paydatetime'  : '2019-11-10',
    'payauthstring': '',
    'pay_obs': 'Transferência via BB',
  },],
}
# 20191101HLB01

# =====
# JAC01
# 2018
# =====

# =====
# JAC01
# 2019
# =====

contract_id     = 'JAC01'
refmonthdatestr = '2019-04-01'
payment_id = dtfunc.get_payment_id_from_contrid_n_refmonth(contract_id, refmonthdatestr)
payments_dict[payment_id] = {
  'payment_id'  : payment_id,
  'contract_id' : contract_id,
  'refmonthdate': refmonthdatestr,
  'paydata_dictlist' : [{
    'payvalue'     : 1500,
    'paydatetime'  : '2019-05-02',
    'payauthstring': '"000206";"DP DINH AG";"1500.00";"C"', # check in CEF's extract
    'pay_obs'      : 'Depósito na Caixa',
  },],
}

contract_id     = 'JAC01'
refmonthdatestr = '2019-05-01'
payment_id = dtfunc.get_payment_id_from_contrid_n_refmonth(contract_id, refmonthdatestr)
payments_dict[payment_id] = {
  'payment_id'  : payment_id,
  'contract_id' : contract_id,
  'refmonthdate': refmonthdatestr,
  'paydata_dictlist' : [{
    'payvalue'     : 1500,
    'paydatetime' : '2019-06-04',
    'payauthstring': '"101343";"DP DINH AG";"1500.00";"C"', # check in CEF's extract
    'pay_obs'      : 'Depósito na Caixa',
  },{
    'payvalue'     : 1500,
    'paydatetime'  : '2019-06-10',
    'payauthstring': '"101726";"CRED TEV";"1500.00";"C"', # check in CEF's extract
    'pay_obs'      : 'Depósito na Caixa',
  },],
}
# 2019-06-01 JAC01 NO PAYMENT checked in CEF's extract
# 2019-07-01 JAC01 NO PAYMENT checked in CEF's extract
# 2019-08-01 JAC01 NO PAYMENT checked in CEF's extract

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
    paydata_dictlist = p['paydata_dictlist']
    for paydata_dict in paydata_dictlist:
      payvalue = paydata_dict['payvalue']
      total_dict[contract_id] += payvalue
      print('\tpayvalue :', payvalue)
      paydatetime = paydata_dict['paydatetime']
      print('\tpaydate :', paydatetime)
      payauthstring = paydata_dict['payauthstring']
      print('\tpayauthstring :', payauthstring)
      pay_obs = paydata_dict['pay_obs']
      print('\tpay_obs :', pay_obs)


def process():
  jsongen.write_pythondata_to_jsondbfolder(payments_dict, json_filename)
  print_payments()

if __name__ == '__main__':
  process()
