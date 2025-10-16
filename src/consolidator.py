import pandas as pd
import os
from pathlib import Path

def consolidar_reportes(carpeta_input='data/input', carpeta_output='output'):
    """
    Lee todos los archivos CSV de una carpeta y los consolida en uno solo.
    """
    # Obtener todos los archivos CSV
    archivos_csv = list(Path(carpeta_input).glob('*.csv'))
    print(f"Archivos encontrados: {len(archivos_csv)}")
    
    # Leer todos los archivos y guardarlos en una lista
    dataframes = []
    for archivo in archivos_csv:
        df = pd.read_csv(archivo)
        print(f"Leyendo: {archivo.name}")
        dataframes.append(df)
    
    # Consolidar todos en uno solo
    df_consolidado = pd.concat(dataframes, ignore_index=True)
    print(f"\nTotal de filas consolidadas: {len(df_consolidado)}")
    
    # Guardar el archivo consolidado
    archivo_salida = Path(carpeta_output) / 'reporte_consolidado.csv'
    df_consolidado.to_csv(archivo_salida, index=False)
    print(f"Archivo guardado en: {archivo_salida}")
    
    return df_consolidado

def calcular_estadisticas(df):
    """
    Calcula estadísticas básicas del dataframe consolidado.
    """
    print("\n=== ESTADÍSTICAS ===")
    print(f"Total ventas: ${df['ventas'].sum():,.0f}")
    print(f"Total gastos: ${df['gastos'].sum():,.0f}")
    print(f"Beneficio total: ${(df['ventas'] - df['gastos']).sum():,.0f}")
    print(f"Promedio ventas: ${df['ventas'].mean():,.0f}")
    print(f"Promedio gastos: ${df['gastos'].mean():,.0f}")

def crear_grafico(df, carpeta_output ='output'):
    '''Crea un gráfico comparando ventas vs gastos por mes.'''
    import matplotlib.pyplot as plt

    plt.figure(figsize=(10,6))
    plt.plot(df['mes'], df['ventas'], marker ='o', label='Ventas', linewidth = 2)
    plt.plot(df['mes'], df['gastos'], marker = 's', label = 'Gastos', linewidth = 2)
    plt.xlabel('Mes')
    plt.ylabel('Cantidad (€)')
    plt.title('Ventas vs Gastos por mes')
    plt.legend()
    plt.xticks(rotation = 45)
    plt.tight_layout()
    plt.grid(True, alpha = 0.3)

    #Guardar archivo
    archivo_grafico = Path(carpeta_output) / 'grafico_ventas_gastos'
    plt.savefig(archivo_grafico, dpi = 30, bbox_inches = 'tight')
    print(f"\nGráfico guardado en: {archivo_grafico}")


if __name__ == "__main__":
    df = consolidar_reportes()
    calcular_estadisticas(df)
    crear_grafico(df)
    print("\n¡Consolidación completada!")
    print(df)