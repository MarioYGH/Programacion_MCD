"""
Script de limpieza y preprocesamiento de la base de datos ECG con artefactos de movimiento.
Motion Artifact Contaminated ECG Database v1.0.0

Uso:
    python src/clean_data.py

Salida:
    data/ecg_clean.csv  — DataFrame con todas las señales limpias en formato tabular.
"""

import os
import wfdb
import pandas as pd
import numpy as np

# ── Configuración ──────────────────────────────────────────────────────────────
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data",
                        "motion-artifact-contaminated-ecg-database-1.0.0")
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "ecg_clean.csv")

CHANNELS = ["ECG1", "ECG2", "ECG3", "ECG4"]


def load_records(data_dir: str) -> list[str]:
    """Lee el archivo RECORDS y devuelve la lista de nombres de registro."""
    records_path = os.path.join(data_dir, "RECORDS")
    with open(records_path, "r") as f:
        records = [line.strip() for line in f if line.strip()]
    return records


def parse_metadata(record_name: str) -> dict:
    """Extrae metadatos del nombre del registro (actividad, ángulo, sujeto)."""
    # Formato: testNN_XXa  donde XX=ángulo, a=actividad (s=sentado, w=caminando, j=trotando)
    parts = record_name.replace("test", "")  # e.g. "01_00s"
    subject_id = int(parts[:2])
    angle = int(parts[3:5])
    activity_code = parts[5]
    activity_map = {"s": "sentado", "w": "caminando", "j": "trotando"}
    return {
        "record": record_name,
        "subject_id": subject_id,
        "angle_deg": angle,
        "activity": activity_map.get(activity_code, "unknown"),
    }


def load_signal(record_path: str) -> pd.DataFrame:
    """Carga la señal de un registro con wfdb y la convierte a DataFrame."""
    record = wfdb.rdrecord(record_path)
    fs = record.fs  # frecuencia de muestreo (500 Hz)
    n_samples = record.sig_len
    time_s = np.arange(n_samples) / fs

    df = pd.DataFrame(record.p_signal, columns=CHANNELS)
    df.insert(0, "time_s", time_s)
    return df


def remove_baseline_wander(signal: pd.Series, window: int = 500) -> pd.Series:
    """Elimina la deriva de línea base con una media móvil (filtro de tendencia)."""
    baseline = signal.rolling(window=window, center=True, min_periods=1).mean()
    return signal - baseline


def clean_signals(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica limpieza básica: elimina NaN y corrige deriva de línea base."""
    df = df.dropna()
    for ch in CHANNELS:
        df[ch] = remove_baseline_wander(df[ch])
    return df


def main():
    print("=== Limpieza de datos ECG ===\n")
    records = load_records(DATA_DIR)
    print(f"Registros encontrados: {len(records)}")

    all_frames = []

    for rec in records:
        record_path = os.path.join(DATA_DIR, rec)
        meta = parse_metadata(rec)
        print(f"  Procesando {rec} | sujeto={meta['subject_id']:02d} "
              f"ángulo={meta['angle_deg']}° actividad={meta['activity']}")

        df = load_signal(record_path)
        df = clean_signals(df)

        # Añadir columnas de metadatos
        for key, val in meta.items():
            df[key] = val

        all_frames.append(df)

    ecg_df = pd.concat(all_frames, ignore_index=True)

    # Reordenar columnas
    meta_cols = ["record", "subject_id", "angle_deg", "activity", "time_s"]
    signal_cols = CHANNELS
    ecg_df = ecg_df[meta_cols + signal_cols]

    ecg_df.to_csv(OUTPUT_FILE, index=False)
    print(f"\n✓ Archivo limpio guardado en: {OUTPUT_FILE}")
    print(f"  Filas totales : {len(ecg_df):,}")
    print(f"  Columnas      : {list(ecg_df.columns)}")


if __name__ == "__main__":
    main()
