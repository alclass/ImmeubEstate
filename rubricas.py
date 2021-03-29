#!/usr/bin/env python3

import datetime
import sys
from collections import namedtuple
import Rentee

MONTHLY = 1
YEARLY = 2

rubricas_dict = {
  'rent' : {
    'freq' : MONTHLY,
    'months' : list(range(1,13)),
    'applies_to' : ['JACUM', 'HLOBO', 'CDUTRA'],
  },
  'proptax' : {
    'freq' : MONTHLY,
    'months' : list(range(1,11)),
    'applies_to' : ['JACUM', 'HLOBO', 'CDUTRA'],
  },
  'condfee' : {
    'freq' : MONTHLY,
    'months' : list(range(1,13)),
    'applies_to' : ['HLOBO', 'CDUTRA'],
  },
  'firetariff' : {
    'freq' : YEARLY,
    'months' : [6],
    'applies_to' : ['JACUM', 'HLOBO', 'CDUTRA'],
  },
}

print (rubricas_dict)

for rubrica in rubricas_dict:
  print(rubrica)

def rubricas_for(immeub_id, refdate):
  rubricas_to_apply = []
  for rubrica_name in rubricas_dict:
    inner_rubrica_dict = rubricas_dict[rubrica_name]
    if immeub_id in inner_rubrica_dict['applies_to']:
      if inner_rubrica_dict['freq'] == MONTHLY:
        if refdate.month in inner_rubrica_dict['months']:
          rubricas_to_apply.append(rubrica_name)
      elif inner_rubrica_dict['freq'] == YEARLY:
        if refdate.month in inner_rubrica_dict['months']:
          rubricas_to_apply.append(rubrica_name)
  return rubricas_to_apply

immeubles = ['JACUM', 'HLOBO', 'CDUTRA']
today = datetime.date.today()
for immeub_id in immeubles:
  rubricas = rubricas_for(immeub_id, today)
  print ('immeub_id', immeub_id)
  print ('rubricas', rubricas)
