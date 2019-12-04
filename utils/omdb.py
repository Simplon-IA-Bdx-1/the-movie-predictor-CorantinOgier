import requests
from datetime import datetime
import os
import json
import random
from pprint import pprint

class Omdb:
    def __init__(self, imdbid=''):
        self.imdbid = imdbid
        
        imdbid = self.imdbid
        if self.imdbid == '': # Si aucun id n'est donné, on génère un id aléatoire
            imdbid = self.rand_imdbid()
        
        data = requests.get('http://www.omdbapi.com/?apikey=' + os.environ['OMDB_APIKEY'] + '&i=' + str(imdbid))
        json_data = data.json()
        while json_data['Response'] != 'True':
            imdbid = self.rand_imdbid()
            data = requests.get('http://www.omdbapi.com/?apikey=' + os.environ['OMDB_APIKEY'] + '&i=' + str(imdbid))
            json_data = data.json()
        
        # pprint(json_data)
        self.json_data = json_data
        
        self.title = None
        if 'Title' in json_data:
            if json_data['Title'] != 'N/A':
                self.title = json_data['Title']
        
        self.release_date = None
        if 'Relesed' in json_data:
            if json_data['Relesed'] != 'N/A':
                self.release_date = datetime.strftime(datetime.strptime(json_data['Released'], '%d %b %Y'), '%Y-%m-%d')
        
        self.duration = None
        if 'Runtime' in json_data:
            if json_data['Runtime'] != 'N/A':
                duration = json_data['Runtime'].split(' ')
                self.duration = duration[0]
        
        self.synopsis = None
        if 'Plot' in json_data:
            if json_data['Plot'] != 'N/A':
                self.synopsis = json_data['Plot']
        
        self.boxoffice = None
        if 'BoxOffice' in json_data:
            if json_data['BoxOffice'] != 'N/A':
                self.boxoffice = int(json_data['BoxOffice'].replace('$','').replace(',',''))
        
        self.actors = None
        if 'Actors' in json_data:
            if json_data['Actors'] != 'N/A':
                self.actors = json_data['Actors'].split(', ')
        
        self.rating = None
        if 'Rated' in json_data:
            if json_data['Rated'] != 'N/A':
                if "12" in json_data['Rated'].strip():
                    self.rating = '-12'
        
        self.imdbid = None
        if 'imdbID' in json_data:
            if json_data['imdbID'] != 'N/A':
                self.imdbid = json_data['imdbID']
    
    def rand_imdbid(self): # Méthode permettant de générer un ID au format IMDB
        return "tt" + str(random.randint(1, 9999999)).rjust(7,'0')