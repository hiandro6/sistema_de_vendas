from sqlalchemy import create_engine,text
from sqlalchemy.orm import Session

from database import Base


engine = create_engine('sqlite:///database/teste.db')
session = Session(bind=engine)
