import pandas as pd
import pyodbc

# Función para normalizar el UBIGEO
def normalizar_ubigeo(ubigeo):
    if isinstance(ubigeo, str):
        # Si es una cadena de texto, eliminar espacios y guiones y rellenar con ceros a la izquierda
        return ubigeo.replace(" ", "").replace("-", "").zfill(6)
    elif isinstance(ubigeo, int):
        # Si es un entero, convertirlo a cadena de texto y luego normalizar
        return str(ubigeo).zfill(6)
    else:
        # En caso de otro tipo de dato, devolver None o manejar según tu caso
        return None

# Establecer la conexión a la base de datos
conexion_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=DESKTOP-471B0LK;"
    "DATABASE=DesarrolloHumano;"
    "UID=sa;"
    "PWD=123;"
    "TrustServerCertificate=yes;"
)

# Conectar a la base de datos
conexion = pyodbc.connect(conexion_str)

try:
    # Usar un context manager para el cursor
    with conexion.cursor() as cursor:
        # Cargar el archivo Excel con los datos de departamentos
        archivo_departamentos = './Departamentos.xlsx'
        datos_departamentos = pd.read_excel(archivo_departamentos)

        # Insertar datos en la tabla Departamentos
        for index, row in datos_departamentos.iterrows():
            ubigeo_normalizado = normalizar_ubigeo(row['UBIGEO'])
            cursor.execute("INSERT INTO Departamentos (Nombre, UBIGEO) VALUES (?, ?)", (row['Nombre'], ubigeo_normalizado))
            
        # Cargar el archivo Excel con los datos de provincias
        archivo_provincias = './Provincias.xlsx'
        datos_provincias = pd.read_excel(archivo_provincias)

        # Insertar datos en la tabla Provincias
        for index, row in datos_provincias.iterrows():
            # Obtener el ID del departamento basado en el nombre del departamento
            cursor.execute("SELECT ID_DEPARTAMENTO FROM Departamentos WHERE Nombre = ?", (row['DEPARTAMENTO'],))
            resultado = cursor.fetchone()
            id_departamento = resultado[0] if resultado else None

            # Verificar que se encontró un ID de departamento
            if id_departamento is not None:
                ubigeo_normalizado = normalizar_ubigeo(row['UBIGEO'])
                # Insertar el registro en la tabla de Provincias
                cursor.execute("INSERT INTO Provincias (ID_DEPARTAMENTO, Nombre, UBIGEO) VALUES (?, ?, ?)",
                               (id_departamento, row['PROVINCIA'], ubigeo_normalizado))

        # Cargar el archivo Excel con los datos de distritos
        archivo_distritos = './Distritos.xlsx'
        datos_distritos = pd.read_excel(archivo_distritos)

        # Insertar datos en la tabla Distritos
        for index, row in datos_distritos.iterrows():
            # Obtener el ID del departamento basado en el nombre del departamento
            cursor.execute("SELECT ID_DEPARTAMENTO FROM Departamentos WHERE Nombre = ?", (row['DEPARTAMENTO'],))
            resultado_departamento = cursor.fetchone()
            id_departamento = resultado_departamento[0] if resultado_departamento else None

            if id_departamento is not None:
                # Obtener el ID de la provincia basado en el nombre de la provincia y el ID del departamento
                cursor.execute("SELECT ID_PROVINCIA FROM Provincias WHERE Nombre = ? AND ID_DEPARTAMENTO = ?",
                               (row['PROVINCIA'], id_departamento))
                resultado_provincia = cursor.fetchone()
                id_provincia = resultado_provincia[0] if resultado_provincia else None

                if id_provincia is not None:
                    ubigeo_normalizado = normalizar_ubigeo(row['UBIGEO'])
                    # Insertar el registro en la tabla de Distritos
                    cursor.execute("INSERT INTO Distritos (ID_PROVINCIA, Nombre, UBIGEO) VALUES (?, ?, ?)",
                                   (id_provincia, row['DISTRITO'], ubigeo_normalizado))

    # Confirmar la transacción
    conexion.commit()

    print("Datos insertados exitosamente en las tablas 'Departamentos', 'Provincias' y 'Distritos'.")

except Exception as e:
    # Deshacer la transacción en caso de error
    conexion.rollback()
    print("Ocurrió un error:", e)

finally:
    # Cerrar la conexión
    conexion.close()
