import pandas as pd

# Cargar el archivo CSV
archivo_csv = 'PROYECTO/Reporte del consumo de energía eléctrica (kWh-mes) - 202301 - 202408.csv'  
data = pd.read_csv(archivo_csv, delimiter=';', encoding='latin1')

# Función para limpiar y normalizar los valores
def clean_and_normalize(value):
    if pd.isna(value):
        return None
    cleaned_value = ' '.join(value.strip().split())  # Eliminar espacios extras, saltos de línea, etc.
    return cleaned_value.upper()  # Convertir a mayúsculas

# Función para mapear los valores originales con sus versiones limpias
def map_original_to_clean(column):
    mapping = {}
    for original_value in column.dropna().unique():
        cleaned_value = clean_and_normalize(original_value)
        mapping[original_value] = cleaned_value
    return mapping


# Columnas a limpiar
columns_to_clean = ['COD_SIS_ELECTR', 'CTARIFA', 'ATARIFA', 'USO', 'GRUPO', 'COD_EMPRESA', 'RAZON_SOCIAL', 'DEPARTAMENTO']

# Crear una copia del DataFrame
data_cleaned = data.copy()

# Limpiar y reemplazar los valores en las columnas especificadas
for column in columns_to_clean:
    if column in data_cleaned.columns:
        # Generar el mapeo original -> limpio
        mapping = map_original_to_clean(data_cleaned[column])
        # Reemplazar los valores en la columna con sus versiones limpias
        data_cleaned[column] = data_cleaned[column].map(mapping)



# Eliminar la columna 'COD_TARIFA'
if 'COD_TARIFA' in data_cleaned.columns:
    data_cleaned.drop(columns=['COD_TARIFA'], inplace=True)

# Guardar el DataFrame limpio en un nuevo archivo CSV
archivo_limpio = 'PROYECTO/BD_STAGE.csv'  
data_cleaned.to_csv(archivo_limpio, index=False, sep=';',  encoding='utf-8') 

print(f"Archivo limpio guardado como: {archivo_limpio}")
