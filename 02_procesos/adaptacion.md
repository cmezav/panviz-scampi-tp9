# Adaptación de los flujos y diseño

| Flujo | Entrada | Adaptación | Salida observable | Pruebas |
|---|---|---|---|---|
| F1 Captura y validación | CSV o edición local de su contenido | Columnas exactas, obligatoriedad, fechas, catálogo y primera aparición válida por ID. Línea y causa de rechazo | Aceptados persistidos y rechazados separados | T01, T03, T05, T06, T09, T11 |
| F2 Consolidación y visualización | Aceptados persistidos | Agrupar por distrito y edad, selector de distrito, permiso validado en la operación y comparación de estado publicado | Resumen y publicación local segregada | T02, T04, T07, T08, T10, T12 |

Se comparten requisito medible, oráculo, prueba, versión, control de cambios, vínculo a evidencias y revisión propuesta. El backend Python delega fecha_valida a la versión seleccionada, persiste importación y publicación en archivos diferentes y registra denegaciones. Importar de nuevo reemplaza el conjunto. El CSV no determina por sí mismo el estado de validación.
