#/usr/bin/env python3
'''
__init__.py in models package
'''
# package models
# App ImmeubRentPySwDv
import os


def adhoc_test():
  print ('abspath to db dir is ', BaseAppPaths.get_database_abspath())

if __name__ == '__main__':
  adhoc_test()
