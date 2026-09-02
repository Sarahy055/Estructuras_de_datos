
import os
import sys


# ============================================================
# CONFIGURACIÓN
# ============================================================

FILAS = 100_000
COLUMNAS = 100_000

NOMBRE_ARCHIVO = "matriz_100000x100000.bin"

# Cada elemento de la matriz ocupa 1 bit.
# 100.000 bits = 12.500 bytes
BYTES_POR_FILA = (COLUMNAS + 7) // 8

# Se agrega 1 byte para el salto de línea \n
BYTES_POR_FILA_ARCHIVO = BYTES_POR_FILA + 1

# Tamaño total esperado del archivo
TAMANO_ESPERADO = FILAS * BYTES_POR_FILA_ARCHIVO


# ============================================================
# LEER UNA FILA
# ============================================================

def leer_fila(archivo, numero_fila):
    """
    Lee únicamente una fila de la matriz.

    No se carga todo el archivo en RAM.
    """

    # Calculamos la posición donde comienza la fila.
    posicion = numero_fila * BYTES_POR_FILA_ARCHIVO

    # Movemos el puntero directamente a esa posición.
    archivo.seek(posicion)

    # Leemos solamente los datos de la fila.
    datos = archivo.read(BYTES_POR_FILA)

    # Leemos el salto de línea que está después de la fila.
    salto = archivo.read(1)

    # Comprobamos que realmente sea \n.
    if salto != b"\n":
        raise ValueError(
            f"La fila {numero_fila} no tiene "
            f"el salto de línea esperado."
        )

    return datos


# ============================================================
# OBTENER UN BIT
# ============================================================

def obtener_bit(datos, columna):
    """
    Obtiene el valor de una posición de la fila.

    Cada elemento ocupa solamente 1 bit.
    """

    # Byte donde se encuentra el elemento.
    numero_byte = columna // 8

    # Posición del bit dentro del byte.
    posicion_bit = columna % 8

    # Obtenemos el byte.
    byte = datos[numero_byte]

    # Extraemos el bit.
    bit = (byte >> posicion_bit) & 1

    return bit


# ============================================================
# MOSTRAR UNA REGIÓN EN LA TERMINAL
# ============================================================

def mostrar_region(
    archivo,
    fila_inicial,
    fila_final,
    columna_inicial,
    columna_final
):
    """
    Muestra en pantalla solamente la región solicitada.
    """

    print()
    print("=" * 75)
    print("REGIÓN DE LA MATRIZ")
    print("=" * 75)

    print(f"Filas:    {fila_inicial} - {fila_final}")
    print(f"Columnas: {columna_inicial} - {columna_final}")

    print("=" * 75)

    # Se procesa una fila a la vez.
    for fila in range(fila_inicial, fila_final + 1):

        # Solo cargamos esta fila en memoria.
        datos = leer_fila(archivo, fila)

        resultado = ""

        # Extraemos únicamente las columnas solicitadas.
        for columna in range(
            columna_inicial,
            columna_final + 1
        ):
            bit = obtener_bit(datos, columna)
            resultado += str(bit)

        # El 1 después de la barra representa
        # visualmente el salto de línea de la fila.
        print(
            f"{fila:6} | {resultado} | 1"
        )


# ============================================================
# GUARDAR REGIÓN EN TXT
# ============================================================

def guardar_region_txt(
    archivo,
    fila_inicial,
    fila_final,
    columna_inicial,
    columna_final,
    nombre_txt="region_matriz.txt"
):
    """
    Guarda solamente la región solicitada
    en un archivo de texto.

    El 1 al final de cada fila representa
    visualmente el salto de línea/separador
    que existe en el archivo binario.
    """

    with open(
        nombre_txt,
        "w",
        encoding="utf-8"
    ) as salida:

        salida.write("MATRIZ DE 100000 x 100000\n")
        salida.write(
            f"Filas: {fila_inicial} - {fila_final}\n"
        )
        salida.write(
            f"Columnas: {columna_inicial} - {columna_final}\n"
        )
        salida.write("\n")

        for fila in range(
            fila_inicial,
            fila_final + 1
        ):

            # Solamente cargamos una fila.
            datos = leer_fila(archivo, fila)

            resultado = ""

            for columna in range(
                columna_inicial,
                columna_final + 1
            ):

                bit = obtener_bit(
                    datos,
                    columna
                )

                resultado += str(bit)

            # Se escribe un 1 al final de la fila
            # como representación visual del
            # salto de línea existente en el .bin.
            salida.write(
                f"{fila:6} | {resultado} | 1\n"
            )

    print()
    print(
        f"✓ Región guardada en: {nombre_txt}"
    )


# ============================================================
# VERIFICAR ARCHIVO
# ============================================================

def verificar_archivo():

    if not os.path.exists(NOMBRE_ARCHIVO):

        print(
            f"✗ No existe el archivo: "
            f"{NOMBRE_ARCHIVO}"
        )

        return False

    # Obtenemos el tamaño sin cargar el archivo.
    tamano_real = os.path.getsize(
        NOMBRE_ARCHIVO
    )

    print("Verificación del archivo")
    print("-" * 40)

    print(
        f"Tamaño esperado: "
        f"{TAMANO_ESPERADO:,} bytes"
    )

    print(
        f"Tamaño real:     "
        f"{tamano_real:,} bytes"
    )

    if tamano_real != TAMANO_ESPERADO:

        print(
            "✗ El tamaño del archivo "
            "es incorrecto."
        )

        return False

    print(
        "✓ El tamaño del archivo "
        "es correcto."
    )

    return True


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

def main():

    # --------------------------------------------------------
    # COMPROBAR ARGUMENTOS
    # --------------------------------------------------------

    if len(sys.argv) != 5:

        print()
        print("Uso:")
        print(
            "python leer_matriz.py "
            "fila_inicial fila_final "
            "columna_inicial columna_final"
        )

        print()
        print("Ejemplo:")
        print(
            "python leer_matriz.py "
            "0 9 0 39"
        )

        return

    # Convertimos los argumentos a números.
    fila_inicial = int(sys.argv[1])
    fila_final = int(sys.argv[2])

    columna_inicial = int(sys.argv[3])
    columna_final = int(sys.argv[4])


    # --------------------------------------------------------
    # VALIDAR FILAS
    # --------------------------------------------------------

    if not (
        0 <= fila_inicial
        <= fila_final
        < FILAS
    ):

        print(
            "✗ Las filas están fuera "
            "del rango permitido."
        )

        return


    # --------------------------------------------------------
    # VALIDAR COLUMNAS
    # --------------------------------------------------------

    if not (
        0 <= columna_inicial
        <= columna_final
        < COLUMNAS
    ):

        print(
            "✗ Las columnas están fuera "
            "del rango permitido."
        )

        return


    # --------------------------------------------------------
    # VERIFICAR ARCHIVO
    # --------------------------------------------------------

    if not verificar_archivo():
        return


    # --------------------------------------------------------
    # ABRIR ARCHIVO
    # --------------------------------------------------------

    with open(
        NOMBRE_ARCHIVO,
        "rb",
        buffering=1024 * 1024
    ) as archivo:

        # Mostrar la región en la terminal.
        mostrar_region(
            archivo,
            fila_inicial,
            fila_final,
            columna_inicial,
            columna_final
        )

        # Guardar la región en TXT.
        guardar_region_txt(
            archivo,
            fila_inicial,
            fila_final,
            columna_inicial,
            columna_final
        )


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":
    main()

