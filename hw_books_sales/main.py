"""
Основной скрипт для работы с системой учета продаж книг.
Обеспечивает загрузку тестовых данных и выполнение запросов к базе.
"""

import json
import os
from typing import Optional
from datetime import datetime

import sqlalchemy
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine

from models import create_tables, Publisher, Shop, Book, Stock, Sale

# Конфигурация подключения к базе данных
# Для PostgreSQL:
DSN = "postgresql://sveta:@localhost:5432/books_sales_db"

# Движок для подключения к БД
engine = create_engine(DSN, echo=False)  # echo=True для отладки SQL-запросов


def load_fixtures(session: Session, fixtures_file: str = 'fixtures/tests_data.json'):
    """
    Загружает тестовые данные из JSON-файла в базу данных.

    Args:
        session: Сессия SQLAlchemy для работы с БД
        fixtures_file: Путь к JSON-файлу с тестовыми данными
    """
    # Проверяем существует ли файл
    if not os.path.exists(fixtures_file):
        print(f"Файл {fixtures_file} не найден. Пропускаем загрузку тестовых данных.")
        return

    # Открываем и читаем JSON-файл
    with open(fixtures_file, 'r', encoding='utf-8') as fd:
        data = json.load(fd)

    # Словарь для сопоставления имени модели с классом модели
    model_mapping = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }

    # Перебираем все записи в JSON-файле
    for record in data:
        # Получаем класс модели по имени из поля 'model'
        model_class = model_mapping.get(record.get('model'))

        if model_class is None:
            print(f"Неизвестная модель: {record.get('model')}")
            continue

        # Создаем экземпляр модели
        # id берем из поля 'pk', остальные поля - из 'fields'
        instance = model_class(id=record.get('pk'), **record.get('fields'))
        session.add(instance)

    # Сохраняем все изменения в базе данных
    session.commit()
    print(f"Загружено {len(data)} записей из {fixtures_file}")


def find_publisher(session: Session, publisher_input: str) -> Optional[Publisher]:
    """
    Находит издателя по имени или ID.

    Args:
        session: Сессия SQLAlchemy
        publisher_input: Строка с именем или ID издателя

    Returns:
        Объект Publisher или None, если не найден
    """
    # Пробуем интерпретировать ввод как ID (целое число)
    if publisher_input.isdigit():
        # Поиск по ID
        publisher = session.query(Publisher).filter(Publisher.id == int(publisher_input)).first()
        if publisher:
            return publisher
        print(f"Издатель с ID {publisher_input} не найден.")
        return None
    else:
        # Поиск по имени (регистронезависимый)
        publishers = session.query(Publisher).filter(
            Publisher.name.ilike(f"%{publisher_input}%")
        ).all()

        if len(publishers) == 0:
            print(f"Издатель '{publisher_input}' не найден.")
            return None
        elif len(publishers) > 1:
            print(f"Найдено несколько издателей по запросу '{publisher_input}':")
            for p in publishers:
                print(f"  - ID: {p.id}, Имя: {p.name}")
            print("Пожалуйста, уточните запрос, используя ID издателя.")
            return None
        else:
            return publishers[0]


def get_publisher_sales(session: Session, publisher: Publisher):
    """
    Получает и выводит все продажи книг указанного издателя.

    Args:
        session: Сессия SQLAlchemy
        publisher: Объект издателя
    """
    # Выполняем сложный JOIN-запрос для получения всех продаж книг издателя
    # Путь: Sale -> Stock -> Book -> Publisher
    #       Sale -> Stock -> Shop
    results = session.query(
        Book.title,  # Название книги
        Shop.name,  # Название магазина
        Sale.price,  # Цена продажи
        Sale.date_sale,  # Дата продажи
        Sale.count  # Количество проданных экземпляров
    ).select_from(Sale) \
        .join(Stock, Stock.id == Sale.id_stock) \
        .join(Book, Book.id == Stock.id_book) \
        .join(Shop, Shop.id == Stock.id_shop) \
        .join(Publisher, Publisher.id == Book.id_publisher) \
        .filter(Publisher.id == publisher.id) \
        .order_by(Sale.date_sale.desc())  # Сортируем по дате (новые сверху)

    # Выводим результаты
    print(f"\nПродажи книг издателя '{publisher.name}':")
    print("-" * 80)
    print(f"{'Название книги':<30} | {'Магазин':<15} | {'Цена':<8} | {'Дата':<12} | {'Кол-во':<6}")
    print("-" * 80)

    found = False
    for title, shop_name, price, date_sale, count in results:
        found = True
        # Форматируем дату в удобный формат (день-месяц-год)
        if isinstance(date_sale, datetime):
            date_str = date_sale.strftime('%d-%m-%Y')
        else:
            date_str = str(date_sale)

        print(f"{title:<30} | {shop_name:<15} | {price:>8.2f} | {date_str:<12} | {count:<6}")

    if not found:
        print("Продажи не найдены.")

    print("-" * 80)


def main():
    """
    Основная функция приложения.
    """
    print("=== Система учета продаж книг ===\n")

    # Создаем таблицы в базе данных (если их нет)
    create_tables(engine)

    # Создаем фабрику сессий
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Загружаем тестовые данные из fixtures
        load_fixtures(session)

        # Запрашиваем у пользователя имя или ID издателя
        while True:
            publisher_input = input("\nВведите имя или ID издателя (или 'exit' для выхода): ").strip()

            if publisher_input.lower() == 'exit':
                print("До свидания!")
                break

            if not publisher_input:
                print("Пожалуйста, введите имя или ID издателя.")
                continue

            # Находим издателя
            publisher = find_publisher(session, publisher_input)

            if publisher:
                # Выводим все продажи найденного издателя
                get_publisher_sales(session, publisher)

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        session.rollback()
    finally:
        # Закрываем сессию
        session.close()


if __name__ == '__main__':
    main()