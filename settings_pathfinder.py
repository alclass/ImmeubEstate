#!/usr/bin/env python3
"""
settings_pathfinders.py
"""
import os
import sqlite3
from pathlib import Path

DEFAULT_DATA_FOLDERNAME = 'dados'
DEFAULT_SQLITE_FILENAME = 'immeub_app.sqlite'


class AppPaths:

  LOCAL_SETTINGS_FILENAME = 'settings_local.py'
  JSONFILES_RELDIR_KEY = 'JSONFILES_RELDIR'
  SQLITEFILES_RELDIR_KEY = 'SQLITEFILES_RELDIR'
  MAIN_SQLITE_FILENAME_KEY = 'MAIN_SQLITE_FILENAME'  # 'real_estate_rent_system.sqlite'

  @classmethod
  def get_sqlite_connection(cls):
    return sqlite3.connect(cls.get_sqlite_datafile_abspath())

  @classmethod
  def get_sqlite_datafile_abspath(cls):
    return os.path.join(cls.get_appdatafolder_abspath(), DEFAULT_SQLITE_FILENAME)

  @classmethod
  def get_appdatafile_abspath(cls, filename):
    return os.path.join(cls.get_appdatafolder_abspath(), filename)

  @classmethod
  def get_appdatafolder_abspath(cls):
    return os.path.join(cls.get_app_package_root_abspath(), DEFAULT_DATA_FOLDERNAME)

  @classmethod
  def get_app_package_root_abspath(cls):
    thisfileabspath = Path(os.path.abspath(__file__))
    appabsrootdirpath = thisfileabspath.parent
    return appabsrootdirpath

  @classmethod
  def get_local_settings_dict(cls):
    appabsrootdirpath = cls.get_app_package_root_abspath()
    settingsabsfilepath = os.path.join(appabsrootdirpath, cls.LOCAL_SETTINGS_FILENAME)
    settingsdict = eval(open(settingsabsfilepath).read())
    return settingsdict

  @classmethod
  def get_local_settings_value_from_key(cls, dictkey):
    configdict = cls.get_local_settings_dict()
    localsettingsvalue = configdict[dictkey]
    return localsettingsvalue

  @classmethod
  def get_abspath_for(cls, entry_dictkey):
    approotabsdir = cls.get_app_package_root_abspath()
    relativedir = cls.get_local_settings_value_from_key(entry_dictkey)
    return os.path.join(approotabsdir, relativedir)

  @classmethod
  def get_jsonfolder_absdirpath(cls):
    appabsrootdirpath = cls.get_app_package_root_abspath()
    configdict = cls.get_local_settings_dict()
    jsonfiles_reldir = configdict[cls.JSONFILES_RELDIR_KEY]
    jsonfolerabsdir = os.path.join(appabsrootdirpath, jsonfiles_reldir)
    return jsonfolerabsdir

  @classmethod
  def get_mainsqlitefile_abspath(cls):
    approotabsdir = cls.get_app_package_root_abspath()
    mainsqlite_relativedir = cls.get_local_settings_value_from_key(cls.MAIN_SQLITE_FILENAME_KEY)
    mainsqlitefile_abspath = os.path.join(approotabsdir, mainsqlite_relativedir)
    return mainsqlitefile_abspath

  @classmethod
  def get_sqlite_folder_abspath(cls):
    approotabsdir = cls.get_app_package_root_abspath()
    sqlitefolder_relativedir = cls.get_local_settings_value_from_key(cls.SQLITEFILES_RELDIR_KEY)
    sqlitefolder_abspath = os.path.join(approotabsdir, sqlitefolder_relativedir)
    return sqlitefolder_abspath


def adhoc_test():
  print('-'*70)
  print('app package root abspath = [[', AppPaths.get_app_package_root_abspath(), ']]')
  print('-'*70)
  print('sqlite folder abspath  = [[', AppPaths.get_sqlite_folder_abspath(), ']]')
  print('-'*70)
  print('main sqlite file abspath  = [[', AppPaths.get_mainsqlitefile_abspath(), ']]')
  print('-'*70)


if __name__ == '__main__':
  adhoc_test()
