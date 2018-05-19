import sqlite3

with sqlite3.connect("blog.db") as connection:
  c = connection.cursor()
  c.execute("""create table posts (title TEXT, post TEXT)""")
  c.execute("""INSERT INTO posts VALUES("Good", "I am good")""")
  c.execute("""INSERT INTO posts VALUES("Well", "Im well")""")
  c.execute("""INSERT INTO posts VALUES("Excellent", "I am excellent")""")
  c.execute("""INSERT INTO posts VALUES("OK", "I am OK")""")
