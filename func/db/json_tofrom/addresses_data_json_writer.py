#!/usr/bin/env python3
'''
addresses_data_json_writer.py
'''
import func.db.json_tofrom.general_json_reader_writer as jsongen
json_filename = 'addresses_realestaterentsystem.json'

addresses_dict = {}
address_id = '20550045'
addresses_dict[address_id] = {
  'address_id'    : address_id,
  'zipcode'       : address_id,
  'addresstype'   : 'Rua',
  'addressname'   : 'Carmela Dutra',
  'neighbourhood' : 'Tijuca',
  'city_id'       : 'rjrj',
}
address_id = '20260142'
addresses_dict[address_id] = {
  'address_id'    : address_id,
  'zipcode'       : address_id,
  'addresstype'   : 'Rua',
  'addressname'   : 'Haddock Lobo',
  'neighbourhood' : 'Tijuca',
  'city_id'       : 'rjrj',
}
address_id = '20260320'
addresses_dict[address_id] = {
  'address_id'    : address_id,
  'zipcode'       : address_id,
  'addresstype'   : 'Rua',
  'addressname'   : 'Jacumã',
  'neighbourhood' : 'Tijuca',
  'city_id'       : 'rjrj',
}
jsongen.write_pythondata_to_jsondbfolder(addresses_dict, json_filename)
