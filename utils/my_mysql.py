import mysql.connector
import os

class Sql: # Nouvelle class Sql
    def __init__(self): # Initialisation de la classe : connexion au serveur avec les variables d'envrionnement et création d'un curseur
         self.db = mysql.connector.connect(user=os.environ['MYSQL_USER'], password=os.environ['MYSQL_PASSWORD'], host=os.environ['MYSQL_HOST'], database=os.environ['MYSQL_DATABASE'])
         self.cursor = self.db.cursor()

    def close(self):
        self.cursor.close()
        self.db.close()

    def query(self, req, data=''): # Méthode générique pour le requêtage de la base
        self.cursor.execute(req, data)
        results = self.cursor.fetchall()
        return results

    def rows(self): # Méthode permettant d'obtenir le nombre de lignes renvoyé
        return self.cursor.rowcount

    def list_db(self, table, nbrows=10000): # Méthode permettant de lister des données à partir d'une table
        req_list = (f"SELECT * FROM {table} LIMIT {nbrows}")
        results = self.query(req_list)
        return results

    def insert_db(self, table, data): # Méthode permettant d'insérer des données dans la base SQL
        db_keys = ', '.join(data.keys())
        db_values = '\', \''.join(data.values())
        req_insert = (f"INSERT INTO {table} ({db_keys}) VALUES('{db_values}')")
        self.cursor.execute(req_insert)
        last_row = self.cursor.lastrowid
        self.db.commit()
        return last_row

    def insert_movie(self, data): # Méthode permettant d'insérer un film dans la base SQL
        insert_req = ("""
            INSERT INTO movies
            (title, original_title, synopsis, duration, rating, release_date, boxoffice, imdbid)
            VALUES (%(title)s, %(original_title)s, %(synopsis)s, %(duration)s, %(rating)s, %(release_date)s, %(boxoffice)s, %(imdbid)s)
        """)
        self.cursor.execute(insert_req, data)
        last_row = self.cursor.lastrowid
        self.db.commit()
        return last_row

    def insert_person(self, data): # Méthode permettant d'insérier une personne dans la base SQL
        insert_req = ("INSERT INTO people (firstname, lastname) VALUES (%(firstname)s, %(lastname)s)")
        self.cursor.execute(insert_req, data)
        last_row = self.cursor.lastrowid
        self.db.commit()
        return last_row