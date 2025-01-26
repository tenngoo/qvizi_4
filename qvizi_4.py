# 1

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import declarative_base, relationship, Session

baza = declarative_base()

class WvdobisBarati(baza):
    __tablename__ = 'wvdobis_baratebi'

    id = Column(Integer, primary_key=True)
    baratis_nomeri = Column(String, unique=True, nullable=False)
    gamoSvleba_tarigi = Column(Date, nullable=False)

    def __repr__(self):
        return f"<WvdobisBarati(baratis_nomeri='{self.baratis_nomeri}', gamoSvleba_tarigi='{self.gamoSvleba_tarigi}')>"

class Tanamshromeli(baza):
    __tablename__ = 'tanamshromlebi'

    id = Column(Integer, primary_key=True)
    saxeli = Column(String, nullable=False)
    wvdobis_barati_id = Column(Integer, ForeignKey('wvdobis_baratebi.id'), unique=True)

    wvdobis_barati = relationship("WvdobisBarati", backref="tanamshromeli")

    def __repr__(self):
        return f"<Tanamshromeli(saxeli='{self.saxeli}', wvdobis_barati_id='{self.wvdobis_barati_id}')>"

engine = create_engine('sqlite:///:memory:')
baza.metadata.create_all(engine)

from datetime import date

def monacemebis_sheqmna():
    sesia = Session(engine)

    barati1 = WvdobisBarati(baratis_nomeri='Card-001', gamoSvleba_tarigi=date(2025, 1, 1))
    barati2 = WvdobisBarati(baratis_nomeri='Card-002', gamoSvleba_tarigi=date(2025, 1, 2))

    tanamshromeli1 = Tanamshromeli(saxeli='Alice', wvdobis_barati=barati1)
    tanamshromeli2 = Tanamshromeli(saxeli='Bob', wvdobis_barati=barati2)

    sesia.add_all([barati1, barati2, tanamshromeli1, tanamshromeli2])
    sesia.commit()
    sesia.close()

monacemebis_sheqmna()

with Session(engine) as sesia:
    tanamshromlebi = sesia.query(Tanamshromeli).all()
    for tanamshromeli in tanamshromlebi:
        print(f"Tanamshromeli: {tanamshromeli.saxeli}, Baratis Nomeri: {tanamshromeli.wvdobis_barati.baratis_nomeri}")

    baratis_nomeri = 'Card-001'
    barati = sesia.query(WvdobisBarati).filter_by(baratis_nomeri=baratis_nomeri).first()
    if barati and barati.tanamshromeli:
        print(f"Baratis Nomeri: {barati.baratis_nomeri} ekutvnis Tanamshromels: {barati.tanamshromeli.saxeli}")

# 2
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, Session

baza = declarative_base()

class MagaziisSeqcia(baza):
    __tablename__ = 'magaziis_seqciebi'

    id = Column(Integer, primary_key=True)
    saxeli = Column(String, nullable=False)

    produqtebi = relationship("Produqti", backref="seqcia")

    def __repr__(self):
        return f"<MagaziisSeqcia(saxeli='{self.saxeli}')>"

class Produqti(baza):
    __tablename__ = 'produqtebi'

    id = Column(Integer, primary_key=True)
    saxeli = Column(String, nullable=False)
    seqcia_id = Column(Integer, ForeignKey('magaziis_seqciebi.id'))

    def __repr__(self):
        return f"<Produqti(saxeli='{self.saxeli}', seqcia_id='{self.seqcia_id}')>"

engine = create_engine('sqlite:///:memory:')
baza.metadata.create_all(engine)

def monacemebis_sheqmna():
    sesia = Session(engine)

    seqcia1 = MagaziisSeqcia(saxeli='Electronics')
    seqcia2 = MagaziisSeqcia(saxeli='Groceries')

    produqti1 = Produqti(saxeli='TV', seqcia=seqcia1)
    produqti2 = Produqti(saxeli='Laptop', seqcia=seqcia1)
    produqti3 = Produqti(saxeli='Apples', seqcia=seqcia2)
    produqti4 = Produqti(saxeli='Milk', seqcia=seqcia2)

    sesia.add_all([seqcia1, seqcia2, produqti1, produqti2, produqti3, produqti4])
    sesia.commit()
    sesia.close()

monacemebis_sheqmna()

with Session(engine) as sesia:
    seqciebi = sesia.query(MagaziisSeqcia).all()
    for seqcia in seqciebi:
        print(f"Seqcia: {seqcia.saxeli}, Produqtebi: {[produqti.saxeli for produqti in seqcia.produqtebi]}")

    produqtis_saxeli = 'TV'
    produqti = sesia.query(Produqti).filter_by(saxeli=produqtis_saxeli).first()
    if produqti and produqti.seqcia:
        print(f"Produqti: {produqti.saxeli} ekutvnis Seqcias: {produqti.seqcia.saxeli}")


# 3

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship, Session

baza = declarative_base()

employee_project = Table(
    'employee_project', baza.metadata,
    Column('employee_id', Integer, ForeignKey('tanamshromlebi.id')),
    Column('project_id', Integer, ForeignKey('proeqtebi.id'))
)

class Tanamshromeli(baza):
    __tablename__ = 'tanamshromlebi'

    id = Column(Integer, primary_key=True)
    saxeli = Column(String, nullable=False)

    proeqtebi = relationship("Proeqti", secondary=employee_project, back_populates="tanamshromlebi")

    def __repr__(self):
        return f"<Tanamshromeli(saxeli='{self.saxeli}')>"

class Proeqti(baza):
    __tablename__ = 'proeqtebi'

    id = Column(Integer, primary_key=True)
    saxeli = Column(String, nullable=False)

    tanamshromlebi = relationship("Tanamshromeli", secondary=employee_project, back_populates="proeqtebi")

    def __repr__(self):
        return f"<Proeqti(saxeli='{self.saxeli}')>"

engine = create_engine('sqlite:///:memory:')
baza.metadata.create_all(engine)

def monacemebis_sheqmna():
    sesia = Session(engine)

    tanamshromeli1 = Tanamshromeli(saxeli='Alice')
    tanamshromeli2 = Tanamshromeli(saxeli='Bob')
    tanamshromeli3 = Tanamshromeli(saxeli='Charlie')

    proeqti1 = Proeqti(saxeli='Website Redesign')
    proeqti2 = Proeqti(saxeli='Marketing Campaign')

    tanamshromeli1.proeqtebi.extend([proeqti1, proeqti2])
    tanamshromeli2.proeqtebi.append(proeqti1)
    tanamshromeli3.proeqtebi.append(proeqti2)

    sesia.add_all([tanamshromeli1, tanamshromeli2, tanamshromeli3, proeqti1, proeqti2])
    sesia.commit()
    sesia.close()

monacemebis_sheqmna()

with Session(engine) as sesia:
    proeqtebi = sesia.query(Proeqti).all()
    for proeqti in proeqtebi:
        print(f"Proeqti: {proeqti.saxeli}, Tanamshromlebi: {[tanamshromeli.saxeli for tanamshromeli in proeqti.tanamshromlebi]}")

    tanamshromlis_saxeli = 'Alice'
    tanamshromeli = sesia.query(Tanamshromeli).filter_by(saxeli=tanamshromlis_saxeli).first()
    if tanamshromeli:
        print(f"Tanamshromeli: {tanamshromeli.saxeli}, Proeqtebi: {[proeqti.saxeli for proeqti in tanamshromeli.proeqtebi]}")