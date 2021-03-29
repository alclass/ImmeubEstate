#!/usr/bin/env python3
from django.db import models

class BankAccount(models.Model):
  # id = models.SmallIntegerField(primary_key=True)
  banknumber = models.IntegerField()
  bank_4char = models.CharField(max_length=4)
  bankname   = models.CharField(max_length=30)
  agency     = models.IntegerField()
  account    = models.CharField(max_length=20)
  customer   = models.CharField(max_length=40, blank=True, null=True)
  cpf        = models.CharField(max_length=11, blank=True, null=True)
  created_at = models.DateTimeField(blank=True, null=True)
  updated_at = models.DateTimeField(blank=True, null=True)

  def __str__(self):
    return '{0} ag.{1} c/c.{2}'.format(self.bank_4char, self.agency, self.account)

  class Meta:
    managed = False
    db_table = 'bankaccounts'
