import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class Publisher(Base):
    __tablename__ = 'publisher'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.VARCHAR(60), nullable=False)

    def __str__(self):
        return f"(id: {self.id}, name: {self.name})"


class Book(Base):
    __tablename__ = 'book'

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.VARCHAR(100), nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey('publisher.id'), nullable=False)

    publisher = relationship(Publisher, backref="books")

    def __str__(self):
        return f"(id: {self.id}, title: {self.title}, id_publisher: {self.publisher})"


class Shop(Base):
    __tablename__ = 'shop'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.VARCHAR(100), nullable=False)

    def __str__(self):
        return f"(id: {self.id}, name: {self.name})"


class Stock(Base):
    __tablename__ = 'stock'

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey('book.id'), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('shop.id'), nullable=False)
    count = sq.Column(sq.Integer)

    book = relationship(Book, backref="stock_book")
    shop = relationship(Shop, backref="stock_shop")

    def __str__(self):
        return f"(id: {self.id}, id_book: {self.book}," \
               f"id_shop: {self.shop}, count: {self.count})"


class Sale(Base):
    __tablename__ = 'sale'

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.DECIMAL(6, 2), nullable=False)
    date_sale = sq.Column(sq.DateTime)
    count = sq.Column(sq.Integer, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('stock.id'), nullable=False)

    stock = relationship(Stock, backref="sales")

    def __str__(self):
        return f"(id: {self.id}, price: {self.price}, date_sale: {self.date_sale}," \
               f"id_stock: {self.stock}, count: {self.count})"


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)