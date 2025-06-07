from collections import Counter
import string

def limpiar_palabra(palabra):
    return palabra.lower().strip(string.punctuation)

def analizar_texto(contenido):
    palabras = contenido.split()
    total_palabras = len(palabras)
    total_caracteres = len(contenido)
    lineas = contenido.count('\n') + 1

    # Contar frecuencia de palabras
    palabras_limpias = [limpiar_palabra(p) for p in palabras]
    frecuencia_palabras = Counter(palabras_limpias)

    return {
        "total_palabras": total_palabras,
        "total_caracteres": total_caracteres,
        "lineas": lineas,
        "frecuencia_palabras": frecuencia_palabras.most_common(10)
    }

def mostrar_resultados(resultado):
    print(f"\nTotal de palabras: {resultado['total_palabras']}")
    print(f"Total de caracteres: {resultado['total_caracteres']}")
    print(f"Número de líneas: {resultado['lineas']}")
    print("\nTop 10 palabras más usadas:")
    for palabra, count in resultado['frecuencia_palabras']:
        print(f"- {palabra}: {count}")

def main():
    ruta_archivo = input("Introduce la ruta del archivo de texto: ")
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
        resultado = analizar_texto(contenido)
        mostrar_resultados(resultado)
    except FileNotFoundError:
        print("Archivo no encontrado.")

main()
