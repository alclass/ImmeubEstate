
#!/usr/bin/env python3

class RenteeDefaut:
  INCIDENCE_FINE = 0.1
  FIX_MONTHLY_INTEREST = 0.01
  DUEDAY_IN_MONTH = 10
  DEFAULT_COMPONENTS_IN_PAY = ['RENTVALUE', 'CONDTARRIF', 'PROPERTYTAX']

class Rentee:

  def __init__(self):
    self.contract_params_key = None
    self.refmonth = None
    self.paydate = None
    self.previous_refmonth_was_closed = None
    self.valor_debito_fechado = None
    self.apply_property_tax = True
    # for testing
    self.outside_calculated_due = None

  def __init2__(self, normal_monthly_bill_items_dict, refdate, ndays, carried_debt, fix_interest):
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

  def generate_bill(self):
    if not self.previous_refmonth_was_closed:
      raise Exception('Previous refmonth was not closed. Program cannot continue.')
    bill_dict = {}



class Closer:

  def calculate_bill_late_in_duemonth(self):
    if self.carried_debt <= 0:
      self.carried_debt_corrected = 0
      return
    self.carried_debt_corrected = increase_fix_interest_n_variable_correction_within_daysfraction(carried_debt, fix_interest, ndays, refdate)
    return amount_in_duemonth

    amount_in_duemonth = carried_debt_corrected + normal_monthly_bill

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
