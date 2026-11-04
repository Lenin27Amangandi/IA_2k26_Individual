import time
import tracemalloc
from collections import deque

TOTAL_M = 3
TOTAL_C = 3
CAPACIDAD_BOTE = 2

ESTADO_INICIAL = (3, 3, 1)
ESTADO_META = (0, 0, 0)

ACCIONES = [(1, 0), (0, 1), (1, 1), (2, 0), (0, 2)]


def es_valido(m_izq, c_izq):
   
    m_der = TOTAL_M - m_izq
    c_der = TOTAL_C - c_izq

    if m_izq < 0 or m_izq > TOTAL_M:
        return False
    if c_izq < 0 or c_izq > TOTAL_C:
        return False

    if m_izq > 0 and c_izq > m_izq:
        return False
    if m_der > 0 and c_der > m_der:
        return False

    return True


def aplicar_accion(estado, accion):
    m_izq, c_izq, bote_izq = estado
    m, c = accion

    if bote_izq == 1:
        nuevo = (m_izq - m, c_izq - c, 0)
    else:
        nuevo = (m_izq + m, c_izq + c, 1)

    if es_valido(nuevo[0], nuevo[1]):
        return nuevo
    return None


def obtener_sucesores(estado, acciones):
    sucesores = []
    for accion in acciones:
        nuevo = aplicar_accion(estado, accion)
        if nuevo is not None:
            sucesores.append((accion, nuevo))
    return sucesores


def texto_accion(estado, accion):
    m, c = accion
    if estado[2] == 1:
        sentido = "izq -> der"
    else:
        sentido = "der -> izq"
    return str(m) + "M + " + str(c) + "C  (" + sentido + ")"


def bfs(acciones=ACCIONES):
    frontera = deque()
    frontera.append((ESTADO_INICIAL, []))
    visitados = set()
    visitados.add(ESTADO_INICIAL)

    expandidos = 0
    max_frontera = 0

    while len(frontera) > 0:
        if len(frontera) > max_frontera:
            max_frontera = len(frontera)

        estado, camino = frontera.popleft()

        if estado == ESTADO_META:
            return camino, expandidos, max_frontera

        expandidos += 1
        for accion, nuevo in obtener_sucesores(estado, acciones):
            if nuevo not in visitados:
                visitados.add(nuevo)
                frontera.append((nuevo, camino + [(accion, nuevo)]))

    return None, expandidos, max_frontera


def dfs(acciones=ACCIONES):
    frontera = []                   
    frontera.append((ESTADO_INICIAL, []))
    visitados = set()                 

    expandidos = 0
    max_frontera = 0

    while len(frontera) > 0:
        if len(frontera) > max_frontera:
            max_frontera = len(frontera)

        estado, camino = frontera.pop() 

        if estado in visitados:
            continue
        visitados.add(estado)

        if estado == ESTADO_META:
            return camino, expandidos, max_frontera

        expandidos += 1
        for accion, nuevo in obtener_sucesores(estado, acciones):
            if nuevo not in visitados:
                frontera.append((nuevo, camino + [(accion, nuevo)]))

    return None, expandidos, max_frontera


def verificar_solucion(camino):
    estado = ESTADO_INICIAL
    for accion, estado_registrado in camino:
        nuevo = aplicar_accion(estado, accion)
        if nuevo is None or nuevo != estado_registrado:
            return False
        estado = nuevo
    return estado == ESTADO_META


def imprimir_solucion(nombre, camino):
    print("Solucion encontrada por " + nombre + " (" + str(len(camino)) + " pasos):")
    print("  paso 0 : inicio                    -> " + str(ESTADO_INICIAL))
    estado = ESTADO_INICIAL
    numero = 1
    for accion, nuevo in camino:
        descripcion = texto_accion(estado, accion)
        print("  paso " + str(numero) + " : " + descripcion.ljust(25) + "-> " + str(nuevo))
        estado = nuevo
        numero += 1


def medir_tiempo(algoritmo, acciones, repeticiones):
    inicio = time.perf_counter()
    for i in range(repeticiones):
        algoritmo(acciones)
    fin = time.perf_counter()
    return (fin - inicio) / repeticiones


def medir_memoria_pico(algoritmo, acciones):
    tracemalloc.start()
    algoritmo(acciones)
    actual, pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return pico / 1024


def evaluar(nombre, algoritmo, acciones, repeticiones):
    camino, expandidos, max_frontera = algoritmo(acciones)
    return {
        "algoritmo": nombre,
        "nodos_expandidos": expandidos,
        "tiempo_s": medir_tiempo(algoritmo, acciones, repeticiones),
        "longitud_camino": len(camino),
        "max_frontera": max_frontera,
        "memoria_pico_kb": medir_memoria_pico(algoritmo, acciones),
        "solucion_valida": verificar_solucion(camino),
        "camino": camino,
    }


def main():
    repeticiones = 2000
    acciones_inverso = list(reversed(ACCIONES))

    resultados = []
    resultados.append(evaluar("BFS", bfs, ACCIONES, repeticiones))
    resultados.append(evaluar("DFS", dfs, ACCIONES, repeticiones))
    resultados.append(evaluar("DFS (orden inverso)", dfs, acciones_inverso, repeticiones))

    for r in resultados:
        imprimir_solucion(r["algoritmo"], r["camino"])
        print()

    print("Resumen (promedio de " + str(repeticiones) + " ejecuciones):")
    for r in resultados:
        print(
            r["algoritmo"].ljust(22)
            + " expandidos=" + str(r["nodos_expandidos"])
            + " tiempo=" + format(r["tiempo_s"], ".8f") + " s"
            + " camino=" + str(r["longitud_camino"])
            + " max_frontera=" + str(r["max_frontera"])
            + " valida=" + str(r["solucion_valida"])
        )

    archivo = open("Tarea_Individual_DG_S4/resultados_benchmark.csv", "w", encoding="utf-8")
    archivo.write("algoritmo,nodos_expandidos,tiempo_s,longitud_camino,max_frontera,memoria_pico_kb,solucion_valida\n")
    for r in resultados:
        linea = (
            r["algoritmo"] + ","
            + str(r["nodos_expandidos"]) + ","
            + format(r["tiempo_s"], ".10f") + ","
            + str(r["longitud_camino"]) + ","
            + str(r["max_frontera"]) + ","
            + format(r["memoria_pico_kb"], ".3f") + ","
            + str(r["solucion_valida"]) + "\n"
        )
        archivo.write(linea)
    archivo.close()
    print()
    print("Resultados guardados en resultados_benchmark.csv")


if __name__ == "__main__":
    main()