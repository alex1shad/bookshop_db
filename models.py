import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class Publisher(Base):
    __tablename__ = 'publisher'

    publisher_id = sq.Column(sq.Integer, primary_key=True)
    publisher_name = sq.Column(sq.String(length=30), unique=True, nullable=False)


class Book(Base):
    __tablename__ = 'book'

    book_id = sq.Column(sq.Integer, primary_key=True)
    book_title = sq.Column(sq.String(length=100), nullable=False)
    publisher_id = sq.Column(sq.Integer, sq.ForeignKey('publisher.publisher_id'), nullable=False)

    publisher_relation = relationship(Publisher, backref='book')


class Shop(Base):
    __tablename__ = 'shop'

    shop_id = sq.Column(sq.Integer, primary_key=True)
    shop_name = sq.Column(sq.String(length=30), unique=True, nullable=False)


class Stock(Base):
    __tablename__ = 'stock'

    stock_id = sq.Column(sq.Integer, primary_key=True)
    book_id = sq.Column(sq.Integer, sq.ForeignKey('book.book_id'), nullable=False)
    shop_id = sq.Column(sq.Integer, sq.ForeignKey('shop.shop_id'), nullable=False)
    book_count = sq.Column(sq.Integer, nullable=False)

    book_relation = relationship(Book, backref='stock')
    shop_relation = relationship(Shop, backref='stock')


class Sale(Base):
    __tablename__ = 'sale'

    sale_id = sq.Column(sq.Integer, primary_key=True)
    book_price = sq.Column(sq.Float, nullable=False)
    date_sale = sq.Column(sq.DateTime, nullable=False)
    stock_id = sq.Column(sq.Integer, sq.ForeignKey('stock.stock_id'), nullable=False)
    sale_count = sq.Column(sq.Integer, nullable=False)

    stock_relation = relationship(Stock, backref='sale')


def create_table(engine):
    Base.metadata.create_all(engine)
