#!/usr/bin/env python3

import collections, datetime

def printlist(alist):
  for elem in alist:
    print(elem)

class MutSeq(collections.Sequence):
  text = 'Hello World'

  def __getitem__(self, item):
    return self[item]

  def __len__(self, item):
    return len(self)

  def append(self, value):
    self.append(value)

  #def __setitem__(self, key, value):(self, value):
    #self.append(value)


class Convert:

  def __init__(self, pdict):
    for k in pdict:
      setattr(self, k, pdict[k])

  def __str__(self):
    outstr = 'Convert dict to class test\n'
    outstr += 'a=%s\n' %str(self.a)
    outstr += 'a=%s\n' %str(self.b)
    return outstr

def convert_dict_to_class():
  pdict = {'a':1,'b':2,}
  c = Convert(pdict)
  print (c)

if __name__ == '__main__':
  # ptest_mutable_sequence()
  #create_a_namedtuplelist()
  convert_dict_to_class()

namedtupleconstr = collections.namedtuple('TestNT', 'amount, pdate')
def create_a_namedtuplelist():
  ntlist =  []

  amount = 10
  pdate = datetime.date(year=2019, month=11, day=10)
  nt = namedtupleconstr(amount=amount, pdate=pdate)
  ntlist.append(nt)

  amount = 10
  pdate = datetime.date(year=2019, month=11, day=15)
  nt = namedtupleconstr(amount=amount, pdate=pdate)
  ntlist.append(nt)

  amount = 10
  pdate = datetime.date(year=2019, month=11, day=1)
  nt = namedtupleconstr(amount=amount, pdate=pdate)
  ntlist.append(nt)

  printlist(ntlist)

  ntlilst2 = sorted(ntlist, key=lambda x: x[1])

  printlist(ntlilst2)


