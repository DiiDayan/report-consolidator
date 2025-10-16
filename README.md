# 📊 Consolidador de Reportes CSV

Herramienta de automatización en Python que consolida múltiples archivos CSV en un único reporte, calcula estadísticas clave y genera visualizaciones automáticas.

## ✨ Características

- **Consolidación automática**: Lee todos los archivos CSV de una carpeta y los combina en uno solo
- **Estadísticas en tiempo real**: Calcula totales, promedios y métricas clave
- **Visualización de datos**: Genera gráficos comparativos automáticamente
- **Fácil de usar**: Ejecuta un solo comando y obtén todos los resultados

## 🚀 Casos de uso

- Consolidar reportes mensuales de ventas
- Combinar datos de múltiples fuentes
- Generar reportes ejecutivos rápidamente
- Automatizar análisis repetitivos

## 📋 Requisitos

- Python 3.8 o superior
- pandas
- matplotlib
- openpyxl

## 🔧 Instalación

1. Clona este repositorio:
```bash
git clone https://github.com/TU-USUARIO/report-consolidator.git
cd report-consolidator
```

2. Crea un entorno virtual:
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## 💻 Uso

1. Coloca tus archivos CSV en la carpeta `data/input/`

2. Ejecuta el script:
```bash
python3 src/consolidator.py
```

3. Encuentra los resultados en la carpeta `output/`:
   - `reporte_consolidado.csv` - Datos consolidados
   - `grafico_ventas_gastos.png` - Visualización

## 📁 Estructura del proyecto
```
report-consolidator/
├── src/
│   └── consolidator.py      # Script principal
├── data/
│   └── input/               # Coloca aquí tus CSVs
├── output/                  # Resultados generados
├── examples/                # Archivos de ejemplo
├── requirements.txt         # Dependencias
└── README.md
```

## 📊 Ejemplo de salida

El script genera:

**Estadísticas:**
```
=== ESTADÍSTICAS ===
Total ventas: $17,400
Total gastos: $9,750
Beneficio total: $7,650
Promedio ventas: $1,933
Promedio gastos: $1,083
```

**Gráfico comparativo** de ventas vs gastos por mes

## 🛠️ Tecnologías

- Python 3.13
- pandas - Manipulación de datos
- matplotlib - Visualización
- openpyxl - Lectura de archivos Excel

## 📝 Licencia

MIT License

## 👩‍💻 Autora

Creado como parte de mi portfolio de proyectos de análisis de datos y automatización.