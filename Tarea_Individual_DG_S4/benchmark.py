import csv

ARCHIVO_CSV = "Tarea_Individual_DG_S4/resultados_benchmark.csv"
ARCHIVO_PNG = "Tarea_Individual_DG_S4/grafico_benchmark.png"

def leer_resultados(nombre_archivo):
    filas = []
    archivo = open(nombre_archivo, "r", encoding="utf-8")
    lector = csv.DictReader(archivo)
    for fila in lector:
        resultado = {
            "algoritmo": fila["algoritmo"],
            "nodos_expandidos": int(fila["nodos_expandidos"]),
            "tiempo_s": float(fila["tiempo_s"]),
            "longitud_camino": int(fila["longitud_camino"]),
            "max_frontera": int(fila["max_frontera"]),
            "memoria_pico_kb": float(fila["memoria_pico_kb"]),
            "solucion_valida": fila["solucion_valida"],
        }
        filas.append(resultado)
    archivo.close()
    return filas


def imprimir_tabla(filas):
    columnas = [
        ("Algoritmo", 22),
        ("Expandidos", 11),
        ("Tiempo (s)", 13),
        ("Camino", 8),
        ("Frontera max", 13),
        ("Mem. pico (KB)", 15),
        ("Valida", 7),
    ]

    linea = ""
    separador = ""
    for nombre, ancho in columnas:
        linea = linea + nombre.ljust(ancho)
        separador = separador + ("-" * (ancho - 1)) + " "
    print(linea)
    print(separador)

    for f in filas:
        texto = (
            f["algoritmo"].ljust(22)
            + str(f["nodos_expandidos"]).ljust(11)
            + format(f["tiempo_s"], ".8f").ljust(13)
            + str(f["longitud_camino"]).ljust(8)
            + str(f["max_frontera"]).ljust(13)
            + format(f["memoria_pico_kb"], ".3f").ljust(15)
            + f["solucion_valida"].ljust(7)
        )
        print(texto)


def imprimir_mejores(filas):
    print()
    print("Mejor valor por metrica (menor es mejor):")
    metricas = [
        ("nodos_expandidos", "Nodos expandidos"),
        ("tiempo_s", "Tiempo de ejecucion"),
        ("longitud_camino", "Longitud del camino"),
        ("max_frontera", "Tamano maximo de la frontera"),
        ("memoria_pico_kb", "Memoria pico"),
    ]
    for clave, nombre in metricas:
        mejor = filas[0]
        for f in filas:
            if f[clave] < mejor[clave]:
                mejor = f
        empatados = []
        for f in filas:
            if f[clave] == mejor[clave]:
                empatados.append(f["algoritmo"])
        if len(empatados) > 1:
            print("  " + nombre.ljust(32) + "empate: " + ", ".join(empatados))
        else:
            print("  " + nombre.ljust(32) + mejor["algoritmo"])


def imprimir_latex(filas):
    print()
    for f in filas:
        fila = (
            f["algoritmo"] + " & "
            + str(f["nodos_expandidos"]) + " & "
            + format(f["tiempo_s"], ".2e") + " & "
            + str(f["longitud_camino"]) + " & "
            + str(f["max_frontera"]) + " & "
            + format(f["memoria_pico_kb"], ".2f") + " \\\\"
        )
        print("  " + fila)


def dibujar_graficos(filas):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print()
        print("matplotlib no esta instalado: se omiten los graficos.")
        print("Instalelo con:  pip install matplotlib")
        return

    nombres = []
    for f in filas:
        nombres.append(f["algoritmo"])

    metricas = [
        ("nodos_expandidos", "Nodos expandidos"),
        ("tiempo_s", "Tiempo (s)"),
        ("longitud_camino", "Longitud del camino"),
        ("max_frontera", "Frontera maxima"),
        ("memoria_pico_kb", "Memoria pico (KB)"),
    ]

    figura, ejes = plt.subplots(2, 3, figsize=(10, 6))
    lista_ejes = ejes.flatten()
    for i in range(len(metricas)):
        clave, titulo = metricas[i]
        valores = []
        for f in filas:
            valores.append(f[clave])
        lista_ejes[i].bar(nombres, valores)
        lista_ejes[i].set_title(titulo)
        lista_ejes[i].tick_params(axis="x", labelrotation=20, labelsize=8)

    lista_ejes[len(metricas)].axis("off")

    figura.tight_layout()
    figura.savefig(ARCHIVO_PNG, dpi=150)
    plt.close(figura)
    print()
    print("Grafico guardado en " + ARCHIVO_PNG)


def main():
    try:
        filas = leer_resultados(ARCHIVO_CSV)
    except FileNotFoundError:
        print("No se encontro " + ARCHIVO_CSV)
        print("Primero ejecute: python misioneros_canibales.py")
        return

    imprimir_tabla(filas)
    imprimir_mejores(filas)
    imprimir_latex(filas)
    dibujar_graficos(filas)


if __name__ == "__main__":
    main()