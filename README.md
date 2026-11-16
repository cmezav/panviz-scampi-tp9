# PANVIZ · Trabajo Parcial 9

Piloto académico de evaluación de procesos y calidad del producto. Equipo 03 (numeración tomada del trabajo anterior). CMMI-DEV v1.3 como marco histórico y autoevaluación inspirada en SCAMPI C. Microprototipo local de vigilancia con datos sintéticos.

## Arranque local

Desde esta carpeta, en Windows PowerShell con Python 3.10 o posterior:

```powershell
py -3 .\05_pruebas\medir.py
py -3 .\07_tablero\generar.py
py -3 .\04_prototipo\panviz.py --version v2 --port 8765
```

Abrir [prototipo](http://127.0.0.1:8765/) y [tablero](http://127.0.0.1:8765/evaluacion) con el servidor activo. En Linux/Mac, sustituir el lanzador py -3 por python3 y las barras invertidas por diagonales. No se instalan dependencias. La variante anterior se inicia con --version v1 --port 8766. Cada versión dispone de estado independiente. Ctrl+C detiene el servidor.

## Demostración

1. En v2 pulsar Cargar muestra de 30 y Validar e importar, o elegir [muestra.csv](04_prototipo/datos/muestra.csv).
2. Comprobar 24 aceptados, 6 rechazados con causas y agrupar por distrito y grupo. Seleccionar Chivay y esperar 6 casos repartidos 3/3.
3. Con rol Lector, pulsar Intentar publicar. Respuesta HTTP 403. El rol publicador simulado permite la publicación local, no representa autenticación. El servidor se enlaza solo a localhost.
4. En el tablero alternar v1/v2. Filtrar área RD y responsable E2; abrir E18 para inspeccionar el log. El formulario guarda aportes candidatos en este navegador y los descarga en CSV.
5. Consultar [Antes](07_tablero/capturas/antes.png), [Después](07_tablero/capturas/despues.png), [ODS](07_tablero/PANVIZ_Evaluacion.ods) y [respaldo de demostración](07_tablero/demostracion.mp4).

## Archivos y reproducción

- [Plan](01_plan/plan_evaluacion.md), [registro de aportes](01_plan/aportes.csv) y [ruta de exposición](01_plan/entrega_exposicion.md).
- [Estándar](02_procesos/estandar_v1.md), [adaptación](02_procesos/adaptacion.md) y [mejora](02_procesos/mejora_v2.md).
- [Requisitos](03_requisitos_riesgos/requisitos.md), [riesgos](03_requisitos_riesgos/riesgos.csv) y [regla cambiada](05_pruebas/diff_regla_fecha.txt).
- [Casos](05_pruebas/casos.csv), [v1](05_pruebas/resultados/v1.json), [v2](05_pruebas/resultados/v2.json) y [protocolo T09/T10](05_pruebas/protocolo_usuario.md).
- [Plan de acopio](06_evidencias/acopio.md), [índice](07_tablero/exportaciones/evidencias.csv), [criterios](07_tablero/exportaciones/criterios.csv), [trazabilidad](07_tablero/exportaciones/trazabilidad.csv), [indicadores](07_tablero/exportaciones/indicadores.csv) y [acciones](06_evidencias/acciones.csv).
- [Acta 01](06_evidencias/entrevistas/Acta_01_uso_proceso.md), [Acta 02](06_evidencias/entrevistas/Acta_02_validacion.md) y [revisión cruzada](06_evidencias/revision_cruzada/registro.md).
- [Herramienta de acopio](07_tablero/herramienta.md), [reporte](08_informe/Reporte_TP9_SCAMPI_PANVIZ.docx) y [comandos PowerShell](01_plan/PowerShell_GitHub.md).

La suite registra una prueba por ID en cada corte. T03 y T04 conservan las tres repeticiones HTTP locales. El generador recalcula el tablero HTML y los CSV a partir de ambos JSON, los 24 criterios y los hallazgos. La hoja ODS es una copia local de esos registros con fórmulas. Para actualizarla después de cambios, importar las tablas CSV a las hojas correspondientes y recalcular. Para el cierre humano, registrar tiempos, condiciones, resultado y evidencia real de T09/T10 en los JSON del corte medido, actualizar los criterios vinculados en generar.py y después regenerar las salidas. La suite automatizada no sustituye el registro de interacción; medir.py escribe el corte automatizado de nuevo.

## Estado de entrega

Capturas de v2: [T09: P026 corregido](06_evidencias/pruebas_usuario/T09_p026_corregido.png) y [T10: resumen de Chivay](06_evidencias/pruebas_usuario/T10_resumen_chivay.png).

v1 es un experimento controlado, no un defecto histórico de PANVIZ. El corte v2 registra 12/12 aprobadas entre 12/12 ejecutadas. Quedan dos entrevistas, revisiones cruzadas y aportes nominales por completar con el equipo, y falta adjuntar su presentación. Los comandos publican un repositorio nuevo en la cuenta que se autentique.

Base conceptual y organización de artefactos: [TP8, repositorio de Gabriela](https://github.com/gbordae/panviz-iras-cmmi/tree/v0.1).

## Verificación individual

Consultar [E35](06_evidencias/revision_individual.md) para las comprobaciones de Cielo y su alcance.
