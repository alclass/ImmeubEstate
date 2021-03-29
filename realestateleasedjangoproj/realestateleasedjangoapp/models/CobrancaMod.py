#!/usr/bin/env python3
from django.db import models

from copy import copy
from datetime import date
# from datetime import timedelta
from dateutil.relativedelta import relativedelta
import json
import sys
# import calendar # calendar.monthrange(year, month)
# from .DateBillCalculatorMod import DateBillCalculator
from .BillingItemMod import BillingItem

try:
  from . import datagen
  from .PaymentMod import Payment
  from .juros_calculator import Juros
  # from .DateBillCalculatorMod import DateBillCalculator
  from .PaymentTimeProcessorMod import PaymentTimeProcessor
except SystemError:
  '''
  SystemError is raised when running this script in its folder
  One option is to include '.' (current folder) in sys.path
  and import the modules without their packages (the folders with __init__.py)   
  '''
  sys.path.insert(0, '.')
  import datagen
  from PaymentMod import Payment
  from juros_calculator import Juros
  # from DateBillCalculatorMod import DateBillCalculator
  from PaymentTimeProcessorMod import PaymentTimeProcessor


REFTYPE_KEY = 'reftype'
CARR_REFTYPE = 'CARR'


class Cobranca(models.Model):

  # REFTYPE_KEY = REFTYPE_KEY

  # id = models.IntegerField(primary_key=True)
  monthrefdate   = models.DateField()
  monthseqnumber = models.PositiveIntegerField(default=1)
  duedate            = models.DateField(blank=True, null=True)
  contract           = models.ForeignKey('Contract', on_delete=models.DO_NOTHING)
  bankaccount = models.ForeignKey('BankAccount', on_delete=models.DO_NOTHING)

  total_amount_paid  = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
  amount_paid_ontime = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
  debt_to_next_bill  = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
  lastprocessingdate = models.DateField(blank=True, null=True)

  amountincreasetrailsjson = models.TextField(blank=True, null=True)

  obsinfo = models.TextField(blank=True, null=True)
  closed  = models.BooleanField(default=False)

  created_at = models.DateTimeField(blank=True, null=True)
  updated_at = models.DateTimeField(blank=True, null=True)

  #billingitems = models.ManyToManyField('BillingItem', related_name='billingitems')
  @property
  def billingitems(self):
    return BillingItem.objects.filter(cobranca=self)

  def route_url(self):
    urldict = {
      'year'       : self.monthrefdate.year,
      'month'      : self.monthrefdate.month,
      'contract_id': self.contract.id
    }

    url = '/lease/cobranca/{year}/{month}/{contract_id}'.format(**urldict)
    return url

  '''
  def __init__(self):
    # super().__init__()
    self.postconstructor()
  '''

  def postinit(self, billingitems=[], previous_bill = None):
    self.date_of_last_interest_applied = None # this is initialized when a first mora pay is done
    if self.duedate is None:
      # the default duedate, if caller passes None to it, is monthref's next month on day 10
      self.duedate = self.monthrefdate + relativedelta(months=+1)
      self.duedate = self.duedate.replace(day=10)
    # the value below should be set after constructor (__init())
    # self.datecalculator = DateBillCalculator()
    self.payments       = [] # payment_obj elements of class Payment
    self.latepaysprocessor = None # is the AmountIncreaseTrail instance that keeps the records of late pays
    # self.late_payments  = []   # derivable, it should be a dynamic property
    # self.total_paid     = 0   # derivable, it should be a dynamic property

    # Accounting-like accounts
    self.debt_account        = 0 # has accessors because base_for_i_n_cm_account
    self.previousmonthsdebts = 0
    self.amount_paid_ontime  = 0
    # dynamic self.base_for_i_n_cm_account = 0 # it depends on debt_account minus 'multa' (fine)
    # self.cred_account      = 0 # is dynamic
    self.payment_account       = 0
    # self.multa_account       = 0 depends on the first AmountIncreaseTrail object
    self.interest_n_cm_account = 0
    self.set_billingitems(billingitems) # generally, it may have: ALUG, COND, IPTU
    # self.inmonth_due_amount is set above # it's the amounts that arise in the contract's monthly bill, not to be confused with the previousdebts
    # self.previousmonthsdebts is also set above
    self.previous_bill = None
    if previous_bill is not None:
      self.previous_bill = previous_bill

    self.aits_as_json = None


  def postconstructor(self, monthrefdate, duedate=None, billingitems=[], previous_bill = None, monthseqnumber=1, contract_id=None):
    self.monthrefdate   = monthrefdate
    self.monthseqnumber = monthseqnumber # with this attribute, it's possible to have more than one bill in a month
    self.contract_id = contract_id
    self.duedate        = duedate
    self.date_of_last_interest_applied = None # this is initialized when a first mora pay is done
    if self.duedate is None:
      # the default duedate, if caller passes None to it, is monthref's next month on day 10
      self.duedate = self.monthrefdate + relativedelta(months=+1)
      self.duedate = self.duedate.replace(day=10)
    # the value below should be set after constructor (__init())
    # self.datecalculator = DateBillCalculator()
    self.payments       = [] # payment_obj elements of class Payment
    self.latepaysprocessor = None # is the AmountIncreaseTrail instance that keeps the records of late pays
    # self.late_payments  = []   # derivable, it should be a dynamic property
    # self.total_paid     = 0   # derivable, it should be a dynamic property

    # Accounting-like accounts
    self.debt_account        = 0 # has accessors because base_for_i_n_cm_account
    self.previousmonthsdebts = 0
    self.amount_paid_ontime  = 0
    # dynamic self.base_for_i_n_cm_account = 0 # it depends on debt_account minus 'multa' (fine)
    # self.cred_account      = 0 # is dynamic
    self.payment_account       = 0
    # self.multa_account       = 0 depends on the first AmountIncreaseTrail object
    self.interest_n_cm_account = 0
    self.set_billingitems(billingitems) # generally, it may have: ALUG, COND, IPTU
    # self.inmonth_due_amount is set above # it's the amounts that arise in the contract's monthly bill, not to be confused with the previousdebts
    # self.previousmonthsdebts is also set above
    self.previous_bill = None
    if previous_bill is not None:
      self.previous_bill = previous_bill

    self.aits_as_json = None

  @property
  def multa_account(self):
    '''
    NOTICE THE IMPORTANT CONVENTION:
      A fine, when applied, is only applied to the first trail.
      If it's not there, then there's no fine.
    :return:
    '''
    if self.latepaysprocessor is not None:
      if len(self.latepaysprocessor.increase_trails) > 0:
        firsttrail = self.latepaysprocessor.increase_trails[0]
        multavalue = 0
        if firsttrail.finevalue is not None:
          multavalue = firsttrail.finevalue
        return multavalue
    return 0

  @property
  def valor_sob_mora(self):
    return self.inmonthpluspreviousdebts - self.amount_paid_ontime

  @property
  def add_previousmonthsdebts_from_previousbill(self):
    if self.previous_bill is not None:
      self.previousmonthsdebts += self.previous_bill.debt_account
    return 0

  def set_billingitems(self, billingitems):
    if billingitems is None:
      return
    self.billingitems = billingitems
    self.inmonth_due_amount  = 0
    self.previousmonthsdebts = 0
    for billingitem in self.billingitems:
      if billingitem[REFTYPE_KEY] == CARR_REFTYPE: # CARR means carried-up and is the previous month's debt_account
        value = billingitem['value']
        self.previousmonthsdebts += value
        self.debt_account        += value
        continue
      value = billingitem['value']
      self.inmonth_due_amount += value
      self.debt_account       += value

  @property
  def inmonthpluspreviousdebts(self):
    '''
    Reader attribute as method
    inmonthpluspreviousdebts is inmonth_due_amount plus previous months' debts
    :return:
    '''
    self.inmonth_due_amount = 0; self.previousmonthsdebts = 0
    for bi in self.billingitems:
      cobrancatipo = bi.cobrancatipo
      if cobrancatipo.char4id != 'CARR':
        self.inmonth_due_amount += bi.value
      else:
        self.previousmonthsdebts += bi.value
    return self.inmonth_due_amount + self.previousmonthsdebts

  @property
  def total_bill_with_mora_if_any(self):
    '''
    Reader attribute as method
    total_bill_with_mora_if_any is inmonthpluspreviousdebts plus, if any, in-month fine, interest and corr.monet.
    :return:
    '''
    mora_increases = self.multa_account + self.interest_n_cm_account
    return self.inmonthpluspreviousdebts + mora_increases

  @property
  def cred_account(self):
    if self.debt_account < 0:
      return -self.debt_account
    return 0

  @property
  def fine_interest_n_cm(self):
    return self.multa_account + self.interest_n_cm_account

  @property
  def base_for_i_n_cm_account(self):
    '''
    base_for_i_n_cm_account is a DEPENDENT variable. It's either:
      base_for_i_n_cm_account = debt_account - multa_account
      or 0 if (debt_account - multa_account) is negative
    :return:
    '''
    basevalue = self.debt_account - self.multa_account
    if basevalue < 0:
      return 0
    return basevalue

  @property
  def inmonthpluspreviousdebts_minus_payments(self):
    return self.inmonthpluspreviousdebts - self.payment_account

  @property
  def payment_missing(self):
    if self.debt_account > 0:
      return self.debt_account
    return 0

  def set_payments(self, payments):
    if len(payments) == 0:
      self.payments = []
      return
    first_payment = payments[0]
    if type(first_payment) != Payment:
      error_msg = 'type(first_payment = [%s]) != Payment' %str(first_payment)
      raise TypeError(error_msg)

    if Payment.are_there_more_than_one_payment_in_a_day(payments):
      payments = Payment.consolidate_days_when_there_are_more_than_one_payment_in_a_day(payments)

    Payment.check_paydates_order_n_raise_exception_if_inconsistent(payments)

    self.payments = payments
    self.payment_account = 0

    for payment in self.payments:
      self.payment_account += payment.paid_amount

  def set_previousmonthsdebts(self, previousmonthsdebts):
    if previousmonthsdebts is None:
      return
    if previousmonthsdebts < 0:
      raise ValueError('previousmonthsdebts (=%s) < 0' %(previousmonthsdebts))
    self.previousmonthsdebts = previousmonthsdebts
    self.debt_account += self.previousmonthsdebts

  def reprocess_payment(self):
    self.payments = copy(self.original_payments)
    self.process_payment()

  def pay_those_on_date(self):

    while len(self.payments) > 0:
      currentpay = self.payments[0]
      if currentpay.paydate <= self.duedate:
        self.amount_paid_ontime += currentpay.paid_amount
        self.debt_account -= currentpay.paid_amount
        del self.payments[0]
      else:
        # ie, break out of while, otherwise this is an infinite loop
        break

  def process_payment(self):
    print (' ============>>>>>>>>>>>>>>> Getting inside process_payment()')

    self.pay_those_on_date()

    if len(self.payments) == 0:
      return

    self.CALLED_FROM_PROCESS_PAYMENT = True
    self.pay_late()

  def pay_late(self):
    '''
    ONLY process_payment() can call THIS METHOD !!!
    Otherwise inconsistencies may happen !
    :return:
    '''

    if not self.CALLED_FROM_PROCESS_PAYMENT:
      error_msg =  'CALLED_FROM_PROCESS_PAYMENT is False. It should not be in method pay_late().'
      raise SystemError(error_msg)
    self.CALLED_FROM_PROCESS_PAYMENT = False

    if self.latepaysprocessor is None:
      self.latepaysprocessor = PaymentTimeProcessor()

    local_inmonthdue = self.inmonth_due_amount - self.amount_paid_ontime

    if local_inmonthdue < 0:
      local_inmonthdue = 0

    local_previousdebts = self.debt_account - local_inmonthdue

    bill_remaining = {
      'inmonthdue'   : local_inmonthdue,
      'previousdebts': local_previousdebts,
      'monthrefdate' : self.monthrefdate,
      'duedate'      : self.duedate,
    }

    self.latepaysprocessor.set_bill_dict(bill_remaining)
    self.latepaysprocessor.set_payment_tuplelist_via_paymentinstances(self.payments)
    self.latepaysprocessor.process_payments()
    #ait = ptp.calculate_debt_ondate_n_return_ait(date(2017, 6, 15))

    # Empty list of payments because they were processed above
    self.payments = []
    self.debt_account = self.latepaysprocessor.debt_account

  def credit_debit_payment(self, paid_amount):
    '''
    Order is:
    1) older debts quit first
    2) non-ALUG quit first
    3) ALUG is the last one to purge
    :return:
    '''
    if paid_amount is None or paid_amount <= 0:
      return
    self.payment_account += paid_amount
    if self.debt_account > 0:
      diff = self.debt_account - paid_amount
      if diff < 0:
        self.debt_account = 0
        self.cred_account += diff
      else:
        self.debt_account -= paid_amount

    else:
      self.cred_account += paid_amount

  def generate_aits_as_json(self):
    '''

    :return:
    '''
    aits = self.latepaysprocessor.increase_trails
    list_of_jsons = []
    for ait in aits:
      jsonrepr = ait.to_json()
      list_of_jsons.append(jsonrepr)
    jsondump = json.dumps(list_of_jsons)
    self.amountincreasetrailsjson = jsondump
    return jsondump

  def recover_aits_from_json(self, jsonlistdump=None):
    list_of_jsons = json.loads(jsonlistdump)
    aits = []
    for jsonelem in list_of_jsons:
      ait = json.loads(jsonelem)
      aits.append(ait)
    return aits

  def decode_to_aits_from_json(self, jsonlistdump=None):
    if jsonlistdump is None:
      return
    aits = self.recover_aits_from_json(jsonlistdump)
    # bill_dict has:
    # monthrefdate, duedate, inmonth_due_amount, previousmonthsdebts, monthseqnumber & contract_id
    bill_dict = {}
    bill_dict['monthrefdate'] = self.monthrefdate
    bill_dict['duedate']      = self.duedate
    bill_dict['inmonth_due_amount']  = self.inmonth_due_amount
    bill_dict['previousmonthsdebts'] = self.previousmonthsdebts
    bill_dict['monthseqnumber'] = self.monthseqnumber
    bill_dict['contract_id'] = self.contract_id

    self.latepaysprocessor.reinit_with_stored_increase_trails(aits, bill_dict, new_payments=[])


  def add_contracts_billing_items_to_self(self, contract_obj):
    '''
    billing_items will be a list of dict for the time being
    :return:
    '''
    for contract_billing_item in contract_obj.billing_items:
      billingitem = copy(contract_billing_item)
      self.billingitems.append(billingitem)

  def is_late_on_duedate(self, paydate):
    if paydate > self.duedate:
      return True
    return False

  def apply_late_mora_if_tardy(self, paydate):
    if self.is_late_on_duedate(paydate):
      return self.apply_late_mora()

  def pretty_print_bill(self):
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

  def get_refstr(self):
    mmm_yyyy_str = format(self.monthyeardateref, 'M/Y')
    n_seq_from_dateref = 1
    if self.n_seq_from_dateref is not None:
      n_seq_from_dateref = self.n_seq_from_dateref
    refstr = mmm_yyyy_str + ' c' + str(n_seq_from_dateref)
    return refstr

  def str2(self):
    refstr         = self.get_refstr()
    duedatestr     = format(self.duedate, 'd/M')
    contrato_sigla = self.contract.imovel.apelido
    return '{0} p/pagt. {1} {2}'.format(refstr, duedatestr, contrato_sigla)

  class Meta:
    managed = False
    db_table = 'cobrancas'

  def __str__(self):
    outline = 'Cobr.{0}/{1} Contr.{2} total: {3:.2f}'.format(
      self.monthrefdate,
      self.monthseqnumber,
      self.contract.id,
      self.inmonthpluspreviousdebts
    )
    return outline


def create_adhoctest_bill():
  billingitems = datagen.create_billingitems_list_for_invoicebill()
  monthyearrefdate = date(2018, 1, 1)
  duedate          = date(2018, 2, 10)
  invoicebill = Cobranca(monthyearrefdate, duedate, billingitems)
  return invoicebill


def adhoctest():
  invoicebill = create_adhoctest_bill()
  payments = datagen.create_payments()
  invoicebill.set_payments(payments)
  invoicebill.process_payment()
  print (invoicebill)
  jsonlistdump = invoicebill.generate_aits_as_json()
  print ('jsonlistdump =>', jsonlistdump)
  aits = invoicebill.recover_aits_from_json(jsonlistdump)
  print ('aits =>', aits  )

if __name__ == '__main__':
  adhoctest()
