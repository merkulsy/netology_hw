from psycopg2 import sql

def create_db(conn):
    """Создание структуры БД (таблицы)"""
    with conn.cursor() as cur:
        # Создание таблицы клиентов
        cur.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL
            );
        """)

        # Создание таблицы телефонов
        cur.execute("""
            CREATE TABLE IF NOT EXISTS phones (
                id SERIAL PRIMARY KEY,
                client_id INTEGER REFERENCES clients(id) ON DELETE CASCADE,
                phone VARCHAR(20) NOT NULL
            );
        """)

        conn.commit()


def add_client(conn, first_name, last_name, email, phones=None):
    """Добавление нового клиента"""
    with conn.cursor() as cur:
        # Проверка, существует ли клиент с таким email
        cur.execute("SELECT id FROM clients WHERE email = %s", (email,))
        if cur.fetchone():
            print(f"Клиент с email {email} уже существует")
            return None

        # Добавление клиента
        cur.execute("""
            INSERT INTO clients (first_name, last_name, email)
            VALUES (%s, %s, %s) RETURNING id
        """, (first_name, last_name, email))
        client_id = cur.fetchone()[0]

        # Добавление телефонов, если они есть
        if phones:
            for phone in phones:
                add_phone(conn, client_id, phone)

        conn.commit()
        print(f"Клиент {first_name} {last_name} добавлен с ID: {client_id}")
        return client_id


def add_phone(conn, client_id, phone):
    """Добавление телефона для существующего клиента"""
    with conn.cursor() as cur:
        # Проверка существования клиента
        cur.execute("SELECT id FROM clients WHERE id = %s", (client_id,))
        if not cur.fetchone():
            print(f"Клиент с ID {client_id} не найден")
            return False

        # Проверка, не существует ли уже такой телефон у клиента
        cur.execute("""
            SELECT id FROM phones 
            WHERE client_id = %s AND phone = %s
        """, (client_id, phone))
        if cur.fetchone():
            print(f"Телефон {phone} уже существует у клиента")
            return False

        # Добавление телефона
        cur.execute("""
            INSERT INTO phones (client_id, phone)
            VALUES (%s, %s)
        """, (client_id, phone))
        conn.commit()
        print(f"Телефон {phone} добавлен клиенту с ID {client_id}")
        return True


def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
    """Изменение данных о клиенте"""
    with conn.cursor() as cur:
        # Проверка существования клиента
        cur.execute("SELECT * FROM clients WHERE id = %s", (client_id,))
        if not cur.fetchone():
            print(f"Клиент с ID {client_id} не найден")
            return False

        # Формирование запроса на обновление
        updates = []
        params = []

        if first_name:
            updates.append("first_name = %s")
            params.append(first_name)
        if last_name:
            updates.append("last_name = %s")
            params.append(last_name)
        if email:
            # Проверка уникальности email
            cur.execute("SELECT id FROM clients WHERE email = %s AND id != %s", (email, client_id))
            if cur.fetchone():
                print(f"Email {email} уже используется другим клиентом")
                return False
            updates.append("email = %s")
            params.append(email)

        if updates:
            params.append(client_id)
            query = sql.SQL("UPDATE clients SET {} WHERE id = %s").format(
                sql.SQL(', ').join(map(sql.SQL, updates))
            )
            cur.execute(query, params)

        # Обновление телефонов, если указаны
        if phones is not None:
            # Удаляем старые телефоны
            cur.execute("DELETE FROM phones WHERE client_id = %s", (client_id,))
            # Добавляем новые
            for phone in phones:
                add_phone(conn, client_id, phone)

        conn.commit()
        print(f"Данные клиента с ID {client_id} обновлены")
        return True


def delete_phone(conn, client_id, phone):
    """Удаление телефона для существующего клиента"""
    with conn.cursor() as cur:
        # Проверка существования клиента
        cur.execute("SELECT id FROM clients WHERE id = %s", (client_id,))
        if not cur.fetchone():
            print(f"Клиент с ID {client_id} не найден")
            return False

        # Удаление телефона
        cur.execute("""
            DELETE FROM phones 
            WHERE client_id = %s AND phone = %s
        """, (client_id, phone))

        if cur.rowcount == 0:
            print(f"Телефон {phone} не найден у клиента с ID {client_id}")
            return False

        conn.commit()
        print(f"Телефон {phone} удален у клиента с ID {client_id}")
        return True


def delete_client(conn, client_id):
    """Удаление существующего клиента"""
    with conn.cursor() as cur:
        # Проверка существования клиента
        cur.execute("SELECT id FROM clients WHERE id = %s", (client_id,))
        if not cur.fetchone():
            print(f"Клиент с ID {client_id} не найден")
            return False

        # Удаление клиента (телефоны удалятся автоматически из-за ON DELETE CASCADE)
        cur.execute("DELETE FROM clients WHERE id = %s", (client_id,))
        conn.commit()
        print(f"Клиент с ID {client_id} удален")
        return True


def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    """Поиск клиента по его данным"""
    with conn.cursor() as cur:
        conditions = []
        params = []

        if first_name:
            conditions.append("c.first_name ILIKE %s")
            params.append(f"%{first_name}%")
        if last_name:
            conditions.append("c.last_name ILIKE %s")
            params.append(f"%{last_name}%")
        if email:
            conditions.append("c.email ILIKE %s")
            params.append(f"%{email}%")
        if phone:
            conditions.append("p.phone = %s")
            params.append(phone)

        if not conditions:
            print("Не указаны критерии поиска")
            return []

        query = """
            SELECT DISTINCT c.id, c.first_name, c.last_name, c.email, 
                   ARRAY_AGG(DISTINCT p.phone) as phones
            FROM clients c
            LEFT JOIN phones p ON c.id = p.client_id
        """

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " GROUP BY c.id, c.first_name, c.last_name, c.email ORDER BY c.id"

        cur.execute(query, params)
        results = cur.fetchall()

        if not results:
            print("Клиенты не найдены")
            return []

        # Форматирование результатов
        clients = []
        for row in results:
            client = {
                'id': row[0],
                'first_name': row[1],
                'last_name': row[2],
                'email': row[3],
                'phones': [p for p in row[4] if p] if row[4] else []
            }
            clients.append(client)

        return clients


# Дополнительная функция для просмотра всех клиентов
def get_all_clients(conn):
    """Получение всех клиентов"""
    with conn.cursor() as cur:
        cur.execute("""
            SELECT c.id, c.first_name, c.last_name, c.email, 
                   ARRAY_AGG(DISTINCT p.phone) as phones
            FROM clients c
            LEFT JOIN phones p ON c.id = p.client_id
            GROUP BY c.id, c.first_name, c.last_name, c.email
            ORDER BY c.id
        """)
        results = cur.fetchall()

        clients = []
        for row in results:
            client = {
                'id': row[0],
                'first_name': row[1],
                'last_name': row[2],
                'email': row[3],
                'phones': [p for p in row[4] if p] if row[4] else []
            }
            clients.append(client)

        return clients


def print_client_info(client):
    """Вывод информации о клиенте"""
    print(f"ID: {client['id']}")
    print(f"Имя: {client['first_name']}")
    print(f"Фамилия: {client['last_name']}")
    print(f"Email: {client['email']}")
    phones_str = ', '.join(client['phones']) if client['phones'] else 'нет'
    print(f"Телефоны: {phones_str}")
    print("-" * 40)
import psycopg2

def main():
    # Параметры подключения к БД
    conn_params = {
        "database": "clients_db",
        "user": "sveta",
        "password": ""
    }

    try:
        with psycopg2.connect(**conn_params) as conn:
            print("Подключение к БД установлено\n")

            print("1. Создание таблиц")
            create_db(conn)
            print("Таблицы созданы\n")

            print("2. Добавление клиентов")
            add_client(conn, "Иван", "Иванов", "ivan@example.com", ["+7(123)456-78-90"])
            add_client(conn, "Мария", "Петрова", "maria@example.com", ["+7(234)567-89-01", "+7(345)678-90-12"])
            add_client(conn, "Алексей", "Сидоров", "alex@example.com", None)  # Без телефона
            print()

            print("3. Все клиенты до изменений:")
            all_clients = get_all_clients(conn)
            for client in all_clients:
                print_client_info(client)

            print("4. Добавление телефона существующему клиенту")
            add_phone(conn, 1, "+7(456)789-01-23")
            add_phone(conn, 3, "+7(567)890-12-34")
            print()

            print("5. Изменение данных клиента")
            change_client(conn, 2, first_name="Мария", last_name="Иванова",
                          email="maria.ivanova@example.com", phones=["+7(999)123-45-67"])
            print()

            print("6. Поиск клиентов")

            print("Поиск по имени 'Иван':")
            results = find_client(conn, first_name="Иван")
            for client in results:
                print_client_info(client)

            print("Поиск по телефону '+7(567)890-12-34':")
            results = find_client(conn, phone="+7(567)890-12-34")
            for client in results:
                print_client_info(client)

            print("Поиск по email 'maria.ivanova@example.com':")
            results = find_client(conn, email="maria.ivanova@example.com")
            for client in results:
                print_client_info(client)
            print()

            print("7. Удаление телефона")
            delete_phone(conn, 1, "+7(123)456-78-90")
            print()

            print("8. Все клиенты после изменений:")
            all_clients = get_all_clients(conn)
            for client in all_clients:
                print_client_info(client)

            print("9. Удаление клиента")
            delete_client(conn, 3)
            print()

            print("10. Финальный список клиентов:")
            all_clients = get_all_clients(conn)
            for client in all_clients:
                print_client_info(client)

            print("Демонстрация всех функций завершена")

    except psycopg2.Error as e:
        print(f"Ошибка при работе с БД: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()