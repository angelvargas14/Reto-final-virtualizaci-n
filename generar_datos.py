import numpy as np

def generar_datos(filename="temperaturas.txt", cantidad=5000000):
    print(f"Generando {cantidad} registros de temperatura...")
    # Simula lecturas de temperatura entre -10.0°C y 50.0°C
    datos = np.random.uniform(-10.0, 50.0, cantidad)
    np.savetxt(filename, datos, fmt="%.2f")
    print(f"Archivo '{filename}' generado con éxito.")

if __name__ == "__main__":
    generar_datos()