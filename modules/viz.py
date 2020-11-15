import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

class movies_viz:

    @classmethod
    def genres_count(cls, df):

        print('\033[1m' + str(len(df["genres"].unique())) + " genres sont présents dans la base :")

        return df.groupby("genres")["genres"].count().sort_values(ascending= False)

    @classmethod
    def genres_mean(cls,df, list_genres):
        df_genres_10 = df[df["genres"].isin(list_genres)].reset_index()
        means = df_genres_10.groupby("genres")["rate"].mean()
        return means


    @classmethod
    def genres_boxplot(cls, df, list_genres):

        df_genres = df[df["genres"].isin(list_genres)].reset_index()
        sns.set(rc={'figure.figsize':(13,8)}) # taille de la figure
        #sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 2.5})
        sns.set_style("whitegrid") #style du graphique 
        sns.boxplot(x="genres", y="rate", data = df_genres,
                    palette = "deep").set(xlabel = "Genres", ylabel = "Notations") #classés par genre, histogramme des rates
        sns.despine(bottom = True)
        plt.ylim([0,10.1])
        plt.title("Histogramme représentatif de la distribution des notes des films classés par genres", size=15)
        plt.show()


    @classmethod
    def runtime_hist(cls, df):
        
        ax = df.runtime.hist(bins=100, grid=False, figsize = (10,7),)
        ax.set_xlim((0,300))    #90 films font plus de 300 minutes, on ne les considère donc pas ici par souci de visibilité
        plt.xlabel('Durée (minutes)')
        ax.xaxis.set_major_locator(ticker.MultipleLocator(25))
        ax.xaxis.set_minor_locator(ticker.MultipleLocator(5))
        plt.ylabel('Nombre de films')
        plt.title("Distribution du nombre de films en fonction de leur durée")
        plt.show()


    @classmethod
    def rank_year(cls,df):

        sns.set(rc={'figure.figsize':(10,7)}) # taille de la figure
        # sns.set_style("whitegrid") # style du graphique 
        sns.lineplot(x="year", y="rate", data = df,
                    palette = "deep").set(xlabel = "Année", ylabel = "Notation") # classés par année, linechart des notes
        sns.despine(bottom = True)
        plt.title("Note moyenne des films par année, et intervalle à 95%", size=15)
        plt.show()

    @classmethod
    def corr_matrix(cls, df):

        df_corr = df[['year','runtime','rate','votes']]

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
