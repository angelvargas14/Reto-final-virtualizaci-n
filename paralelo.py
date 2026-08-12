import time
import math
import psutil
import os
from concurrent.futures import ProcessPoolExecutor

def etapa_1_chunk(chunk):
    val_max = max(chunk)
    val_min = min(chunk)
    suma = sum(chunk)
    count = len(chunk)
    return val_max, val_min, suma, count

def etapa_2_chunk(args):
    chunk, promedio = args
    sq_diff = sum((x - promedio) ** 2 for x in chunk)
    mayores = sum(1 for x in chunk if x > promedio)
    return sq_diff, mayores

def procesar_paralelo(filename="temperaturas.txt", num_workers=None):
    if not os.path.exists(filename):
        print(f"Error: El archivo '{filename}' no existe. Ejecuta primero 'generar_datos.py'.")
        return

    if num_workers is None:
        num_workers = os.cpu_count()
        
    inicio = time.time()
    
    print(f"Cargando datos en memoria (Usando {num_workers} procesos/núcleos)...")
    with open(filename, 'r') as f:
        datos = [float(line.strip()) for line in f]
    
    total_datos = len(datos)
    chunk_size = math.ceil(total_datos / num_workers)
    chunks = [datos[i:i + chunk_size] for i in range(0, total_datos, chunk_size)]
    
    # Etapa 1: Máximo, Mínimo, Suma en paralelo
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        res1 = list(executor.map(etapa_1_chunk, chunks))
    
    val_max = max(r[0] for r in res1)
    val_min = min(r[1] for r in res1)
    suma_total = sum(r[2] for r in res1)
    promedio = suma_total / total_datos
    
    # Etapa 2: Desviación y Filtro en paralelo
    args_etapa2 = [(chunk, promedio) for chunk in chunks]
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        res2 = list(executor.map(etapa_2_chunk, args_etapa2))
        
    suma_sq_diff = sum(r[0] for r in res2)
    mayores_prom = sum(r[1] for r in res2)
    desviacion = math.sqrt(suma_sq_diff / total_datos)
    
    fin = time.time()
    tiempo_total = fin - inicio
    
    print("\n" + "="*40)
    print(f"   RESULTADOS - ALGORITMO PARALELO ({num_workers} vCPUs)")
    print("="*40)
    print(f"Total de datos:       {total_datos:,}")
    print(f"Valor Máximo:         {val_max:.2f} °C")
    print(f"Valor Mínimo:         {val_min:.2f} °C")
    print(f"Promedio:             {promedio:.2f} °C")
    print(f"Desviación Estándar:  {desviacion:.2f}")
    print(f"Datos > Promedio:     {mayores_prom:,}")
    print("-" * 40)
    print(f"Tiempo de Ejecución:  {tiempo_total:.4f} segundos")
    print(f"Uso de CPU:           {psutil.cpu_percent()}%")
    print(f"Uso de RAM:           {psutil.Process(os.getpid()).memory_info().rss / (1024**2):.2f} MB")
    print("="*40)

if __name__ == "__main__":
    procesar_paralelo()