# Registro de revisión cruzada

Registrar fecha, versión, resultado, comprobación repetida y decisión real. Las parejas son propuestas.

| Revisor propuesto | Objeto | Procedimiento | Resultado |
|---|---|---|---|
| E2 | Plan de E1 | Verificar alcance, muestra y exclusiones | Pendiente |
| E3 | Trazabilidad de E2 | Seguir R, C, E y T hasta hallazgo y acción | Pendiente |
| E4 | Implementación de E3 | Reproducir T01 y T07 y comprobar diff | Pendiente |
| E5 | Pruebas de E4 | Recalcular dos indicadores | Pendiente |
| E1 | Evidencias de E5 | Abrir rutas y comprobar hashes y duplicados | Pendiente |

Cualquier desacuerdo se registra con sustentos y decisión. Confirmar o corregir los hallazgos preliminares en sesión.

## Datos precargados para corroborar

Las observaciones siguientes proceden de un borrador de coordinación. Se requiere fecha, versión, revisor y respaldo para cerrar cada fila.

- **E2 → plan de E1.** Contrastar si se entienden los dos flujos, el alcance y las exclusiones. La aclaración propuesta para el informe es que el piloto usa una muestra sintética de 30 registros.
- **E3 → trazabilidad de E2.** La matriz vincula R01 con C10, T01, H01 y A01. La muestra original de v2 tiene seis rechazos. Corroborar qué enlaces abrió el revisor y registrar su decisión.
- **E4 → implementación de E3.** Agregar el resultado de T01, T07 y la comprobación del diff.
- **E5 → pruebas de E4.** Agregar los valores recalculados de dos indicadores y compararlos con el tablero.
- **E1 → evidencias de E5.** Agregar los IDs que se verificaron, las rutas, las huellas y el resultado de la búsqueda de duplicados.
- **C15.** Registrar quién revisó los cinco riesgos y qué observó en cada control.
