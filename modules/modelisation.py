import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import sklearn

##############################################################################################################
# Codage des différentes fonctions requises dans le notebook consacré à la modelisation 
# Stockage de toutes ces fonctions dans la classe preprocessing qui sera importée dans le notebook de visualisation
##############################################################################################################

class preprocessing_data:
    # Différentes fonctions requises dans le notebook consacré à la prépartion des données
    
    @classmethod
    def one_hot_encoding(cls,df, list_genres) :
        """Encode la variable genres en créant des colonnes binaires pour chaque film

        Args:
            df (pandas.core.frame.DataFrame): dataframe nettoyée

        Returns:
            list_genres (list): liste des genres de la base
        """

        list_columns = ["genre_" + genres for genres in list_genres] 

        # Import de la base splitée par genres, déjà utilisée en visualisation
        df_genres_split = pd.read_csv("./data/data_genres_split.csv", sep = "\t")

        # Conversion en variable binaire, puis somme pour chaque film
        df_genres_split = pd.concat([df_genres_split,pd.get_dummies(df_genres_split['genres'], prefix='genre')],axis=1)

        df_one_hot = df_genres_split.groupby(["tconst"]).sum()
        df_one_hot.reset_index(level=0, inplace=True)

        # Jointure avec la base initiale, seules les colonnes "genres_" sont ajoutées
        df = pd.merge(df,df_one_hot[['tconst']+ list_columns], on = ["tconst"], how='left')

        return df 
    


    @classmethod
    def formule_score_film(cls, rank, rate, nb_votes):
        """Calcule le score d'un film

        Args:
            rank (int): rang du film
            rate (float): note du film
            nb_votes (int): nombre de votes qui ont constitué la note du film

        Returns:
            score (float): score d'un film selon la formule expliquée dans le notebook
        """
       
        score = (1/(rank))*(rate**2)*np.sqrt(nb_votes)  # Nombre de votes non pris en compte pour l'instant 

        return  score

    
    
    
    @classmethod
    def add_ranks_films(cls,df):
        """Ajoute à la dataframe la colonne du classement de chaque film selon sa note

        Args:
            df (pandas.core.frame.DataFrame): dataframe nettoyée

        Returns:
            df (pandas.core.frame.DataFrame): dataframe avec la colonne rank
        """
        
        
        # Création une copie de df sur laquelle on classe les observations selon la note du film de manière décroissante
        # (cad les films les mieux notés sont en premier)
        df_sort_rank = df.sort_values(["rate","votes"], ascending = False)
        df_sort_rank = df_sort_rank.reset_index()
        
        # Création du tableau rank de positions des films et insertion de rank en tant que colonne dans df_sort_rank
        rank = np.arange(1,len(df_sort_rank))
        df_rank = pd.DataFrame({'ranks' : rank }) 
        df_sort_rank["rank"] = 0    #UTILE ??
        df_sort_rank["rank"] = df_rank["ranks"]
        
        # merge de df avec df_sort_rank, de sorte à avoir df avec une colonne supplémentaire : le rang de chaque film
        df = pd.merge(df,df_sort_rank)
        df = df.drop('index', 1)

        return df
    
    
    @classmethod
    def add_scores_realisateurs(cls,df):
        """Ajoute à la dataframe la colonne du score du réalisateur

        Args:
            df (pandas.core.frame.DataFrame): dataframe qui contient le rang des films

        Returns:
            df (pandas.core.frame.DataFrame): dataframe avec la colonne score_realisateur
        """
        
        # On utilise la fonction de calcul du score définie precedemment :
        df["score_film"] = preprocessing_data.formule_score_film(df["rank"], df["rate"], df["votes"])
        
        # Somme des scores des films selon chaque réalisateur :
        list_sum_scores = df.groupby(["director"])["score_film"].sum().sort_values(ascending = False)

        # Transformation en pandas dataframe de deux colonnes : le nom du réalisateur et son score
        list_sum_scores = list_sum_scores.to_frame().reset_index()
        
        # Dans list_sum_scores, la colonne "score_film" est en fait la somme des scores des films groupés par réalisateur,
        # donc finalement le score de chaque réalisateur. On renomme alors :
        list_sum_scores = list_sum_scores.rename(columns={'score_film': 'score_realisateur'})
        
        # Jointure finale avec la base df pour y ajouter la colonne du score du réalisateur :
        df = pd.merge(df,list_sum_scores, on = ["director"])
        
    
        return df
    
    
    
    @classmethod
    def add_scores_acteurs(cls,df):
        """Ajoute à la dataframe la colonne du score de l'acteur

        Args:
            df (pandas.core.frame.DataFrame): dataframe nettoyée

        Returns:
            df (pandas.core.frame.DataFrame): dataframe avec la colonne score_acteur
        """
        
        # Somme des scores des films selon chaque acteur :
        list_sum_scores = df.groupby(["casting"])["score_film"].sum().sort_values(ascending = False)

        # Transformation en pandas dataframe de deux colonnes : le nom de l'acteur et son score
        list_sum_scores = list_sum_scores.to_frame().reset_index()
        
        # Dans list_sum_scores, la colonne "score_film" est en fait la somme des scores des films groupés par acteur, 
        # donc finalement le score de chaque acteur. On renomme alors :
        list_sum_scores = list_sum_scores.rename(columns={'score_film': 'score_acteur'})
        
        # Jointure finale avec la base df pour y ajouter la colonne du score de l'acteur :
        df = pd.merge(df,list_sum_scores, on = ["casting"])

        df.loc[df['casting'] == '', 'score_acteur'] = 0
        df['score_acteur'].fillna(0, inplace=True)  
    
        return df

    
    @classmethod
    def add_score_casting(cls,df):
        """[summary]

        Args:
            df (pandas.core.frame.DataFrame): dataframe avec les scores de chaque acteur

        Returns:
            df (pandas.core.frame.DataFrame): dataframe avec le score du casting (moyenne du score des acteurs)
        """
        
        # On groupe par tconst (unique pour chaque film) et on fait la moyenne du score des acteurs par film :
        df = df.groupby("tconst")["score_acteur"].mean().to_frame().reset_index()
    
        # On renomme la colonne score_acteur du resultat précédent qui est en fait désormais le score du casting :
        df.rename(columns = {"score_acteur" : "score_casting"}, inplace = True) 
        
        
        return df



    @classmethod
    def formation_base_finale(cls,df_genres, df_scores):
        """Forme la base finale

        Args:
            df (pandas.core.frame.DataFrame): 
        """

        df_final = pd.merge(df_genres, df_scores[['tconst', "score_realisateur", "score_casting"]], on = ["tconst"], how='left')
        
        df_final.dropna(subset=['score_casting', 'score_realisateur'], inplace = True)

        df_final.drop(columns=['tconst','title', 'genres', 'director', 'casting'], inplace = True)

        return df_final




        