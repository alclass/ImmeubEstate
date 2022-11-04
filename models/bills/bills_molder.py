#!/usr/bin/env python3
# bills.py

import copy, datetime
import fs.lib_functions  as funclib
import fs.date_functions as dtfunc
# import json_tofrom.general_json_reader_writer as jsonreadwrite
import fs.db.json_tofrom.bills_json_reader as billread
from fs.db import json_tofrom as contrread


class Bill:
  '''


  However, this class will implement bill's functionalities.
  Some of these functionalities are:
    1) it contains the initial data for bill monthly closing
    2) it passes itself (an instance) to the closing routines and absorbs its return
    3) it has routines for data entering, so that payment(s) may be recorded
    4) it has routines to generate a monthly bill (after closing, if it's not the first one) and
  '''
  ini_balance: int

  billitem_ntuple_constr = funclib.billitem_ntuple_constr # collections.namedtuple('BillItemNamedTuple', 'itdate, ittype, itvalue, itobs, itformula')
  KItemTypes = funclib.KItemTypes

  INMONTH_AMOUNT_TYPES = funclib.INMONTH_AMOUNT_TYPES
  ITEM_TYPES_SET_ONLY_ONCE_IN_A_BILL = [
    KItemTypes.TK_IBALANCE,
    KItemTypes.TK_RENTVAL,
    KItemTypes.TK_CONDFEE,
    KItemTypes.TK_PROPTAX,
    KItemTypes.TK_FDEPTAR,
    KItemTypes.TK_INTMCORR,
  ]

  def __init__(self, bill_dict): #  , *args, **kwargs # contract, billingitem_namedtuplelist
    '''

    In the old implementation, cls inherited collections.MutableSequence
    Based on a StackOverflow answer in:
    https://stackoverflow.com/questions/3387691/how-to-perfectly-override-a-dict
    A dictionary that applies an arbitrary key-altering
       function before accessing the keys
      # self.store = dict()
      # self.update(dict(*args, **kwargs))  # use the free update to set keys

    billitem_ntuple_constr = collections.namedtuple('BillItemNamedTuple', 'itdate, ittype, itvalue, itobs, itformula')

     {'contract_id': 'HLB01', 'refmonthdate': '2019-10-01', 'duedate': '2019-11-10', 'status': 'closed',
     'ini_balance': 0, 'total_when_open': 2923.79, 'total_paid': 2923.79, 'incidence_value': None, 'fin_balance': 0,
     'inmonth_bitems': {'rentval': 2069.32, 'condfee': 715.67, 'proptax': 138.8},
     'quad_payment_namedtuplelist': [[[2923.79, '2019-11-10 12:00:00', None, None]]]}

    :param contract:
    :param billingitem_namedtuplelist:
    '''

    self.bill_dict = bill_dict
    self.billingitem_namedtuplelist = []
    self.ini_balance = 0
    # self.fin_balance = None
    self.spread_bill_dict()

  def spread_bill_dict(self):

    contract_id = self.bill_dict['contract_id']
    self.contract = contread.get_contract_dict_by_id(contract_id)
    self.refmonthdate = None # the billing items will set refmonthdate
    try:
      inmonth_bitems = self.bill_dict['inmonth_bitems']
      self.inmonth_bitems = InMonthAmount(inmonth_bitems)
    except KeyError:
      pass
    self.init_billingitems()
    self.duedate = self.bill_dict['duedate']
    self.status = self.bill_dict['status']
    self.ini_balance = self.bill_dict['ini_balance']
    self.fin_balance = self.bill_dict['fin_balance']
    self.quad_payment_namedtuplelist = self.bill_dict['quad_payment_namedtuplelist']
    self.spread_quad_payment_namedtuplelist()

  def spread_quad_payment_namedtuplelist(self):
    '''
    'payvalue' : 2200,
    'paydate'  : '2018-12-10',
    'payauthstring': '',
    'pay_obs': 'Depósito no ...',
    :return:
    '''
    for p in self.quad_payment_namedtuplelist:
      if p['payvalue'] > 0:
        itdate = p['paydate']
        itvalue = p['payvalue']
        ittype = self.KItemTypes.TK_PAYMENT
        itobs = ''
        if p['payauthstring'] is not None:
          itobs = p['payauthstring']
        if p['pay_obs'] is not None:
          itobs += ': ' +  p['pay_obs']
        billingitem_namedtuple = self.billitem_ntuple_constr(itdate=itdate, ittype=ittype, itvalue=itvalue, itobs=itobs, itformula=None)

  def init_billingitems(self):
    if self.ini_balance is None:
      error_msg = 'self.ini_balance is None in Bill class (bills.py)'
      raise Exception(error_msg)
    pdate = copy.copy(self.refmonthdate)
    ittype = self.KItemTypes.TK_IBALANCE
    itvalue = self.ini_balance
    billingitem_namedtuple = self.billitem_ntuple_constr(itdate=pdate, ittype=ittype, itvalue=itvalue, itobs=None, itformula=None)
    self.billingitem_namedtuplelist.append(billingitem_namedtuple)
    if self.inmonth_bitems is not None:
      if self.inmonth_bitems.rentval is not None:
        itdate = copy.copy(self.refmonthdate)
        ittype = self.KItemTypes.TK_RENTVAL
        itvalue = self.inmonth_bitems.rentval
        billingitem_namedtuple = self.billitem_ntuple_constr(itdate=itdate, ittype=ittype, itvalue=itvalue, itobs=None, itformula=None)
    if self.inmonth_bitems.condfee is not None:
      itdate = copy.copy(self.refmonthdate)
      ittype = self.KItemTypes.TK_CONDFEE
      itvalue = self.inmonth_bitems.condfee
      billingitem_namedtuple = self.billitem_ntuple_constr(itdate=itdate, ittype=ittype, itvalue=itvalue, itobs=None, itformula=None)
    if self.inmonth_bitems.proptax is not None:
      itdate = copy.copy(self.refmonthdate)
      ittype = self.KItemTypes.TK_PROPTAX
      itvalue = self.inmonth_bitems.proptax
      billingitem_namedtuple = self.billitem_ntuple_constr(itdate=itdate, ittype=ittype, itvalue=itvalue, itobs=None, itformula=None)
    if self.inmonth_bitems.fdeptar is not None:
      itdate = copy.copy(self.refmonthdate)
      ittype = self.KItemTypes.TK_FDEPTAR
      itvalue = self.inmonth_bitems.fdeptar
      billingitem_namedtuple = self.billitem_ntuple_constr(itdate=itdate, ittype=ittype, itvalue=itvalue, itobs=None, itformula=None)
    if self.inmonth_bitems.extraim is not None:
      itdate = copy.copy(self.refmonthdate)
      ittype = self.KItemTypes.TK_EXTRAIM
      itvalue = self.inmonth_bitems.extraim
      billingitem_namedtuple = self.billitem_ntuple_constr(itdate=itdate, ittype=ittype, itvalue=itvalue, itobs=None, itformula=None)

  def init_inmonth_amount(self):

    # Attributes that will be taken later on (on process)
    self.ini_balance  = 0 # saldo may or not be in the initial billing items
    # Receiving params
    #self.contract = contract
    # self.billingitem_namedtuplelist = billingitem_namedtuplelist
    # Checks
    self.check_billingitem_namedtuplelist_n_set_refmonthdate()
    self.check_bitems_that_should_happen_only_once()
    self.sum_n_set_inmonth_amount()

  def qty_bitems(self):
    return len(self.billingitem_namedtuplelist)

  def check_billingitem_namedtuplelist_n_set_refmonthdate(self):
    if len(self.billingitem_namedtuplelist) == 0:
      error_msg = 'type(billingitems_namedtuple) == 0: # at constructing Bill (data entered need to contain the base items RENT (at least this one), PROPT, CONDF et al)'
      raise Exception(error_msg)
    bi_date = self.billingitem_namedtuplelist[0].itdate
    # set_refmonthdate
    self.refmonthdate = datetime.date(year=bi_date.year, month=bi_date.month, day=1)
    for billingitems_namedtuple in self.billingitem_namedtuplelist:
      if type(billingitems_namedtuple) != self.billitem_ntuple_constr: # BillItemNamedTuple
        error_msg = 'type(billingitems_namedtuple) != self.billitem_ntuple_constr: # BillItemNamedTuple at constructing Bill'
        raise Exception(error_msg)
      if billingitems_namedtuple.ittype == self.KItemTypes.TK_IBALANCE:
        self.ini_balance = billingitems_namedtuple.itvalue
      bi_date = billingitems_namedtuple.itdate
      if not dtfunc.are_same_year_n_same_month(self.refmonthdate, bi_date):
        error_msg = 'not dtfunc.are_same_year_n_same_month(self.refmonthdate=%s, bi_date=%s)' %(self.refmonthdate, bi_date)
        raise Exception(error_msg)

  def check_bitems_that_should_happen_only_once(self):
    '''
    For the time being, it checks only fields that should not happen more than once.
    :return:
    '''
    ITEM_TYPES_USED = []
    for billingitem_namedtuple in self.billingitem_namedtuplelist:
      if billingitem_namedtuple.ittype in self.ITEM_TYPES_SET_ONLY_ONCE_IN_A_BILL:
        if billingitem_namedtuple.ittype in ITEM_TYPES_USED:
          error_msg = 'Error: type %s was used more than once.' %billingitem_namedtuple.ittype
          raise Exception(error_msg)
        ITEM_TYPES_USED.append(billingitem_namedtuple.ittype)

  def sum_n_set_inmonth_amount(self):
    '''

    :return:
    '''
    self._inmonth_amount = 0
    INMONTH_AMOUNT_TYPES = self.contract.copy_billing_item_types_for_inmonth_amount()
    for billingitem_namedtuple in self.billingitem_namedtuplelist:
      if billingitem_namedtuple.ittype in INMONTH_AMOUNT_TYPES:
        self._inmonth_amount += billingitem_namedtuple.itvalue

  @property
  def inmonth_amount(self):
    if self._inmonth_amount is None:
      self.sum_n_set_inmonth_amount()
    return self._inmonth_amount

  @inmonth_amount.setter
  def inmonth_amount(self, value):
    error_msg = 'Error: inmonth_amount is a private attribute, it cannot be set.'
    raise Exception(error_msg)

  @property
  def duedate(self):
    if self.refmonthdate is None:
      return None
    return self.contract.get_duedate_with_refmonth(self.refmonthdate)

  @property
  def previousrefmonthdate(self):
    if self.refmonthdate is None:
      return None
    return dtfunc.add_months(self.refmonthdate, -1)

  @property
  def nextrefmonthdate(self):
    if self.refmonthdate is None:
      return None
    return dtfunc.add_months(self.refmonthdate, +1)

  @property
  def mora_params(self):
    if self.contract is None:
      return None
    if self.contract.mora_params is None:
      return None
    return self.contract.mora_params

  @property
  def incidence_fine_fraction(self):
    if self.mora_params is None:
      return None
    return self.mora_params.incidence_fine_fraction

  @property
  def fix_monthly_interest(self):
    if self.mora_params is None:
      return None
    return self.mora_params.fix_monthly_interest

  @property
  def monet_corr_fraction(self):
    if self.mora_params is None:
      return None
    return self.mora_params.monet_corr_fraction

  @property
  def ini_debt(self):
    if self.ini_balance is None:
      return None
    if self.ini_balance <= 0:
      return 0
    return self.ini_balance

  @property
  def ini_cred(self):
    if self.ini_balance is None:
      return None
    if self.ini_balance < 0:
      return -self.ini_balance
    return 0

  @property
  def fin_balance(self):
    for billingitem_namedtuple in self.billingitem_namedtuplelist:
      if billingitem_namedtuple.ittype == self.KItemTypes.TK_FBALANCE:
        return billingitem_namedtuple.itvalue
    return 0

  @property
  def fin_debt(self):
    if self.fin_balance is None:
      return None
    if self.fin_balance > 0:
      return self.fin_balance
    return 0

  @property
  def fin_cred(self):
    if self.fin_balance is None:
      return None
    if self.fin_balance < 0:
      return -self.fin_balance
    return 0

  def generate_bill_as_text(self):
    outstr = 'Mês Ref => %s\n' %self.refmonthdate
    balance = self.ini_balance
    debt_or_cred = ''
    if balance > 0:
      debt_or_cred = '(débito)'
    elif balance < 0:
      debt_or_cred = '(crédito)'
    outstr += 'Saldo Inicial => %.2f %s\n' %(self.ini_balance, debt_or_cred)
    outstr += 'In-month Amount => %.2f\n' %(self.inmonth_amount)
    return outstr

  def __str__(self):
    return self.generate_bill_as_text()


def create_bill_from_orderedDict(oDict):
  contract_id = oDict['contract_id']
  # get_contract_dict_by_id(contract_id)
  contract = contread.get_contract_dict_by_id(contract_id)
  print(contract)


def ptest():
  bill_id = '20191001HLB01'
  bill = billread.read_all(bill_id)
  print(bill)

  contrread
  bill_dict = bills_dict[]
  print(bill_dict)
  contract_id = bill_dict['contract_id']
  contract = contrread.get_contract_dict_by_id(contract_id)
  print(contract)
  bill_obj = Bill(bill_dict)

def process():
  msg = '''
  This module has class Bill (BillMonthCloser inherits from it and is in another module).
  There are unit tests covering them and a simple printable scripts named like cases_bills.py
  '''
  print(msg)
  ptest()

if __name__ == '__main__':
  process()
