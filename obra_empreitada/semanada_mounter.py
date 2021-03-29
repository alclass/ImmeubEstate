#!/usr/bin/env python3
import math
import datetime


contractee1 = {'name': 'Almir Russo', 'prorata': 0.5}
contractee2 = {'name': 'Luiz Carlos', 'prorata': 0.5}


class Data:
  
  contractees = [contractee1, contractee2]

  def __init__(self, total=24000, semanada=1200, complete_semanada=2000):
    self.total = total
    self.complete_semanada = complete_semanada
    self.first_friday_date = datetime.date(year=2021, month=2, day=19)
    self.semanada = semanada

  def payment_per_week(self):
    total_contractees = 0
    for contractee in self.contractees:
      parcel_contractee = contractee['prorata'] * self.semanada
      contractee['week_pay'] = parcel_contractee
      total_contractees += parcel_contractee
    return total_contractees

  def get_n_of_weeks(self):
    return math.ceil(self.total / self.semanada)

  def consume_contract_thru_weeks(self):
    rolling_friday_date = self.first_friday_date
    saldo = 24000
    self.get_n_of_weeks()
    payment_per_week = self.payment_per_week()
    n_week = self.get_n_of_weeks()
    acc_receivable = 0
    for week_number in range(1, n_week+1):
      rolling_friday_date = rolling_friday_date + datetime.timedelta(days=7)
      print(':: Week number', week_number, 'Old Balance', saldo, rolling_friday_date)
      acc_receivable += self.complete_semanada - self.semanada
      saldo -= payment_per_week
      acc_receivable = acc_receivable if acc_receivable < saldo else saldo
      print('=> Contractees')
      for contractee in self.contractees:
        print('\t\t => ', contractee['name'], contractee['week_pay'])
      print('\t week pay', self.semanada)
      print('\t acc_receivable', acc_receivable)
      print('\t\t New Balance', saldo)
      print('='*30)

  def saldo_before_week_number(self, n_week):
    if n_week < 1:
      return self.total
    saldo_before = self.total - self.semanada * (n_week - 1)
    return saldo_before

  def calculate_pay_n_saldo_in_week(self, n_week):
    if n_week < 1:
      print('Before first pay, total = ', self.total)
      return
    saldo_before = self.saldo_before_week_number(n_week)
    saldo_after = saldo_before - self.semanada
    print('Payment in week', n_week)
    print('saldo_before_pay = ', saldo_before)
    print('saldo_after_pay = ', saldo_after)


if __name__ == '__main__':
  d = Data()
  d.calculate_pay_n_saldo_in_week(2)
  d.calculate_pay_n_saldo_in_week(4)
  d.calculate_pay_n_saldo_in_week(20)
  d.consume_contract_thru_weeks()
  d.calculate_pay_n_saldo_in_week(4)
