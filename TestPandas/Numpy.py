import numpy as np

ages = np.array([32, 28, 45, 19])
#calcular la media de las edades
print(np.mean(ages))
# Calcular la mediana de las edades
print(np.median(ages))
#calculo de percentiles
print(np.percentile(ages, 75))
print(" | ")
print(" | ")
#calcular el rango y varianza y covarianza
print("Rango:",np.ptp(ages))
print("Varianza:",np.var(ages))
print("Covarianza:",np.cov(ages))
#generacion de distribuciones aleatorias
print(" | ")
print(" | ")
print(np.random.normal(0, 1, 10))