import requests
from bs4 import BeautifulSoup
from datetime import datetime
import locale

locale.setlocale(locale.LC_TIME, 'FR_fr')

url='https://fr.wikipedia.org/wiki/Joker_(film,_2019)'

page=requests.get(url)

# On définit le parser
soup = BeautifulSoup(page.text, 'html.parser')

fiche_technique = soup.find(id="Fiche_technique")

# On peut accéder aux parents de l'éléments, on va récupérer l'ensemble.
h2_tag = fiche_technique.parent

# Maintenant on va pouvoir obtenir le sibling(le frère), ul qui contient une liste de tous nos éléments.
ul_tag = h2_tag.find_next_sibling("ul")

# On va récupérer les 'li' qui sont les children avec : li_tags = ul_tag.find_all('li') 
# On a les enfants mais aussi les petits-enfants, ce qui peut être embêtant puisqu'on va avoir plusieurs fois les mêmes valeurs.
# L'argument recursive de find_all va nous être utile pour contrer cela.
li_tags = ul_tag.find_all("li", recursive=False)

# Boucle for pour lire les li_tag
# On découpe les chaines de caractères (.split) pour séparer le type de donnée des valeurs
# Le print() vide va permettre de passer à la ligne de manière espacée
# Le split renvoie un tableau, li_tags est un tableau donc split donne un tableau de 2 valeurs
# Directement sur le splitted_li on va faire un strip pour enlever les espaces avant et après
for li_tag in li_tags:
    splitted_li = li_tag.get_text().split(':')
    data_type = splitted_li[0].strip()
    data_value = splitted_li[1].strip()
    
    # print(data_type)
    # print(data_value)


    if data_type == "Titre original":
        title = data_value

    if data_type == "Durée": # /!\ on va .replace minutes pour n'avoir que la durée chiffrée
        duration = data_value.replace("minutes","").strip() # strip() pour enlever l'espace après minutes

    if data_type == "Dates de sortie":  
        release_date_list = li_tag.find_all('li') # On a toujours notre li_tag qui est notre objet soup
        
        for release_date_li in release_date_list:
            release_date_splitted = release_date_li.get_text().split(':')
            release_country = release_date_splitted[0].strip()
            release_date_as_string = release_date_splitted[1].strip()
            
            if release_country == "France":
                release_date_object = datetime.strptime(release_date_as_string, '%d %B %Y') # Sur wiki : jour mois en texte et année
                release_date_sql_string = release_date_object.strftime('%Y-%m-%d') # Format année mois jour
                

    if data_type == "Classification":
        rating_li_list = li_tag.find_all("li")
        for rating_li in rating_li_list:
            rating_splitted = rating_li.get_text().split(':') 
            rating_country = rating_splitted[0].strip()
            rating_string = rating_splitted[1].strip() # Interdit au moins de 12 ans
            if rating_country == "France":
                if rating_string.find('12') != -1: # On cherche '12' avec .find
                    rating = '-12'

print('title :', title)                    
print('duration :', duration)
print('release_date :', release_date_sql_string)
print('rating :', rating)


# On a récupéré nos valeurs, on va maintenant associer des données arbitraires, donnée par donnée avec des boucles if.