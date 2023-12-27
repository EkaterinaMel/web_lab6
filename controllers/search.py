from app import app
from flask import render_template, request, session
import sqlite3
from utils import get_db_connection
from models.search_model import *
@app.route('/search', methods=['get'])
def search():
    conn = get_db_connection()
    user_genre = []
    user_author = []
    user_publisher = []
    books = []
    if request.values.get('search'):
        user_genre = request.values.getlist('genre[]')
        user_author = request.values.getlist('author[]')
        user_publisher = request.values.getlist('publisher[]')
        books = search_books(conn, user_genre, user_author, user_publisher)
    else:
        books = get_books(conn)
    # выводим форму
    html = render_template(
        'search.html',
        list_genre = get_genre(conn),
        list_author = get_author(conn),
        list_publisher = get_publisher(conn),
        user_genre = user_genre,
        user_author = user_author,
        user_publisher = user_publisher,
        books = books,
        int = int
    )
    return html