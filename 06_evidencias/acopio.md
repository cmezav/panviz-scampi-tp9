# Plan de acopio e indexación

El índice generado en 07_tablero/exportaciones/evidencias.csv registra cada artefacto distinto con ID, descripción, tipo, ruta, versión, fecha, autor operativo, revisor, flujo, validez y SHA-256. Se comprueba que los archivos existan y se repite el cálculo con generar.py. Fechas de evidencia corresponden a la preparación/ejecución del corte. Revisores nominales pendientes.

| Evidencias | Qué se recoge | Verificación |
|---|---|---|
| E01–E07 | Plan, estándar, adaptación, plantillas, cambio, requisitos y riesgos | Verificar dos flujos, controles comunes, seis requisitos y cinco riesgos |
| E08–E12 | CSV, oráculos separados y reglas de ambas versiones | Comparar 30 filas, seis inválidos, motivos y totales |
| E13–E19 | Código, vista, casos, suite, dos ejecuciones y protocolo | Ejecutar casos y contrastar versiones, tiempos y resultado |
| E20–E26 | Roles propuestos, hallazgos, acciones, ruta, tablero y dos capturas | Filtrar por área y responsable y abrir un registro de evidencia |
| E27–E32 | Dos actas, diff, registro cruzado, revisión de herramienta y plan de acopio | Actas y revisión marcadas pendientes; diff y herramienta verificables |

Responsabilidad propuesta de acopio: E1 busca estándar, aprobación y acciones; E2 requisitos, oráculos y riesgos; E3 identifica cambios en versión, código y diff; E4 registra resultados y entrevistas; E5 verifica enlace, versión y procedencia. Cada persona registra al menos tres aportes reales en el formulario y conserva sus datos de origen. Consolidar revisando IDs repetidos, rutas/huellas repetidas, versión y alcance. El formulario produce un CSV de aportes candidatos y no acredita por sí solo un trabajo ni cambia las métricas; revisar y vincular al criterio antes de integrarlo.

D es la fecha de aprobación real del plan. Los plazos de 7 y 30 días se convierten a fecha calendario al aprobar. Un archivo de acta vacío no se cuenta como evidencia de una entrevista. No sustituir una persona con resultados de un controlador automatizado.
