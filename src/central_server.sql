-- Crear base de datos Central
CREATE DATABASE Central;
USE Central;

EXEC sys.sp_cdc_enable_db;

CREATE TABLE dbo.CatLineasAereas (
    Code NVARCHAR(2) PRIMARY KEY,
    Linea_Aerea NVARCHAR(128)
);

EXEC sys.sp_cdc_enable_table
    @source_schema = 'dbo',
    @source_name = 'CatLineasAereas',
    @role_name = NULL;
