#!/usr/bin/env python3
'''
json_immeubles_writer.py
Here there cities, addresses & immeubles
'''
import func.db.json_tofrom.general_json_reader_writer as jsongen

json_filename = 'cities_realestaterentsystem.json'
cities_dict = {}
city_id = 'rjrj'
cities_dict ['rjrj'] = { # 'city_id' : '',
  'city_id': 'rjrj',
  'city': 'Rio de Janeiro',
  'state_id': 'RJ',
  'country_n': 55,
}
jsongen.write_pythondata_to_jsondbfolder(cities_dict, json_filename)

json_filename = 'addresses_realestaterentsystem.json'
addresses_dict = {}

address_id = '20550045'
addresses_dict[address_id] = {
  'address_id'    : address_id,
  'zipcode'       : address_id,
  'street_address': 'Rua Carmela Dutra',
  'neighbourhood' : 'Tijuca',
  'city_id'       : 'rjrj',
}
address_id = '20260142'
addresses_dict[address_id] = {
  'address_id'    : address_id,
  'zipcode'       : address_id,
  'street_address': 'Rua Haddock Lobo',
  'neighbourhood' : 'Tijuca',
  'city_id'       : 'rjrj',
}
address_id = '20260320'
addresses_dict[address_id] = {
  'address_id'    : address_id,
  'zipcode'       : address_id,
  'street_address': 'Rua Jacumã',
  'neighbourhood' : 'Tijuca',
  'city_id'       : 'rjrj',
}
jsongen.write_pythondata_to_jsondbfolder(addresses_dict, json_filename)

json_filename = 'immeubles_realestaterentsystem.json'
immeubles_dict = {}

immeuble_id = 'CDUTR'
immeubles_dict[immeuble_id] = {
  'immeuble5letter': immeuble_id,
  'inscr_munic'   : '30677025',
  'inscr_funesbom': '33423161',
  'inscr_rgi'     : '120712',
  'immeuble_type' : 'apartamento',
  'address_id': '20550045',  # for the time being, a zip code
  'street_n'  : 76,
  'apt_n'     : 201,
  'floor'     : 2,
  'floors_in_building': 5,
  'area_m2' : 116,
  'construction_year': 2008,
}
immeuble_id = 'HLOBO'
immeubles_dict[immeuble_id] = {
  'immeuble5letter': immeuble_id,
  'inscr_munic'   : '09364902',
  'inscr_funesbom': '405613-1',
  'inscr_rgi'     : 's/inf/mom',
  'immeuble_type' : 'apartamento',
  'address_id': '20260142',  # for the time being, a zip code
  'street_n'  : 386,
  'apt_n'     : 405,
  'floor'     : 2,
  'floors_in_building': 8,
  'area_m2': 116,
  'construction_year': 1969,
}
immeuble_id = 'JACUM'
immeubles_dict[immeuble_id] = {
  'immeuble5letter': immeuble_id,
  'inscr_munic'   : '01841279',
  'inscr_funesbom': '18854620',
  'inscr_rgi'     : '12711',
  'immeuble_type' : 'apartamento',
  'address_id': '20260320',  # for the time being, a zip code
  'street_n'  : 76,
  'apt_n'     : 202,
  'floor'     : 2,
  'floors_in_building' : 4,
  'area_m2' : 116,
  'construction_year' : 1959,
}
jsongen.write_pythondata_to_jsondbfolder(immeubles_dict, json_filename)
