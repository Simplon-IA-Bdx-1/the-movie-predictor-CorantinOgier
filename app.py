#https://docs.python.org/3/library/argparse.html documentation
"""
Corantin Ogier
themoviepredictor script
"""

import mysql.connector 
import sys
import argparse
import csv

#Fonctions connection, déconnection, curseur pour mypred, sortir de ce cursor, trouver une/des ligne/s, 
def connectToDatabase():
    return mysql.connector.connect(user='predictor', password='predictor',
                              host='127.0.0.1',
                              database='predictor')

def disconnectDatabase(cnx):
    cnx.close()

def findQuery(table, id):
    return ("SELECT * FROM {} WHERE id = {}".format(table, id))


def find(table, id, search):
    cnx = connectToDatabase()
    cursor = createCursor(cnx) #pointeur vers curseur
    if search == 'find':
        cursor.execute(findQuery(table, id)) #on exécute plusieurs query, vu que findQuery nous retourne un tuple (entre parenthèses)
    if search == 'list':
        cursor.execute(findQueryAll(table))
    result = cursor.fetchall() #enregistre tout ce que le curseur a trouvé, dans result, et retourne une liste
    closeCursor(cursor) 
    disconnectDatabase(cnx)
    return result #on retourne le résultat à qui à appelé la fonction

def findQueryAll(table):
    return("SELECT * FROM {}".format(table))

def insertMovieQuery(table, title, duration, original_title, release_date, rating):
    return("INSERT INTO `{}` (title, duration, original_title, release_date, rating) VALUES ('{}', {}, '{}', '{}', '{}')".format(table, title, duration, original_title, release_date, rating))
# On enlève les guillemets sur les acolades correspondantes à duration

def insertPeopleQuery(table, firstname, lastname):
    return("INSERT INTO `{}` (firstname, lastname) VALUES ('{}', '{}')".format(table, firstname, lastname))

def createCursor(cnx):
    return cnx.cursor(dictionary=True)

def closeCursor(cursor):
    cursor.close()

def insertPeople(table, firstname, lastname):
    cnx = connectToDatabase()
    cursor = createCursor(cnx)
    cursor.execute(insertPeopleQuery(table, firstname, lastname))
    cnx.commit()
    closeCursor(cursor)
    disconnectDatabase(cnx)

def insertMovie(table, title, duration, original_title, release_date, rating):
    cnx = connectToDatabase()
    cursor = createCursor(cnx)
    cursor.execute(insertMovieQuery(table, title, duration, original_title, release_date, rating))
    cnx.commit()
    closeCursor(cursor)
    disconnectDatabase(cnx)

    

# ArgumentParser.add_argument(name or flags...[, action][, nargs]
# [, const][, default][, type][, choices][, required][, help][, metavar][, dest])

"""
On met nos lignes de côté et on essaye avec une autre manière de faire

parser = argparse.ArgumentParser(description='Process MoviePredictor data')
parser.add_argument('context', choices=['people', 'movies'], help='Le contexte dans lequel nous allons travailler') #on a choisit le nom context, ensuite [people ou movies]
parser.add_argument('action', choices=['list', 'find'], help='L\'action à effectuer dans le contexte') #-- pour optionnel et positionnel sans tiret, juste le nom
parser.add_argument('--id', type=int, required=False, help='L\'identifiant à rechercher') 
parser.add_argument('--export', choices=['csv'], help='Format d\'exportation')
"""

parser = argparse.ArgumentParser(description='Process MoviePredictor data')
parser.add_argument('context', choices=['people', 'movies'], help='Le contexte dans lequel nous allons travailler')
subparsers = parser.add_subparsers(dest='action', required=True)
parser_list = subparsers.add_parser('list')
parser_find = subparsers.add_parser('find')
parser_find.add_argument('id', metavar='id', type=int)
parser.add_argument('--export', metavar='file.csv')

"""parser_import = subparsers.add_argument('import', metavar='file.csv', help='Importer un fichier csv')
parser_import.add_argument('--file' , help='file.csv')"""

parser_find = subparsers.add_parser('import', help='importer un fichier csv dans la DB')
parser_find.add_argument('--file' , help='file.csv')

parser_insert = subparsers.add_parser('insert')
parser_insert.add_argument('--firstname', metavar='firstname', help='Insérer le prénom')
parser_insert.add_argument('--lastname', metavar='lastname', help='Insérer le nom')
parser_insert.add_argument('--title', metavar='title', help='Titre')
parser_insert.add_argument('--duration', metavar='duration', help='Duree du film')
parser_insert.add_argument('--original-title', metavar='original-title', help='Titre d\'origine du film')
parser_insert.add_argument('--rating', metavar='rating', help='Age recommandé pour voir le film')
parser_insert.add_argument('--release-date', metavar='release-date', help='Date de sortie du film')

args = parser.parse_args() #une fois les add choisis, il analyse nos arguments et les stocks dans args

# arguments = sys.argv.copy()
# arguments.pop(0)

#for arg in arguments:
#    print(arg)

if args.context == "people":
    if args.action == "list": 
        result = find("people", 0, 'list')
        if args.export: #si l'args.export existe sinon on peut écrire 'if args.export != None'
            print('exportation réalisée')
            
            # Autre façon d'ouvrir le csvfile qui permet de ne pas utiliser le csvfile.close()
            
            # with open(args.export, 'w') as csvfile:
            #     writer = csv.writer(csvfile, lineterminator='\n')
            #     writer.writerow(result[0].keys()) 
            
            csvfile = open(args.export, 'w', encoding='UTF-8', newline='\n') #avec la version 3 de python on doit forcément mettre 'w' et non 'wb' suivi d'un newline=' ' ou '\n' pour ne pas avoir de saut de ligne dans notre fichier csv
            writer = csv.writer(csvfile) 
            writer.writerow(result[0].keys()) #pour avoir nos keys correspondantes
            for person in result:
                writer.writerow(person.values())
            csvfile.close()
        else:
            for person in result:
                print("#{}: {} {}".format(person['id'], person['firstname'], person['lastname']))
    if args.action == "find":
        peopleId = args.id
        people = find("people", peopleId, 'find')
        for person in people:
            print("#{}: {} {}".format(person['id'], person['firstname'], person['lastname']))
            #on pourrait rajouter un message d'erreur si l'id n'est pas précisé
            
if args.context == "movies":
    if args.action == "list": 
        result = find("movies", 0, 'list')
        if args.export:
            print('exportation réalisée')
            csvfile = open(args.export, 'w', encoding='UTF-8' , newline='\n')
            writer = csv.writer(csvfile)
            writer.writerow(result[0].keys())
            for movie in result:
                writer.writerow(movie.values())
        else:
            for movie in result:
                print("#{}: {} released on {}".format(movie['id'], movie['title'], movie['release_date']))
    if args.action == "find": 
        movieId = args.id 
        result = find("movies", movieId, 'find')
        for movie in result:
            print("#{}: {} released on {}".format(movie['id'], movie['title'], movie['release_date']))

if args.context == "people":
    if args.action == "insert":
        insertPeople('people', args.firstname, args.lastname)

if args.context == "movies":
    if args.action == "insert":
        insertMovie('movies', args.title, args.duration, args.original_title, args.release_date, args.rating)
    if args.action == "import":
        if args.file:
            with open(args.file) as csv_file:
                reader = csv.DictReader(csv_file, delimiter=',')
                for row in reader:
                    insertMovie("movies", row['title'], row['original_title'], row['duration'], row['release_date'], row['rating'])





