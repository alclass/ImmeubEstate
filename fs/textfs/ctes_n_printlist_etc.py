#!/usr/bin/env python3

import collections

billitem_ntuple_constr = collections.namedtuple('BillItemNamedTuple', 'itdatetime, ittype, description, itvalue, itobs1, itobs2, is_inmonth')
# payrecor_ntuple_constr does not exist anymore for it's the same as billitem_ntuple_constr

class KItemTypes:
  TK_RENTVAL  = 'ALUGUEL'
  TK_CONDFEE  = 'CONDOMINIO'
  TK_PROPTAX  = 'IPTU'
  TK_FDEPTAR  = 'FUNESBOM'
  TK_EXTRAIM  = 'EXTRAIM'  # Extra in-month
  TK_INCFINE  = 'INCIDENCIA'
  TK_INTMCORR = 'CORRMONET'
  TK_IBALANCE = 'SALDOINI'
  TK_FBALANCE = 'SALDOFIN'
  TK_PAYMENT  = 'PAGAMENTO'

  #TK_INIDEBT  = 'DEBITOINI'
  #TK_FINDEBT  = 'DEBITOFIN'
  #TK_FINCRED  = 'CREDITOFIN'
  #TK_INICRED  = 'CREDITOINI'


INMONTH_AMOUNT_TYPES = [
  KItemTypes.TK_RENTVAL,
  KItemTypes.TK_CONDFEE,
  KItemTypes.TK_PROPTAX,
  KItemTypes.TK_FDEPTAR,
  KItemTypes.TK_EXTRAIM,
]


def print_bookkeeping(bookkeeping_tuplelist):
  '''
  A update in __str__() of Closer made this little function outdated or unused / unuseable.

  :param bookkeeping_tuplelist:
  :return:
  '''
  for bookkeeping_tuple in bookkeeping_tuplelist:
    print (bookkeeping_tuple)