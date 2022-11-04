#!/usr/bin/env python3

import fs.datefs.date_functions as dt

from sqlalchemy import *
from sqlalchemy import create_engine

engine = create_engine('sqlite://')
from sqlalchemy import Column, Integer, Text, MetaData, Table

metadata = MetaData()
messages = Table(
    'messages', metadata,
    Column('id', Integer, primary_key=True),
    Column('message', Text),
)

messages.create(bind=engine)

insert_message = messages.insert().values(message='Hello, World!')
engine.execute(insert_message)

from sqlalchemy import select

stmt = select([messages.c.message])
message, = engine.execute(stmt).fetchone()
print(message)


from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String


class Message(Base):
  __tablename__ = 'messages'

  id = Column(Integer, primary_key=True)
  message = Column(String)

Base.metadata.create_all(engine)

message = Message(message="Hello World!")
message.message # 'Hello World!

from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

session.add(message)
session.commit()

query = session.query(Message)
instance = query.first()
print (instance.message) # Hello World!

def ptest_sqlalch(inidatestr, n_years=1):
  print('-'*50)


def process():
  pass

if __name__ == '__main__':
  process()
