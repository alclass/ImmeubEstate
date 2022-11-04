# coding=utf-8

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import settings_pathfinder as settpath

main_sqlitefile_abspath = settpath.AppPaths.get_mainsqlitefile_abspath()

engine = create_engine('sqlite://' + main_sqlitefile_abspath)
Session = sessionmaker(bind=engine)

Base = declarative_base()
