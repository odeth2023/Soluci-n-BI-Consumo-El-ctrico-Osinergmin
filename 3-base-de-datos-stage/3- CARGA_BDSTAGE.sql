
Create Procedure LoadUso
as
begin
INSERT INTO Uso(tipo_uso)
SELECT DISTINCT 
	uso
FROM BD.dbo.archivo_limpio_2$;
end

Create Procedure LoadDescripcionTarifa
as
begin
INSERT INTO DescripcionTarifa (descripcion)
SELECT DISTINCT 
	ATARIFA
FROM BD.dbo.archivo_limpio_2$ bdp;
end

Create Procedure LoadTarifa
as
begin
INSERT INTO Tarifa (cod_tarifa, id_uso)
SELECT DISTINCT 

    bdp.CTARIFA,
	u.id as id_uso

FROM BD.dbo.archivo_limpio_2$ bdp
INNER JOIN 
    [STAGE_OSINERGMIN].[dbo].[Uso] u
    ON bdp.USO = u.tipo_uso
end

Create Procedure LoadGrupo
as
begin
INSERT INTO Grupo(tipo_grupo)
SELECT DISTINCT 
	GRUPO
FROM BD.dbo.archivo_limpio_2$;
end

Create Procedure LoadEmpresa
as
begin
INSERT INTO Empresa (codigo_empresa, nombre, 
					razon_social, id_grupo)
SELECT DISTINCT 

    bdp.COD_EMPRESA,
	bdp.NOM_EMPRESA,
	bdp.RAZON_SOCIAL,
	g.id as id_grupo

FROM BD.dbo.archivo_limpio_2$ bdp
INNER JOIN 
    [STAGE_OSINERGMIN].[dbo].[Grupo] g
    ON bdp.GRUPO = g.tipo_grupo 
end

Create Procedure LoadDepartamento
as
begin
INSERT INTO Departamento(nombre)
SELECT DISTINCT 
	Departamento
FROM BD.dbo.archivo_limpio_2$;
end

Create Procedure LoadSistemaElectrico
as
begin
INSERT INTO SistemaElectrico(cod_sis_electr, id_empresa, 
							id_departamento)
SELECT DISTINCT 
	bdp.COD_SIS_ELECTR,
	e.id as id_empresa,
	d.id as id_departamento

FROM BD.dbo.archivo_limpio_2$ bdp
INNER JOIN 
	[STAGE_OSINERGMIN].[dbo].[Empresa] e
	ON bdp.NOM_EMPRESA=e.nombre
INNER JOIN 
	[STAGE_OSINERGMIN].[dbo].[Departamento] d
	ON bdp.DEPARTAMENTO=d.nombre
end

Create Procedure LoadConsumoElectrico
as
begin
INSERT INTO ConsumoElectrico(fecha_emision, mes_facturacion, 
							id_sistema_electrico, id_ctarifa, 
							id_dtarifa, promedio_consumo, 
							cant_suministros)
SELECT
	TRY_CONVERT(DATE, bdp.FECHA_EMISION, 112) fecha_emision,
	CAST(SUBSTRING(bdp.MES_FACTURACION, 5, 2) AS INT) AS mes_facturacion,
	s.id as id_sistema_electrico,
	t.id as id_ctarifa,
	d.id as id_dtarifa,
	bdp.PROMEDIO_CONSUMO,
	bdp.SUMINISTROS as cant_suministros

FROM BD.dbo.archivo_limpio_2$ bdp
INNER JOIN 
    [STAGE_OSINERGMIN].[dbo].[SistemaElectrico] s
	ON bdp.COD_SIS_ELECTR=s.cod_sis_electr
INNER JOIN 
    [STAGE_OSINERGMIN].[dbo].[Tarifa] t
	ON bdp.CTARIFA=t.cod_tarifa
INNER JOIN
	[STAGE_OSINERGMIN].[dbo].[DescripcionTarifa] d
	ON bdp.ATARIFA=d.descripcion
end

-- hay que hacer lo que hizo el profesor para que el Id empiece desde 1 yasta


SELECT 
    ce.fecha_emision as 'Fecha de emisión',         
    ce.mes_facturacion as 'Mes de facturación',        
    s.cod_sis_electr as 'Sistema Eléctrico',
	t.cod_tarifa as 'Código de Tarifa',
	d.descripcion as 'Descripción de Tarifa',
	ce.promedio_consumo as 'Consumo promedio de Energía',
	ce.cant_suministros as 'Cantidad de Suministros',
	de.nombre as 'Departamento'
FROM 
    [STAGE_OSINERGMIN].[dbo].[ConsumoElectrico] ce
INNER JOIN 
    [STAGE_OSINERGMIN].[dbo].[SistemaElectrico] s
    ON ce.id_sistema_electrico=s.id
INNER JOIN 
    [STAGE_OSINERGMIN].[dbo].[Tarifa] t 
    ON ce.id_ctarifa=t.id
INNER JOIN 
    [STAGE_OSINERGMIN].[dbo].[DescripcionTarifa] d
	ON ce.id_dtarifa=d.id
INNER JOIN
	[STAGE_OSINERGMIN].[dbo].[Departamento] de
	ON s.id_departamento=de.id

where s.cod_sis_electr='SR0283' and t.cod_tarifa='BT5B' and d.descripcion='EXCESO DE 1000 KW.H' and ce.mes_facturacion=12

--
CREATE OR ALTER VIEW hechosConsumoPromedioEnergia
AS
SELECT
	t1.id,
	Tmp.id AS tiempoId
FROM STAGE_OSINERGMIN.dbo.ConsumoElectrico t1
INNER JOIN DW_Osinergmin.dbo.dimTiempo Tmp
	ON Tmp.mes_facturacion = t1.mes_facturacion AND Tmp.year_facturacion = YEAR(t1.fecha_emision)