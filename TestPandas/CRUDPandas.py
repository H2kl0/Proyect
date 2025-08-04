import pandas as pd
datos = {
    'documento': [1, 2, 3],
    'nombre': ['Juan', 'Ana', 'Luis'],
    'edad': [25, 30, 22],
    'ciudad': ['Madrid', 'Barcelona', 'Valencia'],
    'deporte': ['Fútbol', 'Baloncesto', 'Tenis'],
    'puntuacion': [8.5, 9.0, 7.5]
}
df = pd.DataFrame(datos)
print(df)
# Actualizar el DataFrame con una nueva columna
telefono = pd.Series([123456789, 987654321, 456789123])
df['telefono'] = telefono
print(" | ")
print(df)
print(" | ")
# añadir un nuevo dato al DataFrame se mantiene igual y de detecta
telefono = pd.Series([123456789, 987654321, 4567891213])
#leer el DataFrame
print(" | ")
print(df['nombre'])
print(" | ")
#eliminar dataframe
del df['telefono']
print(df)