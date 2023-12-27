from app import app
from flask import render_template, request, session
import sqlite3
from utils import get_db_connection
from models.index_model import *
@app.route('/', methods=['get'])
def index():
    conn = get_db_connection()
    # нажата кнопка Найти
    if request.values.get('reader'):
        reader_id = int(request.values.get('reader'))
        session['reader_id'] = reader_id
    # нажата кнопка Добавить со страницы Новый читатель
    # #(взять в комментарии, пока не реализована страница Новый читатель)
    elif request.values.get('new_reader'):
        new_reader = request.values.get('new_reader')
        session['reader_id'] = get_new_reader(conn, new_reader)
    # нажата кнопка Взять со страницы Поиск
    # #(взять в комментарии, пока не реализована страница Поиск)
    elif request.values.get('book'):
        book_id = int(request.values.get('book'))
        borrow_book(conn, book_id, session['reader_id'])
    # нажата кнопка Не брать книгу со страницы Поиск
    # #(взять в комментарии, пока не реализована страница Поиск)
    elif request.values.get('noselect'):
        a = 1
    # отдать книгу
    elif request.values.get('give'):
        return_book(conn, request.values.get('give'))
    # добавить читателя
    elif request.values.get('add'):
        reader_id = get_new_reader(conn, request.values.get('name'))
        session['reader_id'] = reader_id
    # взять книгу
    elif request.values.get('take'):
        borrow_book(conn, str(request.values.get('take')), str(session['reader_id']))

    elif request.values.get('cancel'):
        session['reader_id']= session['reader_id']

    # вошли первый раз
    else:
        session['reader_id']= 1
    df_reader = get_reader(conn)
    df_book_reader = get_book_reader(conn, session['reader_id'])
    # выводим форму
    html = render_template(
        'index.html',
        reader_id = session['reader_id'],
        combo_box = df_reader,
        book_reader = df_book_reader,
        len = len )
    return html

app.run(debug=True)