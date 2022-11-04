#!/usr/bin/env python3
import unittest

from .importation_calc import ImportationForward
from .importation_calc import ImportationBackward
from .importation_calc import Tributes

class TestImportation(unittest.TestCase):

  def test_1(self):
    '''

    :return:
    '''
    aduan = 84.099695 # 92.723823 (this is when profit is 0)
    despesas_desembaraco = 3
    total_expected = 300
    lucro_alic = 0.1
    importation = ImportationForward(aduan, despesas_desembaraco, lucro_alic)
    iiv = aduan * Tributes.iimport_alic
    self.assertEqual(iiv, importation.iiv)
    ipiv = (aduan + iiv) * Tributes.ipi_alic
    self.assertEqual(ipiv, importation.ipiv)
    picov = aduan * Tributes.get_piscof_alic()
    self.assertEqual(picov, importation.picov)
    icmsbnum = aduan + iiv + ipiv + picov + despesas_desembaraco + Tributes.tx_siscomex
    icmsv = icmsbnum / (1 - Tributes.icms_alic)
    self.assertEqual(icmsv, importation.icmsv)
    total4tribs = iiv + ipiv + picov + icmsv
    self.assertEqual(total4tribs, importation.total4tribs)
    totalantesdolucro = icmsbnum + icmsv
    lucrov = totalantesdolucro * lucro_alic
    total = totalantesdolucro + lucrov
    self.assertEqual(total, importation.total)
    self.assertAlmostEqual(total_expected, round(importation.total, 6))

  def test_2(self):
    '''
    Inverting calculation, but without sympy in this method
    :return:
    '''
    aduan = aduan_expected = 92.723823
    despesas_desembaraco = 3
    previmp = ImportationForward(aduan, despesas_desembaraco)
    invimp = ImportationBackward(previmp.total, previmp.desps)
    self.assertEqual(previmp.iiv, invimp.iiv)
    self.assertEqual(previmp.ipiv, invimp.ipiv)
    self.assertEqual(previmp.picov, invimp.picov)
    self.assertEqual(previmp.icmsb, invimp.icmsb)
    self.assertEqual(previmp.icmsv, invimp.icmsv)
    self.assertEqual(previmp.total, invimp.total)
    self.assertEqual(previmp.total, invimp.total_recalculated)
    self.assertEqual(previmp.aduan, invimp.aduan)
    self.assertEqual(previmp.total4tribs, invimp.total4tribs)
    self.assertEqual(aduan_expected, invimp.aduan)

  def test_3(self):
    aduan = 92.723823
    despesas_desembaraco = 3
    forward_imp = ImportationForward(aduan, despesas_desembaraco)
    backward_imp = forward_imp.backward_importation_obj
    forward_from_backward = backward_imp.forward_importation_obj
    self.assertTrue(forward_imp == backward_imp)
    self.assertTrue(forward_imp == forward_from_backward)
    self.assertTrue(forward_from_backward == backward_imp)

def process():
  pass

if __name__ == '__main__':
  process()
