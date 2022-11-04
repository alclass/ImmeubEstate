#!/usr/bin/env python3
'''
address_json_reader.py
'''
import pprint
import fs.db.json_tofrom.general_json_reader_writer as jsongen

json_filename_sufix = '_realestaterentsystem.json'

DG_ADDRESS = 'ADDRESSES'
DG_BILL    = 'BILLS'
DG_CITY    = 'CITIES'
DG_CONDFEE = 'CONDFEES'
DG_CONTRACT= 'CONTRACTS'
DG_IMMEUBLE= 'IMMEUBLES'
DG_IPCA    = 'IPCAS'
DG_PAYMENT = 'PAYMENTS'
DG_TRIBUTE = 'TRIBUTES'

def form_dgfilename(dgword):
  return dgword.lower() + json_filename_sufix

datagroup_filenames_dict = {}
datagroup_filenames_dict[DG_ADDRESS]  = form_dgfilename(DG_ADDRESS)
datagroup_filenames_dict[DG_BILL]     = form_dgfilename(DG_BILL)
datagroup_filenames_dict[DG_CITY]     = form_dgfilename(DG_CITY)
datagroup_filenames_dict[DG_CONDFEE]  = form_dgfilename(DG_CONDFEE)
datagroup_filenames_dict[DG_CONTRACT] = form_dgfilename(DG_CONTRACT)
datagroup_filenames_dict[DG_IMMEUBLE] = form_dgfilename(DG_IMMEUBLE)
datagroup_filenames_dict[DG_IPCA]     = form_dgfilename(DG_IPCA)
datagroup_filenames_dict[DG_PAYMENT]  = form_dgfilename(DG_PAYMENT)
datagroup_filenames_dict[DG_TRIBUTE]  = form_dgfilename(DG_TRIBUTE)

class DataGroupJsonReader:

  def __init__(self, datagroudid):
    self.datagroudid = datagroudid

  @property
  def dg_filename(self):
    return datagroup_filenames_dict[self.datagroudid]

  def get_dict_by_id_from_json(self, dict_id):
    alldicts = self.read_all()
    try:
      pdict = alldicts[dict_id]
      return pdict
    except KeyError:
      pass
    return None

  def read_all(self):
    '''
    Calling readerfunction(json_filename) will return Python's data structure from the JSON data.
    This datastructure can either be a list or a dict.
    At this moment, all reads will return a dict, because each group (each one as a file),
      each one with a json, transforms to a dict.
    '''
    return jsongen.readjson_n_return_python_data(self.dg_filename)

  def print_all(self):
    print('='*80)
    print ('json_data_reader from file [', self.dg_filename, ']')
    print('='*80)
    pdict = self.read_all()
    for k in pdict:
      print(k, pdict[k])

def ptest():
  pp = pprint.PrettyPrinter()
  for datagroupid in datagroup_filenames_dict:
    dgobj = DataGroupJsonReader(datagroupid)
    # pdict = dgobj.print_all()
    print ('-'*50)
    print ('Data Group', datagroupid)
    print ('-'*50)
    pp.pprint(dgobj.read_all())

if __name__ == '__main__':
  ptest()
