import sqlite3

def init_db():
    # Подключаемся к файлу базы данных (если его нет, он создастся)
    conn = sqlite3.connect('archive_shop.db')
    cursor = conn.cursor()

    # Создаем таблицу для архивных вещей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            brand TEXT NOT NULL,
            season TEXT,
            size TEXT NOT NULL,
            condition TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT,
            image_url TEXT,
            is_available INTEGER DEFAULT 1
        )
    ''')

    # Очищаем таблицу перед заполнением (опционально, для тестов)
    cursor.execute('DELETE FROM items')

    # Добавляем стартовый архивный ассортимент
    archive_items = [
        (
            'Riot Riot Riot Bomber Jacket',
            'Raf Simons',
            'AW 2001',
            'XL',
            '9/10 (Excellent vtg condition)',
            15000.00,
            'One of the most iconic and rarest pieces in fashion history. Features patches of Sonic Youth and David Bowie.',
            'https://example.com/raf_bomber.jpg'
        ),
        (
            'Artisanal Painted Tabi Boots',
            'Maison Margiela',
            'SS 1999',
            '42',
            '8/10 (Beautiful natural cracking)',
            2200.00,
            'Grail-status hand-painted split-toe boots from the Martin Margiela era.',
            'https://example.com/margiela_tabi.jpg'
        ),
        (
            'Monofilament Mesh Jacket',
            'Stone Island',
            'SS 1998',
            'L',
            '8.5/10 (Slight yellowing due to age)',
            1100.00,
            'Designed by Paul Harvey. Made from a nylon mesh derived from aviation technology. Mesh badge included.',
            'https://example.com/si_mesh.jpg'
        )
    ]

    cursor.executemany('''
        INSERT INTO items (title, brand, season, size, condition, price, description, image_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', archive_items)

    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()
    print("База данных успешно инициализирована и заполнена архивными граалями!")

if __name__ == '__main__':
    init_db()