# Requisitos y catálogo de datos

| ID | Flujo | Necesidad | Criterio observable | Pruebas |
|---|---|---|---|---|
| R01 | F1 | Importar CSV y separar inválidos | 24 aceptados y 6 rechazados con línea, ID y causa exacta; importación en ≤2 s | T01, T03 |
| R02 | F1 | Conservar último conjunto válido | Reimportar no acumula IDs y reiniciar recupera los mismos registros | T05, T06 |
| R03 | F2 | Ver válidos por distrito y edad | Cada celda coincide con el oráculo; actualización en ≤2 s | T02, T04 |
| R04 | F2 | Proteger publicación local | Lector recibe HTTP 403 y lo publicado conserva su hash | T07, T08 |
| R05 | F1/F2 | Corregir y encontrar un distrito | Dos tareas sin ayuda, ≤90 s cada una | T09, T10 |
| R06 | F1/F2 | Cambiar regla con bajo impacto | Regla separable, misma vista y regresión de importación, resumen y permiso | T11, T12 |

Contrato ordenado id,distrito,fecha,grupo_etario,estado_validacion. ID, distrito, fecha y grupo son obligatorios. Formato AAAA-MM-DD y fecha de calendario. Distritos Cayma/Cercado (Arequipa), Chivay/Yanque (Caylloma). Grupos Infantil y Adulto mayor. Duplicados conservan la primera entrada válida. El estado de entrada se sobrescribe al clasificar. Prioridad de causas: obligatoriedad, fecha, duplicado y catálogo. La publicación usa autorización en la operación local y roles simulados, sin identidad autenticada.
