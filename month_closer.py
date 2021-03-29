#!/usr/bin/env python3
import datetime
# from functions_lib import print_bookkeeping

MONTHDAYS = [31,28,31,30,31,30,31,31,30,31,30,31]
def get_n_of_days_in_month(p_date):
  return MONTHDAYS[p_date.month-1]

# TOKENS for the bookkeeping tuple list
TOKEN_PLUS_INTEREST_N_MC  = '+INTEREST_N_MC'
TOKEN_PLUS_INCIDENCE_FINE = '+INCIDENCE_FINE'
TOKEN_MINUS_PAYMENT       = '-PAYMENT'

class MoraParams:

  def __init__(self,
      incidence_fine_fraction,
      fix_monthly_interest,
      monet_corr_fraction
               ):
    self.incidence_fine_fraction = incidence_fine_fraction
    self.fix_monthly_interest    = fix_monthly_interest
    self.monet_corr_fraction     = monet_corr_fraction


class Closer:

  def __init__(self, nextrefmonth, inmonth_amount, carried_debt, duedate,
               payment_n_dates_tuplelist, mora_params
              ):
    self.nextrefmonth   = nextrefmonth
    self.inmonth_amount = inmonth_amount
    self.value_subjected_to_incidence_fine = self.inmonth_amount
    self.carried_debt   = carried_debt
    self.duedate        = duedate
    self.set_n_check_payment_n_dates_tuplelist(payment_n_dates_tuplelist)
    self.mora_params = mora_params
    # To be calculated
    # ==================
    self.balance              = 0
    self.incidence_fine_value = 0
    # self.increase_parcels_n_dates_tuplelist = []
    self.bookkeeping_date_op_n_balance_tuplelist = []
    # ==================
    self.STEP_1_HAS_BEEN_CALLED = False
    self.STEP_2_HAS_BEEN_CALLED = False
    self.APPLY_ONCE_INCIDENCE_FINE_HAS_RUN = False
    self.revert_calculations()

  def set_n_check_payment_n_dates_tuplelist(self, payment_n_dates_tuplelist):
    '''
    Check also whether elements are ordered by date
    :param payment_n_dates_tuplelist:
    :return:
    '''
    self.payment_n_dates_tuplelist = []
    for pay_n_date in payment_n_dates_tuplelist:
      pay, paydate = pay_n_date
      pay = float(pay)
      if type(pay) != float or type(paydate) != datetime.date:
        error_msg = 'type(pay=%s) != float or type(date=%s) != datetime.date' %(str(pay), str(paydate))
        raise TypeError(error_msg)
      self.check_consistency_of_dates(paydate)
      self.payment_n_dates_tuplelist.append((pay, paydate))

  def check_consistency_of_dates(self, paydate):
    '''
    Not used for the time being (should rewrite it due to the many possible payments refactoring)
    :return:
    '''
    monthdate = self.nextrefmonth - datetime.timedelta(days=15)
    if paydate is not None:
      if monthdate.month != paydate.month and monthdate.year != paydate.year:
        error_msg = 'monthdate.month (%s) != self.paydate.month (%s) and monthdate.year != self.paydate.year' %(monthdate, paydate)
        raise ValueError(error_msg)

  def get_remaining_daysfraction(self, p_date):
    n_of_day_in_month = p_date.day
    days_in_month = get_n_of_days_in_month(p_date)
    n_of_days = days_in_month - n_of_day_in_month
    remaining_daysfraction = n_of_days / days_in_month
    return remaining_daysfraction

  @property
  def total_interest_n_monetcorr(self):
    if not self.STEP_2_HAS_BEEN_CALLED:
      return None
    total_interest_n_monetcorr = 0
    for date_token_increase_balance in self.bookkeeping_date_op_n_balance_tuplelist:
      _, token, increase, _ = date_token_increase_balance
      if token.startswith('+INTEREST'):
        total_interest_n_monetcorr += increase
    return total_interest_n_monetcorr

  @property
  def total_mora(self):
    if self.total_interest_n_monetcorr is None:
      return None
    return self.total_interest_n_monetcorr + self.incidence_fine_value

  @property
  def has_closing_generated_mora(self):
    if self.paydate is None or self.paydate > self.duedate or self.value_subjected_to_incidence_fine > 0:
      return True
    return False

  def is_payment_late(self, p_date):
    if p_date is None:
      # no payment happened
      return None
    if p_date > self.duedate:
      return True
    return False

  def revert_calculations(self):
    self.balance = 0
    self.incidence_fine_value = 0
    self.value_subjected_to_incidence_fine = self.inmonth_amount
    self.bookkeeping_date_op_n_balance_tuplelist = []
    self.STEP_1_HAS_BEEN_CALLED = False
    self.STEP_2_HAS_BEEN_CALLED = False
    self.APPLY_ONCE_INCIDENCE_FINE_HAS_RUN = False

  def getdaysfraction(self, p_date, previous_day=None):
    '''
    For the time being, there is only one hypothesis when previous_day is not None.
    Explanation.
    When incidence fine happens (when value_subjected_to_incidence_fine > 0),
      previous_day is passed as 11 (or the day after duedate, if duedate is 10, previous_day is 11)

    :param p_date:
    :param previous_day:
    :return:
    '''
    if type(p_date) != datetime.date:
      error_msg = 'type(p_date = %s) != datetime.date' %str(p_date)
      raise TypeError(error_msg)
    days_in_month = get_n_of_days_in_month(p_date)
    if previous_day is None or previous_day < 1:
      return p_date.day / days_in_month
    elif previous_day > p_date.day: # this never happens after 'or': or previous_day > days_in_month:
      return 0
    return (p_date.day - previous_day) / days_in_month

  def process_payment_on_time(self, paid_amount, paydate):
    '''
    This method pays in the days of month up to duedate.

    :param paid_amount:
    :param paydate:
    :param n_of_previous_day:
    :return:
    '''
    compoundfraction = \
      (self.mora_params.fix_monthly_interest + self.mora_params.monet_corr_fraction) * \
       self.getdaysfraction(paydate)
    n_of_previous_day = paydate.day
    increase_parcel = 0
    if self.local_carried_debt > 0:
      if paid_amount <= self.local_carried_debt:
        increase_parcel = paid_amount * compoundfraction
      else:
        increase_parcel = self.local_carried_debt * compoundfraction
    # Pay attention to the order in which actions happen (first, increase parcel, second, diminish)
    self.balance += increase_parcel
    if increase_parcel > 0:
      bookkeeping_tuple = (paydate, TOKEN_PLUS_INTEREST_N_MC, increase_parcel, self.balance)
      self.bookkeeping_date_op_n_balance_tuplelist.append(bookkeeping_tuple)
    self.balance -=  paid_amount
    self.local_carried_debt -= paid_amount
    bookkeeping_tuple = (paydate, TOKEN_MINUS_PAYMENT, paid_amount, self.balance)
    self.bookkeeping_date_op_n_balance_tuplelist.append(bookkeeping_tuple)
    if self.balance >= 0 and self.balance < self.inmonth_amount:
      self.value_subjected_to_incidence_fine = self.balance
    elif self.balance >= self.inmonth_amount:
      self.value_subjected_to_incidence_fine = self.inmonth_amount
    else:
      self.value_subjected_to_incidence_fine = 0


  def process_payment_late(self, paid_amount, paydate):
    '''
    This method pays in the days of month after duedate.

    :param paid_amount:
    :param paydate:
    :param n_of_previous_day:
    :return:
    '''
    previous_day = None
    # Notice that when incidence_fine happens, the correction positions itself on duedate+1day
    if self.incidence_fine_value > 0:
      previous_date = self.duedate + datetime.timedelta(days=1)
      previous_day = previous_date.day
    compoundfraction = \
      (self.mora_params.fix_monthly_interest + self.mora_params.monet_corr_fraction) * \
       self.getdaysfraction(paydate, previous_day)
    increase_parcel = paid_amount * compoundfraction
    # Pay attention to the order in which actions happen (first, increase parcel, second, diminish)
    self.balance += increase_parcel
    if increase_parcel > 0:
      bookkeeping_tuple = (paydate, TOKEN_PLUS_INTEREST_N_MC, increase_parcel, self.balance)
      self.bookkeeping_date_op_n_balance_tuplelist.append(bookkeeping_tuple)
    self.balance -= paid_amount
    bookkeeping_tuple = (paydate, '-PAYMENT', paid_amount, self.balance)
    self.bookkeeping_date_op_n_balance_tuplelist.append(bookkeeping_tuple)

  def step_1_loop_over_payments(self):
    '''
    step 1
    Obs: payments should be ORDERED by date
         (otherwise this code will not work with many payments unordered by dates)
    '''
    self.revert_calculations()
    self.balance = self.carried_debt + self.inmonth_amount
    self.local_carried_debt = self.carried_debt
    # Loop through payments ordered by their dates
    for pay_n_date_tuple in self.payment_n_dates_tuplelist:
      paid_amount, paydate = pay_n_date_tuple
      if paydate <= self.duedate:
        self.process_payment_on_time(paid_amount, paydate)
        continue
      # Below here paydate is greather than duedate (see above the need of dates in ascending order):
      # Because of that, incidence fine should be the first action here
      # Loop is ongoing
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
    self.incidence_fine_value = self.value_subjected_to_incidence_fine * self.mora_params.incidence_fine_fraction
    if self.incidence_fine_value > 0:
      self.balance += self.incidence_fine_value
      afterduedate = self.duedate + datetime.timedelta(days=1)
      bookkeeping_tuple = (afterduedate, TOKEN_PLUS_INCIDENCE_FINE, self.incidence_fine_value, self.balance)
      self.bookkeeping_date_op_n_balance_tuplelist.append(bookkeeping_tuple)
      compoundfraction = (self.mora_params.fix_monthly_interest + self.mora_params.monet_corr_fraction) * \
                          self.getdaysfraction(afterduedate)
      increase = self.balance * compoundfraction
      self.balance += increase
      bookkeeping_tuple = (afterduedate, TOKEN_PLUS_INTEREST_N_MC, increase, self.balance)
      self.bookkeeping_date_op_n_balance_tuplelist.append(bookkeeping_tuple)

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

    if self.balance > 0:
      last_date_in_month = self.nextrefmonth - datetime.timedelta(days=1)
      previous_day = None
      if self.incidence_fine_value > 0:
        previous_date = self.duedate + datetime.timedelta(days=1)
        previous_day  = previous_date.day
      compoundfraction = \
        (self.mora_params.fix_monthly_interest + self.mora_params.monet_corr_fraction) * \
         self.getdaysfraction(last_date_in_month, previous_day)
      last_increase_parcel = self.balance * compoundfraction
      self.balance += last_increase_parcel
      if last_increase_parcel > 0:
        bookkeeping_tuple = (last_date_in_month, TOKEN_PLUS_INTEREST_N_MC, last_increase_parcel, self.balance)
        self.bookkeeping_date_op_n_balance_tuplelist.append(bookkeeping_tuple)

    self.STEP_2_HAS_BEEN_CALLED = True

  def close_month(self):
    self.step_1_loop_over_payments()
    # if there's no payment after duedate, next method needs to be called from here
    self.apply_once_incidence_fine_if_needed()
    self.step_2_close_month()


  def __str__(self):
    outstr = \
'''nextrefmonth = %(nextrefmonth)s
inmonth_amount = %(inmonth_amount)f
value_subjected_to_incidence_fine = %(value_subjected_to_incidence_fine)f
carried_debt         = %(carried_debt)f
duedate        = %(duedate)s
incidence_fine_fraction = %(incidence_fine_fraction)f
fix_monthly_interest = %(fix_monthly_interest)f
monet_corr_fraction  = %(monet_corr_fraction)f
incidence_fine_value = %(incidence_fine_value)f
total_interest_n_monetcorr   = %(total_interest_n_monetcorr)f
total_mora       = %(total_mora)f
balance          = %(balance)f
''' %{
  'nextrefmonth' : self.nextrefmonth,
  'inmonth_amount' : self.inmonth_amount,
  'value_subjected_to_incidence_fine' : self.value_subjected_to_incidence_fine,
  'carried_debt'           : self.carried_debt,
  'duedate'                : self.duedate,
  'incidence_fine_fraction': self.mora_params.incidence_fine_fraction,
  'fix_monthly_interest'   : self.mora_params.fix_monthly_interest,
  'monet_corr_fraction'    : self.mora_params.monet_corr_fraction,
  'incidence_fine_value'   : self.incidence_fine_value,
  'total_interest_n_monetcorr': self.total_interest_n_monetcorr,
  'total_mora': self.total_mora,
  'balance'   : self.balance
}
    for pay_n_date in self.payment_n_dates_tuplelist:
      paid_amount, paydate = pay_n_date
      outstr += '\n in %s paid %f' %(paydate, paid_amount)

    outstr += '\n -------------------------- '

    for date_token_increase_balance in self.bookkeeping_date_op_n_balance_tuplelist:
      outstr += '\n [%s]' %(str(date_token_increase_balance))

    return outstr

def process():
  case_3()

if __name__ == '__main__':
  process()
