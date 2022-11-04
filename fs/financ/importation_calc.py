#!/usr/bin/env python3
import sympy
'''
Referência:
https://nucleoeuropeu.com.br/voce-sabe-como-calcular-impostos-na-importacao/

'''

class Tributes:
  iimport_alic = 0.12
  ipi_alic     = 0.15
  pis_alic     = 0.021
  cofins_alic  = 0.0965
  icms_alic    = 0.2
  tx_siscomex  = 0.01

  @classmethod
  def get_piscof_alic(cls):
    return cls.pis_alic + cls.cofins_alic


class Importation:

  def __init__(self, despesas_desembaraco, lucr_alic=0):

    self.aduan     =  None
    self.desps     = despesas_desembaraco
    self.lucr_alic = lucr_alic
    self.init_inner_attribs()

  def init_inner_attribs(self):
    self._iiv  =  None
    self._ipiv = None
    self._pisv = None
    self._cofv = None
    self._picov = None
    self._icmsb = None
    self._icmsv = None
    self._total4tribs = None
    self._totalanteslucro = None
    self._lucrov= None
    self._total = None

  @property
  def iiv(self):
    '''
    Notice aduan is transformed after process in one of the Child classes
    Passo 1) Impost Import: aplica-se a alíquota sobre o valor aduaneiro da mercadoria
    :return:
    '''
    if self._iiv is None:
      self._ivv = self.aduan * Tributes.iimport_alic
    return self._ivv

  @property
  def ipiv(self):
    '''
    Passo 2: IPI: o cálculo é feito pela soma do valor aduaneiro e do valor do Imposto de Importação. Este valor é multiplicado pela alíquota presente na TIPI
    :return:
    '''
    if self._ipiv is None:
      self._ipiv = (self.aduan + self.iiv) * Tributes.ipi_alic
    return self._ipiv

  @property
  def pisv(self):
    '''
    :return:
    '''
    if self._pisv is None:
      self._pisv = self.aduan * Tributes.pis_alic
    return self._pisv

  @property
  def cofv(self):
    '''
    :return:
    '''
    if self._cofv is None:
      self._cofv = self.aduan * Tributes.cofins_alic
    return self._cofv

  @property
  def picov(self):
    '''
    Passo 3: (de fato, são dois) PIS e Cofins: PIS import é de 2,1%; Cofins é de 9,65%. Assim como para o cálculo do II, as alíquotas de ambos incidem sobre o valor aduaneiro da mercadoria.
    :return:
    '''
    if self._picov is None:
      self._picov = self.aduan * Tributes.get_piscof_alic()
    return self._picov

  @property
  def icmsb(self):
    '''
    ICMSB é a base numerador para o cálculo que dividirá esta cifra com (1 - icms_alic)
    :return:
    '''
    if self._icmsb is None:
      self._icmsb = self.aduan + self.iiv + self.ipiv + self.picov + Tributes.tx_siscomex + self.desps
    return self._icmsb

  @property
  def icmsv(self):
    '''
    Passo 4: ICMS
      (a soma do valor aduaneiro + o Imposto de Importação + o Imposto de Produto Industrializado + o Programa de Integração Social + as Contribuições para Fins Sociais + a taxa do Siscomex + as despesas ocorridas até o momento do desembaraço aduaneiro)
      ÷ (1 – a alíquota devida do Imposto sobre Circulação e Mercadorias e Serviços)
    :return:
    '''
    if self._icmsv is None:
      self._icmsv = self.icmsb / (1 - Tributes.icms_alic)
    return self._icmsv

  @property
  def total4tribs(self):
    if self._total4tribs is None:
      self._total4tribs = self.iiv + self.ipiv + self.picov + self.icmsv
    return self._total4tribs

  @property
  def totalanteslucro(self):
    if self._totalanteslucro is None:
      # self._totalanteslucro = self.icmsb + self.icmsv + self.desps + Tributes.tx_siscomex
      self._totalanteslucro = self.aduan + self.total4tribs + Tributes.tx_siscomex + self.desps
    return self._totalanteslucro

  @property
  def lucrov(self):
    if self._lucrov:
      return self._lucrov
    self._lucrov = self.totalanteslucro * self.lucr_alic
    return self._lucrov

  @property
  def total(self):
    if self._total:
      return self._total
    self._total = self.totalanteslucro + self.lucrov
    return self._total

  def __eq__(self, other):
    if self.aduan != other.aduan:
      return False
    if self.desps != other.desps:
      return False
    if self.lucr_alic != other.lucr_alic:
      return False
    if self.iiv != other.iiv:
      return False
    if self.ipiv != other.ipiv:
      return False
    if self.picov != other.picov:
      return False
    if self.icmsv != other.icmsv:
      return False
    if self.lucrov != other.lucrov:
      return False
    if self.total != other.total:
      return False
    return True

  def str_as_lines(self):
    lines = []
    line = 'Despesas Desembaraço (dado) => %f' %self.desps
    lines.append(line)
    line = 'Lucro alícota (dado) => %f' %self.lucr_alic
    lines.append(line)
    line = 'Valor Aduaneiro => %f' %self.aduan
    lines.append(line)
    line = 'II alícota (param) => %f' %Tributes.iimport_alic
    lines.append(line)
    line = 'II valor => %f' %self.iiv
    lines.append(line)
    line = 'IPI alícota (param) => %f' %Tributes.ipi_alic
    lines.append(line)
    line = 'IPI valor => %f' %self.ipiv
    lines.append(line)
    line = 'PIS & Cofins alícota (param) => %f' %Tributes.get_piscof_alic()
    lines.append(line)
    line = 'PIS & Cofins valor => %f' %self.picov
    lines.append(line)
    line = 'ICMS alícota (param) => %f' %Tributes.icms_alic
    lines.append(line)
    line = 'ICMS valor => %f' %self.icmsv
    lines.append(line)
    line = 'Taxa Siscomex (param) => %f' %Tributes.tx_siscomex
    lines.append(line)
    line = 'Total antes do Lucro valor => %f' %self.totalanteslucro
    lines.append(line)
    line = 'Lucro valor => %f' %self.lucrov
    lines.append(line)
    line = 'Total => %f' %self.total
    lines.append(line)
    return lines

class ImportationForward(Importation):

  def __init__(self, valor_aduaneiro, despesas_desembaraco, lucr_alic=0):

    super().__init__(despesas_desembaraco, lucr_alic)
    self.aduan = valor_aduaneiro
    self._backward_importation_obj = None

  @property
  def backward_importation_obj(self):
    if self._backward_importation_obj:
      return self._backward_importation_obj
    self._backward_importation_obj = ImportationBackward(self.total, self.desps, self.lucr_alic)
    return self._backward_importation_obj

  def str_as_lines(self):
    lines = []
    line = ' ************* FORWARD IMPORTATION *************'
    lines.append(line)
    line = 'Valor aduaneiro (dado/forward) => %f' %self.aduan
    lines.append(line)
    lines += super().str_as_lines()
    return lines

  def __str__(self):
    return '\n'.join(self.str_as_lines())

class ImportationBackward(Importation):

  def __init__(self, total_for_backward, despesas_desembaraco, lucr_alic=0):

    super().__init__(despesas_desembaraco, lucr_alic)
    if total_for_backward is None:
      error_msg = 'Total_for_backward is None in class ImportationBackward'
      raise ValueError(error_msg)
    self.total_for_backward = total_for_backward
    self._total_recalculated = None
    self._forward_importation_obj = None
    self.solve_eq_has_run = False
    self.va = sympy.symbols('va') # va is Valor Aduaneiro; here it's a Sympy symbol to help solve the linear equation that finds it
    self.solve_eq()

  @property
  def iiv_eq(self):
    return self.va * Tributes.iimport_alic

  @property
  def ipiv_eq(self):
    return (self.va + self.iiv_eq) * Tributes.ipi_alic

  @property
  def picov_eq(self):
    return self.va * Tributes.get_piscof_alic()

  @property
  def icmsbnum_eq(self):
    return self.va + self.iiv_eq + self.ipiv_eq + self.picov_eq + Tributes.tx_siscomex + self.desps

  @property
  def icmsv_eq(self):
    return self.icmsbnum_eq / (1 - Tributes.icms_alic)

  @property
  def totalanteslucro_eq(self):
    return self.icmsbnum_eq + self.icmsv_eq

  @property
  def lucro_eq(self):
    return self.totalanteslucro_eq * self.lucr_alic

  @property
  def lucrov(self):
    self.solve_eq()
    if self._lucrov:
      return self._lucrov
    self._lucrov = self.totalanteslucro * self.lucr_alic
    return self._lucrov

  @property
  def total_eq(self):
    return self.totalanteslucro_eq + self.lucro_eq

  @property
  def total_recalculated(self):
    self.solve_eq()
    if self._total_recalculated:
      return self._total_recalculated
    self._total_recalculated = self.icmsb + self.icmsv + self.lucrov
    return self._total_recalculated

  def solve_eq(self):
    if self.solve_eq_has_run:
      return
    eq = self.total_eq - self.total_for_backward
    solv = sympy.solvers.solve(eq, self.va)
    self.aduan = solv[0]
    self.solve_eq_has_run = True

  @property
  def forward_importation_obj(self):
    self.solve_eq()
    if self._forward_importation_obj:
      return self._forward_importation_obj
    if self.aduan is None:
      # can't instantiate Importation with None
      return None
    self._forward_importation_obj = ImportationForward(valor_aduaneiro=self.aduan, despesas_desembaraco=self.desps, lucr_alic=self.lucr_alic)
    return self._forward_importation_obj

  def str_as_lines(self):
    lines = []
    line = ' ************* BACKWARD IMPORTATION *************'
    lines.append(line)
    line = 'Total (dado/backward) => %f' %self.total_for_backward
    lines.append(line)
    lines += super().str_as_lines()
    return lines

  def __str__(self):
    return '\n'.join(self.str_as_lines())

def adhoc_test2():

  print ('-'*50)
  backward_importation = ImportationBackward(300, 3, 0.1)
  print (backward_importation)
  print ('-'*50)
  print (backward_importation.forward_importation_obj)

def adhoc_test1():
  '''
  forward_imp = ImportationForward(84.099695, 3, 0.1)
  print (forward_imp)
  :return:
  '''
  backward_imp = ImportationBackward(300, 3, 0.1)
  print (backward_imp)

def process():
  adhoc_test2()

if __name__ == '__main__':
  process()
