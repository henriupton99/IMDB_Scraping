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
    # CLASSE preprocessing_data : différentes fonctions requises dans le notebook consacré à la prépartion des données
    
    
    
    @classmethod
    def formule_score_film(cls, rank, rate, nb_votes):
        # Fonction formule_score_score_realisateur
        # Prend en argument le rang du film
        # Prend en argument la note du film
        # Prend en argument le nombre de votes qui ont constitué la note du film
        # Retourne le score d'un film selon la formule expliquée dans le notebook
        
        return (1/(rank))*(rate**2) # on prend pas encore le nb de votes pour l instant 

    
    
    
    @classmethod
    def add_ranks_films(cls,df):
        # Prend en argument une base de données df
        # Retourne df avec une colonne supplémentaire : le classement de chaque film selon sa note (rate)
        
        
        # On crée une copie de df sur laquelle on classe les observations selon la note du film de manière décroissante
        # (cad les films les mieux notés sont en premier)
        df_sort_rank = df.sort_values(["rate","votes"], ascending = False)
        df_sort_rank = df_sort_rank.reset_index()
        
        # Création du tableau rank de positions des films et insertion de rank en tant que colonne dans df_sort_rank
        rank = np.arange(1,len(df_sort_rank))
        df_rank = pd.DataFrame({'ranks' : rank }) 
        df_sort_rank["rank"] = 0
        df_sort_rank["rank"] = df_rank["ranks"]
        
        # merge de df avec df_sort_rank, de sorte à avoir df avec une colonne supplémentaire : le rang de chaque film
        df = pd.merge(df,df_sort_rank)
        
        #df = df.drop(['index'])
        
        return df
    
    
    @classmethod
    def add_scores_realisateurs(cls,df):
        # Prend en argument une base de données df qui contient la note, le rank, et le nombre de votes
        # Retourne df avec une colonne supplémentaire : le score du réalisateur (selon la formule expliquée dans le notebook)
        
        # On utilise la fonction de calcul du score définie precedemment :
        df["score_film"] = preprocessing_data.formule_score_film(df["rank"], df["rate"], df["votes"])
        
        # On fait la somme des scores des films selon chaque réalisateur :
        list_sum_scores = df.groupby(["director"])["score_film"].sum().sort_values(ascending = False)
        # Transformation en pandas dataframe de deux colonnes : le nom du réalisateur et son score
        list_sum_scores = list_sum_scores.to_frame().reset_index()
        
        # Dans list_sum_scores, la colonne "score_film" est en fait la somme des scores des films groupés par réalisateur,
        # donc finalement le score de chaque réalisateur. On rename alors :
        list_sum_scores = list_sum_scores.rename(columns={'score_film': 'score_realisateur'})
        
        # On peut finalement faire une jointure avec la base df pour ajouter sur df la colonne du score du réalisateur :
        df = pd.merge(df,list_sum_scores, on = ["director"])
        # df = df.drop(['index'])
    
        return df
    
    
    
    @classmethod
    def add_scores_acteurs(cls,df):
        # Fonction add_score_acteurs
        # Prend en argument une base de données df qui contient la note, le rank, et le nombre de votes
        # Retourne df avec une colonne supplémentaire : le score des acteurs (selon la formule expliquée dans le notebook)
        
        
        # On fait la somme des scores des films selon chaque acteur :
        list_sum_scores = df.groupby(["casting"])["score_film"].sum().sort_values(ascending = False)
        # Transformation en pandas dataframe de deux colonnes : le nom de l'acteur et son score
        list_sum_scores = list_sum_scores.to_frame().reset_index()
        
        # Dans list_sum_scores, la colonne "score_film" est en fait la somme des scores des films groupés par acteur, donc finalement le score de chaque acteur. Donc on rename :
        list_sum_scores = list_sum_scores.rename(columns={'score_film': 'score_acteur'})
        
        # On peut finalement faire une jointure avec la base df pour ajouter sur df la colonne du score de l'acteur :
        df = pd.merge(df,list_sum_scores, on = ["casting"])
        # df = df.drop(['index'])
    
        return df

    
    @classmethod
    def add_score_casting(cls,df):
        # Fonction add_score_casting
        # Prend en argument une base de données df qui contient le score de chaque acteur
        # Retourne df avec une colonne supplémentaire : le score du casting (la moyenne du score des acteurs)
        
        # On groupe par tconst (unique pour chaque film) et on fait la moyenne du score des acteurs par film :
        df = df.groupby("tconst")["score_acteur"].mean().to_frame().reset_index()
    
        # On renomme la colonne score_acteur du resultat précédent qui est en fait désormais le score du casting :
        df.rename(columns = {"score_acteur" : "score_casting"}, inplace = True) 
        
        
        
        return df
        