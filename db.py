import sqlite3
from contextlib import closing
# import os

from objects import Category, Movie

conn = None

def connect():
    global conn
    if not conn:
        # ----- another way to access directory ----- 
        
        # getting the absolute path to the database file
        # current_dir = os.path.dirname(os.path.abspath(__file__))
        # DB_FILE = os.path.join(current_dir, "db", "movies.sqlite")
        
        DB_FILE = "db/movies.sqlite" 
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row

def close():
    if conn:
        conn.close()

def make_category(row):
    return Category(row["categoryID"], row["categoryName"])

def make_movie(row):
    return Movie(row["movieID"], row["name"], row["year"], row["minutes"],
            make_category(row))

def make_movie_list(results):
    movies = []
    for row in results:
        movies.append(make_movie(row))
    return movies

def get_movies(): # this query will retrieve movie information that includes name, year, minutes, and category
    query = '''SELECT movieID, Movie.name, year, minutes,
                  Movie.categoryID,
                  Category.name as categoryName
           FROM Movie JOIN Category
                  ON Movie.categoryID = Category.categoryID'''
    with closing(conn.cursor()) as c:
        c.execute(query)
        results = c.fetchall()

    return make_movie_list(results) # this will create a list of movie objects from the query results

def get_categories():
    query = '''SELECT categoryID, name as categoryName
               FROM Category'''
    with closing(conn.cursor()) as c:
        c.execute(query)
        results = c.fetchall()

    categories = []
    for row in results:
        categories.append(make_category(row))
    return categories

def get_category(category_id):
    query = '''SELECT categoryID, name AS categoryName
               FROM Category WHERE categoryID = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (category_id,))
        row = c.fetchone()
        if row:
            return make_category(row)
        else:
            return None

def get_movies_by_category(category_id):
    query = '''SELECT movieID, Movie.name, year, minutes,
                      Movie.categoryID,
                      Category.name as categoryName
               FROM Movie JOIN Category
                      ON Movie.categoryID = Category.categoryID
               WHERE Movie.categoryID = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (category_id,))
        results = c.fetchall()

    return make_movie_list(results)

def get_movies_by_year(year):
    query = '''SELECT movieID, Movie.name, year, minutes,
                      Movie.categoryID,
                      Category.name as categoryName
               FROM Movie JOIN Category
                      ON Movie.categoryID = Category.categoryID
               WHERE year = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (year,))
        results = c.fetchall()

    return make_movie_list(results)

def add_movie(movie):
    sql = '''INSERT INTO Movie (categoryID, name, year, minutes) 
             VALUES (?, ?, ?, ?)'''
    with closing(conn.cursor()) as c:
        c.execute(sql, (movie.category.id, movie.name, movie.year,
                        movie.minutes))
        conn.commit()

def delete_movie(movie_id):
    sql = '''DELETE FROM Movie WHERE movieID = ?'''
    with closing(conn.cursor()) as c:
        c.execute(sql, (movie_id,))
        test = conn.commit()
        print("Test", test)
