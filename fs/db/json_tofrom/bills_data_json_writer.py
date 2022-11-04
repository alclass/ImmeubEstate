#!/usr/bin/env python3
'''
json_bills_writer.py
'''
import fs.datefs.datebillfunctions as dtbill
import fs.db.json_tofrom.general_json_reader_writer as jsongen
import models.bills.billing_items as bimod
json_filename = 'bills_realestaterentsystem.json'
#quad_payment_namedtuple_constr = collections.namedtuple('QuadPayment', 'paid_amount, paydatetime, int_n_corr_if_any, nutshell_str')

contracts_monthly_bills_dict = {}

seq = 0
def add_one_to_seq():
  global seq
  seq += 1
  return seq

# =====
# CDUTR
# =====

# Jan 2019 => cobrança

# Jul 2019 => cobrança

refmonthdatestr = '2019-07-01'
contract_id     = 'CDT01'
cdutra_rentval = 1000
cdutra_proptax = 100
cdutra_condfee = 100

bill_id = dtbill.join_strdate_n_contractid_into_billid(refmonthdatestr, contract_id)
contracts_monthly_bills_dict[bill_id] = {
  'bill_id'     : bill_id,
  'contract_id' : contract_id,
  'refmonthdate': refmonthdatestr,
  'duedate'     : '2019-09-10',
  'is_closed'   : False,  # open_or_closed
  'ini_balance' : 0,
  'total_when_open' : 2922.24,
  'total_paid'      : 2922.24,
  'incidence_value' : None,
  'fin_balance'     : 0,
  'billing_items_dictlist': [
    {
      'itdatetime' : refmonthdatestr,
      'ittype'     : bimod.BillingItemTypes.K_IBALANCE,
      'description': bimod.BillingItemTypes.get_short_description(bimod.BillingItemTypes.K_IBALANCE),
      'itvalue'    : 1000,
      'itobs1'     : None,
      'itobs2'     : None,
      'is_inmonth' : False,
    },
    {
      'itdatetime' : '2019-07-02', # refmonthdatestr,
      'ittype'     : bimod.BillingItemTypes.K_RENTVAL,
      'description': bimod.BillingItemTypes.get_short_description(bimod.BillingItemTypes.K_RENTVAL),
      'itvalue'    : cdutra_rentval,
      'itobs1'     : None,
      'itobs2'     : None,
      'is_inmonth' : True,
    },
    {
      'itdatetime' : refmonthdatestr,
      'ittype'     : bimod.BillingItemTypes.K_PROPTAX,
      'description': bimod.BillingItemTypes.get_short_description(bimod.BillingItemTypes.K_PROPTAX),
      'itvalue'    : cdutra_proptax,
      'itobs1'     : None,
      'itobs2'     : None,
      'is_inmonth' : True,
    },
    {
      'itdatetime' : refmonthdatestr,
      'ittype'     : bimod.BillingItemTypes.K_CONDFEE,
      'description': bimod.BillingItemTypes.get_short_description(bimod.BillingItemTypes.K_CONDFEE),
      'itvalue'    : cdutra_condfee,
      'itobs1'     : None,
      'itobs2'     : None,
      'is_inmonth' : True,
    },
  ],
}

# process
jsongen.write_pythondata_to_jsondbfolder(contracts_monthly_bills_dict, json_filename)
