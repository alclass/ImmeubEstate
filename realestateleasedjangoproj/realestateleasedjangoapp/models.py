# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.utils.dateformat import format

class AdditionTarifa(models.Model):
  #id = models.SmallIntegerField(primary_key=True)
  cobrancatipo_id  = models.IntegerField()
  contract_id      = models.IntegerField()
  monthyeardateref = models.DateField(blank=True, null=True)
  n_cota           = models.IntegerField(blank=True, null=True)
  total_cotas      = models.IntegerField(blank=True, null=True)
  lineinfo         = models.CharField(max_length=80, blank=True, null=True)
  valor            = models.DecimalField(max_digits=9, decimal_places=2)
  created_at = models.DateTimeField(blank=True, null=True)
  updated_at = models.DateTimeField(blank=True, null=True)

  class Meta:
    managed = False
    db_table = 'additiontarifas'


class AmortizationPayment(models.Model):
  # id = models.SmallIntegerField(primary_key=True)
  payer_person_id         = models.PositiveIntegerField()
  is_loan_delivery        = models.IntegerField()
  loan_duration_in_months = models.PositiveIntegerField(blank=True, null=True)
  paydate                 = models.DateField()
  valor_pago              = models.DecimalField(max_digits=9, decimal_places=2)
  created_at = models.DateTimeField(blank=True, null=True)
  updated_at = models.DateTimeField(blank=True, null=True)

  class Meta:
    managed = False
    db_table = 'amortizationpayments'

aaa='''
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
'''


aaa='''
class BillingItem(models.Model):
  # id = models.IntegerField(primary_key=True)
  cobranca          = models.ForeignKey('Cobranca', models.DO_NOTHING, blank=True, null=True)
  cobrancatipo      = models.ForeignKey('CobrancaTipo', models.DO_NOTHING, blank=True, null=True)
  brief_description = models.CharField(max_length=30)
  charged_value     = models.DecimalField(max_digits=9, decimal_places=2)
  ref_type          = models.CharField(max_length=1)
  freq_used_ref     = models.CharField(max_length=1)
  monthyeardateref  = models.DateField(blank=True, null=True)
  n_cota_ref        = models.PositiveIntegerField(blank=True, null=True)
  total_cotas_ref   = models.PositiveIntegerField(blank=True, null=True)
  was_original_value_modified           = models.IntegerField(blank=True, null=True)
  brief_description_for_modifier_if_any = models.CharField(max_length=20, blank=True, null=True)
  original_value_if_needed              = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
  percent_in_modifying_if_any           = models.IntegerField(blank=True, null=True)
  money_amount_in_modifying_if_any      = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
  obs                                   = models.CharField(max_length=144, blank=True, null=True)
  created_at = models.DateTimeField(blank=True, null=True)
  updated_at = models.DateTimeField(blank=True, null=True)

  def __str__(self):
    monthyeardateref = format(self.monthyeardateref, 'M/Y')
    cobrancatipochar4id = self.cobrancatipo.char4id
    return '{0} p/pagt. {1} {2}'.format(self.charged_value, monthyeardateref, cobrancatipochar4id)

  class Meta:
    managed = False
    db_table = 'billingitems'
'''

class BankDeposit(models.Model):
  bankaccount = models.ForeignKey(BankAccount, on_delete=models.DO_NOTHING, blank=True, null=True)
  cobranca    = models.ForeignKey('Cobranca', on_delete=models.DO_NOTHING)
  value = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
  paid_with_physmoney = models.BooleanField(default=False)
  deposit_date = models.DateField()
  extractinfo = models.CharField(max_length=150, blank=True, null=True)
  obsinfo     = models.CharField(max_length=150, blank=True, null=True)
  created_at = models.DateTimeField(blank=True, null=True)
  updated_at = models.DateTimeField(blank=True, null=True)

  def __str__(self):
    line = 'Depósito: {0}; valor={1:.2f} à Cobrança: {2}({3})'.format(
      self.deposit_date,
      self.value,
      self.cobranca.monthrefdate,
      self.cobranca.monthseqnumber,
    )
    return line

  class Meta:
    managed = False
    db_table = 'bankdeposits'

class AmountIncreaseTrail(models.Model):
  cobranca = models.ForeignKey('Cobranca', on_delete=models.DO_NOTHING)
  montant_ini = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
  monthrefdate = models.DateField()
  monthseqnumber = models.PositiveSmallIntegerField(default=1)
  restart_timerange_date = models.DateField()
  end_timerange_date = models.DateField()
  interest_rate = models.DecimalField(max_digits=6, decimal_places=4, blank=True, null=True)
  corrmonet_in_month = models.DecimalField(max_digits=6, decimal_places=4, blank=True, null=True)
  paid_amount = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
  finevalue   = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
  contract    = models.ForeignKey('Contract', on_delete=models.DO_NOTHING)
  created_at = models.DateTimeField(blank=True, null=True)
  updated_at = models.DateTimeField(blank=True, null=True)

  @property
  def j_mais_cm(self):
    return self.interest_rate + self.corrmonet_in_month

  def __str__(self):
    line = 'Valor-ini: {0:.2f}; Data-ini: {1}; data-fim:{2}; j+cm:{3:.4f} à Cobrança: {4}({5})'.format(
      self.montant_ini,
      self.restart_timerange_date,
      self.end_timerange_date,
      self.j_mais_cm,
      self.cobranca.monthrefdate,
      self.cobranca.monthseqnumber,
    )
    return line

  class Meta:
    managed = False
    db_table = 'amountincreasetrails'

aaa='''
class Cobranca(models.Model):
  # id = models.IntegerField(primary_key=True)
  monthyeardateref   = models.DateField()
  n_seq_from_dateref = models.PositiveIntegerField(default=1)
  duedate            = models.DateField(blank=True, null=True)
  discount           = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
  price_increase_if_any         = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
  lineinfo_discount_or_increase = models.CharField(max_length=144, blank=True, null=True)
  tot_adic_em_tribs             = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
  n_items     = models.PositiveIntegerField(blank=True, null=True)
  contract    = models.ForeignKey('Contract', on_delete=models.DO_NOTHING)
  bankaccount = models.ForeignKey(BankAccount, on_delete=models.DO_NOTHING)
  n_parcelas  = models.PositiveSmallIntegerField(default=1)
  are_parcels_monthly    = models.IntegerField(blank=True, null=True)
  parcel_n_days_interval = models.PositiveSmallIntegerField(blank=True, null=True)
  has_been_paid          = models.IntegerField(default=0)
  created_at = models.DateTimeField(blank=True, null=True)
  updated_at = models.DateTimeField(blank=True, null=True)

  def get_refstr(self):
    mmm_yyyy_str = format(self.monthyeardateref, 'M/Y')
    n_seq_from_dateref = 1
    if self.n_seq_from_dateref is not None:
      n_seq_from_dateref = self.n_seq_from_dateref
    refstr = mmm_yyyy_str + ' c' + str(n_seq_from_dateref)
    return refstr

  def __str__(self):
    refstr         = self.get_refstr()
    duedatestr     = format(self.duedate, 'd/M')
    contrato_sigla = self.contract.imovel.apelido
    return '{0} p/pagt. {1} {2}'.format(refstr, duedatestr, contrato_sigla)

  class Meta:
    managed = False
    db_table = 'cobrancas'
'''

aaa='''
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
'''

class CondominioTarifa(models.Model):
  imovel_id = models.IntegerField()
  tarifa_valor = models.DecimalField(max_digits=9, decimal_places=2)
  monthyeardateref = models.DateField()
  created_at = models.DateTimeField(blank=True, null=True)
  updated_at = models.DateTimeField(blank=True, null=True)

  class Meta:
    managed = False
    db_table = 'condominiotarifas'


class ContractUser(models.Model):
  user_id = models.PositiveIntegerField(blank=True, null=True)
  contract_id = models.PositiveIntegerField(blank=True, null=True)
  created_at = models.DateTimeField(blank=True, null=True)
  updated_at = models.DateTimeField(blank=True, null=True)

  class Meta:
    managed = False
    db_table = 'contract_user'


class ContractBillingRule(models.Model):
  contract_id = models.IntegerField()
  cobrancatipo_id = models.IntegerField()
  ref_type = models.CharField(max_length=1)
  freq_used_ref = models.CharField(max_length=1)
  total_cotas_ref = models.PositiveIntegerField(blank=True, null=True)
  created_at = models.DateTimeField(blank=True, null=True)
  updated_at = models.DateTimeField(blank=True, null=True)

  class Meta:
    managed = False
    db_table = 'contractbillingrules'

aaa='''
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
'''

aaa='''
class Contract(models.Model):
  imovel = models.ForeignKey(Imovel, on_delete=models.DO_NOTHING)
  initial_rent_value = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
  current_rent_value = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
  bankaccount = models.ForeignKey(BankAccount, on_delete=models.DO_NOTHING)
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
'''

class CorrMonet(models.Model):
  mercado_indicador_id = models.PositiveIntegerField()
  indice4char = models.CharField(max_length=4)
  fraction_value = models.DecimalField(max_digits=6, decimal_places=5)
  monthyeardateref = models.DateField()
  created_at = models.DateTimeField(blank=True, null=True)
  updated_at = models.DateTimeField(blank=True, null=True)

  class Meta:
    managed = False
    db_table = 'corrmonets'



class IptuTabela(models.Model):
  imovel_id = models.IntegerField()
  optado_por_cota_unica = models.IntegerField()
  ano = models.PositiveSmallIntegerField()
  ano_quitado = models.IntegerField()
  n_cota_quitada_ate_entao = models.PositiveIntegerField(blank=True, null=True)
  valor_parcela_unica = models.DecimalField(max_digits=8, decimal_places=2)
  valor_parcela_10x = models.DecimalField(max_digits=7, decimal_places=2)
  created_at = models.DateTimeField(blank=True, null=True)
  updated_at = models.DateTimeField(blank=True, null=True)

  class Meta:
    managed = False
    db_table = 'iptutabelas'


class MercadoIndice(models.Model):
  indice4char = models.CharField(max_length=4)
  sigla = models.CharField(max_length=8)
  description = models.CharField(max_length=150, blank=True, null=True)
  since = models.DateField(blank=True, null=True)
  url_datasource = models.CharField(max_length=255, blank=True, null=True)
  is_active = models.IntegerField()
  info = models.TextField(blank=True, null=True)
  created_at = models.DateTimeField(blank=True, null=True)
  updated_at = models.DateTimeField(blank=True, null=True)

  class Meta:
    managed = False
    db_table = 'mercadoindices'


class MoraDebito(models.Model):
  contract_id = models.IntegerField()
  monthyeardateref = models.DateField(blank=True, null=True)
  is_open = models.IntegerField()
  ini_debt_date = models.DateField()
  ini_debt_value = models.DecimalField(max_digits=9, decimal_places=2)
  changed_debt_date = models.DateField(blank=True, null=True)
  changed_debt_value = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
  mora_rules_id = models.IntegerField(blank=True, null=True)
  lineinfo = models.CharField(max_length=80, blank=True, null=True)
  history = models.TextField(blank=True, null=True)
  created_at = models.DateTimeField(blank=True, null=True)
  updated_at = models.DateTimeField(blank=True, null=True)

  class Meta:
    managed = False
    db_table = 'moradebitos'

aaa='''
class Payment(models.Model):
  amount        = models.DecimalField(max_digits=8, decimal_places=2)
  bankaccount   = models.ForeignKey(BankAccount, on_delete=models.DO_NOTHING)
  deposit_date  = models.DateField()
  bankrefstring = models.CharField(max_length=50, blank=True, null=True)
  user          = models.ForeignKey('User', on_delete=models.DO_NOTHING)
  contract      = models.ForeignKey(Contract, on_delete=models.DO_NOTHING)
  created_at = models.DateTimeField(blank=True, null=True)
  updated_at = models.DateTimeField(blank=True, null=True)

  def __str__(self):
    imovel_apelido = str(self.contract.imovel.apelido)
    contract_id    = str(self.contract.id)
    bank_4char     = self.bankaccount.bank_4char
    return 'Pagto: {0} ({1}, {2}, {3}/{4}, {5})'\
      .format(self.amount, bank_4char, self.deposit_date, imovel_apelido, contract_id, self.user.first_n_last_names())

  class Meta:
    managed = False
    db_table = 'payments'
'''

class Person(models.Model):
  user_id_if_applicable = models.PositiveIntegerField(blank=True, null=True)
  cpf = models.IntegerField(blank=True, null=True)
  first_name = models.CharField(max_length=20)
  middle_names = models.CharField(max_length=50, blank=True, null=True)
  last_name = models.CharField(max_length=25, blank=True, null=True)
  birthdate = models.DateField(blank=True, null=True)
  relation = models.CharField(max_length=4, blank=True, null=True)
  created_at = models.DateTimeField(blank=True, null=True)
  updated_at = models.DateTimeField(blank=True, null=True)

  class Meta:
    managed = False
    db_table = 'persons'


class User(models.Model):
  username = models.CharField(max_length=20, blank=True, null=True)
  fullname = models.CharField(max_length=150, blank=True, null=True)
  cpf = models.CharField(max_length=255, blank=True, null=True)
  rg = models.CharField(max_length=30, blank=True, null=True)
  tipo_relacao = models.CharField(max_length=255, blank=True, null=True)
  email = models.CharField(unique=True, max_length=255)
  password = models.CharField(max_length=191)
  remember_token = models.CharField(max_length=100, blank=True, null=True)
  created_at = models.DateTimeField(blank=True, null=True)
  updated_at = models.DateTimeField(blank=True, null=True)

  def first_n_last_names(self):
    if self.fullname is None or len(self.fullname) == 0:
      return ''
    pp = self.fullname.split(' ')
    firstname = pp[0]
    lastname = ''
    if len(pp) > 1:
      lastname = pp[-1]
    return firstname + ' ' + lastname

  def __str__(self):
    return self.first_n_last_names()

  class Meta:
    managed = False
    db_table = 'users'


