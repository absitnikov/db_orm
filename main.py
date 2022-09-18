import json

import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models import create_tables, Publisher, Shop, Book, Stock, Sale


DSN = 'postgresql://postgres: @localhost:5432/db_orm'
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)


Session = sessionmaker(bind=engine)
session = Session()

with open('fixtures/tests_data.json', 'r') as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()


print('enter the publisher id number or name:')
name = input()
if name.isdigit():
    publisher_name = int(name)
    for c in session.query(Publisher).filter(Publisher.id == publisher_name).all():
        print(c)
else:
    for c in session.query(Publisher).filter(Publisher.name == name).all():
        print(c)

if name.isdigit():
    for c in session.query(Shop).join(Stock, Shop.id == Stock.id_shop).join(Book, Book.id == Stock.id_book)\
        .join(Publisher, Publisher.id == Book.id_publisher).\
        filter(Publisher.id == f'{name}').all():
        print(f"Shop {c} sells the publisher's books {name}")
else:
    for c in session.query(Shop).join(Stock, Shop.id == Stock.id_shop).join(Book, Book.id == Stock.id_book)\
        .join(Publisher, Publisher.id == Book.id_publisher).\
        filter(Publisher.name.like(f"{name}")).all():
        print(f"Shop {c} sells the publisher's books {name}")

session.close()

