-- Create the database
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'DesarrolloHumano')
BEGIN
    CREATE DATABASE DesarrolloHumano;
END;
GO

-- Use the database
USE IndiceDesarrolloHumano;
GO

-- Create the Departamentos table
CREATE TABLE Departamentos (
    ID_DEPARTAMENTO INT IDENTITY(1,1) PRIMARY KEY,
    Nombre VARCHAR(50),
    UBIGEO VARCHAR(6)
);
GO

-- Create the Provincias table
CREATE TABLE Provincias (
    ID_PROVINCIA INT IDENTITY(1,1) PRIMARY KEY,
    ID_DEPARTAMENTO INT,
    Nombre VARCHAR(50),
    UBIGEO VARCHAR(6),
    FOREIGN KEY (ID_DEPARTAMENTO) REFERENCES Departamentos(ID_DEPARTAMENTO)
);
GO

-- Create the Distritos table
CREATE TABLE Distritos (
    ID_DISTRITO INT IDENTITY(1,1) PRIMARY KEY,
    ID_PROVINCIA INT,
    Nombre VARCHAR(50),
    UBIGEO VARCHAR(6),
    FOREIGN KEY (ID_PROVINCIA) REFERENCES Provincias(ID_PROVINCIA)
);
GO

-- Create the Poblacion table
CREATE TABLE Poblacion (
    ID INT IDENTITY(1,1) PRIMARY KEY,
    ID_DISTRITO INT,
    Año INT,
    Poblacion INT,
    FOREIGN KEY (ID_DISTRITO) REFERENCES Distritos(ID_DISTRITO)
);
GO

-- Create the IDH table
CREATE TABLE IDH (
    ID INT IDENTITY(1,1) PRIMARY KEY,
    ID_DISTRITO INT,
    Año INT,
    IDH FLOAT,
    FOREIGN KEY (ID_DISTRITO) REFERENCES Distritos(ID_DISTRITO)
);
GO

-- Create the EsperanzaVida table
CREATE TABLE EsperanzaVida (
    ID INT IDENTITY(1,1) PRIMARY KEY,
    ID_DISTRITO INT,
    Año INT,
    Esperanza_Vida FLOAT,
    FOREIGN KEY (ID_DISTRITO) REFERENCES Distritos(ID_DISTRITO)
);
GO

-- Create the EducacionSecundaria table
CREATE TABLE EducacionSecundaria (
    ID INT IDENTITY(1,1) PRIMARY KEY,
    ID_DISTRITO INT,
    Año INT,
    Educacion_Secundaria FLOAT,
    FOREIGN KEY (ID_DISTRITO) REFERENCES Distritos(ID_DISTRITO)
);
GO

-- Create the AñosEducacion table
CREATE TABLE AñosEducacion (
    ID INT IDENTITY(1,1) PRIMARY KEY,
    ID_DISTRITO INT,
    Año INT,
    Años_Educacion FLOAT,
    FOREIGN KEY (ID_DISTRITO) REFERENCES Distritos(ID_DISTRITO)
);
GO

-- Create the IngresoFamiliar table
CREATE TABLE IngresoFamiliar (
    ID INT IDENTITY(1,1) PRIMARY KEY,
    ID_DISTRITO INT,
    Año INT,
    Ingreso_Familiar FLOAT,
    FOREIGN KEY (ID_DISTRITO) REFERENCES Distritos(ID_DISTRITO)
);
GO
