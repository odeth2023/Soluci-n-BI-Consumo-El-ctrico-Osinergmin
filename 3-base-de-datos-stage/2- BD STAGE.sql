--Base de datos STAGE
CREATE DATABASE STAGE_OSINERGMIN;

-- Tabla Uso
CREATE TABLE Uso (
    id INT PRIMARY KEY,
    tipo_uso VARCHAR(50) NOT NULL, 
);

-- Tabla Descripcion de Tarifa
CREATE TABLE DescripcionTarifa (
    id INT PRIMARY KEY,
    descripcion VARCHAR(50) NOT NULL,
);

-- Tabla Tarifa
CREATE TABLE Tarifa (
    id INT PRIMARY KEY,
    cod_tarifa VARCHAR(255) NOT NULL,   
	id_uso int not null,
	FOREIGN KEY (id_uso) REFERENCES USO(id)
);

-- Tabla Grupo
CREATE TABLE Grupo (
    id INT PRIMARY KEY,
    tipo_grupo VARCHAR(50) NOT NULL
);

-- Tabla Empresa
CREATE TABLE Empresa (
    id VARCHAR(10) NOT NULL PRIMARY KEY,
	codigo_empresa varchar(10) not null,
    nombre VARCHAR(100) NOT NULL,
	razon_social varchar(100) not null,
    id_grupo INT NOT NULL,
    FOREIGN KEY (id_grupo) REFERENCES Grupo(id)
);

-- Tabla Departamento
CREATE TABLE Departamento(
    id INT NOT NULL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
);

-- Tabla Sistema Electrico
CREATE TABLE SistemaElectrico (
    id INT PRIMARY KEY,
    cod_sis_electr VARCHAR(10) NOT NULL,
    id_empresa VARCHAR(10) NOT NULL,
	id_departamento int NOT NULL,
    FOREIGN KEY (id_empresa) REFERENCES Empresa(id),
	FOREIGN KEY (id_departamento) REFERENCES Departamento(id)
);

-- Tabla de Consumo Eléctrico
CREATE TABLE ConsumoElectrico (
    id INT PRIMARY KEY,
    fecha_emision DATE NOT NULL,
    mes_facturacion VARCHAR(6) NOT NULL,
	id_sistema_electrico INT NOT NULL,
    id_ctarifa INT NOT NULL,
	id_dtarifa INT NOT NULL,
    promedio_consumo FLOAT NOT NULL,
	cant_suministros int not null,
    FOREIGN KEY (id_ctarifa) REFERENCES Tarifa(id),
	FOREIGN KEY (id_dtarifa) REFERENCES DescripcionTarifa(id),
    FOREIGN KEY (id_sistema_electrico) REFERENCES SistemaElectrico(id)
);



--drop database BD_Osinergmin
-- drop table Tarifa