#!/usr/bin/env python3

import collections, datetime

namedtupleconstr = collections.namedtuple('TestNT', 'amount, pdate')

def namedtuple_to_dict():
  ntlist =  []

  amount = 10
  pdate = datetime.date(year=2019, month=11, day=10)
  nt = namedtupleconstr(amount=amount, pdate=pdate)

  #==========================
  # namedtuple to orderedDict
  #==========================
  orderedDict = nt._asdict()
  # d = dict(nt)

  print(ntlist)
  print(orderedDict)

  #==========================
  # orderedDict to namedtuple
  #==========================
  d = dict(orderedDict)
  print(d)
  orderedDict2 = collections.OrderedDict(d)
  print(orderedDict2)

if __name__ == '__main__':
  namedtuple_to_dict()
