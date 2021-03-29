#!/usr/bin/env python3
'''
json_data_writer.py
'''
import func.db.json_tofrom.general_json_reader_writer as jsongen

json_filename = 'tributes_per_immeuble_realestaterentsystem.json'

tributes_per_immeuble_dict = {}

tributes_per_immeuble_dict = {}
tributes_per_immeuble_dict['CDUTR'] = {
  2019 : {
    'prop_tax_directives': {
      'yearly_value_disconted': 3348.9,
      'value_parcel': 372.10,
      'n_parcels'   : 10,
      'for_months'  : list(range(1, 11)),
    },
    'fdept_tar_directives': {
      'yearly_value': 123.82,
      'apply_in_month': 6,
    }
  }
}
tributes_per_immeuble_dict['HLOBO'] = {
  2019 : {
    'prop_tax_directives': {
      'yearly_value_disconted': 1239.2,
      'value_parcel': 138.80,
      'n_parcels'   : 10,
      'for_months'  : list(range(1, 11)),
    },
    'fdept_tar_directives': {
      'yearly_value': 92.86,
      'apply_in_month': 6,
    }
  }
}
tributes_per_immeuble_dict['JACUM'] = {
  2019 : {
    'prop_tax_directives': {
      'yearly_value_disconted': 803.7,
      'value_parcel': 89.3,
      'n_parcels'   : 10,
      'for_months'  : list(range(1, 11)),
    },
    'fdept_tar_directives': {
      'yearly_value': 123.82,
      'apply_in_month': 6,
    }
  }
}
jsongen.write_pythondata_to_jsondbfolder(tributes_per_immeuble_dict, json_filename)