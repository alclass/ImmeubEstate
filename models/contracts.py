#!/usr/bin/env python3
# contracts.py

import copy, datetime
import func.textfs.ctes_n_printlist_etc as ctes
import func.db.json_tofrom.json_readers as jreader
import models.immeubles

KItemTypes = ctes.KItemTypes

DEFAULT_INCIDENCE_FINE_FRACTION = 0.1
DEFAULT_FIX_MONTHLY_INTEREST    = 0.01
DEFAULT_MONET_CORR_FRACTION     = 0.003
DEFAULT_APPLY_MONTHLY_MONET_CORR= True

class MoraParams:

  def __init__(self):
    self.incidence_fine_fraction      = None
    self.fix_monthly_interest_fraction= None
    self.apply_monthly_monet_corr     = None
    self.refmonthdate                 = None
    self._monthly_monet_corr_fraction = None
    self.fetch_monet_corr_in_db       = None

  def init_by_fields(self,
      incidence_fine_fraction=None,
      fix_monthly_interest_fraction=None,
      apply_monthly_monet_corr=None,
      refmonthdate = None,
      monthly_monet_corr_fraction = None,
      fetch_monet_corr_in_db=True,
    ):
    self.incidence_fine_fraction      = incidence_fine_fraction
    self.fix_monthly_interest_fraction= fix_monthly_interest_fraction
    self.apply_monthly_monet_corr     = apply_monthly_monet_corr
    self.refmonthdate                 = refmonthdate
    self._monthly_monet_corr_fraction = monthly_monet_corr_fraction
    self.fetch_monet_corr_in_db       = fetch_monet_corr_in_db

  def init_by_paramsdict(self, mora_params_dict):

    self.interiorize_params(mora_params_dict)
    self.fix_defaults_if_needed()

  def fetch_n_set_monet_corr_fraction_in_refmonthdate(self):
    if self._monthly_monet_corr_fraction is not None:
      return self._monthly_monet_corr_fraction
    if self.refmonthdate is None:
      return None
    oreader = jreader.DataGroupJsonReader(jreader.DG_IPCA)
    pdict = oreader.get_dict_by_id_from_json(self.refmonthdate)
    # notice it may be None from here
    return self._monthly_monet_corr_fraction

  @property
  def monthly_monet_corr_fraction(self):
    if self._monthly_monet_corr_fraction is not None:
      return self._monthly_monet_corr_fraction
    return self.fetch_n_set_monet_corr_fraction_in_refmonthdate()

  def interiorize_params(self, via_params_dict):
    self.incidence_fine_fraction       = via_params_dict['incidence_fine_fraction']
    self.fix_monthly_interest_fraction = via_params_dict['fix_monthly_interest_fraction']
    self.apply_monthly_monet_corr      = via_params_dict['apply_monthly_monet_corr']

  def fix_defaults_if_needed(self):
    if self.incidence_fine_fraction is None or type(self.incidence_fine_fraction) != float:
      self.incidence_fine_fraction = DEFAULT_INCIDENCE_FINE_FRACTION
    if self.fix_monthly_interest_fraction is None or type(self.fix_monthly_interest_fraction) != float:
      self.fix_monthly_interest_fraction = DEFAULT_FIX_MONTHLY_INTEREST
    if self.apply_monthly_monet_corr is None:
      self.apply_monthly_monet_corr = DEFAULT_APPLY_MONTHLY_MONET_CORR

DEFAULT_BILLING_ITEM_TYPES_FOR_INMONTH_AMOUNT = [
  ctes.KItemTypes.TK_RENTVAL,
  ctes.KItemTypes.TK_CONDFEE,
  ctes.KItemTypes.TK_PROPTAX,
  ctes.KItemTypes.TK_FDEPTAR,
]

class Contract:
  '''

{"contract_id": "CDT02", "contractor_ids": ["munzer1"], "immeuble_id": "CDUTR",
  "contract_inidate": "2016-10-01", "dueday_in_month": 10,
  "older_rent_values_n_interval": [[[2700, "2015-10-01,2018-01-31"], [2800, "2015-10-01,2018-01-31"]]],
  "current_rent_value": 3387.11,
  "rent_duration_dates": [[2700, "2015-10-01,2018-01-31"], [2800, "2015-10-01,2018-01-31"]],
  "chosen_proptax_discount_one_pay": false,
  "mora_params": {"INCIDENCE_FINE": 0.1, "FIX_MONTHLY_INTEREST": 0.01, "MONET_CORR_FRACTION": true},
  "repasse": ["condfee", "firetariff", "proptax"],
  "receive_verification_of": [],
  "guarantee_type": "fianca"},

  '''

  def __init__(self, contract_id):
    '''

    '''
    self.contract_id = contract_id
    self.immeuble5letter = None
    self._immeuble = None
    self._address = None
    self.mora_params = None # itself, from json, is a dict
    self._mora_params_obj = None # itself is an object possibly derived from dict
    self.contractor_ids = None
    self._contractors = None
    self.contract_inidate = None
    self.dueday_in_month  = 10 # default
    self.duration_in_months  = None # default
    self.duration_in_days    = None # default
    self.chosen_proptax_discount_one_pay = False  # default
    self.current_rent_value = None
    self.repasse = None
    self.receive_verification_of = None
    self.guarantee_type = None

  def expand_attributes_from_json(self):
    '''
    This method should not be called from __init__() but is called outside after construction
    :return:
    '''
    if self.contract_id is None:
      error_msg = 'self.contract_id is None in class Contract, method expand_attributes_from_json()'
      raise ValueError(error_msg)
    oreader = jreader.DataGroupJsonReader(jreader.DG_CONTRACT)
    pdict = oreader.get_dict_by_id_from_json(self.contract_id)
    if pdict is None:
      error_msg = 'contract_id %s does not exist in db' % self.contract_id
      raise ValueError(error_msg)
    for k in pdict:
      if k == 'contract_id':
        contract_id = pdict[k]
        if contract_id != self.contract_id:
          error_msg = 'Inconsistent value of contract_id %s against the one inside db dict %s' %(self.contract_id, contract_id)
          raise ValueError(error_msg)
        continue
      setattr(self, k, pdict[k])

  @property
  def immeuble(self):
    if self._immeuble is not None:
      return self._immeuble
    if self.immeuble5letter is None:
      return None

    oreader = jreader.DataGroupJsonReader(jreader.DG_ADDRESS)
    pdict = oreader.get_dict_by_id_from_json(self.immeuble5letter)
    # notice self._immeuble may be None from here
    return self._immeuble

  @classmethod
  def create_instance_by_dict(cls, contract_dict):
    '''

    :param contract_dict:
    :return:
    '''
    contract_id = contract_dict['contract_id']
    contract = cls(contract_id)
    contract.expand_attributes_from_json()
    return contract

  @classmethod
  def create_instance_by_id_from_json(cls, contract_id):
    pdict = contrread.get_contract_dict_by_id(contract_id)
    return Contract.create_instance_by_dict(pdict)

  '''
  def set_billing_item_types_for_inmonth_amount(self):
    self.billing_item_types_for_inmonth_amount = self.contract_content_dict['billing_item_types_for_inmonth_amount']
    if self.billing_item_types_for_inmonth_amount is None:
      self.billing_item_types_for_inmonth_amount = copy.copy(DEFAULT_BILLING_ITEM_TYPES_FOR_INMONTH_AMOUNT)
  '''

  def copy_billing_item_types_for_inmonth_amount(self):
    return copy.copy(self.billing_item_types_for_inmonth_amount)

  @property
  def incidence_fine_fraction(self):
    return self.mora_params.incidence_fine_fraction

  @property
  def contractors(self):
    if self._contractors is not None:
      return self._contractors
    if self.contractor_ids is None:
      return None
    self._contractors = []
    for contractor_id in self.contractor_ids:
      contractor = persread.get_person_from_json_by_id(contractor_id)
      self._contractors.append(contractor)

  @property
  def mora_params_obj(self):
    if self._mora_params_obj is not None:
      return self._mora_params_obj
    if self.mora_params is None:
      return None
    self._mora_params_obj = MoraParams()
    self._mora_params_obj.init_by_paramsdict(self.mora_params)
    return self._mora_params_obj

  @property
  def incidence_fine_fraction(self):
    if self.mora_params_obj:
      return self.mora_params_obj.incidence_fine_fraction
    return None

  @property
  def fix_monthly_interest(self):
    if self.mora_params_obj:
      return self.mora_params_obj.fix_monthly_interest_fraction
    return None

  @property
  def apply_monthly_monet_corr(self):
    if self.mora_params_obj:
      return self.mora_params_obj.apply_monthly_monet_corr
    return None

  def find_n_set_immeuble(self):
    if self.immeuble5letter is None:
      return None
    if self._immeuble is not None:
      return self._immeuble
    self._immeuble = models.immeubles.Immeuble.fetch_immeuble_by_5letter(self.immeuble5letter)
    # it may be None from here
    return self._immeuble

  def find_n_set_address(self):
    _ = self.find_n_set_immeuble()
    if self._immeuble is None:
      return None
    if self._immeuble.address is None:
      return None
    self._address = self._immeuble.address

    # pdict = immeubread.get_immeuble_dict_by_i5letter(self.immeuble5letter)
    #Immeuble.(self.immeuble5letter)
    self._immeuble = models.immeubles.Immeuble.fetch_address_by_id(self.immeuble5letter)

  @property
  def immeuble(self):
    if self._immeuble is not None:
      return self._immeuble
    if self.immeuble5letter is None:
      return None
    self.find_n_set_immeuble()
    return self._immeuble

  @property
  def address(self):
    if self._address is not None:
      return self._address
    if self.immeuble5letter is None:
      return None
    if self.immeuble is None:
      self.find_n_set_immeuble()
    if self.immeuble is None:
      return None
    self.immeuble.set_address()
    if self.immeuble.address is None:
      return None
    self._address = self.immeuble.address
    return self._address

  @property
  def full_address(self):
    _ = self.find_n_set_address()
    if self.address is None:
      return 's/inf'
    return str(self.address)

  def get_duedate_with_refmonth(self, refmonthdate):
    '''

    This class Contract knows nothing of refmonthdate.  This is composed with classes Bill and Closer.
    No error-recovery exists here for the time being concerning refmonthdate. It's been decided to avoid picking up today's date if refmonthdate is not good.
    :param refmonthdate:
    :return:
    '''
    if refmonthdate is None:
      return None
    return datetime.date(year=refmonthdate.year, month=refmonthdate.month, day=self.due_day_in_month)

  def __str__(self):
    outstr = 'Contract: %s\n' %self.contract_id
    outstr += '\tAddress => %s\n' %self.full_address
    outstr += '\tdayday in month => %s\n' %self.dueday_in_month
    outstr += '\tduration_in_months => %s\n' %self.duration_in_months
    outstr += '\tincidence_fine_fraction => %f\n' %self.incidence_fine_fraction
    outstr += '\tfix_monthly_interest_fraction => %f\n' %self.fix_monthly_interest
    outstr += '\tapply_monthly_monet_corr => %s\n' %str(self.apply_monthly_monet_corr)
    #outstr += '\tbilling_item_types_for_inmonth_amount => %s\n' %str(self.billing_item_types_for_inmonth_amount)
    return outstr

def simpletest():
  contract_id = 'CDT02'
  contract = Contract.create_instance_by_id_from_json(contract_id)
  print ('Contract =>')
  print (contract)

def process():
  simpletest()

if __name__ == '__main__':
  process()