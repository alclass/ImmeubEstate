import datetime

def calculate_daysfraction(ndays, refdate=None):
  if refdate is None:
    refdate = datetime.date.today()
  n_days_in_month = refdate
  if ndays >= n_days_in_month:
    return 1
  return ndays/n_days_in_month

def increase_fix_interest_n_variable_correction_within_daysfraction(self, amount, fix_interest, variable_correction, ndays, refdate):
  daysfraction = calculate_daysfraction(ndays, refdate)
  return amount * (1 + (fix_interest + variable_correction) * daysfraction)

class BillGenerator:

  def __init__(self, normal_monthly_bill_items_dict, refdate, ndays, carried_debt, fix_interest):
    self.refdate = refdate
    self.ndays   = ndays
    self.carried_debt = carried_debt
    self.fix_interest = fix_interest
    self.normal_monthly_bill_items_dict = normal_monthly_bill_items_dict

  @property
  def normal_monthly_bill(self):
    monthly_bill = 0
    for k in self.normal_monthly_bill_items_dict:
      monthly_bill += self.normal_monthly_bill_items_dict[k]
    return monthly_bill

  def calculated_carried_debt_if_any(self):
    if self.carried_debt <= 0:
      self.carried_debt_corrected = 0
      return
    self.carried_debt_corrected = increase_fix_interest_n_variable_correction_within_daysfraction(carried_debt, fix_interest, ndays, refdate)
    return amount_in_duemonth

    amount_in_duemonth = carried_debt_corrected + normal_monthly_bill


  def calculate_bill_late_in_duemonth(self):

  def calculate_monthly_bill(self):
      self.calculated_carried_debt_if_any()
      if self.carried_debt_corrected > 0:
        self.normal_monthly_bill_items_dict['carried_debt_corrected'] = self.carried_debt_corrected
        self.current_monthly_bill = self.carried_debt_corrected + self.carried_debt_corrected
      if self.today <= refdate:
        self.current_monthly_bill = self.current_monthly_bill + self.normal_monthly_bill
        self.normal_monthly_bill_items_dict['current_monthly_bill'] = self.carried_debt_corrected = self.current_monthly_bill
      else:
        # incidence fine
        self.incidence_fine_amount = self.normal_monthly_bill * (1 + self.params.INCIDENCE_FINE)
        fined_monthly_bill = self.normal_monthly_bill + self.incidence_fine_amount
        fined_n_corrected_monthly_bill = increase_fix_interest_n_variable_correction_within_daysfraction(fined_monthly_bill, fix_interest, ndays, refdate)
        self.current_monthly_bill = fined_n_corrected_monthly_bill + self.carried_debt_corrected
        normal_monthly_bill_corrected = increase_fix_interest_n_variable_correction_within_daysfraction(self.normal_monthly_bill, fix_interest, ndays, refdate)

        if self.carried_debt_corrected > 0:
          self.normal_monthly_bill_items_dict['carried_debt_corrected'] = self.carried_debt_corrected
          self.current_monthly_bill = self.self.carried_debt_corrected + self.carried_debt_corrected
        self.normal_monthly_bill_items_dict['current_monthly_bill'] = self.carried_debt_corrected = self.current_monthly_bill
