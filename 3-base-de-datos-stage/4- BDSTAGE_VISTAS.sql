CREATE OR ALTER VIEW vw_ConsumoEnergia AS
SELECT   
ce.id as id,
t.id as tiempoId,
dimEmp.id as empresaId,
u.id as ubicacionId,
dimTa.id as tarifaId,
ce.promedio_consumo
FROM            
STAGE_OSINERGMIN.dbo.ConsumoElectrico ce

-- DIM TIEMPO
INNER JOIN DW_Osinergmin.dbo.dimTiempo t
	ON YEAR(ce.fecha_emision)=t.year_facturacion
	AND ce.mes_facturacion= t.mes_facturacion

-- DIM EMPRESA 
INNER JOIN STAGE_OSINERGMIN.dbo.SistemaElectrico s
	ON ce.id_sistema_electrico=s.id
INNER JOIN STAGE_OSINERGMIN.dbo.Empresa e
	ON s.id_empresa=e.id
INNER JOIN STAGE_OSINERGMIN.dbo.Grupo g
	ON e.id_grupo = g.id
INNER JOIN DW_Osinergmin.dbo.dimEmpresa dimEmp
	ON dimEmp.cod_sis_electr = s.cod_sis_electr
	AND dimEmp.grupo = g.tipo_grupo
	AND dimEmp.nombre = e.nombre

-- DIM UBICACION
join DW_Osinergmin.dbo.dimUbicacion u
ON s.id_departamento=u.id

-- DIM TARIFA
inner join STAGE_OSINERGMIN.dbo.Tarifa ta1
	ON ta1.id = ce.id_ctarifa
inner join STAGE_OSINERGMIN.dbo.DescripcionTarifa dt1
	ON dt1.id = ce.id_dtarifa
inner join STAGE_OSINERGMIN.dbo.Uso us1
	ON us1.id = ta1.id_uso
inner join DW_Osinergmin.dbo.dimTarifa dimTa
	ON ta1.cod_tarifa = dimTa.tarifa 
	AND us1.tipo_uso = dimTa.uso
	AND CASE WHEN dt1.descripcion = 'EXCESO DE 1000 KW.H' THEN 1 ELSE 0 END = dimTa.excedido


CREATE OR ALTER VIEW vw_Tiempo AS
SELECT DISTINCT 
YEAR(fecha_emision) AS year_facturacion, 
mes_facturacion,

FORMAT(DATEFROMPARTS(2024, mes_facturacion, 1), 'MMMM', 'es-ES') AS nombre_mes,
CASE
   WHEN mes_facturacion IN (10,11,12) THEN N'primavera'
   WHEN mes_facturacion IN (1,2,3) THEN N'verano'
   WHEN mes_facturacion IN (4,5,6) THEN N'otoño'
   WHEN mes_facturacion IN (7,8,9) THEN N'invierno'
END as estacion

FROM dbo.ConsumoElectrico 



CREATE OR ALTER VIEW vw_tarifa AS
SELECT DISTINCT 
dbo.Tarifa.cod_tarifa AS TARIFA, 
CASE WHEN dbo.DescripcionTarifa.descripcion = 'EXCESO DE 1000 KW.H' THEN 1 ELSE 0 END AS EXCEDIDO, 
CASE WHEN dbo.DescripcionTarifa.descripcion = 'EXCESO DE 1000 KW.H' THEN N'SI' ELSE N'NO' END AS descripcion_excedido, 
dbo.Uso.tipo_uso
FROM            dbo.ConsumoElectrico INNER JOIN
                         dbo.Tarifa ON dbo.ConsumoElectrico.id_ctarifa = dbo.Tarifa.id INNER JOIN
                         dbo.DescripcionTarifa ON dbo.ConsumoElectrico.id_dtarifa = dbo.DescripcionTarifa.id INNER JOIN
                         dbo.Uso ON dbo.Tarifa.id_uso = dbo.Uso.id

SELECT DISTINCT dbo.Empresa.nombre, dbo.Grupo.tipo_grupo, dbo.SistemaElectrico.cod_sis_electr
FROM            dbo.Empresa INNER JOIN
                         dbo.Grupo ON dbo.Empresa.id_grupo = dbo.Grupo.id INNER JOIN
                         dbo.SistemaElectrico ON dbo.Empresa.id = dbo.SistemaElectrico.id_empresa


SELECT        id, nombre AS departamento
FROM            dbo.Departamento