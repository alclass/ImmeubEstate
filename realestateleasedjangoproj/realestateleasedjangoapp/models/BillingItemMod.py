#!/usr/bin/env python3
from django.db import models

class BillingItem(models.Model):
  # id = models.IntegerField(primary_key=True)
  cobranca          = models.ForeignKey('Cobranca', models.DO_NOTHING, blank=True, null=True)
  brief_description = models.CharField(max_length=30)
  carried_from_cobranca_id = models.PositiveIntegerField(blank=True, null=True)
  cobrancatipo      = models.ForeignKey('CobrancaTipo', models.DO_NOTHING, blank=True, null=True)
  value     = models.DecimalField(max_digits=9, decimal_places=2)
  use_partnumber    = models.BooleanField(default=False)
  monthrefdate      = models.DateField(blank=True, null=True)
  partnumber        = models.PositiveIntegerField(blank=True, null=True)
  totalparts        = models.PositiveIntegerField(blank=True, null=True)
  was_original_value_modified    = models.IntegerField(blank=True, null=True)
  brief_description_for_modifier = models.CharField(max_length=20, blank=True, null=True)
  original_value   = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
  modifying_percent  = models.SmallIntegerField(blank=True, null=True)
  modifying_amount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
  obsinfo          = models.TextField(blank=True, null=True)
  created_at = models.DateTimeField(blank=True, null=True)
  updated_at = models.DateTimeField(blank=True, null=True)

  def __str__(self):
    strdict = {}
    strdict['cobrancatipochar4id'] = self.cobrancatipo.char4id
    strdict['value'] = self.value
    strdict['ano_mes_str'] = '{1}-{0:02d}'.format(self.monthrefdate.month, self.monthrefdate.year)
    imovel4char = 's/m'
    if self.cobranca:
      if self.cobranca.contract:
        if self.cobranca.contract.imovel:
          imovel4char = self.cobranca.contract.imovel.apelido
    strdict['imovel4char'] = imovel4char
    return '{imovel4char} {cobrancatipochar4id} {ano_mes_str} {value:6.2f}'.format(**strdict)

  class Meta:
    managed = False
    db_table = 'billingitems'
