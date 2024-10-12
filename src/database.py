import sqlite3

# Функция для создания базы данных и таблицы клиентов
def create_client_table():
    conn = sqlite3.connect('pizzeria.db')  # Подключение к базе данных
    cursor = conn.cursor()

    # Создание таблицы клиентов, если она еще не существует
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            phone TEXT NOT NULL UNIQUE,
            address TEXT NOT NULL
        )
    ''')

    conn.commit()  # Сохраняем изменения
    conn.close()   # Закрываем соединение

# Функция для добавления нового клиента
def add_new_client(first_name, last_name, phone, address):
    conn = sqlite3.connect('pizzeria.db')  # Подключение к базе данных
    cursor = conn.cursor()

    # Вставка данных нового клиента
    cursor.execute('''
        INSERT INTO clients (first_name, last_name, phone, address)
        VALUES (?, ?, ?, ?)
    ''', (first_name, last_name, phone, address))

    conn.commit()  # Сохраняем изменения
    conn.close()   # Закрываем соединение

# Функция для поиска клиента по номеру телефона
def find_client_by_phone(phone):
    conn = sqlite3.connect('pizzeria.db')  # Подключение к базе данных
    cursor = conn.cursor()

    # Поиск клиента по номеру телефона
    cursor.execute('SELECT * FROM clients WHERE phone = ?', (phone,))
    client = cursor.fetchone()  # Получаем первую найденную строку

    conn.close()  # Закрываем соединение
    return client  # Возвращаем найденного клиента (или None, если клиент не найден)
