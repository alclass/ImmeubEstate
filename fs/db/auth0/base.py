# coding=utf-8

str_creat_tabl_actors = '''
CREATE TABLE `actors` (
	`id`	INTEGER,
	`name`	TEXT,
	`birthday`	TEXT,
	PRIMARY KEY(`id`)
);
'''

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///auth0.sqlite')
Session = sessionmaker(bind=engine)

Base = declarative_base()