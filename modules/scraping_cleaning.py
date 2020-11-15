# Module pandas pour manipuler le dataframe ensuite constitué :
import pandas as pd

# Module numpy pour manipuler essentiellement des arrays :
import numpy as np

# Module re (regex ou regular expressions) pour le nettoyage de la base :
import re

# Modules pour le web scraping :
import urllib
import bs4
# pour la récupération du code source :
from urllib import request


class imdb_scraping :

    @classmethod
    def init_results(cls):
        list_args = [
            'tconst', 'title', 'year', 'runtime', 'genres', 'metascore', 'rate',
            'votes', 'certificate', 'director', 'casting']
        results = {}
        for arg in list_args:
            results[arg] = list()

        return results



    @classmethod
    def fill_results(cls, n, list_url, dict_results) :

        for i in range(n): # Lancement de la grande boucle de web scraping
        
            url = list_url[-1]     # Si premier scraping, on prend l'url définie plus haut,  
                                   # sinon on prend l'url récupérée sur la dernière page scrapée

            # Etape de récupération du code source :
            req = urllib.request.Request(url, headers = {'User-Agent' : 'Mozilla/5.0'})
            request_text = request.urlopen(req).read()

            # Utilisation du package BeautifulSoup 
            # pour interpréter les balises contenues dans la chaine de caractères du code source
            page = bs4.BeautifulSoup(request_text, "html.parser")

            # Dans l'architecture du code source, toutes les informations qu'on veut receuillir 
            # pour un seul film sont contenues dans une division ayant la classe "lister-item mode-advanced"
            # Donc on récolte toutes ces divisions pour pouvoir ensuite aller récolter pour tous les films de 
            # la page concernée
            divisions = page.findAll('div', {'class' : 'lister-item mode-advanced'})

            # On boucle pour tous les films de la page :
            for division in divisions :
                
                # Récolte du titre du film
                title = division.h3.a.text
                dict_results['title'].append(title)

                # Récolte de l'année de sortie du film
                year = division.h3.find('span',{'class': "lister-item-year text-muted unbold"}).text
                dict_results['year'].append(year)

                # Récolte de la durée du film
                runtime = division.find('span',{'class':'runtime'}).text if division.p.find('span',{'class':'runtime'}) else 'NA'
                dict_results['runtime'].append(runtime)

                # Récolte des genres principaux du film
                genres = division.find('span',{'class':'genre'}).text if division.p.find('span',{'class':'genre'}) else 'NA'
                dict_results['genres'].append(genres)

                # Récolte du métascore du film
                metascore = division.find('span', {"class" : 'metascore'}).text if division.find('span', {'class':'metascore'}) else 'NA'
                dict_results['metascore'].append(metascore)

                # Récolte de la note du film
                rate = division.find('div',{'class':'inline-block ratings-imdb-rating'}).find('strong').text if division.find('div',{'class':'inline-block ratings-imdb-rating'}) else 'NA'
                dict_results['rate'].append(rate)

                # Récolte du nombre de votes pour le film
                votes = division.find('span',{'name':'nv'}).text if division.find('span',{'name':'nv'}) else 'NA'
                dict_results['votes'].append(votes)

                # Récolte de l'information s'il s'agit d'un film pour adultes
                certificate = division.find('span',{'class':'certificate'}).text if division.find_all('span',{'class':'certificate'}) else 'NA'
                dict_results['certificate'].append(certificate)

                # Récolte du réalisateur du film
                director = division.find_all('p',class_ ='')[0].a.text if division.find_all('p',class_ ='')[0].a else 'NA'
                dict_results['director'].append(director)

                # Récolte du casting (acteurs) du film
                casting = [acteur.text for acteur in division.find_all('p',class_ ='')[0].find_all('a')[1:]]
                dict_results['casting'].append(casting)

                # Récolte du tconst du film (identifiant du film) et stockage dans le tableau tconst :
                txt = str(division.h3.a)
                expression = re.compile("tt\\d+")        
                tconst = expression.findall(txt)
                dict_results['tconst'].append(tconst)
                
            # Crawling : récupération de l'url de la page suivante
            next_url = "https://www.imdb.com"+ page.find('div',{'class' : 'desc'}).find('a',{'class':'lister-page-next next-page'})['href']
            list_url.append(next_url)
            print("nombre de pages scrappées :" + str(i+1), end = "\r")

        df = pd.DataFrame.from_dict(dict_results)

        return df

# class movies_cleaning :

#     @classmethod