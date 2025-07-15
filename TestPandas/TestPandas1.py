import pandas as pd
# Lectura de un archivo Excel con Pandas
# usa un archivo Excel como ejemplo :D
# Asegúrate de tener instalado el paquete openpyxl para leer archivos Excel
archive = r'' #Aqui se hizo con la ruta absoluta
df = pd.read_excel(archive, sheet_name='Hoja1',)
print(df)