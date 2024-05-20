import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

class AnalisisExploratorio:
    def __init__(self, dataframe,columnas):
        self.df = dataframe
        self.columnas=columnas

    def mostrar_primeras_filas(self, n=5):
        return self.df[self.columnas].head(n).to_string()
    

    def resumen_estadistico(self):
        print("\nResumen estadístico de las columnas numéricas:")
        return self.df[self.columnas].describe().to_string()

 
    def plot_distributions(self):
        numeric_columns = self.df.select_dtypes(include=['float64', 'int64']).columns
        for col in numeric_columns:
            plt.figure(figsize=(10, 5))
            sns.histplot(self.df[col].dropna(), kde=True)
            plt.title(f'Distribución de {col}')
            plt.show()

        categorical_columns = self.df.select_dtypes(include=['object']).columns
        for col in categorical_columns:
            plt.figure(figsize=(10, 5))
            sns.countplot(y=self.df[col].dropna())
            plt.title(f'Distribución de {col}')
            plt.show()

  

    def valores_nulos(self):
        valores_nulos = self.df[self.columnas].isnull().sum()
        return  valores_nulos.to_string()

    