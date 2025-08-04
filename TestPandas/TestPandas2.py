import pandas as pd
import numpy as np

datos = {'Nombre': ['Ana', 'Luis', 'Pedro'],
         'Edad': [23, 34, 45],
         'Ciudad': ['Madrid', 'Barcelona', 'Valencia'],
         'Salario': [30000, 40000, 50000],
         'Fecha_Ingreso': pd.to_datetime(['2020-01-01', '2019-05-15', '2018-07-20']),
         'Activo': [True, False, True],
         'telefono': ['123456789', '987654321', '456789123'],
         'email': ['anasita@gmail.com', 'luisillopillo@gmail.com', 'pedroprox@gmail.com']}

df = pd.DataFrame(datos)
# print(df.iloc[1:3,0:3])  # iloc sirve para acceder a filas y columnas por posicion
# print(df.loc[1:1,['Edad', 'Nombre']])  #loc sirve para acceder a filas y columnas por etiquetas 
# print(df.tail)# tail nos mostrara las ultimas 5 filas y head las primeras 5 filas del DataFrame info nos motrara informacion del DataFrame
# print(df.describe) # describe nos mostrara estadisticas de las columnas numericas del DataFrame
#filtrando valores
# print(df[df['Edad'] > 30])  # Filtra filas donde la edad es mayor a 30
# print(df[df['Ciudad'].str.contains('Madrid')])  # Filtra filas donde la ciudad contiene 'Madrid'
# print(df[df['Salario'].between(30000, 40000)])  # Filtra filas donde el salario está entre 30000 y 40000    
# Ordenando el DataFrame por Edad
# print(df.sort_values(by='Edad'))  # Ordena por la columna 'Edad'    
# Agrupando por Ciudad y calculando la media del Salario
# print(df.groupby('Ciudad')['Salario'].mean())  # Agrupa por 'Ciudad'