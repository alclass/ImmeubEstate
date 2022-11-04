# coding=utf-8
import sqlite3

def create_table_bills():
  print('create_table_bills()')
  dbname = 'billsregister.sqlite'
  conn = sqlite3.connect(dbname)
  print('openned connection to', dbname)
  c = conn.cursor()
  str_creat_tabl_bills = '''
  CREATE TABLE `bills` (
    `bill_id`	TEXT,
    `contract5char`	TEXT,
    `refmonthdate`	TEXT,
    `duedate`	TEXT,
    `is_closed`	INTEGER,
    `billing_items_json`	TEXT,
    `created_at`	TEXT,
    `modified_at`	TEXT,
    PRIMARY KEY(`bill_id`)
  )
  '''
  c.execute(str_creat_tabl_bills)
  conn.commit()
  conn.close()
  print('FINISHED:', str_creat_tabl_bills)

def process():
  create_table_bills()

if __name__ == '__main__':
  process()



