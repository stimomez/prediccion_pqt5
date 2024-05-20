

from pyspark.sql.types import TimestampType
# Función auxiliar para reemplazar valores nulos en columnas de tipo Timestamp
def fill_nulls_with_mode(df, modes):
    for col_name, mode_value in modes.items():
        if df.schema[col_name].dataType == TimestampType():
            df = df.withColumn(col_name, F.when(F.col(col_name).isNull(), F.lit(mode_value).cast(TimestampType())).otherwise(F.col(col_name)))
        else:
            df = df.fillna({col_name: mode_value})
    return df

# Reemplazar los valores nulos con la moda correspondiente
df_filled = fill_nulls_with_mode(df, modes)

# Verificar que no haya valores nulos restantes
df_filled.show()

# Normalización

from pyspark.ml.feature import MinMaxScaler
from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import VectorAssembler

# Listar las columnas numéricas que quieres normalizar
numeric_cols = [col_name for col_name, dtype in df_filled.dtypes if dtype in ['int', 'double']]
numeric_cols.remove('dow_rate_consumo')

# Inicializar el VectorAssembler
assembler = VectorAssembler(inputCols=numeric_cols, outputCol="features")

# Transformar el DataFrame en un vector de características
df_vector = assembler.transform(df_filled)

# Inicializar el MinMaxScaler
scaler = MinMaxScaler(inputCol="features", outputCol="scaled_features")

# Ajustar el scaler al DataFrame y transformar los datos
scaler_model = scaler.fit(df_vector)
df_scaled = scaler_model.transform(df_vector)

# Seleccionar solo las columnas necesarias para el modelo
df_model = df_scaled.select("features", "dow_rate_consumo")

# Separación de pruebas y entrenamiento

# Dividir los datos en entrenamiento (80%) y prueba (20%)
# train_df, test_df = df_model.randomSplit([0.8, 0.2], seed=42)
train_df, test_df = df_model.randomSplit([0.2, 0.1], seed=42)

# Mostrar la cantidad de registros en cada conjunto
print("Cantidad de registros en el conjunto de entrenamiento:", train_df.count())
print("Cantidad de registros en el conjunto de prueba:", test_df.count())

# Entrenamiento del modelo
from pyspark.ml.regression import GBTRegressor

# Crear el modelo GBTRegressor
gbt = GBTRegressor(featuresCol="features", labelCol="dow_rate_consumo", maxIter=100)

# Entrenar el modelo
gbt_model = gbt.fit(train_df)

# Evaluación del modelo

from pyspark.ml.evaluation import RegressionEvaluator

# Hacer predicciones en los datos de prueba
predictions = gbt_model.transform(test_df)

# Crear un evaluador para medir la exactitud del modelo
evaluator = RegressionEvaluator(labelCol="dow_rate_consumo", predictionCol="prediction", metricName="rmse")

# Calcular el RMSE (Root Mean Squared Error)
rmse = evaluator.evaluate(predictions)
print(f"Root Mean Squared Error (RMSE) en los datos de prueba = {rmse}")

# Mostrar las predicciones
prediccion=predictions.select("dow_rate_consumo", "prediction", "features").show(10)
