import pandas as pd
import numpy as np
import transformers

# Concatiner des fichiers csv ont la même structure
df = pd.concat([
    pd.read_csv('./csv/Youtube01.csv'),
    pd.read_csv('./csv/Youtube02.csv'),
    pd.read_csv('./csv/Youtube03.csv'),
    pd.read_csv('./csv/Youtube04.csv'),
    pd.read_csv('./csv/Youtube05.csv')
])
# INE : 203318099BC
print(df)

# Infos du fichier
print(df.info())

# Compter la valeur de la ccolonne CLASS
print(df.CLASS.value_counts())

# avoir le pourcentage de chaque valeur d'une colonne
print(df.CLASS.value_counts(normalize=True))