import findspark
from pyspark.sql import SparkSession
# import matplotlib.pyplot as plt
# import urllib.request

class PrediccionML:
    def __init__(self):
        findspark.init()
        self.spark = self.createInstanceSparkSession()
        
    def createInstanceSparkSession(self):
        # Crea una instancia de SparkSession
        return SparkSession.builder \
            .master("local[*]") \
            .appName("Google_Colab_PySpark") \
            .getOrCreate()
            
    def sparkReadCsv(self, filename):
        # Lee el archivo CSV desde el sistema de archivos local en Spark
        return self.spark.read.csv(filename, header=True, inferSchema=True, sep=',')