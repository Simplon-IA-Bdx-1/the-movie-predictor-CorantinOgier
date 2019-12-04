# The Movie Predictor (tmp)

## 1. Objectif :
Insérer un film aléatoirement dans une base MySQL à partir de l'API OMDB en exécutant un container docker

## 2. Setup :
 - Renseigner les variables d'envionnement du projet dans le fichier auth.env disponible à la racine du projet :

 ```
OMDB_APIKEY=XXXX
MYSQL_RANDOM_ROOT_PASSWORD=yes
MYSQL_USER=XXXX
MYSQL_PASSWORD=XXXX
MYSQL_DATABASE=XXXX
MYSQL_HOST=tmp_database
```

 - A partir du dossier racine du projet, exécuter la commande suivante depuis le terminal :
 ```
 docker-compose up -d 
```
 - Par défaut, après avoir récupéré les données d'un film, le container Python s'éteindra. Pour conserver le container actif et exécuter d'autres commandes (liste des commandes disponible au chapitre "**4. Commandes**" ci-après), il est nécessaire de décommenter la ligne **command** du docker-compose.yml :

  ```
 services:
    app:
        command: tail -f /dev/null
 ```


 ## 3. Description du setup du projet :
 - Trois containers docker :
    - Un container **Python** nommé "_tmp_app_" :
        - Contient le serveur python permettant l'exécution de l'application
        - Construit à partir de l'image "python:3.7-alpine" du hub docker
        - Les packages suivants, nécéssaires à l'exécution du code, sont installés dans le container (cf Dockerfile) :
             - argparse
             - beautifulsoup4
             - requests
             - mysql-connector-python
        - Connecté  au réseau local ("tmp_network") commun aux containers du projet
    - Un container **MySQL** nommé "_tmp_database_" :
        - Contient le serveur de base de donnée MySQL
        - Construit à partir de l'image "mysql:latest" du hub docker
        - Connecté  au réseau local ("tmp_network") commun aux containers du projet
        - Utilise un volume docker ("tmp_volume) pour stocker la base de données (/var/lib/mysql)
    - Un container **Adminer** nommé "_tmp_adminer_" :
        - Contient l'application Adminer permettant d'administrer la base de donnée MySQL depuis une interface graphique accessible via un navigateur web à l'adresse : http://localhost:8080
        - Construit à partir de l'image "dehy/adminer:latest" du hub docker
        - Connecté  au réseau local ("tmp_network") commun aux containers du projet et écoute sur le port 8080 (port 80 en interne)

## 4. Commandes :

Pour interagir avec le container python sous Windows 10, dans Cmder :

```
winpty docker exec -it tmp_python sh
```


 - Commandes sur **people** :
    - Lister les personnes disponibles dans la base MySQL :
        - python app.py people list
    - Rechercher une personne avec son id dans la base MySQL : 
        - python app.py people find 1
    - Insérer  une personne dans la base MySQL : 
        - python app.py people insert --firstname 'Louis' --lastname 'de Funès'
 - Commandes sur **movies** :
    - Lister les films disponibles dans la base MySQL :
        - python app.py movies list
    - Rechercher un film avec son id dans la base MySQL :
        - python app.py movies find 1
    - Insérer  un film dans la base MySQL : 
        - python app.py movies insert --title 'Joker' --original-title 'Joker US' --duration '125' --releasedate '2019-08-21' --rating 'TP'
    - Insérer des films dans la base MySQL à partir d'un fichier csv :
        - python app.py movies import --file new_movies.csv
 - Commandes sur **import** :
    - Insérer un film et les personnes associées dans la base MySQL à partir de son id IMDB :
        - python app.py import --api omdb --imdbid 'tt0058135'
    - Insérer un film choisi aléatoirement et les personnes associées dans la base MySQL :
        - python app.py import --api omdb