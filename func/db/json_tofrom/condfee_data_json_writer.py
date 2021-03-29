#!/usr/bin/env python3
'''
json_writer_condfee.py
'''
import func.db.json_tofrom.general_json_reader_writer as jsongen

json_filename = 'condfeebills_realestaterentsystem.json'

condfee_month_by_month_immeub_dict = {}
condfee_month_by_month_immeub_dict['CDUTR'] = {
  '2019' : [1407.61, 1543.90, 1543.90, 1160.50, 1336.06, 1407.20, 1160.50, 1673.54, 1473.94, 1393.55, -1, -1],
}

condfee_month_by_month_immeub_dict['HLOBO'] = {
  '2019' : [ 754.39,  710.16, 701.35, 701.35, 771.80, 712.36, 702.45, 714.12, 711.26, 715.67, 722.27, -1],
}

# process
jsongen.write_pythondata_to_jsondbfolder(condfee_month_by_month_immeub_dict, json_filename)