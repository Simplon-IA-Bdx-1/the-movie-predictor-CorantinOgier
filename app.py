#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import librairies gloables
from pprint import pprint
import argparse
import csv
import os

# Import librairies locales
from utils.my_mysql import Sql
from utils.person import Person
from utils.movie import Movie
from utils.omdb import Omdb

# Parser CLI
parser = argparse.ArgumentParser(description='Process MoviePredictor data')
parser.add_argument('context', choices=['people', 'movies', 'import'], help='Le contexte dans lequel nous allons travailler')

known_args = parser.parse_known_args()[0]
if known_args.context == "import":
    parser.add_argument('--api' , help='Choix de l\'API', required=True)
    parser.add_argument('--imdbid' , help='ID du film dans IMDB', required=False)

action_subparser = parser.add_subparsers(title='action', dest='action')

list_parser = action_subparser.add_parser('list', help='Liste les entitées du contexte')
list_parser.add_argument('--export' , help='Chemin du fichier exporté')

find_parser = action_subparser.add_parser('find', help='Trouve une entité selon un paramètres')
find_parser.add_argument('id' , help='Identifant à rechercher')

import_parser = action_subparser.add_parser('import', help='Importe le contenu du fichier csv')
import_parser.add_argument('--file' , help='Chemin du fichier importé')

scrap_parser = action_subparser.add_parser('scrap', help='Scrap le contenu de la page')
scrap_parser.add_argument('--url' , help='URL de la page wikipedia')
scrap_parser.add_argument('--id' , help='ID de la page IMdb')
scrap_parser.add_argument('--iterations' , help='Nombre d\'iterations')

insert_parser = action_subparser.add_parser('insert', help='Insert une nouvelle entité')
known_args = parser.parse_known_args()[0]

if known_args.context == "people":
    insert_parser.add_argument('--firstname' , help='Prénom de l\'acteur', required=True)
    insert_parser.add_argument('--lastname' , help='Nom de l\'acteur', required=True)

if known_args.context == "movies":
    insert_parser.add_argument('--title' , help='Titre français du film', required=True)
    insert_parser.add_argument('--original-title' , help='Titre original du film', required=True)
    insert_parser.add_argument('--duration' , help='Durée en minutes', type=int, required=True)
    insert_parser.add_argument('--releasedate' , help='Date de sortie en France', required=True)
    insert_parser.add_argument('--rating' , help='Classification', choices=['TP', '-12', '-16'], required=True)     

args = parser.parse_args()

db = Sql() # Création de l'objet db de la classe Sql

if args.context == "people": # Contexte
    if args.action == "list": # Action
        people_list = [] # On crée une liste contenant les people
        for res in db.list_db('people'): # Boucle sur requete SQL
            person = Person(res[1], res[2]) # On crée un objet person de la classe Person
            person.id = res[0]
            person.print_person(res[0]) # Affiche les résultats sous forme de texte formaté
            people_list.append(person) # On ajoute une nouvelle person à la liste contenant les people
        if args.export:
            with open(args.export, 'w', encoding='utf-8', newline='\n') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(people_list[0].__dict__.keys())
                for res in people_list: # Boucle sur requete SQL
                    writer.writerow(res.__dict__.values())
    if args.action == "find": # Cherche un ID dans la BDD
        person_id = { 'id' : args.id }
        results = db.query("SELECT * FROM people WHERE id = %(id)s", person_id)
        if results:
            person = Person(results[0][1], results[0][2])
            person.print_person(results[0][0])
        else:
            print(f"Aucune personne avec l'id {args.id} n'a été trouvé !")
    if args.action == "insert": # Ajoute des données dans la BDD
        insert_data = {
            'firstname' : args.firstname,
            'lastname' : args.lastname,
        }
        person_id = db.insert_person(insert_data)
        print(f"Nouvelle personne insérée avce l'id {person_id}")

if args.context == "movies": # Contexte
    if args.action == "list": # Action
        movies_list = []
        for res in db.list_db('movies'): # Boucle sur requete SQL
            movie = Movie(res[1])
            movie.id = res[0]
            movie.original_title = res[2]
            movie.synopsis = res[3]
            movie.duration = res[4]
            movie.rating = res[5]
            movie.production_budget = res[6]
            movie.marketing_budget = res[7]
            movie.release_date = res[8]
            movie.is_3d = res[9]
            movie.imdbid = res[10]
            movie.boxoffice = res[11]
            movie.print_movie(res[0])
            movies_list.append(movie) # On ajoute un nouveau movie à la liste contenant les movies
        
        if args.export:
            with open(args.export, 'w', encoding='utf-8', newline='\n') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(movies_list[0].__dict__.keys())
                for res in movies_list: # Boucle sur requete SQL
                    writer.writerow(res.__dict__.values())
    if args.action == "find": # Cherche un ID dans la BDD
        movie_id = { 'id' : args.id }
        results = db.query("SELECT * FROM movies WHERE id = %(id)s", movie_id)
        if results:
            movie = Movie(results[0][1])
            movie.print_movie(results[0][0])
        else:
            print(f"Aucun film avec l'id {args.id} n'a été trouvé !")
    if args.action == "insert": # Ajoute des données dans la BDD
        insert_data = {
            'title' : str(args.title),
            'original_title' : str(args.original_title),
            'duration' : str(args.duration),
            'release_date' : str(args.releasedate),
            'rating' : str(args.rating),
        }
        movie_id = db.insert_db('movies', insert_data)
        print(f"Nouveau film inséré avec l'id {movie_id}")
    if args.action == "import": # Importe des données dans la BDD depuis un csv
        with open(args.file, 'r') as csvfile:
            reader = csv.DictReader(csvfile) # Reader dans un dictionnaire
            for row in reader:
                insert_data = {
                    'title' : str(row['title']),
                    'original_title' : str(row['original_title']),
                    'duration' : str(row['duration']),
                    'rating' : str(row['rating']),
                    'release_date' : str(row['release_date']),
                }
                movie_id = db.insert_db('movies', insert_data)
                db = Sql() # Création de l'objet db de la classe Sql
                print(f"Film \"{row['title']}\" inséré avec l'id {movie_id}")

if args.context == "import":
    if args.api == "omdb":
        if args.imdbid == None:
            print(f'Choix d\'un film de manière aléatoire')
        
        omdb = Omdb(args.imdbid)
        
        movie_imdbid = { 'imdbid' : omdb.imdbid }
        results = db.query("SELECT * FROM movies WHERE imdbid = %(imdbid)s", movie_imdbid)
        if not results: # Si le film n'est pas dans la base, on l'insère
            insert_data = {
                'title' : omdb.title,
                'original_title' : omdb.title,
                'synopsis' : omdb.synopsis,
                'duration' : omdb.duration,
                'rating' : omdb.rating,
                'release_date' : omdb.release_date,
                'boxoffice' : omdb.boxoffice,
                'imdbid' : omdb.imdbid,
            }
            movie_id = db.insert_movie(insert_data)
            print(f"Nouveau film inséré avec l'id {movie_id}")
        else: # Si le film est dans la base on récupère son id
            movie_id = results[0][0]
            print(f"Le film \"{results[0][1]}\" (ID#{results[0][0]}) est déjà dans la base !")

        if omdb.actors is not None:
            for actor in omdb.actors:
                firstname = actor.split(' ', 1)[0]
                lastname = actor.split(' ', 1)[1]

                data = {
                    'firstname' : firstname,
                    'lastname' : lastname,
                }
                results = db.query("SELECT * FROM people WHERE firstname = %(firstname)s AND lastname = %(lastname)s", data)
                if not results: # Si l'acteur n'est pas dans la base, on l'insère
                    people_id = db.insert_person(data)
                    print(f"Nouvelle personne ({data.get('firstname')} {data.get('lastname')}) insérée avec l'id {people_id}")
                else: # Si l'acteur est dans la base on récupère son id
                    people_id = results[0][0]

                
                data = {
                    'movie_id' : str(movie_id),
                    'people_id' : str(people_id),
                }
                results = db.query("SELECT * FROM movies_people_roles WHERE movie_id = %(movie_id)s AND people_id = %(people_id)s", data)
                if not results: # Si la relation movie / people n'est pas dans la base, on l'insère
                    db.insert_db('movies_people_roles', data)

db.close()