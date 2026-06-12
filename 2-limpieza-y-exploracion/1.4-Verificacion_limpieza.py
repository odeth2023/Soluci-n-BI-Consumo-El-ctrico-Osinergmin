import pandas as pd

# Cargar el archivo CSV
archivo_csv = 'BD_STAGE_Archivo_Limpio.csv'  
data = pd.read_csv(archivo_csv, delimiter=';', encoding='latin1')

#ANALIAZNDO COD_SIS_ELECTR, CTARIFA, ATARIFA, USO, GRUPO, COD_EMPRESA, RAZON_SOCIAL
# Función para normalizar los valores
def normalize(value):
    if pd.isna(value):
        return None
    return ' '.join(value.strip().lower().split())

# Encontrando valores similares en una columna
def find_similar_values(column, column_name):
    # Se crea un mapeo de valores normalizados a los originales
    normalized_mapping = {}
    for original_value in column.dropna():
        normalized_value = normalize(original_value)
        if normalized_value in normalized_mapping:
            normalized_mapping[normalized_value].add(original_value)
        else:
            normalized_mapping[normalized_value] = {original_value}

    # Se calcula la cantidad de errores
    errors = [values for values in normalized_mapping.values() if len(values) > 1]
    error_count = len(errors)

    print(f"\nColumna: {column_name}")
    # Mostrando resultados
    if error_count == 0:
        print(f"No presenta errores.")
    else:
        print(f"Cantidad de errores encontrados: {error_count}")

# Ejecutando la función para cada columna
columns_to_analyze = {
    'COD_SIS_ELECTR': data['COD_SIS_ELECTR'],
    'DEPARTAMENTO':data['DEPARTAMENTO'],
    'CTARIFA': data['CTARIFA'],
    'ATARIFA': data['ATARIFA'],
    'USO': data['USO'],
    'GRUPO': data['GRUPO'],
    'COD_EMPRESA': data['COD_EMPRESA'],
    'NOM_EMPRESA': data['NOM_EMPRESA']
}

for column_name, column_data in columns_to_analyze.items():
    find_similar_values(column_data, column_name)


