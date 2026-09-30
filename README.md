# Análisis Reproducible — ECG con Artefactos de Movimiento

Base de datos: **Motion Artifact Contaminated ECG Database v1.0.0**  
Fuente: PhysioNet — 27 registros ECG de 4 canales a 500 Hz con distintas actividades físicas.

## Estructura del proyecto

```
Programacion_MCD/
├── data/                  # Base de datos original (sin modificar)
├── notebooks/             # Exploración en Jupyter
│   └── 01_exploracion.ipynb
├── src/                   # Scripts de Python
│   └── clean_data.py      # Limpieza y exportación a CSV
├── docs/                  # Documentación adicional
├── requirements.txt       # Dependencias del proyecto
├── Dockerfile             # Entorno reproducible
└── README.md
```

## Pasos para ejecutar el proyecto

### 1. Clonar el repositorio

```bash
git clone https://github.com/<tu-usuario>/Programacion_MCD.git
cd Programacion_MCD
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Ejecutar el script de limpieza

```bash
python src/clean_data.py
```

Genera `data/ecg_clean.csv` con todas las señales preprocesadas.

### 4. Explorar el notebook

```bash
jupyter notebook notebooks/01_exploracion.ipynb
```

### 5. (Opcional) Ejecutar con Docker

```bash
docker build -t ecg-analysis .
docker run -p 8888:8888 ecg-analysis
```

Abre `http://localhost:8888` en tu navegador.

## Descripción de los datos

| Columna       | Descripción                              |
|---------------|------------------------------------------|
| `record`      | Nombre del registro original             |
| `subject_id`  | ID del sujeto (01–27)                    |
| `angle_deg`   | Ángulo del electrodo (0°, 45°, 90°)      |
| `activity`    | sentado / caminando / trotando           |
| `time_s`      | Tiempo en segundos                       |
| `ECG1`–`ECG4` | Voltaje de cada canal en mV              |

## Dependencias principales

- `pandas` — Manipulación de datos
- `wfdb` — Lectura de archivos `.dat`/`.hea` de PhysioNet
- `matplotlib` — Visualización
- `jupyter` — Notebooks interactivos