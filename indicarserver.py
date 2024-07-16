import pandas as pd
import pyodbc

# Función para cargar datos de un archivo Excel y asegurarse de tener todas las columnas necesarias
def cargar_excel(ruta_archivo, hoja, columnas_necesarias):
    df = pd.read_excel(ruta_archivo, sheet_name=hoja)

    # Eliminar registros con todos los valores NaN
    df = df.dropna(axis=0, how='all')

    # Asegurarse de que todas las columnas necesarias estén presentes
    for col in columnas_necesarias:
        if col not in df.columns:
            raise ValueError(f"La columna '{col}' no está presente en el archivo {ruta_archivo}.")

    return df

# Función para normalizar el UBIGEO
def normalizar_ubigeo(ubigeo):
    # Eliminar espacios y guiones y rellenar con ceros a la izquierda
    return ubigeo.replace(" ", "").replace("-", "").zfill(6)

# Establecer la conexión a la base de datos (ajustar según tu configuración)
conexion_str = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=DESKTOP-471B0LK;"
    "DATABASE=DesarrolloHumano;"
    "UID=sa;"
    "PWD=123;"
    "TrustServerCertificate=yes;"
)

conexion = None

try:
    # Establecer la conexión
    conexion = pyodbc.connect(conexion_str)
    cursor = conexion.cursor()

    # Cargar datos de los archivos Excel
    archivo_idh = './IDH y Componentes - transf.xlsx'
    archivo_departamentos = './Departamentos.xlsx'
    archivo_provincias = './Provincias.xlsx'
    archivo_distritos = './Distritos.xlsx'

    # Cargar datos de los archivos Excel
    df_idh = cargar_excel(archivo_idh, 'Variables del IDH 2003-2017',
                          ['UBIGEO', 'DEPARTAMENTO', 'PROVINCIA', 'DISTRITO'])
    df_departamentos = cargar_excel(archivo_departamentos, 'Sheet1', ['UBIGEO', 'Nombre'])
    df_provincias = cargar_excel(archivo_provincias, 'Sheet1', ['UBIGEO', 'DEPARTAMENTO', 'PROVINCIA'])
    df_distritos = cargar_excel(archivo_distritos, 'Sheet1', ['UBIGEO', 'DEPARTAMENTO', 'PROVINCIA', 'DISTRITO'])

    # Convertir nombres a minúsculas y capitalizar la primera letra
    for df in [df_idh, df_departamentos, df_provincias, df_distritos]:
        for col in df.columns:
            if isinstance(df[col], str):
                df[col] = df[col].str.lower().str.capitalize()

    # Lista de años
    anos = [2003, 2007, 2010, 2011, 2012, 2015, 2017]

    # Procesar cada año
    for ano in anos:
        try:
            # Seleccionar las columnas de interés para el año actual
            cols = ['UBIGEO', 'DEPARTAMENTO', 'PROVINCIA', 'DISTRITO',
                    f'habitantes_{ano}', f'idh_{ano}', f'esperanza_vida_{ano}',
                    f'secundaria_completa_{ano}', f'anho_educacion_{ano}',
                    f'ingreso_capital_mensual_{ano}']

            df_ano = df_idh[cols].copy()

            # Renombrar las columnas para que coincidan con la tabla SQL
            df_ano.columns = ['UBIGEO', 'DEPARTAMENTO', 'PROVINCIA', 'DISTRITO',
                              'Población', 'IDH', 'Esperanza_Vida', 'Educacion_Secundaria',
                              'Años_Educacion', 'Ingreso_Familiar']

            # Añadir la columna del año
            df_ano['Año'] = ano

            # Insertar los datos en las tablas correspondientes
            for index, row in df_ano.iterrows():
                try:
                    # Verificar si 'DEPARTAMENTO' y 'UBIGEO' no son NaN
                    if pd.notna(row['DEPARTAMENTO']) and pd.notna(row['UBIGEO']):
                        # Normalizar el UBIGEO
                        ubigeo_normalizado = normalizar_ubigeo(row['UBIGEO'])

                        # Obtener el ID del distrito basado en el nombre del distrito y UBIGEO normalizado
                        cursor.execute("SELECT ID_DISTRITO FROM Distritos WHERE Nombre = ? AND UBIGEO = ?",
                                       (row['DISTRITO'], ubigeo_normalizado))
                        resultado = cursor.fetchone()
                        id_distrito = resultado[0] if resultado else None

                        if id_distrito is not None:
                            # Insertar el registro en la tabla de población
                            cursor.execute("""INSERT INTO Poblacion (ID_DISTRITO, Año, Poblacion)
                                              VALUES (?, ?, ?)""",
                                           (id_distrito, row['Año'], row['Población']))
                            conexion.commit()
                            
                            # Insertar el registro en la tabla de IDH
                            cursor.execute("""INSERT INTO IDH (ID_DISTRITO, Año, IDH)
                                              VALUES (?, ?, ?)""",
                                           (id_distrito, row['Año'], row['IDH']))
                            conexion.commit()

                            # Insertar el registro en la tabla de esperanza de vida
                            cursor.execute("""INSERT INTO EsperanzaVida (ID_DISTRITO, Año, Esperanza_Vida)
                                              VALUES (?, ?, ?)""",
                                           (id_distrito, row['Año'], row['Esperanza_Vida']))
                            conexion.commit()

                            # Insertar el registro en la tabla de educación secundaria
                            cursor.execute("""INSERT INTO EducacionSecundaria (ID_DISTRITO, Año, Educacion_Secundaria)
                                              VALUES (?, ?, ?)""",
                                           (id_distrito, row['Año'], row['Educacion_Secundaria']))
                            conexion.commit()

                            # Insertar el registro en la tabla de años de educación
                            cursor.execute("""INSERT INTO AñosEducacion (ID_DISTRITO, Año, Años_Educacion)
                                              VALUES (?, ?, ?)""",
                                           (id_distrito, row['Año'], row['Años_Educacion']))
                            conexion.commit()

                            # Insertar el registro en la tabla de ingreso familiar
                            cursor.execute("""INSERT INTO IngresoFamiliar (ID_DISTRITO, Año, Ingreso_Familiar)
                                              VALUES (?, ?, ?)""",
                                           (id_distrito, row['Año'], row['Ingreso_Familiar']))
                            conexion.commit()
                            
                            print(f"Insertado indicador para distrito {row['DISTRITO']} en año {ano}.")

                        else:
                            print(f"ID de distrito no encontrado para {row['DISTRITO']} con UBIGEO {ubigeo_normalizado}.")
                    else:
                        print(f"Datos faltantes en la fila {index}: DEPARTAMENTO={row['DEPARTAMENTO']}, UBIGEO={row['UBIGEO']}")
                except Exception as e:
                    print(f"Error al procesar la fila {index}: {e}")

            print("Commit final realizado para el año:", ano)

        except Exception as e:
            # Deshacer la transacción en caso de error para este año
            conexion.rollback()
            print(f"Error al procesar el año {ano}: {e}")

    print("Datos insertados exitosamente en las tablas de indicadores.")

except Exception as e:
    # Deshacer la transacción en caso de error
    if conexion:
        conexion.rollback()
    print("Ocurrió un error:", e)

finally:
    # Cerrar la conexión
    if conexion:
        conexion.close()
