import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import plotly.express as px


##############################################################################################################
# Codage des différentes fonctions requises dans le notebook consacré à la visualisation des données
# Stockage de toutes ces fonctions dans la classe movie_viz qui sera importée dans le notebook de visualisation
##############################################################################################################

class split_method:
    # Classe pour la méthode de split des valeurs d'une colonne :
    
    @classmethod
    def split_elem_col(cls, data, col_name):
    # Fonction split_elem_col
    # Prend en argument data un dataframe
    # Prend en argument col_name le nom de la colonne ou l'on souhaite split les données
    # Retourne un dataframe sur lesquels les éléments de la colonne concernée sont split
        
        
        s = data[col_name].str.split(',').apply(pd.Series, 1).stack()
        s.index = s.index.droplevel(-1)
        s.name = col_name
        del data[col_name]
        df_res = data.join(s)
        
        return df_res






class movies_viz:
    # CLASSE movie_viz : différentes fonctions requises dans le notebook consacré à la visualisation des données
    
    @classmethod
    def runtime_hist(cls, df):
        # Fonction runtime_hist
        # Prend en argument une base de données df
        # Retourne un histogramme représentatif de la distribution du nombre de films en fonction de leur durée
        
        # Définition de la figure :
        ax = df.runtime.hist(bins=100, grid=False, figsize = (10,7),)
        
        # 90 films font plus de 300 minutes, on ne les considère donc pas ici par souci de visibilité :
        ax.set_xlim((0,300))
        
        # Set des labels et paramétrage pour les axes :
        plt.xlabel('Durée (minutes)')
        ax.xaxis.set_major_locator(ticker.MultipleLocator(25))
        ax.xaxis.set_minor_locator(ticker.MultipleLocator(5)) 
        plt.ylabel('Nombre de films')
        
        # Fixation du titre du graphique :
        plt.title("Distribution du nombre de films en fonction de leur durée") 
        
        # Affichage visuel du graphique :
        plt.show()


    @classmethod
    def plotly_barplot(cls,df):
        fig = px.histogram(df, x='runtime')
        fig.show()

    
        
        
    @classmethod
    def rank_year(cls,df):
        # Fonction rank_year
        # Prend en argument une base de données df
        # Retourne une courbe représentative de l'évolution de la note moyenne des films par année
        
        # Définition de la taille de la figure :
        sns.set(rc={'figure.figsize':(10,7)})
        
        # Génération du graphique d'intérêt :
        sns.lineplot(x="year", # Evolution au fil des années
                     y="rate", # de la note moyenne 
                     data = df, # dans la base de données
                    palette = "deep").set(xlabel = "Année", ylabel = "Notation") # classés par année, linechart des notes
        
        # Paramètre graphique de seaborn :
        sns.despine(bottom = True)
        
        # Fixation du titre du graphique :
        plt.title("Note moyenne des films par année, et intervalle à 95%", size=15)
        
        # Affichage visuel du graphique :
        plt.show()

    
    @classmethod
    def genres_count(cls, df):
        # Fonction genres_count
        # Prend en argument une base de données df
        # Affiche le nombre de genres présents dans la base df
        # Retourne le nombre de films par genres présents dans la base df
    
        # Affichage du nombre de genres distincts présents dans la base df :
        print('\033[1m' + str(len(df["genres"].unique())) + " genres sont présents dans la base :")
        
        return df.groupby("genres")["genres"].count().sort_values(ascending= False)

    
    
    
    @classmethod
    def genres_means(cls,df, list_genres):
        # Fonction genres_mean
        # Prend en argument une base de données df
        # Prend en argument une liste de genres de films list_genres
        # Retourne la liste des notes moyennes pour chaque genres de la liste
        
        # On conserve uniquement les films dont le genre est dans la liste list_genres et on les stocke dans df_genres :
        df_genres = df[df["genres"].isin(list_genres)].reset_index()
       
        # Calcul de la moyenne des votes par genres et stockage dans la variable means :
        means = df_genres.groupby("genres")["rate"].mean()
        
        return means


    
    
    @classmethod
    def genres_boxplot(cls, df, list_genres):
        # Fonction genres_boxplot
        # Prend en argument une base de données df
        # Prend en argument une liste de genres de films list_genres
        # Retourne des boites à moustaches représentatives de la distribution des notes des films groupés par genres
        
        # On conserve uniquement les films pour lesquels le genre est dans list_genres et on les stocke dans df_genres :
        df_genres = df[df["genres"].isin(list_genres)].reset_index()
        
        # Paramètre de taille de la figure de seaborn :
        sns.set(rc={'figure.figsize':(13,8)})
        
        # Style du graphique :
        sns.set_style("whitegrid")
        
        # Génération du graphique d'intérêt :
        sns.boxplot(x="genres", # Groupement par genres 
                    y="rate", # Distribution des notes
                    data = df_genres, # Base de données des genres d'intérêt
                    palette = "deep").set(xlabel = "Genres", ylabel = "Notations") # palette de couleurs
        
        # Paramètre graphique de seaborn :
        sns.despine(bottom = True)
        
        # Fixation de la limite d'affichage des notes
        plt.ylim([0,10.1])
        
        # Ajout du titre au graphique
        plt.title("Boîtes à moustaches représentatives de la distribution des notes des films groupés par genres", size=15)
        
        # Affichage visuel de la figure paramètrée :
        plt.show()

        
        
        
    @classmethod
    def corr_matrix(cls, df):
        # Fonction corr_matrix
        # Prend en argument une base de données df
        # Retourne la matrice de corrélation entre les variables d'intérêts
        
        # Sous base de df avec uniquement les variables d'intérêt
        df_corr = df[["year","runtime","rate","votes"]]

        # Calcul de la matrice de corrélation
        corr = df_corr.corr()

        # Génération d'un masque pour n'afficher que le triangle inférieur
        mask = np.zeros_like(corr)
        mask[np.triu_indices_from(mask)] = True

        # Généation d'une palette de couleur adéquate
        cmap = sns.diverging_palette(230, 20, as_cmap=True)

        # Plot de la heatmap
        with sns.axes_style("white"):
            plt.subplots(figsize=(7, 5))
            sns.heatmap(corr, mask=mask, cmap = cmap, annot=True, square=True)

    
    @classmethod
    def pairplot(cls,df):
        df_corr = df[['year','runtime','rate','votes']]
        sns.pairplot(df_corr, corner = True)
