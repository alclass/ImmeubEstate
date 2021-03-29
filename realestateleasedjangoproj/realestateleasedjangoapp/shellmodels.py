#!/usr/bin/env python3
import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print (BASE_DIR)
'''
pp = BASE_DIR.split('/')
BASE_DIR = '/'.join(pp[:-1])
print (BASE_DIR)
'''
sys.path.insert(0, BASE_DIR)

from realestateleasedjangoapp.models import BankAccount as BA

def show_1st_bankaccount():
  firstrec = BA.objects.first()
  print (firstrec)

if __name__ == '__main__':
  show_1st_bankaccount()
