import matplotlib.pyplot as plt
import pandas as pd
datos = {
    'Food': ['Pizza', 'Burger', 'Pasta', 'Pizza', 'Burger'],
    'Price': [10, 8, 12, 10, 8],
    'Quantity': [1, 2, 1, 2, 1],
    'Rating': [4.5, 4.0, 4.2, 4.5, 4.0] 
}
df = pd.DataFrame(datos)
print(df)
x_values = df['Food'].unique()
y_values = df['Food'].value_counts().tolist()
plt.bar(x_values, y_values)
plt.show()
plt.close('all')