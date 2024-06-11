import pandas as pd

# Cargar el archivo Excel y seleccionar la hoja adecuada
archivo = pd.read_excel('./IDH y Componentes - transf.xlsx', sheet_name='Variables del IDH 2003-2017')

# Eliminar registros con todos los valores NaN
archivo = archivo.dropna(axis=0, how='all')

# Usar la primera fila como nombres de columna
archivo.columns = archivo.iloc[0]
archivo = archivo.drop(archivo.index[0])

# Asegurarnos de que las columnas UBIGEO, DEPARTAMENTO y Provincia existan
if 'UBIGEO' in archivo.columns and 'DEPARTAMENTO' in archivo.columns and 'PROVINCIA' in archivo.columns:
    # Seleccionar solo las columnas de interés
    ubigeo_provincias = archivo[['UBIGEO', 'DEPARTAMENTO', 'PROVINCIA']]
    
    # Convertir todos los nombres de departamento y provincia a minúsculas
    ubigeo_provincias['DEPARTAMENTO'] = ubigeo_provincias['DEPARTAMENTO'].str.lower()
    ubigeo_provincias['PROVINCIA'] = ubigeo_provincias['PROVINCIA'].str.lower()
    
    # Capitalizar la primera letra de cada nombre de departamento y provincia
    ubigeo_provincias['DEPARTAMENTO'] = ubigeo_provincias['DEPARTAMENTO'].str.capitalize()
    ubigeo_provincias['PROVINCIA'] = ubigeo_provincias['PROVINCIA'].str.capitalize()
    
    # Eliminar registros con campos vacíos en UBIGEO, DEPARTAMENTO o PROVINCIA
    ubigeo_provincias = ubigeo_provincias.dropna(subset=['UBIGEO', 'DEPARTAMENTO', 'PROVINCIA'])
    
    # Eliminar duplicados manteniendo solo el primero de cada provincia por departamento
    provincias_por_departamento = ubigeo_provincias.drop_duplicates(subset=['DEPARTAMENTO', 'PROVINCIA'], keep='first')
    
    # Guardar el DataFrame en un archivo Excel
    provincias_por_departamento.to_excel('./provincias_por_departamento.xlsx', index=False)
    
    print("Se ha guardado exitosamente el DataFrame en 'provincias_por_departamento.xlsx'.")
else:
    print("Las columnas UBIGEO, DEPARTAMENTO y Provincia no se encuentran en el archivo.")
