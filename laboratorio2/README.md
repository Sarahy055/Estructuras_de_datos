# Laboratorio 2: Árbol de Merkle.

Estudiante: Sarahy Paulina Cardales Acevedo CC: 1062963790

Lenguaje utilizado: Python

# Descripción: 

En este laboratorio se implementa un Ábol de merkle, iutilizando python y la función hash criptográfica SHA-256.

El objetivo es construir una estructura que permita representar un conjunto de datos mediante una única raíz, denominada Merkle Proof y comporbar cómo cualquier modificación en los datos originales produce un cambio en la raíz.

La implementación también incluye la generación y verificación de una pruena de inclusión para comporbar que una determinada transacción pertenece al árbol.

# Técnologías utilizadas:
- Python
- Biblioteca estándar hashlib
- algoritmo de hash SHA-256

# Diagrama del ábol Merkel:
El diagrmaa del Árbol de Merkle construido durante el laboratorio se realizó de manera manual y se encuentra en el archivo, incluido en este repositorio en la carpeta laboratorio 2: 

'arbol.txt'

El diagrama representa la estructura completa del árbol utilizado en el experimento, desde las transacciones orginales hasta la Merkle Root

La estructura representada es:
- H1,H2,H3,H4 y H5: hashes SHA-256 de las cinco transacciones.
- H5: se duplica debido que inicialmente exiten 5 hojas (número impar).
- H12, H34 y H55: hashes obtenidos al concatenar los hashes de sus respectivos hijos y aplicar SHA-256.
- H1234 y H5555: hashes de los niveles superiores.
- RAÍZ: hash final que representa todo el conjunto de transacciones.


# Función hash 
La función utilizada para calcular las hashes es:

def h(texto):

  return hashlib.sha256(texto.encade()).hexdigest()

Esta función recibe un texto, lo convierte a bytes mediante "encode()" y calcula su hash utilizando SHA-256.

El resultado es una cadena hexadecimal de 64 caracteres. 

# Transacciones utlizadas
Para el experimento se utilizaron cinco transacciones simuladas manualmente:


tx1: Sara paga 15 

tx2: Juan paga 20

tx3: Mateo paga 30

tx4: Ana paga 25

tx5: Alejandra paga 10 

Cada una de estas transacciones se convierte en una hoa de Árbol de Merkle mediante SHA-256. Y como tiene 5 hojas (impar), la quinta hoja se duplica para poder construir el siguiente nivel. 

# Construcción del árbol:
La función encargada de construir los diferentes niveles fue:
  
def construir_niveles(hojas):

    niveles = []
    nivel_actual = hojas
    
    while True:
      if len(nivel_actual) %2 == 1 and len(nivel_actual) > 1:
        nivel_actual.append(nivel_actual[-1])
      niveles.append(nivel_actual)

      if len(nivel_actual) == 1:
          break
      nivel_actual = [
        h(nivel_actual[i] + nivel_actual[i + 1])
        for i in range(0, len(nivel_actual), 2)
      ]
    return niveles
  
El algoritmo funciona de la siguiente manera:

Primero recibe la lista de hashes de las hojas, luego comprueba si el número de nodos es impar, si es impar y todavía no se ha llegado a la raíz, duplica el último nodo.
Guarda el nivel actual, luego ombina los hahes de dos en dos.
Calcula el SHA-256 de cada concatenación. Y se repite este proceso hasta obtener un único hash.

# Obtención de la Merkle Root
Después de construir todos los niveles, se obtienen la raíz mediante:
niveles = construir.niveles(hojas)
raiz= niveles[-1][0]
print("Raíz del árbol de Merkle", raiz)

La variable "raiz" obtiene el hash que representa todo el conjunto de transacciones.

# Experimentos:
## 1) modificación de una transacción:
Para comprobar la propiedad de propagación de los hashes, se modificó la tercera transacción.

Transacción original:
- "tx3: Mateo paga 30"
  
Transacción modificada:
- "tx3: Mateo paga 35"

El código implementado fue:
transacciones_modificadas = transacciones.copy()
transacciones_modificadas[2] = "tx3: Mateo paga 35"

Después se vuelven a calcular las hojas y la Merkle Root. Finalmente se compara la raíz modificada:

print("¿La raíz ha cambiado?", raiz != raiz_mod)

El resultado esperado fue:
¿La raíz ha cambiado? -> True

Esto demuestra que un cambio en una sola transacción se porpaga por los diferentes niveles del árbol hasta modificar la Merkle Root.

## 2) prueba inclusión:
Esta prueba permite demostrar que una determinada transacción pertenece al Árbol de Merkle sin tener que proporcionar todas las transacciones. La prueba se genera sobre la transacción 3:

tx3: Mateo paga 30

y corresponde al índice:
indice_tx3 = 2

La prueba se genera mediante: 
prueba_inclusion = generar_prueba(hojas, indice_tx3)

La función obtiene el hash necesario para cada nivel y su posición. Esto permite reconstruir el camino desde la hoa hasta la raíz.

## 3) Verificación de la prueba inclusión
La prueba se verifica utilizando: 

es_valida = verificar_prueba (
    hojas[indice_tx3],
    prueba_inclusion,
    raiz
)

La función comienza con el hash de la transacción y va combinándolo con los hashes de los hermanos indicados en la prueba. 

Y funciona así: Si el resultado final coincide con la merkle Root, la prueba es válida. 

El resultado esperado es = ¿Es válida la prueba? -> True

## 4) Verificación con un dato incorrecto 
Finalmente se utiliza un dato diferente al que originalmente pertenece al árbol:"tx3: Mateo paga 35"

Se calcula su hash:
hash_incorrecto = h("tx3: Mateo paga 35")

Después se intenta verificar utilizando la misma prueba de inclusión y la raíz original:

es_valida_incorrecta = verificar_prueba (
    hash_incorrecto,
    prueba_inclusion,
    raiz
)
El resultado esperado es:
Prueba con dato incorrecto: False

Esto demuestra que la prueba no es válida cuadno se intenta utilizar un dato diferente al que fue incluido originalmente en el árbol.

# Evidencias 
Capturas del sistema funcionando:
1. Con raíz no modificada
2. Prueba de inclusión valida
3. Prueba de inclusión inválida
<img width="1181" height="437" alt="Captura de pantalla 2026-09-18 165726" src="https://github.com/user-attachments/assets/9823b7bd-9eee-40c4-8482-6f8be91fdbb4" />

<img width="1173" height="204" alt="Captura de pantalla 2026-09-18 165756" src="https://github.com/user-attachments/assets/133b106a-7fff-4198-964f-b215f1af0515" />


1. Con raíz modificada
2. Prueba de inclusión valida
3. Prueba de inclusión inválida
<img width="1169" height="452" alt="Captura de pantalla 2026-09-18 165828" src="https://github.com/user-attachments/assets/f1141807-6386-4498-bd11-7a5f4eb76851" />

<img width="1179" height="212" alt="Captura de pantalla 2026-09-18 165844" src="https://github.com/user-attachments/assets/18fe3098-ac2e-43b6-9b92-1d5f44dbe6a9" />

# Código de honor:

Para este laboratorio se adopta el código de honor académico:

https://www-hbs-edu.translate.goog/mba/handbook/standards-of-conduct/academic/honor-code?_x_tr_sl=en&_x_tr_tl=es&_x_tr_hl=es&_x_tr_pto=tc&_x_tr_hist=true

El trabajo se realiza teniedno en cuenta los principios de honestidad académica y responsabilidad sobre el contenido entregado.

Se utilizó la herramienta IA como apoyo durante el desarrollo de esta actividad.

El uso estuvo orientado a:
- Comprender la construcción de los diferentes niveles del árbol
- Comprender el funcionamiento de las pruebas de inclusión
- Recibir orientación sobre la estructura del código. 

El código fue revisado y ejecutado para comprobar su funcionamiento. La Ai generativa se utiizó como apoyo para este laboratorio. 

# Conclusión:

La implementaciín permite construir un árbol de merkle a partir de 5 transacciones utilizando SHA-256.

Los resultados muestrna que:
1. Las transacciones pueden representarse mediante hashes.
2. Los hashes pueden combianrse de forma jerárquica hasta obtener una única Merkle Root.
3. Cuando existe un número impar de nodos, el último se duplica para continuar la construcción.
4. Una modificación en una transacción provica un cambio en la Merkle Root.
5. Es posible generar una prueba de inclusión para demostrar que una transacción pertenece al árbol.
6. La prueba falla cuando se intenta verificar con un dato diferente.

De esta manera, el laboratorio permite observar de forma práctiva cómo los Árboles de Merkle proporcionan una forma eficiente de representar y verfificar la integridad de un conjunto de datos.
