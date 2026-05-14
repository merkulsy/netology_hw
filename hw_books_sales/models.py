"""
Модуль с моделями SQLAlchemy для системы учета продаж книг.
Содержит определения всех необходимых таблиц и связей между ними.
"""

from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.engine import Engine

# Создаем базовый класс для декларативного определения моделей
Base = declarative_base()


class Publisher(Base):
    """
    Модель издателя (автора).
    Хранит информацию об издателях книг.
    """
    __tablename__ = 'publisher'  # Имя таблицы в базе данных

    # Поля таблицы
    id = Column(Integer, primary_key=True)  # Уникальный идентификатор, первичный ключ
    name = Column(String, nullable=False, unique=True)  # Название издателя, обязательное поле

    # Связь с книгами (один издатель может иметь много книг)
    # back_populates указывает на обратную связь в модели Book
    books = relationship('Book', back_populates='publisher', cascade='all, delete-orphan')

    def __repr__(self):
        """Строковое представление модели для отладки"""
        return f"<Publisher(id={self.id}, name='{self.name}')>"


class Book(Base):
    """
    Модель книги.
    Хранит информацию о книгах, выпущенных издателями.
    """
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)  # Название книги
    id_publisher = Column(Integer, ForeignKey('publisher.id'), nullable=False)  # Внешний ключ к издателю

    # Связи с другими моделями
    publisher = relationship('Publisher', back_populates='books')  # Связь с издателем
    stocks = relationship('Stock', back_populates='book', cascade='all, delete-orphan')  # Связь с остатками

    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', publisher_id={self.id_publisher})>"


class Shop(Base):
    """
    Модель магазина.
    Хранит информацию о магазинах, где продаются книги.
    """
    __tablename__ = 'shop'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)  # Название магазина

    # Связь с остатками книг в магазине
    stocks = relationship('Stock', back_populates='shop', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Shop(id={self.id}, name='{self.name}')>"


class Stock(Base):
    """
    Модель остатков книг в магазинах.
    Хранит информацию о количестве конкретной книги в конкретном магазине.
    """
    __tablename__ = 'stock'

    id = Column(Integer, primary_key=True)
    id_book = Column(Integer, ForeignKey('book.id'), nullable=False)  # Внешний ключ к книге
    id_shop = Column(Integer, ForeignKey('shop.id'), nullable=False)  # Внешний ключ к магазину
    count = Column(Integer, nullable=False, default=0)  # Количество экземпляров в наличии

    # Связи с другими моделями
    book = relationship('Book', back_populates='stocks')  # Связь с книгой
    shop = relationship('Shop', back_populates='stocks')  # Связь с магазином
    sales = relationship('Sale', back_populates='stock', cascade='all, delete-orphan')  # Связь с продажами

    def __repr__(self):
        return f"<Stock(id={self.id}, book_id={self.id_book}, shop_id={self.id_shop}, count={self.count})>"


class Sale(Base):
    """
    Модель продажи.
    Хранит информацию о фактах продажи книг: дата, цена, количество.
    """
    __tablename__ = 'sale'

    id = Column(Integer, primary_key=True)
    price = Column(Numeric(10, 2), nullable=False)  # Цена продажи (с двумя знаками после запятой)
    date_sale = Column(Date, nullable=False)  # Дата продажи
    id_stock = Column(Integer, ForeignKey('stock.id'), nullable=False)  # Внешний ключ к остатку
    count = Column(Integer, nullable=False)  # Количество проданных экземпляров

    # Связь с остатком
    stock = relationship('Stock', back_populates='sales')  # Связь с остатком

    def __repr__(self):
        return f"<Sale(id={self.id}, price={self.price}, date='{self.date_sale}', count={self.count})>"


def create_tables(engine: Engine):
    """
    Функция для создания всех таблиц в базе данных.

    Args:
        engine: Движок SQLAlchemy для подключения к БД
    """
    # Создаем все таблицы, определенные в метаданных Base
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    print("Таблицы успешно созданы!")