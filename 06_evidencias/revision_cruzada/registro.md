# E30 · Registro de revisión cruzada

**Fecha reportada:** 15/11/2026. **Alcance:** piloto académico PANVIZ TP9, corte v2.

| Revisor | Objeto y versión | Comprobación y hallazgo | Decisión y respaldo |
|---|---|---|---|
| Cielo Meza (E2) | Plan de Gabriela, `dee2390` | Comprobó el alcance académico inspirado en SCAMPI C, con CMMI-DEV v1.3 como referencia. La muestra original de v2 tiene 30 registros sintéticos, 24 aceptados y 6 rechazados. Verificó los distritos, los dos grupos etarios y el formato de fecha del contrato de datos. | **Conforme.** [Plan revisado](https://github.com/cmezav/panviz-scampi-tp9/blob/dee239095485fb0a67c13be5ffb769d6057d88fa/01_plan/plan_evaluacion.md) y [registro v2](../../05_pruebas/resultados/v2.json). |
| Rodrigo Fernandez (E3) | R01 y K01–K05, base de requisitos `0fb250d` | Contrastó R01 → C10 → E10/E17/E18 → T01 → H01 → A01 y revisó las respuestas y responsables de los cinco riesgos. Sugirió identificar por nombre al responsable de K04. K05 ya tiene respaldo de ejecución con usuario en E38. | **Conforme.** [Matriz de trazabilidad](../../07_tablero/exportaciones/trazabilidad.csv), [riesgos](../../03_requisitos_riesgos/riesgos.csv) y [E38](../pruebas_usuario/sesion_2026-11-15.md). |
| Michael Suclle (E4) | Implementación v2, `2883441` | Reportó T01 aprobada (6 de 6 inválidos rechazados, 24 aceptados; 2,028 ms) y T07 aprobada (HTTP 403, sin publicación; 0,868 ms). Verificó que v2 incorpora `date.fromisoformat` para validar el calendario. | **Conforme** para T01, T07 y el diff revisado. [Resultados v2](../../05_pruebas/resultados/v2.json) y [diff de fecha](../../05_pruebas/diff_regla_fecha.txt). |
| Italo Ccoscco (E5) | Indicadores de v2, antes de integrar E30 | Recalculó 12 pruebas ejecutadas y 12 aprobadas (100 %). La cobertura reportada en ese corte fue 19/24 (79,2 %). El contraste con la matriz confirma que el numerador cuenta criterios con al menos una evidencia vinculada. | **Conforme.** [Matriz del corte revisado](https://github.com/cmezav/panviz-scampi-tp9/blob/dee239095485fb0a67c13be5ffb769d6057d88fa/07_tablero/exportaciones/criterios.csv) y [resultados v2](../../05_pruebas/resultados/v2.json). |
| Gabriela Borda (E1) | Índice E01–E12, `dee2390` | Comprobó las rutas de la muestra y que los SHA-256 y las rutas de estos doce registros eran distintos. Reportó los prefijos de E01, E02 y E03 y no encontró duplicados exactos en la muestra revisada. | **Conforme** para E01–E12. [Índice revisado](https://github.com/cmezav/panviz-scampi-tp9/blob/dee239095485fb0a67c13be5ffb769d6057d88fa/07_tablero/exportaciones/evidencias.csv) y [guía de acopio](../acopio.md). |

## Resolución y seguimiento

- El plan distingue las exclusiones del piloto de los controles de la muestra. Se actualizó su estado de validación humana para enlazar E38 y E29.
- C11 tiene respaldo parcial en el contraste de R01. C15 cuenta con la revisión de K01–K05. C19 cuenta con la revisión de verificación por Michael e Italo.
- Cielo registró una decisión separada sobre el [estándar v1](../../02_procesos/estandar_v1.md): aprobado con observaciones para el piloto.
- A01 quedó cerrada tras la conformidad técnica de Michael. El detalle del contraste queda registrado abajo.

## Contraste de resultados para cerrar A01

**Michael Suclle · 15/11/2026, 21:15 (hora de Lima) · v2.**
Se usó la corrección de calendario del [commit 2883441](https://github.com/cmezav/panviz-scampi-tp9/commit/28834415d0097ef3006c3fee58f74297e0d964c1)
y el [registro de resultados v2](../../05_pruebas/resultados/v2.json).

| Caso | Resultado contrastado |
|---|---|
| T01 | Aprobada. Se rechazaron los seis inválidos y se aceptaron 24 registros. |
| T02 | Aprobada. Seis registros por distrito, tres por grupo etario. |
| T11 | Aprobada. P025 fue rechazada por calendario y la vista coincidió. |
| T12 | Aprobada. Totales iguales al oráculo, seis rechazos y HTTP 403 para el rol lector. |

Michael había reportado la repetición de T01 y la revisión del
[diff de fecha](../../05_pruebas/diff_regla_fecha.txt). Para T02, T11 y T12
contrastó los resultados consignados en v2.json. Dio su conformidad con
cerrar técnicamente A01.
