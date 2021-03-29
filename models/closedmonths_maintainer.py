#!/usr/bin/env python3
import datetime
import date_functions as dtfunc
# from functions_lib import print_bookkeeping

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


class ClosedMonthsMaintainer:

  def __init__(self, closed_months_dict):
    self.closed_months_dict = closed_months_dict

  def delete_month(self, month_n):
    if month_n in self.closed_months_dict:
      del self.closed_months_dict[month_n]


def process():
  print('This module is to be used imported. Main element here is class Closer().')

if __name__ == '__main__':
  process()
