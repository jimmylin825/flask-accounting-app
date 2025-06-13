from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from flask_login import UserMixin

data_path = "sqlite:///database.db"
engine = create_engine(data_path)
Base = declarative_base()


class Expense(Base):
    __tablename__ = "expense"
    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable = False)
    category = Column(String, nullable = False)
    amount = Column(Integer, nullable = False)
    type =  Column(String, nullable = False)
    date = Column(DateTime, default = datetime.now)
    note = Column(String)

class User(Base, UserMixin):
    __tablename__ = "user"
    id = Column(Integer, primary_key = True)
    username = Column(String(20), unique = True, nullable = False)
    password_hash = Column(String(200), nullable = False)


Base.metadata.create_all(engine)
Session = sessionmaker(bind = engine)
