#!/usr/bin/env python3
'''
cities_data_json_writer.py
'''
import fs.db.json_tofrom.general_json_reader_writer as jsongen

json_filename = 'cities_realestaterentsystem.json'
cities_dict = {}
city_id = 'rjrj'
cities_dict ['rjrj'] = { # 'city_id' : '',
  'city_id'       : 'rjrj',
  'cityname'      : 'Rio de Janeiro',
  'state2letter'  : 'RJ',
  'statename'     : 'Rio de Janeiro',
  'country2letter': 'br',
}
jsongen.write_pythondata_to_jsondbfolder(cities_dict, json_filename)
