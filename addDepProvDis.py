import pandas as pd
import mysql.connector

# Establecer la conexión a la base de datos
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # La contraseña de tu base de datos
    database="IndiceDesarrolloHumano"
)
try:
    # Usar un context manager para el cursor
    with conexion.cursor() as cursor:
        # Cargar el archivo Excel con los datos de departamentos
        archivo_departamentos = './Departamentos.xlsx'
        datos_departamentos = pd.read_excel(archivo_departamentos)

        # Insertar datos en la tabla Departamentos
        for index, row in datos_departamentos.iterrows():
            cursor.execute("INSERT INTO Departamentos (Nombre, UBIGEO) VALUES (%s, %s)", (row['Nombre'], row['UBIGEO']))
            
        # # Cargar el archivo Excel con los datos de provincias
        archivo_provincias = './Provincias.xlsx'
        datos_provincias = pd.read_excel(archivo_provincias)

        

        # Insertar datos en la tabla Provincias
        for index, row in datos_provincias.iterrows():
            # Obtener el ID del departamento basado en el nombre del departamento
            cursor.execute("SELECT ID_DEPARTAMENTO FROM Departamentos WHERE Nombre = %s", (row['DEPARTAMENTO'],))
            resultado = cursor.fetchone()
            id_departamento = resultado[0] if resultado else None

            # Verificar que se encontró un ID de departamento
            if id_departamento is not None:
                # Insertar el registro en la tabla de Provincias
                cursor.execute("INSERT INTO Provincias (ID_DEPARTAMENTO, Nombre, UBIGEO) VALUES (%s, %s, %s)",
                               (id_departamento, row['PROVINCIA'], row['UBIGEO']))

        # Cargar el archivo Excel con los datos de distritos
        archivo_distritos = './Distritos.xlsx'
        datos_distritos = pd.read_excel(archivo_distritos)



        # Insertar datos en la tabla Distritos
        for index, row in datos_distritos.iterrows():
            # Obtener el ID del departamento basado en el nombre del departamento
            cursor.execute("SELECT ID_DEPARTAMENTO FROM Departamentos WHERE Nombre = %s", (row['DEPARTAMENTO'],))
            resultado_departamento = cursor.fetchone()
            id_departamento = resultado_departamento[0] if resultado_departamento else None

            if id_departamento is not None:
                # Obtener el ID de la provincia basado en el nombre de la provincia y el ID del departamento
                cursor.execute("SELECT ID_PROVINCIA FROM Provincias WHERE Nombre = %s AND ID_DEPARTAMENTO = %s",
                               (row['PROVINCIA'], id_departamento))
                resultado_provincia = cursor.fetchone()
                id_provincia = resultado_provincia[0] if resultado_provincia else None

                if id_provincia is not None:
                    # Insertar el registro en la tabla de Distritos
                    cursor.execute("INSERT INTO Distritos (ID_PROVINCIA, Nombre, UBIGEO) VALUES (%s, %s, %s)",
                                   (id_provincia, row['DISTRITO'], row['UBIGEO']))


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

       

