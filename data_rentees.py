#!/usr/bin/env python3

import datetime
import sys
from collections import namedtuple
import Rentee

contract_params_dict = {
  'JACUM' : {
    'name':'Beth & Filipe',
    #'INCIDENCE_FINE' : 0.1,
    #'FIX_MONTHLY_INTEREST' : 0.01,
    #'DUEDAY_IN_MONTH' : 10,
    'rubricas_dict' :  {
      'rent' : {
        'value' : 3553,
        'months' : list(range(1, 13)),
      },
      # there isn't condfee in JACUM
      'proptax' : {
        'value' : 330,
        'months' : list(range(1, 11)),
      },
      'firetariff' : {
        'value' : 120,
        'months' : [6],
      },
    }, # ends rubricas_dict
  },
  'CDUTRA' : {
    'name':'Munzer',
    #'INCIDENCE_FINE' : 0.1,
    #'FIX_MONTHLY_INTEREST' : 0.01,
    #'DUEDAY_IN_MONTH' : 10,
    'rubricas_dict' :  {
      'rent' : {
        'value' : 3553,
        'months' : list(range(1, 13)),
      },
      'condfee' : {
        'value' : 1540,
        'months' : list(range(1, 13)),
      },
      'proptax' : {
        'value' : 330,
        'months' : list(range(1, 11)),
      },
      'firetariff' : {
        'value' : 120,
        'months' : [6],
      },
    }, # ends rubricas_dict
  }, # ends CDUTRA
  'HLOBO' : {
    'name':'Lucio',
    #'INCIDENCE_FINE' : 0.1,
    #'FIX_MONTHLY_INTEREST' : 0.01,
    #'DUEDAY_IN_MONTH' : 10,
    'rubricas_dict' :  {
      'rent' : {
        'value' : 1553,
        'months' : list(range(1, 13)),
      },
      'condfee' : {
        'value' : 840,
        'months' : list(range(1, 13)),
      },
      'proptax' : {
        'value' : 230,
        'months' : list(range(1, 11)),
      },
      'firetariff' : {
        'value' : 110,
        'months' : [6],
      },
    } # ends rubricas_dict
  }, # ends HLOBO
}
print ('contract_params_dict')
print (contract_params_dict)

rec1namedtuple = {
  'contract_params_key': 'JACUM',
  'refmonth': '1/11/2019',
  # 'paydate': '9/11/2019',
  'previous_refmonth_was_closed': '1', # it's always at month's turn
  'valor_debito_fechado':'0',
  # for testing
  'outside_calculated_due': '1553',
}
rec1obj = namedtuple("Rentee", rec1namedtuple.keys())(*rec1namedtuple.values())
print (rec1obj)

rec2namedtuple = {
  'contract_params_key': 'CDUTRA',
  'refmonth': '1/11/2019',
  'paydate': '11/11/2019',
  'condo_rate': '3500',
  'apply_property_tax': True,
  'previous_refmonth_was_closed': '1', # it's always at month's turn
  'valor_debito_fechado':'33000',
  'outside_calculated_due': '1',
}
rec2obj = namedtuple("Rentee", rec2namedtuple.keys())(*rec2namedtuple.values())
print (rec2obj)

rec3namedtuple = {
  'refmonth': '1/11/2019',
  'paydate': '11/11/2019',
  'rentvalue': '3500',
  'condo_rate': '3500',
  'apply_property_tax': True,
  'carried_debt': '33000',
  'contract_params_key': 'CDUTRA',
  'outside_calculated_due': '1',
}
rec3obj = namedtuple("Rentee", rec3namedtuple.keys())(*rec3namedtuple.values())
print (rec3obj)
print (type(rec3obj))
