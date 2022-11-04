#!/usr/bin/env python3
"""
sqlite_cep_functions.py
"""
import settings_pathfinder as sp


def get_connection():
  return sp.AppPaths.get_sqlite_connection()


class CEP:
  TABLENAME = 'ceps'
  cep = 'cep'
  logra = 'logra'
  compl = 'compl'
  bairro = 'bairro'
  local = 'local'
  uf = 'uf'
  ibge = 'ibge'
  ddd = 'ddd'
  siafi = 'siafi'


CEPFIELDLIST = [
  CEP.cep, CEP.logra, CEP.compl, CEP.bairro,
  CEP.local, CEP.uf, CEP.ibge, CEP.ddd, CEP.siafi
]


def update_if_different(i_cep, found_row_cep, conn):
  """
  bool_ret =

  :param i_cep:
  :param found_row_cep:
  :param conn:
  :return:
  """
  sql = "UPDATE " + CEP.TABLENAME + " SET %(fieldnames_in_sql)s  WHERE " + CEP.cep + "=?;"
  fieldnames_in_sql = ''
  tuplevalues = []
  fieldnames = CEPFIELDLIST[:]
  for fieldname in fieldnames:
    # fieldname = CEPFIELDLIST[fieldseq]
    if i_cep[fieldname] != found_row_cep[fieldname]:
      fieldnames_in_sql = fieldnames_in_sql + fieldname + '=? AND\n'
      tuplevalues.append(found_row_cep[fieldname])
  if len(fieldnames_in_sql) > 0 and len(tuplevalues) > 0:
    fieldnames_in_sql += fieldnames_in_sql.rstrip(' AND\n')
    tuplevalues.append(found_row_cep[CEP.cep])
    sql = sql % {'fieldnames_in_sql': fieldnames_in_sql}
    cursor = conn.cursor()
    tuplevalues = tuple(tuplevalues)
    cursor.execute(sql, tuplevalues)
    conn.commit()
    conn.close()
    return True
  print('No need for db-updating')
  return False


def insert_cep(i_cep, conn):
  _ = i_cep
  cursor = conn.cursor()
  strvalues = '('
  strfields = '('
  for field in CEPFIELDLIST:
    strfields += field + ', '
    strvalues += '"' + str(eval('i_cep["' + field + '"]')) + '", '
  strfields = strfields.rstrip(', ') + ') VALUES '
  strvalues = strvalues.rstrip(', ') + ');'
  sql = "INSERT into ceps " + strfields + strvalues
  cursor.execute(sql)
  conn.commit()
  conn.close()
  return True


def transpose_tuplerows_into_dict(tuplefoundrowvalues):
  found_cep_dict = {}
  for i, fieldname in enumerate(CEPFIELDLIST):
    found_cep_dict[fieldname] = tuplefoundrowvalues[i]
  return found_cep_dict


def insert_or_update_cep(i_cep):
  """
  sqlite has a default built-in "id" field called
  Example:
  {'cep': '20260-020', 'logradouro': 'Travessa Pastor Daniel Ribeiro',
   'complemento': '', 'bairro': 'Rio Comprido',
   'localidade': 'Rio de Janeiro', 'uf': 'RJ',
   'ibge': '3304557', 'gia': '', 'ddd': '21', 'siafi': '6001'}
  """
  sql = "SELECT * FROM " + CEP.TABLENAME + " WHERE  " + CEP.cep + "=?;"
  cep = i_cep['cep']
  tuplevalues = (cep, )
  conn = get_connection()
  cursor = conn.cursor()
  cursor.execute(sql, tuplevalues)
  tuplefoundrowvalues = cursor.fetchone()
  if tuplefoundrowvalues:
    found_row_cep_dict = transpose_tuplerows_into_dict(tuplefoundrowvalues)
    return update_if_different(i_cep, found_row_cep_dict, conn)
  return insert_cep(i_cep, conn)


def tst_insert_update_example(cep):
  bool_ret = insert_or_update_cep(cep)
  print('bool_ret', bool_ret)


def filter_dict(p_dict):
  cep = p_dict['cep']
  cep = cep.replace('-', '')
  p_dict['cep'] = int(cep)
  logra = p_dict['logradouro']
  del p_dict['logradouro']
  p_dict['logra'] = logra
  compl = p_dict['complemento']
  del p_dict['complemento']
  p_dict['compl'] = compl
  local = p_dict['localidade']
  del p_dict['localidade']
  p_dict['local'] = local
  ddd = p_dict['ddd']
  p_dict['ddd'] = int(ddd)
  ibge = p_dict['ibge']
  p_dict['ibge'] = int(ibge)
  siafi = p_dict['siafi']
  p_dict['siafi'] = int(siafi)

  return p_dict


def tst_prep_insert_update_example():
  example_row_dict = {
    'cep': '20260-020', 'logradouro': 'Travessa Pastor Daniel Ribeiro',
    'complemento': '', 'bairro': 'Rio Comprido',
    'localidade': 'Rio de Janeiro', 'uf': 'RJ',
    'ibge': '3304557', 'gia': '', 'ddd': '21', 'siafi': '6001'
  }
  example_row_dict = filter_dict(example_row_dict)
  print(example_row_dict)
  return example_row_dict


def tst_insert_update():
  row_dict = tst_prep_insert_update_example()
  tst_insert_update_example(row_dict)


def process():
  """
  example_cep_dict = {}
  print('create_table_in_db()')
  insert_or_update_cep(example_cep_dict)
  """
  tst_insert_update()


if __name__ == '__main__':
  process()
