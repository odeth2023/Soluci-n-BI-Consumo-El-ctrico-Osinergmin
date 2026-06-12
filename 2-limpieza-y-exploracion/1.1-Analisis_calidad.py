import pandas as pd

# Cargar el archivo CSV
archivo_csv = 'PROYECTO/Reporte del consumo de energía eléctrica (kWh-mes) - 202301 - 202408.csv'  
data = pd.read_csv(archivo_csv, delimiter=';', encoding='latin1')


# Dimensiones del dataset
num_filas, num_columnas = data.shape

# Tipos de datos
print("Tipos de datos por columna:")
print(data.dtypes, "\n")

# Valores nulos
nulos_por_columna = data.isnull().sum()
porcentaje_nulos = (nulos_por_columna / num_filas) * 100
print("Valores nulos por columna:")
print(pd.DataFrame({'Nulos': nulos_por_columna, '% Nulos': porcentaje_nulos}).sort_values(by='Nulos', ascending=False), "\n")

# Duplicados
duplicados = data.duplicated().sum()
print(f"El dataset tiene {duplicados} filas duplicadas.\n")

# Analizando las fechas/Fecha de corte después de fecha de emisión
# Convirtiendo las columnas de fecha a formato datetime
data['FECHA_CORTE'] = pd.to_datetime(data['FECHA_CORTE'], format='%d%m%Y', errors='coerce')
data['FECHA_EMISION'] = pd.to_datetime(data['FECHA_EMISION'], format='%Y%m%d', errors='coerce')

# Validando que FECHA_CORTE sea posterior a FECHA_EMISION
data['CORTE_POSTERIOR_A_EMISION'] = data['FECHA_CORTE'] > data['FECHA_EMISION']

print("\nAnálisis de fechas:Fecha de corte después de fecha de emisión")
print(f"Filas donde FECHA_CORTE es posterior a FECHA_EMISION: {data['CORTE_POSTERIOR_A_EMISION'].sum()} / {len(data)}")

# Mostrando ejemplos de filas que no cumplen cada condición
print("\nEjemplos donde FECHA_CORTE no es posterior a FECHA_EMISION:")
print(data.loc[~data['CORTE_POSTERIOR_A_EMISION'], ['FECHA_CORTE', 'FECHA_EMISION']].head())



# Analizando las fechas/Mes de emisión mismo de fecha de emisión
# Extrayendo año y mes de FECHA_EMISION
data['AÑO_EMISION'] = data['FECHA_EMISION'].dt.year
data['MES_EMISION'] = data['FECHA_EMISION'].dt.month

# Validando la concordancia con MES_FACTURACION
data['MES_FACTURACION'] = pd.to_numeric(data['MES_FACTURACION'], errors='coerce')
data['AÑO_FACTURACION'] = (data['MES_FACTURACION'] // 100).astype(int)
data['MES_FACTURACION_MES'] = (data['MES_FACTURACION'] % 100).astype(int)
data['FACTURACION_CONCORDE'] = (
    (data['AÑO_EMISION'] == data['AÑO_FACTURACION']) &
    (data['MES_EMISION'] == data['MES_FACTURACION_MES'])
)

print("Análisis de fechas: Mes de emisión mismo de fecha de emisión")
print(f"Filas donde MES_FACTURACION concuerda con FECHA_EMISION: {data['FACTURACION_CONCORDE'].sum()} / {len(data)}")

# Mostrando ejemplos de filas que no cumplen cada condición
print("\nEjemplos donde MES_FACTURACION no concuerda con FECHA_EMISION:")
print(data.loc[~data['FACTURACION_CONCORDE'], ['MES_FACTURACION', 'FECHA_EMISION']].head())




# Valores únicos
print("Número de valores únicos por columna:")
valores_unicos = data.nunique()
print(valores_unicos, "\n")


#ANALIZANDO COD_SIS_ELECTR, CTARIFA, ATARIFA, USO, GRUPO, COD_EMPRESA
# Normalizando valores
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
