#!/usr/bin/env python3
"""
sqlite_cep_functions.py

In SQLite rowid is an implicit autoincrement integer field (having values 1, 2, 3...)

"""
import settings_pathfinder as sp
from sqlalchemy import Table, MetaData, Column, Integer, String, create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

sqlite_filepath = sp.AppPaths.get_sqlite_datafile_abspath()
engine = create_engine('sqlite:///'+sqlite_filepath)
metadata = MetaData()
ceptable = Table(
  "ceps", metadata,
  Column('rowid', Integer),
  Column('cep', Integer),
  Column('logra', String),
  Column('compl', String, nullable=True),
  Column('bairro', String, nullable=True),
  Column('local', String),
  Column('uf', String(2)),
  Column('ibge', Integer),
  Column('ddd', Integer),
  Column('siafi', Integer)
)

# ceptable.create(bind=engine)

stmt = select([ceptable.c.cep])
ceprec, = engine.execute(stmt).fetchone()
print('cep', ceprec)


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


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

query = session.query(Cep)
instance = query.first()
print(instance)
