# Module pandas pour manipuler le dataframe ensuite constitué :
import pandas as pd

# Module numpy pour manipuler essentiellement des arrays :
import numpy as np

# Module re (regex ou regular expressions) pour le nettoyage de la base :
import re

# Modules pour le web scraping :
import urllib
import bs4

# Module pour la récupération du code source :
from urllib import request


##############################################################################################################
# Codage des différentes fonctions requises dans le notebook consacré à la récolte des données d'IMDb
# Stockage de toutes ces fonctions dans la classe imdb_scraping qui sera importée dans le notebook
##############################################################################################################

class imdb_scraping :
    
    
    @classmethod
    def init_results(cls):
        """Initialisation du dictionnaire des listes vides (une pour chaque variable) qui stockeront les résultats du scraping 

        Returns:
            results (dict): dictionnaire de listes vides
        """ 

        # Liste des variables que l'on souhaite scraper
        list_args = [
            'tconst', 'title', 'year', 'runtime', 'genres', 'metascore', 'rate',
            'votes', 'certificate', 'director', 'casting']
        
        # Initialisation du dictionnaire de listes vides
        results = {}
        for arg in list_args:
            results[arg] = list()

        return results



    @classmethod
    def fill_results(cls, n, list_url, dict_results) :
        """Scraping et stockage des données récoltées

        Args:
            n (int): nombre d'itérations de la boucle de scraping (nombre de pages à scraper)
            list_url (list): liste dans lequel . Son dernière élément est la première page à scraper
            dict_results (dict): dictionnaire des listes vides initialisées par la fonction init_results

        Returns:
            df (pandas.core.frame.DataFrame): dataframe générée à partir de dict_results une fois celui-ci rempli
        """
        
        # Lancement de la grande boucle de web scraping :
        for i in range(n): 
        
            url = list_url[-1]     # S'il s'agit du premier scraping, on prend l'url défini plus haut,
                                   # Sinon on prend l'url récupéré sur la dernière page scrapée

            # Récupération du code source :
            req = urllib.request.Request(url, headers = {'User-Agent' : 'Mozilla/5.0'})
            request_text = request.urlopen(req).read()

            # Utilisation du package BeautifulSoup 
            # pour interpréter les balises contenues dans la chaine de caractères du code source
            page = bs4.BeautifulSoup(request_text, "html.parser")

            # Dans l'architecture du code source, toutes les informations qu'on veut receuillir 
            # pour un seul film sont contenues dans une division ayant la classe "lister-item mode-advanced"
            # On cherche donc toutes ces divisions pour pouvoir ensuite aller récolter pour tous les films de 
            # la page concernée :
            divisions = page.findAll('div', {'class' : 'lister-item mode-advanced'})

            # Boucle sur tous les films de la page :
            for division in divisions :
                
                # Récolte du titre du film :
                title = division.h3.a.text
                dict_results['title'].append(title)

                # Récolte de l'année de sortie du film :
                year = division.h3.find('span',{'class': "lister-item-year text-muted unbold"}).text
                dict_results['year'].append(year)

                # Récolte de la durée du film :
                runtime = division.find('span',{'class':'runtime'}).text if division.p.find('span',{'class':'runtime'}) else 'NA'
                dict_results['runtime'].append(runtime)

                # Récolte des genres principaux du film :
                genres = division.find('span',{'class':'genre'}).text if division.p.find('span',{'class':'genre'}) else 'NA'
                dict_results['genres'].append(genres)

                # Récolte du métascore du film :
                metascore = division.find('span', {"class" : 'metascore'}).text if division.find('span', {'class':'metascore'}) else 'NA'
                dict_results['metascore'].append(metascore)

                # Récolte de la note du film :
                rate = division.find('div',{'class':'inline-block ratings-imdb-rating'}).find('strong').text if division.find('div',{'class':'inline-block ratings-imdb-rating'}) else 'NA'
                dict_results['rate'].append(rate)

                # Récolte du nombre de votes pour le film :
                votes = division.find('span',{'name':'nv'}).text if division.find('span',{'name':'nv'}) else 'NA'
                dict_results['votes'].append(votes)

                # Récolte de l'information s'il s'agit d'un film pour adultes :
                certificate = division.find('span',{'class':'certificate'}).text if division.find_all('span',{'class':'certificate'}) else 'NA'
                dict_results['certificate'].append(certificate)

                # Récolte du réalisateur du film :
                director = division.find_all('p',class_ ='')[0].a.text if division.find_all('p',class_ ='')[0].a else 'NA'
                dict_results['director'].append(director)

                # Récolte du casting (acteurs) du film :
                casting = [acteur.text for acteur in division.find_all('p',class_ ='')[0].find_all('a')[1:]]
                dict_results['casting'].append(casting)

                # Récolte du tconst du film (identifiant du film) :
                txt = str(division.h3.a)
                expression = re.compile("tt\\d+")        
                tconst = expression.findall(txt)
                dict_results['tconst'].append(tconst)
                
            # Crawling : récupération de l'url de la page suivante
            next_url = "https://www.imdb.com"+ page.find('div',{'class' : 'desc'}).find('a',{'class':'lister-page-next next-page'})['href']
            list_url.append(next_url)
            print("nombre de pages scrappées :" + str(i+1), end = "\r")

        # Conversion en dataframe
        df = pd.DataFrame.from_dict(dict_results)

        return df

    
    
    
    
##############################################################################################################
# Codage des différentes fonctions requises dans le notebook consacré au nettoyage des données
# Stockage de toutes ces fonctions dans la classe imdb_cleaning qui sera importée dans le notebook
##############################################################################################################

class imdb_cleaning :
    
    @classmethod
    def regex_clean(cls, elem, expr):
        """Applique une expression régulière à un élément

        Args:
            elem (string): élément à nettoyer
            expr (re.Pattern): expression régulière

        Returns:
            res (string): expression régulière trouvée dans elem
        """

        # On compile l'expression régulière donnée en entrée :
        expression = re.compile(expr)
    
        # On essaye de trouver une expression régulière dans elem : 
        try :
            res = expression.findall(elem)[0]
        except :
            res = 'NaN' # Si valeur manquante
            
        return res




    @classmethod
    def data_cleaning(cls, df):
        """Nettoie la base de données issue du scraping

        Args: 
            df (pandas.core.frame.DataFrame): base de données des films à nettoyer

        Returns:
            df_cleaned (pandas.core.frame.DataFrame): dataframe nettoyée
        """
    
        # On modifie les options de pandas pour permettre de modifier le type des variables :
        pd.options.mode.chained_assignment = None 
    
        # Conversion des variables à nettoyer au format string pour permettre d'appliquer la fonction regex_clean :
        df["year"] = df["year"].astype(str)
        df["runtime"] = df["runtime"].astype(str)
        df["genres"] = df["genres"].astype(str)
    
        # Nettoyage des données via la fonction regex_clean :
        df["tconst"] = df["tconst"].apply(lambda x: cls.regex_clean(x, "tt\\d+"))
        df["year"] = df["year"].apply(lambda x : cls.regex_clean(x, "\\d{4}"))
        df["runtime"] = df["runtime"].apply(lambda x : cls.regex_clean(x,"\\d{1,4}"))
        df["genres"] = df["genres"].apply(lambda x : x.replace("\n",""))   #déjà clean dans la nouvelle version
    
        # On neutralise les valeurs manquantes dans nos variables d'intérêt :
        df_cleaned = df[df['rate'].notnull() & (df["runtime"] != "NaN") & (df["year"] != "NaN") & (df["genres"] != "nan")]
    
        # Suppression des colonnes du metascore et certificate qui, après analyse, ont trop de valeurs manquantes :
        df_cleaned = df_cleaned.drop(columns=["metascore","certificate"])
    
        # Réindexation de la base df_cleaned :
        df_cleaned = df_cleaned.reset_index(drop=True)
    
        # Nettoyage de la variable du nombre de votes et conversion en entier pour exploitation future :
        df_cleaned["votes"] = df_cleaned["votes"].apply(lambda x : x.replace(',','').replace('.',''))
        df_cleaned["votes"] = df_cleaned["votes"].astype("int")
    
        return df_cleaned