# IMPRIME UN ARBOL DE NAVIDAD
#       *  
#     ***** 
#    *******
#   *********
#  ***********
tamano_arbol = 10
# formula: N*2+1
for fila in range(tamano_arbol):
    print("." * (tamano_arbol - fila - 1) + "*" * (fila * 2 + 1))