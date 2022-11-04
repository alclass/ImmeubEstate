#!/usr/bin/env python3
"""
sqlite_cep_functions.py

In SQLite rowid is an implicit autoincrement integer field (having values 1, 2, 3...)

"""
import settings_pathfinder as sp
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


def get_engine():
  sqlite_filepath = sp.AppPaths.get_sqlite_datafile_abspath()
  engine = create_engine('sqlite:///'+sqlite_filepath)
  return engine

def get_session():
  sessionmade = sessionmaker(bind=get_engine())
  session = sessionmade()
  return session

class Cep(Base):
  __tablename__ = 'ceps'
  rowid = Column(Integer)
  cep = Column(Integer, primary_key=True)
  logra = Column(String)
  compl = Column(String, nullable=True)
  bairro = Column(String, nullable=True)
  local = Column(String)
  uf = Column(String(2))
  ibge = Column(Integer, nullable=True)
  ddd = Column(Integer, nullable=True)
  siafi = Column(Integer, nullable=True)

  @property
  def cep_formatted(self):
    cepf = str(self.cep)
    if len(cepf) < 4:
      return cepf
    cepf = cepf[:-3] + '-' + cepf[-3:]
    return cepf

  def __repr__(self):
    return 'cep ' + self.cep_formatted


def example_query():
  engine = get_engine()
  sessionmade = sessionmaker(bind=engine)
  session = sessionmade()
  query = session.query(Cep)
  instance = query.first()
  print(instance)


def process():
  print('example_query()')
  example_query()


if __name__ == '__main__':
  process()
