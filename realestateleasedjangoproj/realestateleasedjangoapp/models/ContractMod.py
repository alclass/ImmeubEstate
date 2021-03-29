#!/usr/bin/env python3
from django.db import models

class Contract(models.Model):
  imovel = models.ForeignKey('Imovel', on_delete=models.DO_NOTHING)
  initial_rent_value = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
  current_rent_value = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
  bankaccount = models.ForeignKey('BankAccount', on_delete=models.DO_NOTHING)
  # models.PositiveIntegerField(blank=True, null=True)
  reajuste_indice4char = models.CharField(max_length=4, blank=True, null=True)
  corrmonet_indice4char = models.CharField(max_length=4)
  pay_day_when_monthly = models.IntegerField(blank=True, null=True)
  apply_multa_incid_mora = models.IntegerField(blank=True, null=True)
  perc_multa_incid_mora = models.IntegerField(blank=True, null=True)
  apply_juros_fixos_am = models.IntegerField(blank=True, null=True)
  perc_juros_fixos_am = models.IntegerField(blank=True, null=True)
  apply_corrmonet_am = models.IntegerField(blank=True, null=True)
  signing_date = models.DateField(blank=True, null=True)
  start_date = models.DateField(blank=True, null=True)
  duration_in_months = models.IntegerField(blank=True, null=True)
  n_days_aditional = models.IntegerField(blank=True, null=True)
  repassar_condominio = models.IntegerField()
  repassar_iptu = models.IntegerField()
  is_active = models.IntegerField(blank=True, null=True)
  created_at = models.DateTimeField(blank=True, null=True)
  updated_at = models.DateTimeField(blank=True, null=True)

  def __str__(self):
    return 'Contract {0} {1} {2}'.format(self.id, self.start_date, str(self.imovel))

  class Meta:
    managed = False
    db_table = 'contracts'