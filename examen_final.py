import json
import math
import matplotlib.pyplot as plt
import numpy as np

def calcular_trayectoria(v0, angulo, velocidad_viento):
    # Convertir el ángulo a radianes
    angulo_rad = math.radians(angulo)

    # Componentes de la velocidad inicial
    vx = v0 * math.cos(angulo_rad)
    vy = v0 * math.sin(angulo_rad)

    # Ajustar la velocidad del viento
    vx -= velocidad_viento

    # Tiempo total de vuelo
    tiempo_vuelo = (2 * vy) / 9.8

    # Altura máxima
    altura_maxima = (vy**2) / (2 * 9.8)

    # Distancia máxima
    distancia_maxima = vx * tiempo_vuelo

    # Trayectoria
    t = np.linspace(0, tiempo_vuelo, num=1000)
    x = vx * t
    y = vy * t - 0.5 * 9.8 * t**2

    return {
        'velocidad_inicial': v0,
        'angulo': angulo,
        'velocidad_viento': velocidad_viento,
        'distancia_maxima': distancia_maxima,
        'altura_maxima': altura_maxima,
        'tiempo_vuelo': tiempo_vuelo,
        'trayectoria': (x.tolist(), y.tolist())  # Convertir a listas para ser serializado en JSON
    }

def graficar_trayectorias(proyectiles):
    fig, ax = plt.subplots()
    
    for proyectil in proyectiles:
        ax.plot(proyectil['trayectoria'][0], proyectil['trayectoria'][1], label=f"Proyectil {proyectiles.index(proyectil) + 1}")

    ax.set_title('Trayectorias de Proyectiles')
    ax.set_xlabel('Distancia (m)')
    ax.set_ylabel('Altura (m)')
    ax.legend()
    ax.grid(True)

    plt.show()

def guardar_resultados(proyectiles):
    resultados_json = {}
    for proyectil in proyectiles:
        angulo_key = str(proyectil['angulo'])
        velocidad_key = str(proyectil['velocidad_inicial'])
        
        if angulo_key not in resultados_json:
            resultados_json[angulo_key] = {}
        
        resultados_json[angulo_key][velocidad_key] = proyectil

    with open('resultados_proyectiles.json', 'w') as file:
        json.dump(resultados_json, file, indent=4)

def main():
    num_proyectiles = int(input("Ingrese el número de proyectiles: "))
    velocidad_viento = float(input("Ingrese la velocidad del viento (m/s): "))

    proyectiles = []

    for i in range(1, num_proyectiles + 1):
        v0 = float(input(f"Ingrese la velocidad inicial para el proyectil {i} (m/s): "))
        angulo = float(input(f"Ingrese el ángulo inicial para el proyectil {i} (grados): "))

        trayectoria = calcular_trayectoria(v0, angulo, velocidad_viento)
        proyectiles.append(trayectoria)

    # Encontrar todos los proyectiles que alcanzaron la misma altura máxima
    altura_maxima_global = max(proyectiles, key=lambda x: x['altura_maxima'])['altura_maxima']
    proyectiles_misma_altura = [p for p in proyectiles if p['altura_maxima'] == altura_maxima_global]

    # Mostrar los proyectiles con la misma altura máxima
    print("\nProyectiles que alcanzaron la misma altura máxima:")
    for proyectil in proyectiles_misma_altura:
        print(f"Proyectil {proyectiles.index(proyectil) + 1}: Altura máxima = {proyectil['altura_maxima']} metros")
        print(f"   Parámetros: Velocidad Inicial = {proyectil['velocidad_inicial']} m/s, Ángulo = {proyectil['angulo']} grados")

    # Proyectiles con tiempo de vuelo mayor a 5 segundos
    print("\nProyectiles con tiempo de vuelo mayor a 5 segundos:")
    for i, proyectil in enumerate(proyectiles):
        if proyectil['tiempo_vuelo'] > 5:
            print(f"Proyectil {i + 1}: Tiempo de vuelo = {proyectil['tiempo_vuelo']} segundos")
            print(f"   Parámetros: Velocidad Inicial = {proyectil['velocidad_inicial']} m/s, Ángulo = {proyectil['angulo']} grados")

    # Almacenar los resultados en un archivo JSON clasificándolos según el ángulo y la velocidad
    guardar_resultados(proyectiles)

    # Visualizar la trayectoria en el gráfico
    graficar_trayectorias(proyectiles)

if __name__ == "__main__":
    main()






