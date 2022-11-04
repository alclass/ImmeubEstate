#!/usr/bin/env python3
'''
immeubles_json_writer.py
'''
import fs.db.json_tofrom.general_json_reader_writer as jsongen

json_filename = 'immeubles_realestaterentsystem.json'
immeubles_dict = {}

immeuble5letter = 'CDUTR'
immeubles_dict[immeuble5letter] = {
  'immeuble5letter': immeuble5letter,
  'address_id'    : '20550045',  # for the time being, a zip code
  'inscr_munic'   : '30677025',
  'inscr_funesbom': '33423161',
  'inscr_rgi'     : '120712',
  'immeuble_type' : 'apartamento',
  'area_m2'    : 116,
  'n_quartos'  : 4,
  'n_banheiros': 3,
  'construction_year' : 2008,
  'n_in_address'      : 76,
  'address_complement': 201,
  'location_ref': 'Entre as estações do Metrô Saens Pena e São Francisco Xavier',
  'floor': 2,
  'floors_in_building': 5,
}
immeuble5letter = 'HLOBO'
immeubles_dict[immeuble5letter] = {
  'immeuble5letter': immeuble5letter,
  'address_id'     : '20260142',  # for the time being, a zip code
  'inscr_munic'    : '09364902',
  'inscr_funesbom' : '405613-1',
  'inscr_rgi'      : 's/inf/mom',
  'immeuble_type'  : 'apartamento',
  'area_m2'    : 116,
  'n_quartos'  : 4,
  'n_banheiros': 3,
  'construction_year' : 1969,
  'n_in_address'      : 370,
  'address_complement': 405,
  'location_ref': 'Próximo à estação do Metrô Afonso Pena, entre R. Afonso Pena e Prof. Gabizo',
  'floor': 2,
  'floors_in_building': 8,
}
immeuble5letter = 'JACUM'
immeubles_dict[immeuble5letter] = {
  'immeuble5letter': immeuble5letter,
  'address_id'     : '20260320',  # for the time being, a zip code
  'inscr_munic'    : '01841279',
  'inscr_funesbom' : '18854620',
  'inscr_rgi'      : '12711',
  'immeuble_type'  : 'apartamento',
  'area_m2'    : 116,
  'n_quartos'  : 3,
  'n_banheiros': 3,
  'construction_year' :1959,
  'n_in_address'      : 76,
  'address_complement': 202,
  'location_ref': 'Próximo à estação do Metrô Afonso Pena, entre R. Afonso Pena e Prof. Gabizo',
  'floor': 2,
  'floors_in_building': 4,
}
jsongen.write_pythondata_to_jsondbfolder(immeubles_dict, json_filename)
