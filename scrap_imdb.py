import requests
from bs4 import BeautifulSoup
from datetime import datetime
import locale

locale.setlocale(locale.LC_TIME, 'FR_fr')

url='https://www.imdb.com/title/tt2527338/'

page=requests.get(url, headers={'Accept-Language': 'fr-fr'})

soup = BeautifulSoup(page.text, 'html.parser')

detail = soup.find(id="titleDetails")

div_tags = detail.find_all('div', recursive=False)



for div_tag in div_tags:
    splitted_div=div_tag.get_text().split(':', 1)
    data_type = splitted_div[0].strip()
    
    if data_type == "Also Known As":
        title = splitted_div[1].strip()
        splitting_title = title.split('See')
        splitted_title = splitting_title[0].strip()

    if data_type == "Runtime": 
        duration = splitted_div[1].replace("min", "").strip() 

    if data_type == "Release Date":
        release_date = splitted_div[1].strip()
        release_date_splitted = release_date.split('(')
        release_date_as_string = release_date_splitted[0].strip()


print('title :', splitted_title)
print('release_date :', release_date_as_string)
print('duration :', duration)


