
import os

# ============================================================
# CONFIGURACIÓN DE LA MATRIZ
# ============================================================

FILAS = 100_000
COLUMNAS = 100_000

NOMBRE_ARCHIVO = "matriz_100000x100000.bin"

# Cada elemento ocupa 1 bit.
# 100.000 bits = 12.500 bytes
BYTES_POR_FILA = (COLUMNAS + 7) // 8

# Se agrega 1 byte para el salto de línea \n
BYTES_POR_FILA_ARCHIVO = BYTES_POR_FILA + 1

# Tamaño esperado del archivo
TAMANO_ESPERADO = FILAS * BYTES_POR_FILA_ARCHIVO


# ============================================================
# CREACIÓN DE UNA FILA
# ============================================================

# Una fila inicialmente contiene solamente ceros.
# bytes(n) crea n bytes con valor 0.
FILA_CEROS = bytes(BYTES_POR_FILA) + b"\n"


# ============================================================
# CREACIÓN DEL ARCHIVO
# ============================================================

def crear_matriz():

    print("Creando matriz...")
    print(f"Dimensiones: {FILAS} x {COLUMNAS}")
    print(f"Bytes de datos por fila: {BYTES_POR_FILA}")
    print(f"Bytes por fila incluyendo salto de línea: "
          f"{BYTES_POR_FILA_ARCHIVO}")
    print(f"Tamaño esperado: {TAMANO_ESPERADO:,} bytes")
    print()

    # Se escribe directamente en disco.
    # No se crea la matriz completa en RAM.
    with open(NOMBRE_ARCHIVO, "wb", buffering=1024 * 1024) as archivo:

        # Escribimos por bloques para disminuir la cantidad
        # de operaciones de escritura al disco.
        FILAS_POR_BLOQUE = 1024

        bloque = FILA_CEROS * FILAS_POR_BLOQUE

        filas_escritas = 0

        while filas_escritas + FILAS_POR_BLOQUE <= FILAS:

            archivo.write(bloque)
            filas_escritas += FILAS_POR_BLOQUE

            if filas_escritas % 10_240 == 0:
                porcentaje = (filas_escritas / FILAS) * 100
                print(f"Progreso: {porcentaje:.1f}%")

        # Escribir las filas que sobren
        filas_restantes = FILAS - filas_escritas

        if filas_restantes > 0:
            archivo.write(FILA_CEROS * filas_restantes)

    # ========================================================
    # VERIFICACIÓN DEL TAMAÑO
    # ========================================================

    tamano_real = os.path.getsize(NOMBRE_ARCHIVO)

    print()
    print("Archivo creado.")
    print(f"Tamaño real:     {tamano_real:,} bytes")
    print(f"Tamaño esperado: {TAMANO_ESPERADO:,} bytes")

    if tamano_real == TAMANO_ESPERADO:
        print("✓ El tamaño del archivo es correcto.")
    else:
        print("✗ El tamaño del archivo NO coincide.")


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":
    crear_matriz()

