##4

#4.1) Ket noi
from sqlalchemy import create_engine

engine = create_engine('sqlite:///:memory:', echo=True)

#4.2) Define and Create Tables
from sqlalchemy import Table, String, MetaData, ForeignKey, Column, Time, Integer, Float
metadata = MetaData()
TAIXE = Table(
    'TAIXE', metadata,
    Column('MATX', String, primary_key=True),
    Column('HOTEN', String),
    Column('SDT', String),
    Column('DTB', Float),
    Column('LXE', String),
)

KH = Table(
    'KH', metadata,
    Column('MAKH', String, primary_key=True),
    Column('HOTEN', String),
    Column('SDT', Integer),
)

DATXE = Table(
    'DATXE', metadata,
  Column('MADX', String, primary_key=True),
  Column('MAKH', None, ForeignKey('KH.MAKH')),
  Column('DDI', String),
  Column('DDEN', String),
  Column('LXE', String),
  Column('GIA', Integer),
  Column('TGDAT', Time),
)

DOIXE = Table(
    'DOIXE', metadata,
  Column('MADX', None, ForeignKey('DATXE.MADX'), primary_key=True),
  Column('MATX', None, ForeignKey('TAIXE.MATX'), primary_key=True),
  Column('TGBDAU', Time),
  Column('TGKTHUC', Time),
  Column('KQUA', String),
)

CHUYENDI = Table(
    'CHUYENDI', metadata,
  Column('MACD', String, ),
  Column('MADX', None, ForeignKey('DATXE.MADX')),
  Column('MATX', None, ForeignKey('TAIXE.MATX')),
  Column('TGDI', Time),
  Column('TGDEN', Time),
  Column('GIA', Integer),
  Column('HTTTOAN', String),
  Column('DIEM', Integer),
)

metadata.create_all(engine)