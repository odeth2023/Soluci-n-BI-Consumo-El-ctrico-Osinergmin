# Soluci-n-BI-Consumo-El-ctrico-Osinergmin
Proyecto académico desarrollado para el curso Laboratorio de Integración V
en Zegel Instituto (2024).

## Descripción
Solución de inteligencia de negocios aplicada a los reportes de facturación
y consumo eléctrico de empresas distribuidoras en el Perú, remitidos a
Osinergmin entre 2022 y agosto de 2024.

## Tecnologías
- SQL Server (base de datos stage y modelo estrella)
- SSIS (flujo ETL)
- SQL Server Analysis Services (cubo OLAP)
- Power BI (dashboards y predicción)
- Python / Excel (exploración y limpieza inicial)

## Qué hace
- Pipeline ETL completo: extracción desde CSV, limpieza,
  normalización y carga a modelo estrella
- Cubo OLAP con dimensiones de empresa, tarifa, tiempo y ubicación
- 6 reportes en Power BI: consumo mensual, estacional, por empresa,
  por departamento, empresas que excedieron el límite y predicción
  de demanda hasta 2025

## Fuente de datos
Datos abiertos de Perú – Reporte de consumo de energía eléctrica
(kWh/mes) publicado por Osinergmin.
