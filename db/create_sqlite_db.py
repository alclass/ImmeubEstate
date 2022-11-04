#!/usr/bin/env python3
"""
create_sqlite_db.py
"""
import settings_pathfinder as sp


def get_connection():
  return sp.AppPaths.get_sqlite_connection()


def create_table_in_db():
  """
  sqlite has a default built-in "id" field called
  Example:
  {'cep': '20260-020', 'logradouro': 'Travessa Pastor Daniel Ribeiro',
   'complemento': '', 'bairro': 'Rio Comprido',
   'localidade': 'Rio de Janeiro', 'uf': 'RJ',
   'ibge': '3304557', 'gia': '', 'ddd': '21', 'siafi': '6001'}

  """
  sql = '''
  CREATE TABLE IF NOT EXISTS ceps (
    cep INT PRIMARY KEY,
    logra TEXT NOT NULL,
    compl TEXT,
    bairro TEXT,
    local TEXT NOT NULL,
    uf CHAR(2) NOT NULL,
    ibge INT,
    ddd INT,
    siafi INT
  )
  '''
  conn = get_connection()
  cursor = conn.cursor()
  c = cursor.execute(sql)
  print(sql, c)
  return


def process():
  print('create_table_in_db()')
  create_table_in_db()


if __name__ == '__main__':
  process()
