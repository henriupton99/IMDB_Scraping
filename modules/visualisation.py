import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import plotly.graph_objects as go


###################################################################################################################
# Codage des différentes fonctions requises dans le notebook consacré à la visualisation des données
# Stockage de toutes ces fonctions dans les classes split_method & movie_viz qui seront importées dans le notebook
###################################################################################################################

class split_method:
    
    @classmethod
    def split_elem_col(cls, data, col_name):
        """Splite une dataframe selon une colonne. Exemple : si on trouve "Comedy, Romance" dans la colonne genres, 
           crée deux lignes avec "Comedy" et "Romance".

        Args:
            data (pandas.core.frame.DataFrame): dataframe nettoyée
            col_name (string): nom de la colonne où l'on souhaite split les données

        Returns:
            df_res (pandas.core.frame.DataFrame): dataframe sur lesquels les éléments de la colonne concernée sont split
        """        
        
        s = data[col_name].str.split(',').apply(pd.Series, 1).stack()
        s.index = s.index.droplevel(-1)
        s.name = col_name
        del data[col_name]
        df_res = data.join(s)
        
        return df_res






class movies_viz:
   
    @classmethod
    def plotly_histo(cls,df, bins_size = 5):
        """Renvoie l'histogramme de la distribution de la durée des films 

        Args:
            data (pandas.core.frame.DataFrame): dataframe nettoyée
            bins_size (int): largeur des barres
        """

        # Création de la figure
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=df["runtime"], xbins_size = bins_size))

        # Esthétique
        fig.update_layout(height = 400,
                                yaxis_title = "Nombre de films",
                                yaxis_title_font = {'size' : 17, 'family': 'Helvetica Neue'},
                                yaxis_tickfont = {'size': 14, 'family': 'Helvetica Neue'},
                                xaxis_title = "Durée du film (minutes)",
                                xaxis_range = [0,300],
                                xaxis_title_font = {'size' : 17, 'family': 'Helvetica Neue'},
                                xaxis_tickfont = {'size': 14, 'family': 'Helvetica Neue'},
                                showlegend=False,
                        bargroupgap = 0.1)
        fig.show()

    
        
        
    @classmethod
    def rank_year(cls,df):
        """Retourne une courbe représentative de l'évolution de la note moyenne des films par année

        Args:
            df (pandas.core.frame.DataFrame): dataframe nettoyée
        """
    
        # Taille de la figure :
        sns.set(rc={'figure.figsize':(10,7)})
        
        # Génération du graphique :
        sns.lineplot(x="year",
                     y="rate", 
                     data = df,
                    palette = "deep").set(xlabel = "Année", ylabel = "Notation")
        
        # Paramètre graphique de seaborn :
        sns.despine(bottom = True)
        
        # Titre du graphique :
        plt.title("Note moyenne des films par année, et intervalle à 95%", size=15)
        
        plt.show()

    
    @classmethod
    def genres_count(cls, df):
        """Affiche le nombre de genres présents dans la base df

        Args:
            df (pandas.core.frame.DataFrame): dataframe splitée
        """
    
        print('\033[1m' + str(len(df["genres"].unique())) + " genres sont présents dans la base :")
        
        return df.groupby("genres")["genres"].count().sort_values(ascending= False)

    
    
    
    @classmethod
    def genres_means(cls,df, list_genres):
        """Retourne la liste des notes moyennes pour chaque genres de la liste

        Args:
            df (pandas.core.frame.DataFrame): dataframe splitée
            list_genres (list): liste de genres

        Returns:
            means (pandas.core.series.Series): Notes moyennes pour chaque genre
        """
        
        # On conserve uniquement les films dont le genre est dans la liste list_genres et on les stocke dans df_genres :
        df_genres = df[df["genres"].isin(list_genres)].reset_index()
       
        # Calcul de la moyenne des votes par genres et stockage dans la variable means :
        means = df_genres.groupby("genres")["rate"].mean()

        return means


    
    
    @classmethod
    def genres_boxplot(cls, df, list_genres):
        """Retourne des boites à moustaches représentatives de la distribution des notes des films groupés par genres

        Args:
            df (pandas.core.frame.DataFrame): dataframe splitée
            list_genres (list): liste de genres
        """
        
        # On conserve uniquement les films pour lesquels le genre est dans list_genres et on les stocke dans df_genres :
        df_genres = df[df["genres"].isin(list_genres)].reset_index()
        
        # Paramètre de taille de la figure seaborn :
        sns.set(rc={'figure.figsize':(13,8)})
        
        # Style du graphique :
        sns.set_style("whitegrid")
        
        # Génération du graphique :
        sns.boxplot(x="genres",
                    y="rate",
                    data = df_genres,
                    palette = "deep").set(xlabel = "Genres", ylabel = "Notations") # palette de couleurs
        
        # Paramètre graphique :
        sns.despine(bottom = True)
        
        # Limite d'affichage des notes
        plt.ylim([0,10.1])
        
        # Titre au graphique
        plt.title("Boîtes à moustaches représentatives de la distribution des notes des films groupés par genres", size=15)
        
        # Affichage
        plt.show()

        
        
        
    @classmethod
    def corr_matrix(cls, df):
        """Retourne la matrice de corrélation entre les variables d'intérêts

        Args:
            df (pandas.core.frame.DataFrame): dataframe nettoyée
        """
        
        # Sous-base de df avec uniquement les variables d'intérêt
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
        """Génère le pairplot seaborn

        Args: 
        df (pandas.core.frame.DataFrame): dataframe nettoyée
            
        """
        
        df_corr = df[['year','runtime','rate','votes']]
        sns.pairplot(df_corr, corner = True)
