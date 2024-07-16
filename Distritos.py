import pandas as pd

# Cargar el archivo Excel y seleccionar la hoja adecuada
archivo = pd.read_excel('./IDH y Componentes - transf.xlsx', sheet_name='Variables del IDH 2003-2017')

# Eliminar registros con todos los valores NaN
archivo = archivo.dropna(axis=0, how='all')

# Asegurarnos de que las columnas UBIGEO, DEPARTAMENTO, PROVINCIA y DISTRITO existan
if 'UBIGEO' in archivo.columns and 'DEPARTAMENTO' in archivo.columns and 'PROVINCIA' in archivo.columns and 'DISTRITO' in archivo.columns:
    # Seleccionar solo las columnas de interés
    ubigeo_distritos = archivo[['UBIGEO', 'DEPARTAMENTO', 'PROVINCIA', 'DISTRITO']]
    
    # Convertir todos los nombres a minúsculas
    for col in ['DEPARTAMENTO', 'PROVINCIA', 'DISTRITO']:
        ubigeo_distritos[col] = ubigeo_distritos[col].str.lower()
    
    # Capitalizar la primera letra de cada nombre
    for col in ['DEPARTAMENTO', 'PROVINCIA', 'DISTRITO']:
        ubigeo_distritos[col] = ubigeo_distritos[col].str.capitalize()
    
    # Eliminar registros con campos vacíos en UBIGEO, DEPARTAMENTO, PROVINCIA o DISTRITO
    ubigeo_distritos = ubigeo_distritos.dropna(subset=['UBIGEO', 'DEPARTAMENTO', 'PROVINCIA', 'DISTRITO'])
    
    # Eliminar duplicados manteniendo solo el primero de cada distrito por provincia
    distritos_por_provincia = ubigeo_distritos.drop_duplicates(subset=['DEPARTAMENTO', 'PROVINCIA', 'DISTRITO'], keep='first')
    
    # Guardar el DataFrame en un archivo Excel
    distritos_por_provincia.to_excel('./Distritos.xlsx', index=False)

    # Seleccionar las columnas deseadas
    # Aquí 'COL1', 'COL2', 'COL3', 'COL4', 'COL5' son los nombres de las otras cinco columnas que quieres mostrar
    columnas_a_mostrar = ['DEPARTAMENTO', 'PROVINCIA', 'DISTRITO']
    resultado = distritos_por_provincia[columnas_a_mostrar]
    print("Se ha guardado exitosamente el DataFrame en 'Distritos.xlsx'.")
else:
    print("Las columnas UBIGEO, DEPARTAMENTO, PROVINCIA o DISTRITO no se encuentran en el archivo.")
