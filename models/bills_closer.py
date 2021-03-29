#!/usr/bin/env python3
import datetime
import func.date_functions as dtfunc
import func.lib_functions  as funclib
# import models.bills
import models.bills
import func.db.json_tofrom.jsonreaders as paymread
def generate_bill_as_text(bill):
  outstr    = ''
  totaldebt = 0
  totalcred = 0
  for i, bitem_namedtuple in enumerate(bill.closed_billingitem_namedtuplelist):
    seq = i + 1
    itdate = bitem_namedtuple.itdate
    ittype = bitem_namedtuple.ittype
    itvalue = bitem_namedtuple.itvalue
    itobs = str(bitem_namedtuple.itobs)
    itformula = str(bitem_namedtuple.itformula)

    line = '%(zseq)s %(itdate)s %(ittype)s  %(itvalue).2f  %(itobs)s    %(itformula)s \n' \
    % {
      'zseq': str(seq).zfill(2),
      'itdate': itdate,
      'ittype': ittype,
      'itvalue': itvalue,
      'itobs': str(itobs),
      'itformula': str(itformula),
    }
    if bitem_namedtuple.ittype == bill.KItemTypes.TK_PAYMENT:
      totalcred += bitem_namedtuple.itvalue
    elif bitem_namedtuple.ittype == bill.KItemTypes.TK_FBALANCE:
      pass
    else:
      totaldebt += bitem_namedtuple.itvalue
    outstr += line

  line = 'Total débito %.2f\n' % totaldebt
  outstr += line
  line = 'Inmonth_amount %.2f\n' % (bill.inmonth_amount)
  outstr += line
  line = 'Total crédito %.2f\n' % totalcred
  outstr += line
  line = 'Incidência %.2f\n' % bill.incidence_fine_value
  outstr += line
  line = 'Juros e Corr. Monet. %.2f\n' % bill.total_interest_n_monetcorr
  outstr += line
  line = 'Total mora %.2f\n' % bill.total_mora
  outstr += line
  if bill.fin_balance > 0:
    line = 'Saldo %.2f\n' % bill.fin_balance
    outstr += line
  return outstr


class CloseProcessor:

  def __init__(self, bill_id):

    self.bill_id = bill_id
    self.bill = models.bills.Bill.fetch_bill_by_id_from_json(self.bill_id)
    if self.bill.is_closed:
      error_msg = 'Error: bill (%s) is closed' %self.bill_id
      raise ValueError(error_msg)

    self.close_process()

  def close_process(self):
    payment_id = self.bill.get_months_payment_id()
    payobj = paymread.get_payment_by_id(payment_id)









class NextBill:

  def __init__(self, closed_bill):

    self.closed_bill = closed_bill
    self.nextrefmonthdate = self.closed_bill.nextrefmonthdate
    self.nextrefmonth_billing_items_namedtuplelist = []
    self.process()

  def process(self):

    # 1 fetch base billing items for contract
    self.base_billing_items_namedtuplelist = self.closed_bill.contract.get_base_billing_items_as_ntlist()

    # 2 extract debts or credits, if any, from closed bill
    self.previous_debts_creds_billing_items_namedtuplelist = self.closed_bill.extract_debts_or_creds_billing_items_as_ntlist()

    # 3 join base billing items with, if any, debts or credits
    newlist = []
    for e in self.base_billing_items_namedtuplelist:
      newlist.append(e)
    for e in self.previous_debts_creds_billing_items_namedtuplelist():
      newlist.append(e)

    self.nextrefmonth_billing_items_namedtuplelist = newlist


  def __init__(self, closed_bill):
    return generate_bill_as_text(self)









class BillMonthCloser(bills.Bill):

  #billitem_ntuple_constr = ctes.billitem_ntuple_constr # collections.namedtuple('BillItemNamedTuple', 'itdate, ittype, itvalue, itobs, itformula')

  payment_n_date_tuple_constr = funclib.payment_n_date_tuple_constr

  def __init__(self, billForClosing, paidamount_n_paydate_namedtuplelist):

    # base class is constructed with (contract, billingitem_namedtuplelist)
    super().__init__(billForClosing.contract, billForClosing.billingitem_namedtuplelist)
    self.paidamount_n_paydate_namedtuplelist = paidamount_n_paydate_namedtuplelist

    # ==================
    # To be calculated
    # Fields necessary for Closer
    self.balance = 0
    self._incidence_fine_value = None
    self._total_interest_n_monetcorr = None
    self.closed_billingitem_namedtuplelist = []
    # ==================
    self.STEP_1_HAS_BEEN_CALLED = False
    self.APPLY_ONCE_INCIDENCE_FINE_HAS_RUN = False
    self.STEP_2_HAS_BEEN_CALLED = False
    self.close_month()

# Properties in base-class
# @property  def inmonth_amount(self):
# @property  def ini_balance(self):
# @property  def ini_debt(self):
# @property  def ini_credit(self):
# @property  def duedate(self):
# @property  def refmonthdate(self):
# @property  def nextrefmonthdate(self):
# @property  def previousrefmonthdate(self):
# @property  def mora_params(self):
# @property  def incidence_fine_fraction(self):
# @property  def fix_monthly_interest_fraction(self):
# @property  def apply_monthly_monet_corr(self):

  def get_incidence_fine_value_from_ntlist(self):
    for billitems_namedtuple in self.closed_billingitem_namedtuplelist:
      if billitems_namedtuple.ittype == self.KItemTypes.TK_INCFINE:
         return billitems_namedtuple.itvalue
    return None

  @property
  def incidence_fine_value(self) -> object:
    if self._incidence_fine_value is None:
      v = self.get_incidence_fine_value_from_ntlist()
      if v is None:
        return None
      self._incidence_fine_value = v
      return self._incidence_fine_value
    return self._incidence_fine_value

  @incidence_fine_value.setter
  def incidence_fine_value(self, value):
    error_msg = 'Program Error: Forbidden to set incidence_fine_value directly in classes Bill or BillMonthCloser'
    raise Exception(error_msg)

  @property
  def total_interest_n_monetcorr(self):
    if not self.STEP_2_HAS_BEEN_CALLED:
      return None
    if self._total_interest_n_monetcorr is not None:
      return self._total_interest_n_monetcorr
    self._total_interest_n_monetcorr = 0
    for billitems_namedtuple in self.closed_billingitem_namedtuplelist:
      if billitems_namedtuple.ittype == self.KItemTypes.TK_INTMCORR:
        self._total_interest_n_monetcorr += billitems_namedtuple.itvalue
    return self._total_interest_n_monetcorr

  @property
  def total_mora(self):
    if self.total_interest_n_monetcorr is None or self.incidence_fine_value is None:
      return None
    return self.total_interest_n_monetcorr + self.incidence_fine_value

  def totalize(self):
    '''
      #@property
      def set_types_totalizable(self):
        self.set_types_totalizable = inspect.getmembers(Bill.KItemTypes, lambda a: not (inspect.isroutine(a)))
    '''
    total = 0
    for bitem_namedtuple in self.closed_billingitem_namedtuplelist:
      value = bitem_namedtuple.itvalue
      if bitem_namedtuple.ittype == self.KItemTypes.TK_PAYMENT:
        value = -value
      total += value

    return total

  @property
  def has_closing_generated_mora(self):
    if not self.STEP_2_HAS_BEEN_CALLED:
      return None
    if self.total_mora > 0:
      return True
    return False

  @property
  def value_subjected_to_incidence_fine(self):
    if self.balance >= 0 and self.balance < self.inmonth_amount:
      return self.balance
    elif self.balance >= self.inmonth_amount:
      return self.inmonth_amount
    else:
      return 0

  def not_used_for_now_add_payment_n_date_namedtuple(self, payment_n_date_namedtuple):
    '''
    For the time being there's no checking against duplicate equal payments
    '''
    paid_amount = payment_n_date_namedtuple.paid_amount
    paydate     = payment_n_date_namedtuple.paydate
    if paid_amount not in [int, float]:
      error_msg = 'Error: paid_amount (%s) not in [int, float]' %str(paid_amount)
      raise Exception(error_msg)
    if paydate not in [datetime.date, datetime.datetime]:
      error_msg = 'Error: paydate (%s) not in [int, float]' %str(paydate)
      raise Exception(error_msg)
    if not dtfunc.are_same_year_n_same_month(self.refmonthdate, paydate):
      error_msg = '_refmonthdate(%s) and paydate(%s) are not in the same month and year' %(str(self.refmonthdate), str(paydate))
      raise TypeError(error_msg)

    self.payment_n_date_namedtuplelist.append(payment_n_date_namedtuple)

  def is_payment_complete_on_refmonth(self):
    if not self.STEP_2_HAS_BEEN_CALLED:
      return None
    if self.balance <= 0:
      return True
    return False

  def revert_calculations(self):
    self.balance = self.ini_debt + self.inmonth_amount
    self.extended_billingitem_namedtuplelist  = []
    self.closed_billingitem_namedtuplelist = []
    self._incidence_fine_value = None
    self.STEP_1_HAS_BEEN_CALLED = False
    self.STEP_2_HAS_BEEN_CALLED = False
    self.APPLY_ONCE_INCIDENCE_FINE_HAS_RUN = False

  def process_payment_on_time(self, paid_amount, paydate):
    '''
    This method pays in the days of month up to duedate.

    :param paid_amount:
    :param paydate:
    :param n_of_previous_day:
    :return:
    '''
    increase_parcel = 0
    if self.inmonth_amount < self.balance:
      compoundfraction = \
        (self.mora_params.fix_monthly_interest + self.mora_params.monet_corr_fraction) * \
        dtfunc.get_remaining_daysfraction(paydate)
      correctable_amount_before_duedate = self.balance - self.inmonth_amount
      arithemic_transcription = None
      if paid_amount > correctable_amount_before_duedate:
        increase_parcel = correctable_amount_before_duedate * compoundfraction
        arithemic_transcription = '%.2f * %.2f' % (correctable_amount_before_duedate, compoundfraction)
      else:
        increase_parcel = paid_amount * compoundfraction
        arithemic_transcription = '%.2f * %.2f' %(paid_amount, compoundfraction)

    # Pay attention to the order in which actions happen (first, increase parcel, second, diminish)
    if increase_parcel > 0:
      self.balance += increase_parcel
      obs_balance = str(self.balance)
      bitem_type = self.KItemTypes.TK_INTMCORR
      bookkeeping_namedtuple = self.billitem_ntuple_constr(itdate=paydate, ittype=bitem_type, itvalue=increase_parcel, itobs=obs_balance, itformula=arithemic_transcription)
      self.extended_billingitem_namedtuplelist.append(bookkeeping_namedtuple)
    self.balance -=  paid_amount
    bitem_type = self.KItemTypes.TK_PAYMENT
    obs_balance = str(self.balance)
    bookkeeping_namedtuple = self.billitem_ntuple_constr(itdate=paydate, ittype=bitem_type, itvalue=paid_amount,
                                                         itobs=obs_balance, itformula=None)
    self.extended_billingitem_namedtuplelist.append(bookkeeping_namedtuple)

  def process_payment_late(self, paid_amount, paydate):
    '''
    This method pays in the days of month after duedate.

    :param paid_amount:
    :param paydate:
    :param n_of_previous_day:
    :return:
    '''
    correcting_value = 0 # this is important in case payer has credit, ie, balance < 0
    if self.balance > 0:
      if paid_amount <= self.balance:
        correcting_value = paid_amount
      else:
        correcting_value = self.balance
    increase_parcel = 0
    arithemic_transcription = ''
    if correcting_value > 0:
      compoundfraction = \
        (self.mora_params.fix_monthly_interest + self.mora_params.monet_corr_fraction) * \
        dtfunc.get_daysfraction_with_date(paydate)
      increase_parcel = correcting_value * compoundfraction
      arithemic_transcription = '%f * %f' %(correcting_value, compoundfraction)
    # Pay attention to the order in which actions happen (first, increase parcel; second, abate pay)
    if increase_parcel > 0:
      self.balance += increase_parcel
      bitem_type = self.KItemTypes.TK_INTMCORR
      obs_balance = str(self.balance)
      bookkeeping_namedtuple = self.billitem_ntuple_constr(itdate=paydate, ittype=bitem_type, itvalue=increase_parcel, itobs=obs_balance, itformula=arithemic_transcription)
      self.extended_billingitem_namedtuplelist.append(bookkeeping_namedtuple)
    self.balance -= paid_amount
    obs_balance = str(self.balance)
    bitem_type = self.KItemTypes.TK_PAYMENT
    bookkeeping_namedtuple = self.billitem_ntuple_constr(itdate=paydate, ittype=bitem_type, itvalue=paid_amount,
                                                         itobs=obs_balance, itformula=None)
    self.extended_billingitem_namedtuplelist.append(bookkeeping_namedtuple)

  def step_1_loop_over_payments(self):
    '''
    step 1
    Obs: payments should be ORDERED by date
         (otherwise this code will not work with many payments unordered by dates)
    '''
    self.revert_calculations()

    # Loop through payments ordered by their dates
    for pay_n_date_namedtuple in self.paidamount_n_paydate_namedtuplelist:
      if not pay_n_date_namedtuple.ittype == self.KItemTypes.TK_PAYMENT:
        continue
      paid_amount = pay_n_date_namedtuple.itvalue
      paydate = pay_n_date_namedtuple.itdate
      if paydate <= self.duedate:
        self.process_payment_on_time(paid_amount, paydate)
        continue
      self.apply_once_incidence_fine_if_needed()
      self.process_payment_late(paid_amount, paydate)

    self.STEP_1_HAS_BEEN_CALLED = True

  def apply_once_incidence_fine_if_needed(self):
    '''
    The logical condition that incidence happened is the verify truthiness of:
      self.incidence_fine_value > 0

    :return:
    '''
    if self.APPLY_ONCE_INCIDENCE_FINE_HAS_RUN:
      return False
    added_incidence_fine = False
    self._incidence_fine_value = self.value_subjected_to_incidence_fine * self.mora_params.incidence_fine_fraction
    if self._incidence_fine_value > 0:
      formula = '%f * %f' %(self.value_subjected_to_incidence_fine, self.mora_params.incidence_fine_fraction)
      self.balance += self.incidence_fine_value
      afterduedate = self.duedate + datetime.timedelta(days=1) # eg dueday is 10, refmonth=2019-10, then afterdate will be 2019-10-11
      billingitem_namedtuple = self.billitem_ntuple_constr(
        itdate=afterduedate,
        ittype=self.KItemTypes.TK_INCFINE,
        itvalue=self._incidence_fine_value,
        itobs=None,
        itformula=formula,
      )
      self.extended_billingitem_namedtuplelist.append(billingitem_namedtuple)

    self.APPLY_ONCE_INCIDENCE_FINE_HAS_RUN = True

  def step_2_close_month(self):
    '''
    step 2
    Step 2 is called after step 1 just to close month to its last day

    The import thing here is to monetary correct the balance on the last day of month
    '''
    if not self.STEP_1_HAS_BEEN_CALLED:
      error_msg = 'step 2 was called with step 1 previously run'
      raise RuntimeError(error_msg)

    # if there's no payment after duedate, next method needs to be called from here
    self.apply_once_incidence_fine_if_needed()

    last_date_in_month = dtfunc.last_date_in_month(self.refmonthdate)
    last_increase_parcel = 0
    if self.balance > 0:
      # closing month entices a daysfractions equal to 1 (ie, it covers the whole month, it's month's closing)
      compoundfraction = (self.mora_params.fix_monthly_interest + self.mora_params.monet_corr_fraction)
      # (no need after having refactored) \ * self.getdaysfraction(last_date_in_month)
      last_increase_parcel = self.balance * compoundfraction
      formula = '%.2f * %.2f' %(self.balance, compoundfraction)
      self.balance += last_increase_parcel
      if last_increase_parcel > 0:
        billingitem_namedtuple = self.billitem_ntuple_constr(
          itdate=last_date_in_month,
          ittype=self.KItemTypes.TK_INTMCORR,
          itvalue=last_increase_parcel,
          itobs=str(self.balance),
          itformula=formula,
        )
        self.extended_billingitem_namedtuplelist.append(billingitem_namedtuple)

    billingitem_namedtuple = self.billitem_ntuple_constr(
      itdate=last_date_in_month,
      ittype=self.KItemTypes.TK_FBALANCE,
      itvalue=self.balance,
      itobs="Saldo Final",
      itformula=None,
    )
    self.extended_billingitem_namedtuplelist.append(billingitem_namedtuple)

    self.STEP_2_HAS_BEEN_CALLED = True

  def close_month(self):
    self.step_1_loop_over_payments()
    self.step_2_close_month()
    self.join_billing_items_with_payment_result()

    #self.check_n_set_paidamount_n_paydate_namedtuplelist()

  def join_billing_items_with_payment_result(self):
    newlist = []
    for e in self.billingitem_namedtuplelist:
      newlist.append(e)
    for e in self.extended_billingitem_namedtuplelist:
      newlist.append(e)
    self.closed_billingitem_namedtuplelist = newlist

  def check_n_set_paidamount_n_paydate_namedtuplelist(self):
    for paidamount_n_paydate_namedtuple in self.paidamount_n_paydate_namedtuplelist:
      if type(paidamount_n_paydate_namedtuple) != BillMonthCloser.billitem_ntuple_constr:
        error_msg = 'self.paidamount_n_paydate_namedtuplelist != Bill.billitem_ntuple_constr in class BillForClosing'
        raise Exception(error_msg)
    if len(self.paidamount_n_paydate_namedtuplelist) < 2:
      return
    first_paidamount_n_paydate_namedtuple = self.paidamount_n_paydate_namedtuplelist[0]
    lastpaydate = first_paidamount_n_paydate_namedtuple.itdate
    bool_sort_paydates = False
    for paidamount_n_paydate_namedtuple in self.check_n_set_paidamount_n_paydate_namedtuplelist[1:]:
      if paidamount_n_paydate_namedtuple.itdate < lastpaydate:
        bool_sort_paydates = True
        break
    if bool_sort_paydates:
      self.paidamount_n_paydate_namedtuplelist = sorted(self.paidamount_n_paydate_namedtuplelist, key=lambda x : x[1])

  def print_closed_months_bill(self):
    pass

  def generate_bill_closed_as_text(self):
    '''

    billitem_ntuple_constr = collections.namedtuple('BillItemNamedTuple', 'itdate, ittype, itvalue, itobs, itformula')

    :return:
    '''
    outstr = super().generate_bill_as_text()
    outstr += generate_bill_as_text(self)
    return outstr

  def __str__(self):
    outstr = \
'''refmonthdate = %(refmonthdate)s
inmonth_amount = %(inmonth_amount)f
value_subjected_to_incidence_fine = %(value_subjected_to_incidence_fine)f
carried_debt         = %(carried_debt)f
duedate        = %(duedate)s
incidence_fine_fraction = %(incidence_fine_fraction)f
fix_monthly_interest_fraction = %(fix_monthly_interest_fraction)f
apply_monthly_monet_corr  = %(apply_monthly_monet_corr)f
incidence_fine_value = %(incidence_fine_value)f
total_interest_n_monetcorr   = %(total_interest_n_monetcorr)f
total_mora       = %(total_mora)f
balance          = %(balance)f
''' %{
  'refmonthdate' : self.refmonthdate,
  'inmonth_amount' : self.inmonth_amount,
  'value_subjected_to_incidence_fine' : self.value_subjected_to_incidence_fine,
  'carried_debt'           : self.ini_debt,
  'carried_debt'           : self.ini_cred,
  'duedate'                : self.duedate,
  'incidence_fine_fraction': self.incidence_fine_fraction,
  'fix_monthly_interest_fraction'   : self.fix_monthly_interest,
  'apply_monthly_monet_corr'    : self.monet_corr_fraction,
  'incidence_fine_value'   : self.incidence_fine_value,
  'total_interest_n_monetcorr': self.total_interest_n_monetcorr,
  'total_mora': self.total_mora,
  'balance'   : self.balance
}
    for i, billingitem_namedtuple in enumerate(self.closed_billingitem_namedtuplelist):
      seq = i + 1
      itdate = billingitem_namedtuple.itdate
      ittype = billingitem_namedtuple.ittype
      itvalue = billingitem_namedtuple.itvalue
      itobs = str(billingitem_namedtuple.itobs)
      itformula = str(billingitem_namedtuple.itformula)
      line = '%(zseq)s %(itdate)s %(ittype)s  %(itvalue).2f  %(itobs)s    %(itformula)s \n' \
      %{
          'zseq'     : str(seq).zfill(2),
          'itdate'   : itdate,
          'ittype'   : ittype,
          'itvalue'  : itvalue,
          'itobs'    : str(itobs),
          'itformula': str(itformula),
        }
      outstr += line

    outstr += '\n -------------------------- '

    return outstr

  def extract_debts_or_creds_billing_items_as_ntlist(self):
    debts_or_creds_billing_items_as_ntlist = []
    for closed_billingitem_namedtuple in self.closed_billingitem_namedtuplelist:
      if closed_billingitem_namedtuple.ittype in [self.KItemTypes.TK_INCFINE, self.KItemTypes.TK_INTMCORR]:
        debts_or_creds_billing_items_as_ntlist.append(closed_billingitem_namedtuple)
    return closed_billingitem_namedtuple

def process():
  msg = '''
  This module has class BillMonthCloser. Bill is its base class from which it inherits and is in another module).
  There are unit tests covering them and a simple printable scripts named like cases_bills_month_closer.py
  '''
  print(msg)

if __name__ == '__main__':
  process()
