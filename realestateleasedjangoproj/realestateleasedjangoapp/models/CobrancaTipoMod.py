#!/usr/bin/env python3
from django.db import models


class CobrancaTipo(models.Model):
  char4id = models.CharField(unique=True, max_length=4, blank=True, null=True)
  brief_description = models.CharField(max_length=30)
  is_repasse = models.IntegerField(blank=True, null=True)
  long_description = models.CharField(max_length=120, blank=True, null=True)
  created_at = models.DateTimeField(blank=True, null=True)
  updated_at = models.DateTimeField(blank=True, null=True)

  def __str__(self):
    return '{0} {1}'.format(self.char4id, self.brief_description)

  class Meta:
    managed = False
    db_table = 'cobrancatipos'
