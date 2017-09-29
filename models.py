from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, VARCHAR, DECIMAL, DATE

Base = declarative_base()

class Person(Base):
    __tablename__ = 'person'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(VARCHAR(250), nullable=False)
    salary = Column(DECIMAL(10,2), nullable=False)
    birthday = Column(String, nullable=False)

    def __repr__(self):
        return "<Person(id='%d', name='%s')>" % (self.id, self.name)

