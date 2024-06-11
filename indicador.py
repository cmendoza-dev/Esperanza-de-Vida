import pandas as pd

# Cargar el archivo Excel y seleccionar la hoja adecuada
archivo = pd.read_excel('./IDH y Componentes - transf.xlsx', sheet_name='Variables del IDH 2003-2017')

# Eliminar registros con todos los valores NaN
archivo = archivo.dropna(axis=0, how='all')

# Usar la primera fila como nombres de columna
archivo.columns = archivo.iloc[0]
archivo = archivo.drop(archivo.index[0])

# Asegurarnos de que las columnas UBIGEO, DEPARTAMENTO, PROVINCIA y DISTRITO existan
if 'UBIGEO' in archivo.columns and 'DEPARTAMENTO' in archivo.columns and 'PROVINCIA' in archivo.columns and 'DISTRITO' in archivo.columns:
    # Lista de años
    anos = [2003, 2007, 2010, 2011, 2012, 2015, 2017]
    
    # Lista de indicadores
    indicadores = ['Indicador1', 'Indicador2', 'Indicador3', 'Indicador4']
    
    # Lista para almacenar los DataFrames de cada indicador
    dfs_indicadores = []
    
    # Para cada indicador
    for indicador in indicadores:
        # Seleccionar las columnas de interés (incluyendo UBIGEO, DEPARTAMENTO, PROVINCIA, DISTRITO y los años del indicador)
        df_indicador = archivo[['UBIGEO', 'DEPARTAMENTO', 'PROVINCIA', 'DISTRITO', indicador]]
        
        # Convertir todos los nombres a minúsculas y capitalizar la primera letra
        for col in ['DEPARTAMENTO', 'PROVINCIA', 'DISTRITO']:
            df_indicador[col] = df_indicador[col].str.lower().str.capitalize()
        
        # Derretir el DataFrame para tener un solo año por fila
        df_indicador = pd.melt(df_indicador, id_vars=['UBIGEO', 'DEPARTAMENTO', 'PROVINCIA', 'DISTRITO'], var_name='Año', value_name=indicador)
        
        # Agregar el DataFrame a la lista de DataFrames de indicadores
        dfs_indicadores.append(df_indicador)
    
    # Combinar los DataFrames de indicadores en un solo DataFrame final
    resultado_final = dfs_indicadores[0]  # Tomamos el primer DataFrame como base
    for df in dfs_indicadores[1:]:
        resultado_final = pd.merge(resultado_final, df, on=['UBIGEO', 'DEPARTAMENTO', 'PROVINCIA', 'DISTRITO', 'Año'], how='outer')
    
    # Guardar el DataFrame en un archivo Excel
    resultado_final.to_excel('./distritos_con_idh.xlsx', index=False)
    
    print("Se ha guardado exitosamente el DataFrame en 'distritos_con_idh.xlsx'.")
else:
    print("Las columnas UBIGEO, DEPARTAMENTO, PROVINCIA o DISTRITO no se encuentran en el archivo.")
