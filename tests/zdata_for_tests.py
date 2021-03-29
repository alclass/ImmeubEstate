#!/usr/bin/env python3
import json
'''

table contracts
 id
 immeub_id
 monthly_interest_fraction
 incidente_fine_fraction
 initial_rent_value
 sigla_reajuste

table people
 id
 name
 cpf

table contract_person
 id
 person_id
 contract_id

table closed_months
 id
 contract_id
 _refmonthdate
 ini_carried_debt
 inmount_amount
 interest_total
 mora_total
 total

 json_billing_items
'''

import datetime
import sys
from collections import namedtuple
import dict_code_generator

json_file_data = []

persons_dict = {}
persons_dict['lucio1'] = {
  'fullname': 'Lucio Surname',
  'cpf'     : '12345678911',
  'phones'  : ['2199991111'],
  'emails'  : ['lucio@email'],
}
persons_dict['beth1'] = {
  'fullname': 'Beth Miranda',
  'cpf'     : '12345678911',
  'phones'  : ['2199991111'],
  'emails'  : ['lucio@email'],
}
persons_dict['filipe1'] = {
  'fullname': 'Filipe Teixeira',
  'cpf'     : '12345678911',
  'phones'  : ['2199991111'],
  'emails'  : ['filipe@email'],
}
persons_dict['munzer1'] = {
  'fullname': 'Filipe Teixeira',
  'cpf'     : '12345678911',
  'phones'  : ['2199991111'],
  'emails'  : ['filipe@email'],
}
json_file_data.append(persons_dict)

immeubles_dict = {}
immeubles_dict['JACUM'] = {
  'municip_id'  : 'xxxxxxx',
  'rgi_id'      : 'xxxxxxx',
  'immeub_type' : 'apartamento',
  'floor'    : 2,
  'floors_in_building': 5,
  'area_m2'  : 116,
  'construction_year': 1959,
  'zipcode'  : '12345678',
  'street' : 'Rua Jacumã',
  'street_n' : 76,
  'apt_n'    : 202,
  'neighbourhood' : 'Tijuca',
  'city': 'Rio de Janeiro',
  'state_id': 'RJ',
  'country_n' : 55,
}
immeubles_dict['HLOBO'] = {
  'municip_id'  : 'xxxxxxx',
  'rgi_id'      : 'xxxxxxx',
  'immeub_type' : 'apartamento',
  'floor'       : 2,
  'floors_in_building': 5,
  'area_m2'  : 116,
  'construction_year': 1959,
  'zipcode'  : '12345678',
  'street  ' : 'Rua Haddock Lobo',
  'street_n' : 386,
  'apt_n'    : 405,
  'neighbourhood' : 'Tijuca',
  'city': 'Rio de Janeiro',
  'state_id': 'RJ',
  'country_n' : 55,
}
immeubles_dict['CDUTR'] = {
  'municip_id'  : 'xxxxxxx',
  'rgi_id'      : 'xxxxxxx',
  'immeub_type' : 'apartamento',
  'floor'       : 2,
  'floors_in_building': 5,
  'area_m2'  : 116,
  'construction_year': 1959,
  'zipcode'  : '12345678',
  'street' : 'Rua Carmela Dutra',
  'street_n' : 76,
  'apt_n'    : 201,
  'neighbourhood' : 'Tijuca',
  'city': 'Rio de Janeiro',
  'state_id': 'RJ',
  'country_n' : 55,
}

contracts_dict = {}
contracts_dict['JAC01'] = {
  'person_ids': ['beth1', 'filipe1'],
  'immeub_id': 'JACUM',
  'dueday_in_month': 10,
  'contract_date': '2015-10-01',
  'older_rent_values_n_interval' : [(2700,'2015-10-01,2018-01-31'), (2800,'2015-10-01,2018-01-31')],
  'current_rent_value': 1550,
  'rent_duration_dates': ('2019-04-01','2021-09-30'),
  'proptax_timerule': {
    'value': 330,
    'months': list(range(1, 11)),
  },
  'firetariff_timerule': {
    'value': 120,
    'months': [6],
  },
  'mora_params' : {
    'INCIDENCE_FINE': 0.1,
    'FIX_MONTHLY_INTEREST': 0.01,
    'MONET_CORR_FRACTION': 0.03,
  },
  'repasse' : ['proptax', 'firetariff'],
  'receive_verification' : ['condfee'],
  'guarantee_type': '',
}
contracts_dict['HLB01'] = {
  'recipient_ids' : ['beth1','filipe1'],
  'name': 'Lucio',
  'street_address': 'Rua Haddock Lobo',
  'dueday_in_month': 10,
  'contract_date': '2016-10-01',
  'older_rent_values_n_interval' : [(2700,'2015-10-01,2018-01-31'), (2800,'2015-10-01,2018-01-31')],
  'current_rent_value': 2900,
  'rent_duration_dates': ('2019-04-01','2021-09-30'),
  'proptax_timerule': {
    'value': 330,
    'months': list(range(1, 11)),
  },
  'firetariff_timerule': {
    'value': 120,
    'months': [6],
  },
  'mora_params' : {
    'INCIDENCE_FINE': 0.1,
    'FIX_MONTHLY_INTEREST': 0.01,
    'MONET_CORR_FRACTION': 0.03,
  },
  'repasse' : ['proptax', 'firetariff'],
  'receive_verification' : ['condfee'],
  'guarantee_type': 'carta_fianca',
}
contracts_dict['CDT01'] = {
  'name': 'Munzer',
  'street_address': 'Rua Haddock Lobo',
  'dueday_in_month': 10,
  'contract_date': '2016-10-01',
  'older_rent_values_n_interval' : [(2700,'2015-10-01,2018-01-31'), (2800,'2015-10-01,2018-01-31')],
  'current_rent_value': 2900,
  'rent_duration_dates': ('2019-04-01','2021-09-30'),
  'proptax_timerule': {
    'value': 330,
    'months': list(range(1, 11)),
  },
  'firetariff_timerule': {
    'value': 120,
    'months': [6],
  },
  'mora_params' : {
    'INCIDENCE_FINE': 0.1,
    'FIX_MONTHLY_INTEREST': 0.01,
    'MONET_CORR_FRACTION': 0.03,
  },
  'repasse' : ['condfee', 'proptax', 'firetariff'],
  'receive_verification' : [],
  'guarantee_type': 'fianca',
}
json_file_data.append(contracts_dict)

rent_bill_monthdict_list = []

rent_bill_monthdict_listelement = {
  'contract_id'  : 'JAC01',
  'refmonthdate' : '2019-10-01',
  'duedate'      : '2019-11-10',
  'status'       : 'open', # open_or_closed
  'ini_balance': 1,
  'total_when_open': 1,
  'total_paid': 1,
  'incidence_value': 1,
  'fin_balance': 1,
  'inmonth_bitems' : {
    'rentval': 1,
    # 'condfee': 1,
    'proptax': 1,
   }, # ends inmonth_bitems key
   'triple_pay_date_intcorr_list': [('paidamount1', 'date1', 'intcorr1')],
}
rent_bill_monthdict_list.append(rent_bill_monthdict_listelement)

rent_bill_monthdict_listelement = {
  'contract_id'  : 'JAC01',
  'refmonthdate' : '2019-10-01',
  'duedate'      : '2019-11-10',
  'status'       : 'open', # open_or_closed
  'ini_balance'  : 40000,
  'total_when_open' : 43000,
  'total_paid'   : 0,
  'incidence_value': 150,
  'fin_balance'  : 0,
  'inmonth_bitems': {
    'rentval' : 1500,
    # 'condfee': 1,
    'proptax' : 1,
  }, # ends inmonth_bitems key
  'triple_pay_date_intcorr_list': [('paidamount1', 'date1', 'intcorr1')],
}
rent_bill_monthdict_list.append(rent_bill_monthdict_listelement)

rent_bill_monthdict_listelement = {
  'contract_id'  : 'JAC01',
  'refmonthdate' : '2019-11-01',
  'duedate'      : '2019-12-10',
  'status'       : '', # open_or_closed
  'ini_balance'  : 1,
  'total_when_open' : 1,
  'total_paid'   : 1,
  'incidence_value': 1,
  'fin_balance'  : 1,
  'inmonth_bitems': {
    'rentval' : 1,
    # 'condfee': 1,
    'proptax' : 1,
  }, # ends inmonth_bitems key
  'triple_pay_date_intcorr_list': [('paidamount1', 'date1', 'intcorr1')],
}
rent_bill_monthdict_list.append(rent_bill_monthdict_listelement)

rent_bill_monthdict_listelement = {
  'contract_id'  : 'HLB01',
  'refmonthdate' : '2019-11-01',
  'duedate'      : '2019-12-10',
  'ini_balance'  : 1,
  'total_when_open' : 1,
  'total_paid'   : 1,
  'incidence_value': 1,
  'fin_balance'  : 1,
  'inmonth_bitems': {
    'rentval' : 1,
    # 'condfee': 1,
    'proptax' : 1,
  }, # ends inmonth_bitems key
  'triple_pay_date_intcorr_list': [('paidamount1', 'date1', 'intcorr1')],
}
rent_bill_monthdict_list.append(rent_bill_monthdict_listelement)


# process

json_filename = 'data_rent_system.txt'
with open(json_filename, 'w') as outfile:
  json.dump(json_file_data, outfile)
