import hashlib

def h(texto):
    return hashlib.sha256(texto.encode()).hexdigest()


def construir_niveles(hojas):
    niveles = []
    nivel_actual = hojas

    while True:
        if len(nivel_actual) % 2 == 1 and len(nivel_actual) > 1:
            nivel_actual.append(nivel_actual[-1])  # Duplicar el último nodo si es impar

        niveles.append(nivel_actual)
        if len(nivel_actual) == 1:
            break 

        nivel_actual = [h(nivel_actual[i] + nivel_actual[i + 1]) for i in range(0, len(nivel_actual), 2)]
    return niveles

def generar_prueba(hojas, indice):
    niveles = construir_niveles(hojas)
    prueba = []
    for nivel in niveles[:-1]:  # Excluir la raíz
        if indice % 2 == 0:
            prueba.append((nivel[indice + 1], "derecha"))  # Hermano derecho
        else:
            prueba.append((nivel[indice - 1], "izquierda"))  # Hermano izquierdo
        indice //= 2
    return prueba

def verificar_prueba(hash_hoja, prueba, raiz):
    actual = hash_hoja
    for hash_hermano, direccion in prueba:
        if direccion == "izquierda":
            actual = h(hash_hermano + actual)
        else:
            actual = h(actual + hash_hermano)
    return actual == raiz

#Transacciones
transacciones = ["tx1: Sara paga 15", "tx2: Juan paga 20", "tx3: Mateo paga 30", "tx4: Ana paga 25", "tx5: Alejandra paga 10"
 ]

#hojas
hash_file1 = h(transacciones[0])
hash_file2 = h(transacciones[1])
hash_file3 = h(transacciones[2])
hash_file4 = h(transacciones[3])
hash_file5 = h(transacciones[4])

hojas = [hash_file1, hash_file2, hash_file3, hash_file4, hash_file5]

niveles = construir_niveles(hojas)
raiz = niveles[-1][0]

print("Raíz del árbol de Merkle:", raiz)

#modificar una transacción
transacciones_modificadas = transacciones.copy()
transacciones_modificadas[2] = "tx3: Mateo paga 35"  

hojas_mod = [ h(transacciones_modificadas[0]), h(transacciones_modificadas[1]), h(transacciones_modificadas[2]), h(transacciones_modificadas[3]),
             h(transacciones_modificadas[4]) ]

raiz_mod = construir_niveles(hojas_mod)[-1][0]

print("Raíz del árbol de Merkle (modificado):", raiz_mod)
print("¿La raíz ha cambiado?", raiz != raiz_mod)

#prueba inclusión
indice_tx3 = 2
prueba_inclusion = generar_prueba(hojas, indice_tx3)
es_valida = verificar_prueba(hojas[indice_tx3], prueba_inclusion, raiz)

print("Prueba de inclusión para la transacción 3:", prueba_inclusion)
print("¿Es válida la prueba?", es_valida)

#verificar dato incorrecto
hash_incorrecto = h("tx3: Mateo paga 35")  
es_valida_incorrecta = verificar_prueba(hash_incorrecto, prueba_inclusion, raiz)
print("Prueba con dato incorrecto:", es_valida_incorrecta)