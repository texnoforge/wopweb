from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from wopweb.db import Base


class Alphabet(Base):
    __tablename__ = 'abc'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    handle = Column(String, unique=True)

    symbols = relationship("Symbol", back_populates='abc')

    def __init__(self, name, handle):
        self.name = name
        self.handle = handle

    def __repr__(self):
        return f'<Alphabet {self.name!r}>'


class Symbol(Base):
    __tablename__ = 'symbol'
    id = Column(Integer, primary_key=True)
    meaning = Column(String)
    name = Column(String)
    handle = Column(String)
    abc_id = Column(Integer, ForeignKey('abc.id'))

    abc = relationship("Alphabet")

    def __init__(self, meaning, name, handle, abc=None):
        self.meaning = meaning
        self.name = name
        self.handle = handle
        self.abc = abc

    def __repr__(self):
        return f'<Symbol {self.name!r}/{self.meaning!r}>'
