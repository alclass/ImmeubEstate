#!/usr/bin/env python3
import inspect
'''
1) http://www.blog.pythonlibrary.org/2013/01/11/how-to-get-a-list-of-class-attributes/
This blog post is where the [inspect] module appeared first to me

2) To help find, from dirtree, text files (py & txt) with the word "inspect", ie, helping find expression 'import inspect' 
egrep -ir --include=*.{py,txt} "(inspect)"
'''
import func.textfs.ctes_n_printlist_etc as ctes
K_ONE = '1'
K_TWO = '2'
class Bill:

  KItemTypes = ctes.KItemTypes

class A:

  def __init__(self):
    self.field1 = 'one'

def process():
  instance = A()
  #members = inspect.getmembers(a)
  # = inspect.getmembers(Bill.KItemTypes, lambda a: not (inspect.isroutine(a)))
  #lst = inspect.getmembers(instance, lambda a: not (inspect.isroutine(a)))
  # lst = inspect.getmembers(Bill.KItemTypes, lambda a: not (inspect.isroutine(a)))
  # lst = [i for i in dir(instance) if not callable(i)]
  lst = instance.__dict__.keys()
  lst = Bill.KItemTypes.__dict__.keys()
  print (lst )
  # print(m, 'not is method', not (inspect.isroutine(m)) )


if __name__ == '__main__':
  process()