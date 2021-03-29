#!/usr/bin/env python3
import sympy

def ptest():
  x = sympy.symbols('x')
  a = 10 - x
  b = 7 * a + 5
  solv = sympy.solvers.solve(b, x)
  eq = sympy.Eq(b) # , a.doit()
  #result = a(7)
  print (eq, solv)

iif  = 0.12
ipif = 0.15

def test_taxes():
  va = sympy.symbols('va')
  iiv = va * iif
  ipiv = (va + iiv) * ipif
  total_eq = va + iiv + ipiv - 100
  solv = sympy.solvers.solve(total_eq, va)
  aduan = solv[0]
  print (solv, aduan)
  iiv = aduan * iif
  print ('iiv', iiv)
  ipiv = (aduan + iiv) * ipif
  print ('ipiv', ipiv)
  total = aduan + iiv + ipiv
  print ('total', total)

def process():
  # ptest()
  test_taxes()

if __name__ == '__main__':
  process()