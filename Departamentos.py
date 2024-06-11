import pandas as pd

# Cargar el archivo Excel y seleccionar la hoja adecuada
archivo = pd.read_excel('./IDH y Componentes - transf.xlsx', sheet_name='Variables del IDH 2003-2017')

# Eliminar columnas y filas completamente vacías
archivo = archivo.dropna(axis=1, how='all')
archivo = archivo.dropna(axis=0, how='all')

# Usar la primera fila como nombres de columna
archivo.columns = archivo.iloc[0]
archivo = archivo.drop(archivo.index[0])

# Asegurarnos de que las columnas UBIGEO y DEPARTAMENTO existan
if 'UBIGEO' in archivo.columns and 'DEPARTAMENTO' in archivo.columns:
    # Seleccionar solo las columnas de interés
    ubigeo_departamentos = archivo[['UBIGEO', 'DEPARTAMENTO']]
    
    # Convertir todos los nombres de departamento a minúsculas
    ubigeo_departamentos['DEPARTAMENTO'] = ubigeo_departamentos['DEPARTAMENTO'].str.lower()
    
    # Capitalizar la primera letra de cada nombre de departamento
    ubigeo_departamentos['DEPARTAMENTO'] = ubigeo_departamentos['DEPARTAMENTO'].str.capitalize()
    
    # Eliminar duplicados manteniendo solo el primero de cada DEPARTAMENTO
    primeros_registros = ubigeo_departamentos.drop_duplicates(subset=['DEPARTAMENTO'], keep='first')
    
  # Eliminar registros NaN en caso de que haya alguno después de las operaciones anteriores
    primeros_registros = primeros_registros.dropna()

     # Eliminar la fila que contiene "Peru" como departamento
    primeros_registros = primeros_registros[primeros_registros['DEPARTAMENTO'] != 'Perú']
  # Guardar el DataFrame en un archivo Excel
    primeros_registros.to_excel('./departamentos_unicos.xlsx', index=False)
    
    print("Se ha guardado exitosamente el DataFrame en 'departamentos_unicos.xlsx'.")
    # Mostrar los resultados
    print(primeros_registros)
     # Contar la cantidad de departamentos únicos
    cantidad_departamentos = primeros_registros['DEPARTAMENTO'].nunique()
    print(f'Hay {cantidad_departamentos} departamentos únicos.')
else:
    print("Las columnas UBIGEO y DEPARTAMENTO no se encuentran en el archivo.")

    