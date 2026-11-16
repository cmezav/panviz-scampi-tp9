# Acta 01 · Uso del proceso (E27)

- **Entrevistadora:** Cielo Cristal Meza Vizcarra.
- **Entrevistada:** Gabriela Nayely Borda Espinoza.
- **Fecha y hora:** 15/11/2026, de 20:45 a 20:50 (hora de Lima).
- **Duración reportada:** 5 minutos.
- **Versión revisada:** estándar v1 aplicado en el piloto PANVIZ v2.
- **Consentimiento:** Gabriela autorizó el uso de sus respuestas en el acta del TP9.

| Pregunta | Respuesta de Gabriela | Contraste con el repositorio |
|---|---|---|
| ¿Cómo se aplica el estándar en F1 y F2? | En F1 se valida la muestra de 30 registros: campos obligatorios, ID único y separación de aceptados y rechazados. En F2 se consulta el resumen por distrito y grupo. Con la muestra original, Chivay devuelve seis casos, tres por grupo. | [Adaptación de flujos](../../02_procesos/adaptacion.md) y [sesión E38](../pruebas_usuario/sesion_2026-11-15.md). |
| ¿Qué cambio obligó a repetir las pruebas? | Gabriela señaló la corrección del calendario y mencionó la detección de duplicados y el filtro del resumen. | La [mejora v2](../../02_procesos/mejora_v2.md) y el [diff](../../05_pruebas/diff_regla_fecha.txt) acreditan el cambio de validación del calendario y la regresión de T01, T02, T11 y T12. Los duplicados y el filtro se comprobaron como controles; esos archivos no documentan un cambio de versión en ellos. T10 se repitió porque el primer intento partió con Chivay preseleccionado. |
| ¿Qué revisión quedó respaldada y cuál falta? | Gabriela señaló la verificación individual de Cielo y que faltaba formalizar la revisión cruzada. También mencionó las actas y los roles propuestos. | [E35](../revision_individual.md) respalda la revisión individual. En los registros vigentes, Michael e Italo participaron en [E38](../pruebas_usuario/sesion_2026-11-15.md) y [E29](Acta_02_validacion.md). La [revisión cruzada E30](../revision_cruzada/registro.md) y las confirmaciones nominales de aportes siguen pendientes. |

**Decisión de Gabriela:** conformidad condicionada a incorporar las actas y la evidencia de revisión cruzada. E27 y E29 quedan documentadas. Falta E30 y sigue pendiente la aprobación definitiva por otra persona.

**Seguimiento:** incorporar los resultados y respaldos de E30 y registrar quién revisó y aprobó el estándar, qué versión revisó y en qué fecha.

**Seguimiento:** después de documentar [E30](../revision_cruzada/registro.md), Cielo aprobó el [estándar v1](../../02_procesos/estandar_v1.md) para el piloto con observaciones documentales atendidas.
