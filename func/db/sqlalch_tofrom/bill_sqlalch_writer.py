# coding=utf-8

from sqlalchemy import Column, String, Date, Boolean, TIMESTAMP
import json

from func.db import json_tofrom as sqlalchbase
import func.datefs.datebillfunctions as dtbill
import func.datefs.date_functions as dtfunc
import models.billing_items as bimod
'''
movies_actors_association = Table(
  'movies_actors', Base.metadata,
  Column('movie_id', Integer, ForeignKey('movies.id')),
  Column('actor_id', Integer, ForeignKey('actors.id'))
)
'''

class BillSqlAlch(sqlalchbase.Base):
  __tablename__ = 'bills'

  # id = Column(Integer, primary_key=True)
  # contract = relationship("Contract", backref="contract")
  bill_id = Column(String, primary_key=True)
  # contract_id = Column(Integer)
  contract5char = Column(String, nullable=False)
  refmonthdate = Column(Date, nullable=False)
  duedate = Column(Date)
  is_closed = Column(Boolean, default=False)
  billing_items_json = Column(String, default='')
  created_at = Column(TIMESTAMP)
  modified_at = Column(TIMESTAMP)
  # actors = relationship("Actor", secondary=movies_actors_association)

  def form_bill_id(self):
    refmonthdatestr = dtfunc.transform_date_to_8char(self.refmonthdate)
    return refmonthdatestr + self.contract5char

  def __init__(self, contract5char, refmonthdate, duedate, billing_items_json):
    self.contract5char = contract5char
    self.refmonthdate = refmonthdate
    self.bill_id = self.form_bill_id()
    self.duedate = duedate
    self.billing_items_json = billing_items_json

  def str_as_lines(self):
    lines = []
    line = 'Bill (from SqlAlchemy)'
    lines.append(line)
    line = 'Bill id %s' %self.bill_id
    lines.append(line)
    line = 'refmonthdate: ' + str(self.refmonthdate)
    lines.append(line)
    line = 'duedate: ' + str(self.duedate)
    lines.append(line)
    line = 'billing_items_json: ' + self.billing_items_json
    lines.append(line)
    return lines

  def __str__(self):
    return '\n'.join(self.str_as_lines())

def massdata():
  refmonthdatestr = '2019-07-01'
  duedatestr = '2019-09-10'
  contract5char = 'CDT02'
  billing_items_dictlist = [
    {
      'itdatetime': refmonthdatestr,
      'ittype': bimod.BillingItemTypes.K_IBALANCE,
      'description': bimod.BillingItemTypes.get_short_description(bimod.BillingItemTypes.K_IBALANCE),
      'itvalue': 1000,
      'itobs1': None,
      'itobs2': None,
      'is_inmonth': False,
    }, ],
  bill_id = dtbill.join_strdate_n_contractid_into_billid(refmonthdatestr, contract5char)
  contracts_monthly_bills_dict = {}
  contracts_monthly_bills_dict[bill_id] = {
    'bill_id'     : bill_id,
    'contract_id' : contract5char,
    'refmonthdate': refmonthdatestr,
    'duedate'     : duedatestr,
    'is_closed'   : False,  # open_or_closed
    'ini_balance' : 0,
    'total_when_open' : 2922.24,
    'total_paid'      : 2922.24,
    'incidence_value' : None,
    'fin_balance'     : 0,
    'billing_items_dictlist': billing_items_dictlist,
  }

  billing_items_json = json.dumps(billing_items_dictlist, ensure_ascii=False)
  print ('billing_items_str', billing_items_json)
  refmonthdate = dtfunc.transform_datestr_to_date(refmonthdatestr)
  duedate = dtfunc.transform_datestr_to_date(duedatestr)
  session = sqlalchbase.Session()
  contract_id = 7
  bill_rec = BillSqlAlch(
    contract5char, refmonthdate, duedate, billing_items_json
  )
  session.add(bill_rec)
  print ('saving bill')
  # 10 - commit and close session
  session.commit()
  session.close()

def write_to_sqlalch():
  print ('In write_to_sqlalch()')
  massdata()

def read_from_sqlalch():
  session = sqlalchbase.Session()
  all = session.query(BillSqlAlch).all()
  for i, o in enumerate(all):
    print(i, '=>', o)
  print('final', i, 'len', len(all))

  #BillSqlAlch.query.delete()
  #session.query(BillSqlAlch).delete()
  #session.commit()


def process():
  write_to_sqlalch()
  read_from_sqlalch()


if __name__ == '__main__':
  process()
