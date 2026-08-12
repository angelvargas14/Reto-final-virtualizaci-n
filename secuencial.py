import time
import math
import psutil
import os

def procesar_secuencial(filename="temperaturas.txt"):
    if not os.path.exists(filename):
        print(f"Error: El archivo '{filename}' no existe. Ejecuta primero 'generar_datos.py'.")
        return

    inicio = time.time()
    
    print("Cargando datos en memoria...")
    with open(filename, 'r') as f:
        datos = [float(line.strip()) for line in f]
    
    total_datos = len(datos)
    print("Procesando en modo secuencial...")
    val_max = max(datos)
    val_min = min(datos)
    suma = sum(datos)
    promedio = suma / total_datos
    
    # Desviación estándar y conteo de mayores al promedio
    suma_sq_diff = sum((x - promedio) ** 2 for x in datos)
    desviacion = math.sqrt(suma_sq_diff / total_datos)
    mayores_prom = sum(1 for x in datos if x > promedio)
    
    fin = time.time()
    tiempo_total = fin - inicio
    
    print("\n" + "="*40)
    print("      RESULTADOS - ALGORITMO SECUENCIAL")
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
    procesar_secuencial()