import sqlite3 as sql

conn = sql.connect('ad14.db')

conn.execute("PRAGMA foreign_keys = ON")

cursor = conn.cursor()

# cursor.execute("""CREATE TABLE utilizadores (
#                 id INTEGER PRIMARY KEY,
#                 nome TEXT,
#                 username TEXT,
#                 password TEXT
#                 );""")

# cursor.execute("""CREATE TABLE albuns (
#                 id INTEGER PRIMARY KEY,
#                 id_banda INTEGER,
#                 nome TEXT,
#                 ano_album INTEGER,
#                 FOREIGN KEY(id_banda) REFERENCES bandas(id)
#                 );""")

# cursor.execute("""CREATE TABLE bandas (
#                 id INTEGER PRIMARY KEY,
#                 nome TEXT,
#                 ano INTEGER,
#                 genero TEXT
#                 );""")

# cursor.execute("""CREATE TABLE rates (
#                 id INTEGER PRIMARY KEY,
#                 designacao TEXT,
#                 sigla TEXT
#                 );""")


# cursor.execute("""CREATE TABLE listas_albuns (
#                 id_user INTEGER,
#                 id_album INTEGER,
#                 id_rate INTEGER,
#                 PRIMARY KEY (id_user, id_album),
#                 FOREIGN KEY(id_user) REFERENCES utilizadores(id),
#                 FOREIGN KEY(id_album) REFERENCES albuns(id)
#                 FOREIGN KEY(id_rate) REFERENCES rates(id)
#                 );""")

