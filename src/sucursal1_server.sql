-- Crear base de datos Sucursal1
CREATE DATABASE Sucursal1;
USE Sucursal1;

-- Habilitar CDC a nivel de base de datos
EXEC sys.sp_cdc_enable_db;

-- Crear tablas
CREATE TABLE dbo.Pasajeros (
    ID_Pasajero INT PRIMARY KEY,
    Pasajero NVARCHAR(128),
    Edad INT
);

CREATE TABLE dbo.Vuelos (
    Sucursal INT,
    Cve_LA NVARCHAR(2),
    Viaje DATE,
    Clase NVARCHAR(32),
    Precio INT,
    Ruta NVARCHAR(32),
    Cve_Cliente INT
);

-- Habilitar CDC en las tablas
EXEC sys.sp_cdc_enable_table
    @source_schema = 'dbo',
    @source_name = 'Pasajeros',
    @role_name = NULL;

EXEC sys.sp_cdc_enable_table
    @source_schema = 'dbo',
    @source_name = 'Vuelos',
    @role_name = NULL;
