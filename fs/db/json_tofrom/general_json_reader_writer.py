#!/usr/bin/env python3
import json, os, pprint
from settings_pathfinder import AppPaths

def get_jsonfile_absdir(jsonfilename):
  jsonfolder_abspath = AppPaths.get_jsonfolder_absdirpath()
  if jsonfolder_abspath is None:
    # error_msg = 'Error: jsonfolder_abspath is None'
    # raise IOError(error_msg)
    return None
  return os.path.join(jsonfolder_abspath, jsonfilename)

def readjson_n_return_python_data(jsonfilename):
  '''

  :param jsonfilename:
  :return:
  '''
  jsonfilepath = get_jsonfile_absdir(jsonfilename)
  if jsonfilepath is None:
    # error_msg = 'Error: jsonfilepath is None'
    # raise IOError(error_msg)
    return None
  with open(jsonfilepath, 'r') as f:
    return json.load(f)

def write_pythondata_to_jsondbfolder(python_data, jsonfilename):
  '''

  :return:
  '''
  jsonfilepath = get_jsonfile_absdir(jsonfilename)
  with open(jsonfilename, 'w') as outfile:
    json.dump(python_data, outfile, ensure_ascii=False)
  print('='*80)
  print ('json_data_written to file [', jsonfilename, ']')
  print (jsonfilepath)
  print('='*80)

def ptest():
  json_filename = 'bills_realestaterentsystem.json'
  pdict = readjson_n_return_python_data(json_filename)
  pp = pprint.PrettyPrinter()
  for k in pdict:
    pp.pprint(pdict[k]) # k, '=>',

if __name__ == '__main__':
  ptest()

'''
# old code that has been refactored

ROOTIDR = os.path.abspath('/')
def read_local_app_settings_into_dict():
  thisfilepath = Path(os.path.abspath(__file__))
  directory_downgoing = thisfilepath.parent
  REASONABLE_N_OF_DIRLEVELS = 64; dirlevelstaken = 0
  while 1:
    contents = os.listdir(directory_downgoing)
    if SETTINGS_LOCAL_FILENAME_CONVENTION in contents:
      settingsfilepath = os.path.join(directory_downgoing, SETTINGS_LOCAL_FILENAME_CONVENTION)
      cfgdict = {}
      try:
        cfgdict = eval(open(settingsfilepath).read())
      except Exception as e:
        error_msg = "Error: could not either read app's local settings file or put it into a dict. See also: " + str(e)
        raise Exception(error_msg)
      return cfgdict
    if directory_downgoing == ROOTIDR:
      SEARCH_END = True
      break
    directory_downgoing = directory_downgoing.parent
    dirlevelstaken += 1
    if dirlevelstaken > REASONABLE_N_OF_DIRLEVELS:
      break
  return None

def function_abc(jsonfilename):

  configdict = read_local_app_settings_into_dict()
  app_absdir = configdict[APP_ABSDIR]
  jsonfiles_reldir = configdict[JSONFILES_RELDIR]
  jsonfolerabsdir = os.path.join(app_absdir, jsonfiles_reldir)
  jsonfileabsdir = os.path.join(jsonfolerabsdir, jsonfilename)
  return jsonfileabsdir

def old_get_json_db_dirpath(jsonfilename):
  ''
  This method was used at a previous moment when each json datagroup was read from a module of its own. Now a class does the reading for all groups.
  :param jsonfilename:
  :return:
  ''
  directory = os.path.dirname(__file__)
  localpath = Path(directory)
  parentpath = localpath.parent
  # print os.path.abspath(os.path.join(yourpath, os.pardir))
  jsondbpath = os.path.join(parentpath, 'db/jsonfiles')
  # jsondbpath = os.path.join(jsondbpath, 'jsonfiles')
  filepath = os.path.join(jsondbpath, jsonfilename)
  return filepath


'''
