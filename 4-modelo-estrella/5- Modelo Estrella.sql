--Modelo Estrella

--Dimensión Empresa
CREATE TABLE dimEmpresa (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nombre VARCHAR(100) NULL,
    grupo VARCHAR(20) NULL,
    cod_sis_electr VARCHAR(10) NOT NULL
);

--Dimensión Tarifa
CREATE TABLE dimTarifa (
    id INT IDENTITY(1,1) PRIMARY KEY,
    tarifa VARCHAR(10) NULL,
    excedido TINYINT NULL,
	descripcion_excedido nvarchar not null,
    uso VARCHAR(20) NOT NULL
);

--Dimensión Tiempo
CREATE TABLE dimTiempo (
    id INT IDENTITY(1,1) PRIMARY KEY,
    year_facturacion INT NOT NULL,
    mes_facturacion INT NULL,
	nombres_mes varchar(10) not null,
	estacion varchar(10) not null
);

--Dimensión Ubicación
CREATE TABLE dimUbicacion (
    id INT NOT NULL,
    departamento VARCHAR(100) NULL,
    CONSTRAINT PK_dimUbicacion PRIMARY KEY (id)
);

--Tabla de Hechos
CREATE TABLE hechosConsumoPromedioEnergia (
    id INT NOT NULL,
    tiempoId INT NULL,
    empresaId INT NULL,
    ubicacionId INT NULL,
    tarifaId INT NULL,
    ConsumoPromedio INT NULL,
    CONSTRAINT PK_fctPromedioEnergia PRIMARY KEY (id),
    CONSTRAINT FK_fctPromedioEnergia_tiempo FOREIGN KEY (tiempoId) REFERENCES dimTiempo(id),
    CONSTRAINT FK_fctPromedioEnergia_empresa FOREIGN KEY (empresaId) REFERENCES dimEmpresa(id),
    CONSTRAINT FK_fctPromedioEnergia_ubicacion FOREIGN KEY (ubicacionId) REFERENCES dimUbicacion(id),
    CONSTRAINT FK_fctPromedioEnergia_tarifa FOREIGN KEY (tarifaId) REFERENCES dimTarifa(id)
);

--select

SELECT 
    h.id AS id_PromedioEnergia,
    t.year_facturacion AS año,
    t.mes_facturacion AS mes,
    e.nombre AS nombre_empresa,
    e.grupo,
    e.cod_sis_electr,
    u.departamento,
    tr.tarifa,
    tr.excedido,
    tr.uso,
    h.ConsumoPromedio
FROM hechosConsumoPromedioEnergia h
LEFT JOIN dimTiempo t ON h.tiempoId = t.id
LEFT JOIN dimEmpresa e ON h.empresaId = e.id
LEFT JOIN dimUbicacion u ON h.ubicacionId = u.id
LEFT JOIN dimTarifa tr ON h.tarifaId = tr.id;
