import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pyspark.sql.functions import col

class AnalisisExploratorio:
    def __init__(self, dataframe,columnas):
        self.df = dataframe
        self.columnas=columnas




    def mostrar_primeras_filas(self, n=5):
        filas = self.df.select(self.columnas).limit(n).collect()
        row_data =filas[0]        
        # Convertir la fila en un diccionario
        encabezado = row_data.asDict() 
        #    columns=column_names
        dataFramePanda=pd.DataFrame(filas,columns=encabezado.keys())
        return dataFramePanda.to_string()
    

    def resumen_estadistico(self):
        # return self.df[self.columnas].describe().to_string()
        # Obtener un resumen estadístico del DataFrame
        resumen = self.df[self.columnas].describe()

        # Convertir el resumen estadístico a un DataFrame de Pandas
        resumen_pandas = resumen.toPandas()

        # Convertir el DataFrame de Pandas a una cadena
        resumen_cadena = resumen_pandas.to_string()
        
        return resumen_cadena


 
   

  

    def valores_nulos(self):
        # Contar los valores nulos en la columna 'nombre_columna'
        valores_nulos = self.df.where(col('OID').isNull()).count()
        print(valores_nulos)
        ## Verificar valores nulos en las columnas especificadas
        valores_nulos = {col: self.df.filter(self.df[col].isNull()).count() for col in self.columnas}
   
        # Convertir el diccionario en una cadena formateada
        texto_valores_nulos = "\n".join([f"{col}: {num_nulos}" for col, num_nulos in valores_nulos.items()])

        
        return  texto_valores_nulos

    