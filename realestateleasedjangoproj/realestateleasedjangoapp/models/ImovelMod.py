#!/usr/bin/env python3
from django.db import models


class Imovel(models.Model):
  apelido = models.CharField(max_length=255)
  predio_nome = models.CharField(max_length=35, blank=True, null=True)
  logradouro = models.CharField(max_length=255)
  tipo_lograd = models.CharField(max_length=255)
  numero = models.PositiveSmallIntegerField(blank=True, null=True)
  complemento = models.CharField(max_length=255)
  cep = models.CharField(max_length=255)
  tipo_imov = models.CharField(max_length=25, blank=True, null=True)
  n_quartos = models.PositiveIntegerField(blank=True, null=True)
  n_banheiros = models.PositiveIntegerField(blank=True, null=True)
  n_dependencias = models.PositiveIntegerField(blank=True, null=True)
  n_salas = models.PositiveIntegerField(blank=True, null=True)
  n_cozinhas = models.PositiveIntegerField(blank=True, null=True)
  varanda_area_m2 = models.PositiveIntegerField(blank=True, null=True)
  n_vagas_garagem = models.PositiveIntegerField(blank=True, null=True)
  is_rentable = models.IntegerField()
  area_edif_iptu_m2 = models.SmallIntegerField(blank=True, null=True)
  area_terr_iptu_m2 = models.SmallIntegerField(blank=True, null=True)
  created_at = models.DateTimeField(blank=True, null=True)
  updated_at = models.DateTimeField(blank=True, null=True)

  def __str__(self):
    return '{0} {1}'.format(self.apelido, self.predio_nome)

  class Meta:
    managed = False
    db_table = 'imoveis'
