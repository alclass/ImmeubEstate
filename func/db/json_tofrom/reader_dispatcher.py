#!/usr/bin/env python3
import json
'''
Order of data in json:

1) a list of persons dict
2) a list of immeubles dict
3) a list of contracts dict
4) a list of monthly bills dict
'''

# INDICES
PERSONS_INDEX_IN_JSON_DATA = 0
IMMEUBLES_INDEX_IN_JSON_DATA = 1
CONTRACT_INDEX_IN_JSON_DATA = 2
MONTHLY_BILLS_INDEX_IN_JSON_DATA = 3

class DataTypes:
  PERSONS   = 'PERSONS'
  IMMEUBLES = 'IMMEUBLES'
  CONTRACTS = 'CONTRACTS'
  BILLS     = 'BILLS'
  PAYMENTS  = 'PAYMENTS'
  PROPTAX_N_FDEPTAR     = 'PROPTAX_N_FDEPTAR'
  CONDFEE               = 'CONDFEE'
  MON_CORR_IPCA_INDICES = 'MON_CORR_IPCA_INDICES'

  datatypes = [PERSONS, IMMEUBLES, CONTRACTS, BILLS, PAYMENTS, PROPTAX_N_FDEPTAR, CONDFEE, MON_CORR_IPCA_INDICES]

  directives = {
    PERSONS: {
      'filename': 'persons.json',
    },
    IMMEUBLES: {
      'filename': 'immeubles.json',
    },
    CONTRACTS: {
      'filename': 'contracts.json',
    },
    BILLS: {
      'filename': 'bills.json',
    },
    PAYMENTS: {
      'filename': 'payments.json',
    },
    PROPTAX_N_FDEPTAR: {
      'filename': 'proptax_n_fdeptar.json',
    },
    CONDFEE: {
      'filename': 'condfee.json',
    },
    MON_CORR_IPCA_INDICES: {
      'filename': 'mon_corr_ipca_indices.json',
    }
  }


class ReaderDispatcher:

  datatypes = DataTypes.datatypes

  def __init__(self, datatype, doc_id):
    self.datatype = datatype
    self.doc_id = doc_id

  def get_filename(self):
    return DataTypes.directives[self.datatype]['filename']



class BillReader(ReaderDispatcher):

  def __init__(self, datatype, refmonthdate):

    super().__init__(datatype, refmonthdate, contract_id)
    self.contract_id = contract_id

  def read_bill(self):
    json_filename = self.get_filename()
    with open(json_filename) as json_file:
      json_file_data_as_dict = json.load(json_file)
    json_file_data_as_dict[]
