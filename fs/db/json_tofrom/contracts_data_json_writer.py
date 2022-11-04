#!/usr/bin/env python3
'''
json_writer_contracts.py
'''
import fs.db.json_tofrom.general_json_reader_writer as jsongen

json_filename = 'contracts_realestaterentsystem.json'
contracts_dict = {}

contract_id = 'CDT02'
contracts_dict[contract_id] = {
  'contract_id': contract_id,
  'contractor_ids'  : ['munzer1'],
  'immeuble5letter' : 'CDUTR',
  'contract_inidate': '2016-10-01',
  'dueday_in_month' : 10,
  'receivable_value': 3387.11,
  'reajust_refmonth': 4,
  'receivable_frequency': 'monthly',
  'duration_in_months': 30,
  'duration_in_days': None,
  'autorecontract': True,
  'past_contracted_dateranges': ('2019-04-01','2021-09-30'),
  'past_values_n_intervals' : [(3000,'2017-04-01','2018-03-31'),(3128.14,'2018-04-01','2019-03-31'),],
  # (3387.11,'2019-04-01','2019-11-30'),],
  'chosen_proptax_discount_one_pay': False,
  'mora_params' : {
    'incidence_fine_fraction': 0.1,
    'fix_monthly_interest_fraction': 0.01,
    'apply_monthly_monet_corr' : True,
  },
  'repasse' : ['condfee', 'firetariff', 'proptax'],
  'receive_verification_of' : [],
  'guarantee_type': 'fianca',
}

contract_id = 'HLB01'
contracts_dict[contract_id] = {
  'contract_id': contract_id,
  'contractor_ids'  : ['lucio1'],
  'immeuble5letter' : 'HLOBO',
  'contract_inidate': '2016-10-15',
  'dueday_in_month' : 10,
  'receivable_value': 2139.29,
  'reajust_refmonth': 11,
  'receivable_frequency': 'monthly',
  'duration_in_months': 30,
  'duration_in_days': None,
  'autorecontract': True,
  'contracted_dateranges': [('2016-10-15','2019-04-14'), ('2019-04-15', None)],
  'past_values_n_intervals' : [(1900,'2016-10-15','2018-10-31'), (2069.32,'2018-11-01','2019-10-31'),],
  'chosen_proptax_discount_one_pay': False,
  'mora_params' : {
    'incidence_fine_fraction': 0.1,
    'fix_monthly_interest_fraction': 0.01,
    'apply_monthly_monet_corr' : True,
  },
  'repasse' : ['condfee', 'firetariff', 'proptax'],
  'receive_verification_of' : [],
  'guarantee_type': 'carta_fianca',
}

contract_id = 'JAC01'
contracts_dict[contract_id] = {
  'contract_id': contract_id,
  'contractor_ids': ['beth1', 'filipe1'],
  'immeuble5letter': 'JACUM',
  'contract_inidate': '2015-11-01',
  'dueday_in_month': 10,
  'receivable_value': 1656.43,
  'reajust_refmonth': 11,
  'receivable_frequency': 'monthly',
  'duration_in_months': 30,
  'duration_in_days': None,
  'autorecontract': False,
  'past_contracted_dateranges': [('2015-11-01','2018-04-30'),('2018-05-01','2021-10-31'),],
  'past_values_n_intervals' : [
    (1000,'2015-11-01','2016-10-31'),(1250,'2016-11-01','2017-10-31'),(1523.06,'2017-11-01','2019-10-31'),],
  'chosen_proptax_discount_one_pay': False,
  'mora_params' : {
    'incidence_fine_fraction': 0.1,
    'fix_monthly_interest_fraction': 0.01,
    'apply_monthly_monet_corr' : True,
  },
  'repasse' : ['proptax', 'firetariff'],
  'receive_verification_of' : ['condfee'],
  'guarantee_type': None,
}

# process
jsongen.write_pythondata_to_jsondbfolder(contracts_dict, json_filename)