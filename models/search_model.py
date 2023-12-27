import pandas
def get_genre(conn):
    return pandas.read_sql( ''' 
    SELECT genre_id, genre_name, COUNT(book_id) AS amount
    FROM genre 
    JOIN book USING(genre_id)
    GROUP BY genre_id
    ''', conn)

def get_author(conn):
    return pandas.read_sql( ''' 
    SELECT author_id, author_name, COUNT(book_id) AS amount 
    FROM author 
    JOIN book_author USING(author_id)
    JOIN book USING(book_id)
    GROUP BY author_id
    ''', conn)

def get_publisher(conn):
    return pandas.read_sql( ''' 
    SELECT publisher_id, publisher_name, COUNT(book_id) AS amount 
    FROM publisher 
    JOIN book USING(publisher_id)
    GROUP BY publisher_id
    ''', conn)

def get_books(conn):
    return pandas.read_sql(''' 
    WITH get_authors( book_id, authors_name) 
    AS( 
    SELECT book_id, GROUP_CONCAT(author_name) 
    FROM author JOIN book_author USING(author_id) 
    GROUP BY book_id 
    ) 
    SELECT title AS Название, authors_name AS Авторы, 
    genre_name AS Жанр, publisher_name AS Издательство,
    year_publication AS Год_издания, available_numbers AS Количество, book_id
    FROM book 
    JOIN genre USING(genre_id) 
    JOIN publisher USING(publisher_id) 
    JOIN get_authors USING(book_id) 
    ''', conn)

# Название, Авторы, Жанр, Издательство, Год_издания, Количество, book_id
def search_books(conn, user_genre, user_author, user_publisher):
    genres = ""
    authors = ""
    publishers = ""
    for i in range(0, len(user_genre)):
        genres += "genre_id="+user_genre[i]+" "
        if (i != len(user_genre)-1):
            genres += "OR "
    for i in range(0, len(user_author)):
        authors += "author_id="+user_author[i]+" "
        if (i != len(user_author)-1):
            authors += "OR "
    for i in range(0, len(user_publisher)):
        publishers += "publisher_id="+user_publisher[i]+" "
        if (i != len(user_publisher)-1):
            genres += "OR "

    if authors != "": authors = "WHERE "+authors
    if (genres != "") | (publishers != ""): genres = "WHERE "+genres
    return pandas.read_sql(''' 
    WITH get_authors( book_id, authors_name) 
    AS( 
    SELECT book_id, GROUP_CONCAT(author_name) 
    FROM author JOIN book_author USING(author_id)
    '''+authors+'''
    GROUP BY book_id 
    ) 
    SELECT title AS Название, authors_name AS Авторы, 
    genre_name AS Жанр, publisher_name AS Издательство,
    year_publication AS Год_издания, available_numbers AS Количество, book_id
    FROM book 
    JOIN genre USING(genre_id) 
    JOIN publisher USING(publisher_id) 
    JOIN get_authors USING(book_id) 
    '''+genres+publishers, conn)