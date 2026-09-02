# Laboratorio 1 - Almacenamiento y lectura de una matriz de 100.000 x 100.000

**Estudiante:** Sarahy Paulina Cardales Acevedo

## 1. Descripción del laboratorio

El objetivo de este laboratorio es resolver el problema de crear, almacenar, manipular y leer una matriz de **100.000 filas por 100.000 columnas**, teniendo en cuenta principalmente el consumo de memoria RAM, la velocidad de escritura en disco y la eficiencia durante la lectura de los datos.

Una matriz de estas dimensiones contiene:

100.000 × 100.000 = 10.000.000.000 elementos

Es decir, contiene **10 mil millones de elementos**.

Si cada elemento se almacenara como un entero convencional, el espacio necesario sería muy grande. Además, intentar crear toda la matriz como una estructura de Python en memoria produciría un consumo excesivo de RAM.

Por esta razón, la solución utiliza una representación binaria en la que cada elemento de la matriz ocupa solamente **1 bit**.


# 2. Estructura del repositorio

El repositorio contiene los siguientes archivos:

- Laboratorio1/
-crear_matriz.py
-leer_matriz.py
-README.md
-.gitignore
-matriz_100000x100000.bin
-region_matriz.txt


### `crear_matriz.py`

Se encarga de crear el archivo que representa la matriz de 100.000 × 100.000.
La matriz se escribe directamente en disco y no se crea completa en memoria RAM.

### `leer_matriz.py`

Permite consultar solamente una región determinada de la matriz.

El usuario puede indicar:

* fila inicial
* fila final
* columna inicial
* columna final

El programa busca directamente las filas solicitadas y solamente carga esas filas en memoria.
También genera el archivo `region_matriz.txt`, que permite visualizar fácilmente el fragmento consultado.

### `matriz_100000x100000.bin`

Es el archivo que contiene físicamente la matriz.
La matriz está almacenada de manera binaria para reducir considerablemente el espacio utilizado.

### `region_matriz.txt`

Es un archivo de evidencia que contiene únicamente el fragmento de la matriz que se solicitó visualizar. No contiene la matriz completa.


# 3. Representación de la matriz

La matriz tiene las siguientes dimensiones:

Filas:    100.000
Columnas: 100.000

Por lo tanto: 100.000 × 100.000 = 10.000.000.000 elementos

Como cada elemento solamente puede tener los valores `0` o `1`, no es necesario utilizar un byte completo para cada elemento.

Se utiliza **1 bit por elemento**.

Por lo tanto, una fila de 100.000 elementos necesita: 100.000 / 8 = 12.500 bytes
Cada fila ocupa entonces: 12.500 bytes de datos


# 4. Almacenamiento físico del archivo

Aunque conceptualmente se está trabajando con una matriz de dos dimensiones, el archivo en disco se almacena de forma secuencial.

Es decir, físicamente se tiene una estructura similar a:

[Fila 0][salto de línea]
[Fila 1][salto de línea]
[Fila 2][salto de línea]
...
[Fila 99999][salto de línea]


Cada fila contiene:

12.500 bytes de datos + 1 byte de salto de línea

Por lo tanto: 12.501 bytes por fila


El salto de línea utilizado es: \n
y ocupa un byte porque el archivo se abre en modo binario.


# 5. ¿Por qué se utiliza un salto de línea?

El salto de línea permite mantener una separación física entre las filas del archivo.
De esta manera, además de conocer las dimensiones de la matriz, se puede verificar que después de los datos correspondientes a cada fila exista el delimitador esperado.

La estructura de una fila es:

[12.500 bytes de datos][\n]

En el código, el salto de línea se escribe mediante:
b"\n"


Por ejemplo:
FILA_CEROS = bytes(BYTES_POR_FILA) + b"\n"


Al leer una fila, el programa también comprueba que el siguiente byte sea realmente el salto de línea:


salto = archivo.read(1)

if salto != b"\n":
    raise ValueError(
        "La fila no tiene el salto de línea esperado."
    )

De esta forma, el salto de línea no solamente se agrega al archivo, sino que también se verifica durante la lectura.


# 6. Tamaño del archivo

Cada fila ocupa:


12.500 bytes de datos + 1 byte de salto de línea =
12.501 bytes


Como existen 100.000 filas:
100.000 × 12.501
= 1.250.100.000 bytes


Por lo tanto, el archivo utiliza aproximadamente:
1,16 GiB

La fórmula utilizada en el programa es:


BYTES_POR_FILA = (COLUMNAS + 7) // 8

BYTES_POR_FILA_ARCHIVO = BYTES_POR_FILA + 1

TAMANO_ESPERADO = FILAS * BYTES_POR_FILA_ARCHIVO


Esto permite calcular el tamaño esperado sin necesidad de crear la matriz en RAM.

El programa también obtiene el tamaño real del archivo mediante:
os.path.getsize(NOMBRE_ARCHIVO)

y compara el tamaño real con el tamaño esperado.


# 7. ¿Por qué no se almacena cada elemento como un entero?

Una alternativa sencilla sería guardar cada `0` y `1` utilizando un byte completo. Sin embargo, esto desperdiciaría espacio porque solamente se necesitan dos estados.

En la solución propuesta:

1 elemento = 1 bit


Por ejemplo, ocho elementos: 0 1 1 0 1 0 0 1

pueden almacenarse dentro de un único byte. Esto permite reducir considerablemente el espacio utilizado.

# 8. Manipulación de bits

Para encontrar un elemento determinado de una fila se utilizan dos operaciones:

numero_byte = columna // 8
posicion_bit = columna % 8


La división entera permite determinar en qué byte se encuentra el elemento.
El módulo permite determinar qué bit dentro de ese byte corresponde a la columna.

Después se extrae el bit mediante:
bit = (byte >> posicion_bit) & 1

Por lo tanto, no es necesario convertir toda la fila en una lista de números.


# 9. Cómo se evita cargar toda la matriz en RAM

La matriz completa contiene:
10.000.000.000 elementos

Por lo tanto, cargarla completa en RAM sería muy costoso, la solución evita hacerlo. En lugar de ejecutar algo como: datos = archivo.read()

que intentaría leer todo el archivo, se utiliza:

archivo.seek(posicion)
datos = archivo.read(BYTES_POR_FILA)

`seek()` permite mover el puntero del archivo directamente hasta la posición donde comienza la fila que se necesita.

Después solamente se lee esa fila.

Por ejemplo, si se solicita la fila 50.000, no es necesario cargar las filas 0 a 49.999.

El programa calcula directamente: posicion = numero_fila * BYTES_POR_FILA_ARCHIVO

y se desplaza hasta esa posición.

De esta manera, la cantidad de datos cargados en RAM durante la lectura es mucho menor que el tamaño completo de la matriz.


# 10. Cómo se obtiene una fila específica

Para obtener una fila se calcula:

posicion = numero_fila * BYTES_POR_FILA_ARCHIVO


Por ejemplo, conceptualmente:

Fila 0:posición = 0 × 12.501

Fila 1: posición = 1 × 12.501

Fila 2: posición = 2 × 12.501

...

Fila 50.000: posición = 50.000 × 12.501


Después se utiliza: archivo.seek(posicion)


para llegar directamente a esa fila.

Se leen los 12.500 bytes correspondientes a los datos y posteriormente un byte adicional para verificar el salto de línea.

# 11. Creación de la matriz

Para crear la matriz se ejecuta desde la terminal: python crear_matriz.py

El programa crea:
matriz_100000x100000.bin


Inicialmente la matriz contiene ceros.

El archivo se crea directamente en disco, por lo que no es necesario construir una matriz de 100.000 × 100.000 en RAM.

Durante la creación también se calcula el tamaño esperado y se compara con el tamaño real del archivo.


# 12. Visualización de la matriz

Debido a que la matriz es demasiado grande para mostrarla completa de forma razonable, la solución permite consultar solamente un fragmento.

El usuario indica cuatro valores:

fila_inicial
fila_final
columna_inicial
columna_final

Por ejemplo: python leer_matriz.py 0 9 0 39

Esto significa:

Filas: 0 hasta 9
Columnas:0 hasta 39


Por lo tanto, se está solicitando una región de:
10 filas × 40 columnas

El programa no lee toda la matriz.

Lee una fila, obtiene las columnas solicitadas, muestra el resultado y continúa con la siguiente fila.

El archivo se almacena en formato binario para reducir el espacio utilizado. La matriz no se almacena como una cadena de caracteres, sino como bits empaquetados por filas. Para verificar visualmente su contenido se utiliza region_matriz.txt, que muestra las regiones solicitadas de la matriz.

# 13. Ejemplo de extracción de un fragmento

Si se ejecuta: python leer_matriz.py 0 9 0 39


el programa obtiene:
Filas: 0 - 9
Columnas: 0 - 39


La salida puede verse de la siguiente manera:

     0 | 0000000000000000000000000000000000000000 | 1
     1 | 0000000000000000000000000000000000000000 | 1
     2 | 0000000000000000000000000000000000000000 | 1
     3 | 0000000000000000000000000000000000000000 | 1
     4 | 0000000000000000000000000000000000000000 | 1
     5 | 0000000000000000000000000000000000000000 | 1
     6 | 0000000000000000000000000000000000000000 | 1
     7 | 0000000000000000000000000000000000000000 | 1
     8 | 0000000000000000000000000000000000000000 | 1
     9 | 0000000000000000000000000000000000000000 | 1

La primera parte indica el número de fila.

La secuencia de `0` y `1` corresponde a las columnas solicitadas.

El `1` que aparece después de la segunda barra:
| 1

representa visualmente el salto de línea que delimita esa fila en el archivo.

Es importante aclarar que ese `1` **no es un elemento adicional de la matriz**. Es solamente una representación visual del delimitador de fila.

En el archivo binario el delimitador continúa siendo: \n

# 14. Archivo `region_matriz.txt`

Además de mostrar el fragmento en la terminal, el programa genera: region_matriz.txt
Este archivo contiene únicamente la región solicitada.

Por ejemplo:

MATRIZ DE 100000 x 100000
Filas: 0 - 9
Columnas: 0 - 39

     0 | 0000000000000000000000000000000000000000 | 1
     1 | 0000000000000000000000000000000000000000 | 1
     2 | 0000000000000000000000000000000000000000 | 1
     3 | 0000000000000000000000000000000000000000 | 1
     4 | 0000000000000000000000000000000000000000 | 1
     5 | 0000000000000000000000000000000000000000 | 1
     6 | 0000000000000000000000000000000000000000 | 1
     7 | 0000000000000000000000000000000000000000 | 1
     8 | 0000000000000000000000000000000000000000 | 1
     9 | 0000000000000000000000000000000000000000 | 1


Este archivo se utiliza principalmente como evidencia de que la matriz puede ser leída y visualizada.
No se utiliza el TXT para almacenar la matriz completa, ya que hacerlo aumentaría considerablemente el tamaño del archivo.

La matriz real continúa siendo:
matriz_100000x100000.bin


# 15. ¿Cómo solicitar diferentes fragmentos?

Se pueden solicitar diferentes regiones simplemente cambiando los argumentos del comando.

### Primeras 10 filas y 40 columnas
python leer_matriz.py 0 9 0 39

### Filas 100 a 109 y columnas 200 a 239
python leer_matriz.py 100 109 200 239

### Región cercana al centro de la matriz
python leer_matriz.py 49995 50005 49995 50005

### Región cercana al final
python leer_matriz.py 99990 99999 99960 99999


En todos los casos solamente se leen las filas necesarias.


# 16. Verificación de los límites

El programa verifica que las filas solicitadas estén dentro de: 0 ≤ fila < 100.000
y que las columnas estén dentro de: 0 ≤ columna < 100.000


Por ejemplo, una solicitud válida sería: python leer_matriz.py 0 9 0 39 ,

pero una solicitud como: python leer_matriz.py 0 100000 0 39 no es válida porque la fila 100.000 no existe.

La última fila es: 99.999
y la última columna también es:99.999


# 17. Verificación del salto de línea

Cuando se lee una fila, el programa realiza dos lecturas:

datos = archivo.read(BYTES_POR_FILA)
salto = archivo.read(1)


La primera obtiene los datos de la fila.
La segunda obtiene el byte correspondiente al salto de línea.

Posteriormente se comprueba:
if salto != b"\n":
    raise ValueError(...)

Esto permite detectar si la estructura esperada del archivo se ha alterado.


# 18. Verificación del tamaño

Antes de realizar una lectura, `leer_matriz.py` comprueba que el archivo exista.

Después obtiene su tamaño mediante:
os.path.getsize(NOMBRE_ARCHIVO)

y lo compara con:
1.250.100.000 bytes

Si los tamaños coinciden, se muestra:
 "El tamaño del archivo es correcto."

De esta manera se puede comprobar que el archivo corresponde a las dimensiones esperadas.

- Estructura de las filas y delimitación

La matriz se almacena físicamente en el archivo binario de forma secuencial, pero se interpreta lógicamente como una matriz de dos dimensiones. Cada fila contiene los 100.000 elementos almacenados como bits, ocupando 12.500 bytes, y al final de cada fila se agrega un byte correspondiente al salto de línea \n.

Por lo tanto, cada fila ocupa exactamente 12.501 bytes dentro del archivo:

[12.500 bytes de datos][\n]

Esta estructura permite conocer directamente la posición de cualquier fila sin tener que recorrer todo el archivo. Para acceder a una fila determinada, se calcula su posición mediante:

posición = número_de_fila × 12.501

El programa utiliza seek() para desplazarse directamente hasta esa posición. Después de leer los 12.500 bytes correspondientes a los datos de la fila, lee un byte adicional y verifica que sea \n. De esta manera, además de localizar la fila solicitada, se comprueba que el delimitador se encuentre correctamente ubicado.

Por ejemplo, para acceder a la fila 2:

posición = 2 × 12.501 = 25.002 bytes

El programa se desplaza directamente a esa posición y lee la fila correspondiente, sin necesidad de cargar las filas anteriores en memoria.

Esta estructura permite mantener el archivo físicamente secuencial y, al mismo tiempo, realizar un acceso eficiente a las filas de la matriz.

# 19. Archivo .gitignore y generación de la matriz

El archivo .gitignore se utiliza para indicarle a Git qué archivos no deben ser incluidos ni enviados al repositorio de GitHub. En este proyecto se configuró para ignorar el archivo matriz_100000x100000.bin, debido a que contiene la matriz de 100000 × 100000 y tiene un tamaño aproximado de 1.2 GB, superando el límite permitido para un archivo individual en GitHub.
La matriz binaria sí se encuentra generada y almacenada localmente en el equipo donde se desarrolla el proyecto. Sin embargo, no se sube al repositorio debido a su gran tamaño. En su lugar, el repositorio contiene el código necesario para generarla nuevamente. Para crear el archivo matriz_100000x100000.bin, basta con ejecutar:

python crear_matriz.py

Este programa genera nuevamente la matriz con las dimensiones establecidas y verifica que el tamaño del archivo generado coincida con el tamaño esperado. De esta manera, aunque el archivo binario no se encuentre almacenado en GitHub, puede ser reproducido a partir del código incluido en el repositorio.

# 20. Problemas que resuelve la solución

## Consumo excesivo de RAM

No se crea la matriz completa como una estructura de Python. Los datos se escriben directamente en disco. Durante la lectura tampoco se carga el archivo completo. Se utiliza `seek()` para llegar a la fila solicitada y se lee solamente la información necesaria.

## Escritura lenta a disco

La escritura se realiza por bloques de filas en lugar de realizar una operación individual por cada fila. También se utiliza almacenamiento en buffer.

Esto reduce la cantidad de operaciones de entrada y salida.

## Optimización del almacenamiento

Los elementos son binarios y cada uno ocupa un solo bit. Esto evita utilizar un byte completo para cada `0` o `1`.
Además, el archivo utiliza una estructura sencilla basada en filas y saltos de línea, sin crear estructuras adicionales innecesarias.

## Optimización de la lectura

La posición de una fila se calcula directamente:
posicion = numero_fila * BYTES_POR_FILA_ARCHIVO

Después se utiliza:
archivo.seek(posicion)

Esto permite acceder directamente a la zona del archivo que se necesita. No es necesario recorrer ni cargar las filas anteriores.


# Conclusión

La solución representa una matriz de **100.000 × 100.000** utilizando una estructura binaria compacta, donde cada elemento ocupa solamente un bit.

El archivo se organiza por filas y cada fila termina con un salto de línea `\n`, permitiendo mantener una separación clara entre las filas y verificar su estructura durante la lectura.

El tamaño total esperado del archivo es: 1.250.100.000 bytes

La creación se realiza directamente sobre disco y mediante bloques para disminuir las operaciones de escritura.

Para la lectura no se carga el archivo completo en RAM. Se utiliza `seek()` para localizar directamente la fila solicitada y posteriormente se lee solamente la información necesaria para obtener el fragmento solicitado.

Finalmente, la visualización se realiza mediante `leer_matriz.py`, donde se indican las filas y columnas que se desean consultar. El fragmento se muestra en la terminal y también se guarda en `region_matriz.txt`, permitiendo presentar una evidencia legible de una pequeña parte de la matriz sin necesidad de intentar visualizar los 10 mil millones de elementos.

De esta manera, la solución aborda los tres problemas principales planteados: **consumo de RAM, escritura eficiente a disco y optimización de la manipulación, almacenamiento y lectura de los datos.**
