#!/usr/bin/env python3
'''
json_writer_persons.py
'''
import func.db.json_tofrom.general_json_reader_writer as jsongen

json_filename = 'persons_realestaterentsystem.json'

persons_dict = {}
persons_dict['lucio1'] = {
  'fullname': 'Lucio Lemes',
  'cpf'     : '12345678911',
  'phones'  : ['2199991111'],
  'emails'  : ['lucio@email'],
}
persons_dict['beth1'] = {
  'fullname': 'Beth Miranda',
  'cpf'     : '12345678911',
  'phones'  : ['2199991111'],
  'emails'  : ['beth@email'],
}
persons_dict['filipe1'] = {
  'fullname': 'Filipe Teixeira',
  'cpf'     : '12345678911',
  'phones'  : ['2199991111'],
  'emails'  : ['filipe@email'],
}
persons_dict['munzer1'] = {
  'fullname': 'Munzer',
  'cpf'     : '12345678911',
  'phones'  : ['2199991111'],
  'emails'  : ['munzer@email'],
}

jsongen.write_pythondata_to_jsondbfolder(persons_dict, json_filename)
