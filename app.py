from flask import Flask, render_template, g, abort
import sqlite3

app = Flask(__name__)
DATABASE = 'archive_shop.db'


# Хелпер для удобного подключения к БД (в рамках одного запроса)
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        # Это позволит получать результаты в виде словарей, а не кортежей (item['title'] вместо item[1])
        db.row_factory = sqlite3.Row
    return db


# Закрываем соединение с БД, когда Flask заканчивает обрабатывать запрос
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# Главная страница: список всех доступных архивных вещей
@app.route('/')
def index():
    db = get_db()
    cursor = db.cursor()
    # Берем только те вещи, которые еще не проданы (is_available = 1)
    cursor.execute('SELECT * FROM items WHERE is_available = 1 ORDER BY id DESC')
    items = cursor.fetchall()
    return render_template('index.html', items=items)


# Страница конкретного лота (по его ID)
@app.route('/item/<int:item_id>')
def item_detail(item_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM items WHERE id = ?', (item_id,))
    item = cursor.fetchone()

    if item is None:
        abort(404)  # Если вещи с таким ID нет, отдаем ошибку 404

    return render_template('item.html', item=item)


if __name__ == '__main__':
    # Запускаем сервер в режиме отладки (debug=True)
    app.run(debug=True, port=5000)