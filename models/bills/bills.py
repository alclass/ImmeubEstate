#!/usr/bin/env python3
# bills.py

import collections, copy, datetime
import fs.datefs as dtfunc
from models.contracts import Contract
import fs.textfs.ctes_n_printlist_etc as ctes
import fs.db.json_tofrom.jsonreaders as jreader
from models.payments import Payment

class InMonthAmount:

  def __init__(self, inmonth_bitems):

    self.rentval = None
    self.condfee = None
    self.proptax = None
    self.fdeptar = None
    self.extraim = None

    try:
      self.rentval = inmonth_bitems['rentval']
    except KeyError:
      pass
    try:
      self.condfee = inmonth_bitems['condfee']
    except KeyError:
      pass
    try:
      self.proptax = inmonth_bitems['proptax']
    except KeyError:
      pass
    try:
      self.proptax = inmonth_bitems['proptax']
    except KeyError:
      pass

class BItemCodes(collections.MutableMapping):
  '''
  B00 IBALANCE
  B01 RENTVAL
  B02 CONDFEE
  B03 PROPTAX
  B04 FDEPTAR
  E01 EXTRAIT1
  E02 EXTRAIT2
  E0<n> EXTRAIT<n>
  P01 PAYMENT1
  P02 PAYMENT2
  P0<n> PAYMENT<n>
  I01 INTNMOCO1
  I02 INTNMOCO2
  INC INTNMOCO<n>
<n>  P0<n> PAYMENT<n>

  Z99 FBALANCE (a derived field)
  '''

  codes_order =  [ ]
  pass

class BillingItem:

  DESCRIPTIONS = []
  DESCRIPTIONS.append('Saldo Inicial');  TYPE_IBALANCE   = 0
  DESCRIPTIONS.append('Saldo Final');    TYPE_FBALANCE   = 1
  DESCRIPTIONS.append('Aluguel Base');   TYPE_RENTVAL    = 2
  DESCRIPTIONS.append('Tar. Condomínio');TYPE_CONDFEE    = 3
  DESCRIPTIONS.append('IPTU');           TYPE_PROPTAX    = 4
  DESCRIPTIONS.append('Taxa Funesbom');  TYPE_FDEPTAR    = 5
  DESCRIPTIONS.append('Enc Ext Mensal'); TYPE_EXTRAIM    = 6
  DESCRIPTIONS.append('Total Mês Imed'); TYPE_TOTAL_MI   = 7
  DESCRIPTIONS.append('Total Mês');      TYPE_TOTAL_MES  = 8
  DESCRIPTIONS.append('Pagamento');      TYPE_PAYMENT    = 9
  DESCRIPTIONS.append('Juros & Cor.Mon.');TYPE_INTMONCOR = 10
  DESCRIPTIONS.append('Total J&CM Mês'); TYPE_INTMC      = 11
  DESCRIPTIONS.append('Multa Incidência');TYPE_INC_FINE  = 12
  DESCRIPTIONS.append('Total I,J&CM Mês');TYPE_TOT_INCINT= 13

  def __init__(self, seq=None, itdate=None, ittype=None, itvalue=None, obs=None, formula=None):
    self.seq        = seq
    self.itdate     = itdate
    self.ittype     = ittype
    self.description= ''
    self.set_description_by_ittype()
    self.itvalue    = itvalue
    self.obs        = obs
    self.formula    = formula

  def set_description(self):
    try:
      self.description= self.DESCRIPTIONS[self.ittype]
    except KeyError:
      self.description = 'Rubrica'

  def spread_bitem_dict(self, bitem_dict):
    for k in bitem_dict:
      setattr(self, k, bitem_dict[k])

def sort_bitem_by_date_n_type(bitem_dictlist):
  return sorted(bitem_dictlist, key=lambda k: (k['itdatetime'], k['ittype']))

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

  billitem_ntuple_constr = ctes.billitem_ntuple_constr # collections.namedtuple('BillItemNamedTuple', 'itdate, ittype, itvalue, itobs, itformula')
  KItemTypes = ctes.KItemTypes

  INMONTH_AMOUNT_TYPES = ctes.INMONTH_AMOUNT_TYPES
  ITEM_TYPES_SET_ONLY_ONCE_IN_A_BILL = [
    KItemTypes.TK_IBALANCE,
    KItemTypes.TK_RENTVAL,
    KItemTypes.TK_CONDFEE,
    KItemTypes.TK_PROPTAX,
    KItemTypes.TK_FDEPTAR,
    # KItemTypes.TK_INTMCORR,
  ]

  def __init__(self, bill_id): #  , *args, **kwargs # contract, billingitem_namedtuplelist
    self.bill_id = bill_id
    self.contract_id = bill_id
    self._contract = None

    self.billing_item_dictlist = []
    self.ini_balance = 0
    self._inmonth_amount = None
    # self.fin_balance = None

  @classmethod
  def create_instance(cls, bill_id):
    bill = cls(bill_id)
    oreader = jreader.DataGroupJsonReader(jreader.DG_ADDRESS)
    pdict = oreader.get_dict_by_id_from_json(bill_id)
    if pdict is None:
      return None
    bill.init_bill_with_dict(pdict)
    return bill

  def init_bill_with_dict(self, bill_dict): #  , *args, **kwargs # contract, billingitem_namedtuplelist

    self.bill_dict = bill_dict
    self.expand_attributes_from_dict()

  def expand_attributes_from_dict(self):
    '''
    This method should be called after init_bill_with_dict(self, bill_dict)
    :return:
    '''

    for k in self.bill_dict:
      setattr(self, k, self.bill_dict[k])

    # self.init_billingitems()

  @classmethod
  def fetch_bill_by_id_from_json(cls, bill_id):
    oreader = jreader.DataGroupJsonReader(jreader.DG_ADDRESS)
    pdict = oreader.get_dict_by_id_from_json(bill_id)
    if pdict is None:
      return None
    billobj = cls(bill_id)
    billobj.bill_dict = pdict
    billobj.expand_attributes_from_dict()
    return billobj

  @property
  def contract(self):
    if self._contract is not None:
      return self._contract
    if self.contract_id is None:
      return None
    oreader = jreader.DataGroupJsonReader(jreader.DG_CONTRACT)
    pdict = oreader.get_dict_by_id_from_json(self.contract_id)
    if pdict is None:
      return None
    contract = Contract(self.contract_id)
    contract.expand_attributes_from_json(pdict)
    self._contract = contract
    return self._contract

  def integrate_payments(self, paymentdictlist):
    '''
    '''
    self.integrated_bitems = copy.copy(self.billing_items_dictlist)
    self.integrated_bitems += paymentdictlist
    self.integrated_bitems = sort_bitem_by_date_n_type(self.integrated_bitems)
    for billing_item_dict in self.integrated_bitems:
      print (billing_item_dict)

  def qty_bitems(self):
    return len(self.billing_items_dictlist)

  def check_billingitem_namedtuplelist_n_set_refmonthdate(self):
    if len(self.billing_items_dictlist) == 0:
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
    for billing_items_dict in self.billing_items_dictlist:
      if billing_items_dict['is_inmonth']:
        self._inmonth_amount += billing_items_dict['itvalue']


  @property
  def inmonth_amount(self):
    if self._inmonth_amount is None:
      self.sum_n_set_inmonth_amount()
    return self._inmonth_amount

  @inmonth_amount.setter
  def inmonth_amount(self, value):
    '''
  @property
  def duedate(self):
    if self.refmonthdate is None:
      return None
    return self.contract.get_duedate_with_refmonth(self.refmonthdate)

    :param value:
    :return:
    '''
    error_msg = 'Error: inmonth_amount is a private attribute, it cannot be set.'
    raise Exception(error_msg)

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
    '''
  @property
  def fin_balance(self):
    for billingitem_namedtuple in self.billingitem_namedtuplelist:
      if billingitem_namedtuple.ittype == self.KItemTypes.TK_FBALANCE:
        return billingitem_namedtuple.itvalue
    return 0

    :return:
    '''
    if self.ini_balance is None:
      return None
    if self.ini_balance < 0:
      return -self.ini_balance
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

  def str_as_lines(self):
    '''

    :return:
    '''
    lines = []
    line = 'Bill id %s Ref-Month %s' %(self.bill_id, self.refmonthdate)
    lines.append(line)
    line = 'Saldo inicial: %s In-Month %s' %(str(self.ini_balance), self.inmonth_amount)
    lines.append(line)
    self.billing_items_dictlist = sort_bitem_by_date_n_type(self.billing_items_dictlist)
    for billing_items_dict in self.billing_items_dictlist:
      itdatetime  = billing_items_dict['itdatetime']
      ittype      = billing_items_dict['ittype']
      description = billing_items_dict['description']
      itvalue     = billing_items_dict['itvalue']
      itobs1      = billing_items_dict['itobs1']
      itobs2      = billing_items_dict['itobs2']
      is_inmonth  = billing_items_dict['is_inmonth']
      line        = '%s %d %s %f %s %s' %(itdatetime, ittype, description, itvalue, itobs1, is_inmonth)
      lines.append(line)
    return lines

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

  def pretty_print_bill(self):
    '''

    :return:
    '''
    text = '\n'
    line = 'Boleta de Cobrança do Aluguel e Encargos:\n'
    text += line
    line = '====================\n'
    text += line
    line = 'Mês ref ------- % s\n' %(self.monthrefdate)
    text += line
    line = 'Data de venc. ------- % s\n' %(self.duedate)
    text += line
    line = '-------------------\n'
    text += line
    line = 'Itens: ------- % s\n' %(self.duedate)
    text += line
    for i, billingitem in enumerate(self.billingitems):
      line = '%d -> %s  ----------  %s\n' %(i, billingitem[self.REFTYPE_KEY], str(billingitem['value']))
      text += line
    line = "Valor em débito do mês ant. %s\n" % (str(self.previousmonthsdebts))
    text += line
    line = '-------------------\n'
    text += line
    line = 'Total (Itens) ----  %.2f\n' % (self.inmonthpluspreviousdebts)
    text += line
    line = '==================\n'
    text += line
    line = 'Payments:\n'
    text += line
    line = 'Pagamento(s) no prazo:  %.2f\n' % (self.amount_paid_ontime)
    text += line
    line = 'Valor sob mora:  %.2f\n' % (self.valor_sob_mora)
    text += line
    if self.latepaysprocessor is not None:
      for ait in self.latepaysprocessor.increase_trails:
        text += str(ait)
    if self.multa_account > 0:
      line = 'Multa incidência de atraso ----  %.2f\n' % (self.multa_account)
      text += line
    if self.interest_n_cm_account > 0:
      line = 'Juro e Corr. Monet. relat. tempo-atraso %.2f\n' %(self.interest_n_cm_account)
      text += line
    line = 'Total (Mês) ----  %.2f\n' % (self.inmonthpluspreviousdebts)
    text += line
    line = 'Total Pago ----  %.2f\n' % (self.payment_account)
    text += line
    if self.inmonthpluspreviousdebts_minus_payments > 0:
      line = 'Total menos pagt(s) ----  %.2f\n' % (self.inmonthpluspreviousdebts_minus_payments)
      text += line
    if self.fine_interest_n_cm > 0:
      line = 'Total Mora   -------   %.2f\n' %(self.fine_interest_n_cm)
      text += line
    if self.multa_account + self.interest_n_cm_account > 0:
      line = 'Total mês considerado mora-atraso -----  %.2f\n' % (self.total_bill_with_mora_if_any)
      text += line
    if self.debt_account > 0:
      line = 'Valor aberto em débito: %.2f\n' %(self.debt_account)
      text += line
    if self.cred_account > 0:
      line = 'Crédito para próx. mês: %.2f\n' %(self.cred_account)
      text += line
    return text

  def __str__(self):
    # return self.generate_bill_as_text()
    return '\n'.join(self.str_as_lines())

def ptest():
  bill_id = '20190701CDT01'
  print('bill_id =', bill_id)
  bill = Bill.create_instance(bill_id)
  if bill is None:
    print ('bill is None')
    return
  bill.expand_attributes_from_dict()
  print(bill)
  payment_id = bill_id
  paydict = jreader.get_payment_by_id_from_json(payment_id)
  payobj = Payment.create_instance_from_dict(paydict)
  if payobj is None:
    print ('payobj is None')
    return
  bill.integrated_payment(payobj)
  print(bill)

def process():
  msg = '''
  This module has class Bill (BillMonthCloser inherits from it and is in another module).
  There are unit tests covering them and a simple printable scripts named like cases_bills.py
  '''
  print(msg)
  ptest()

if __name__ == '__main__':
  process()
