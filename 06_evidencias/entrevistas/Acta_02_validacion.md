# Acta 02 · Validación de resultados (E29)

- **Entrevistador:** Michael Suclle.
- **Usuario entrevistado:** Italo Ccoscco.
- **Fecha y hora:** 15/11/2026, de 20:24 a 20:30 (hora de Lima).
- **Duración reportada:** 6 minutos.
- **Versión revisada:** PANVIZ v2, piloto local.
- **Consentimiento:** Italo autorizó que sus respuestas se usen en el acta del TP9.

## Respuestas y contraste

| Pregunta | Respuesta registrada | Respaldo |
|---|---|---|
| ¿Cómo supiste que P026 quedó corregido? | Al validar la muestra de 30, P026 salió rechazado porque su distrito estaba vacío. Ingresé Chivay y volví a validar. P026 desapareció de los rechazos y quedaron 25 aceptados y 5 rechazados. | [T09, E36](../pruebas_usuario/captura_T09_italo.png) |
| ¿Cómo llegaste al resumen de Chivay y verificaste el total? | Recargué la muestra original y la validé. Inicié con el filtro en Todos. Seleccioné Chivay y comprobé el total de 6 registros: 3 infantiles y 3 de adulto mayor. | [T10, E37](../pruebas_usuario/captura_T10_italo_repeticion.png). El [CSV original](../../04_prototipo/datos/muestra.csv) permite contrastar los IDs P013, P015 y P017 (infantil), y P014, P016 y P018 (adulto mayor). |
| ¿Aceptas el resultado para el piloto? | Lo acepto tal cual. El prototipo respondió bien en local y las dos tareas se completaron sin ayuda en menos de 90 segundos. | [Sesión cronometrada E38](../pruebas_usuario/sesion_2026-11-15.md) |

**Decisión de Italo:** acepta el resultado de PANVIZ v2 para T09 y T10 en el piloto, sin ajustes solicitados.

**Contraste con Michael:** T09 aprobó en 61 s y T10 aprobó en 53 s. En T09, el conteo 24/6 era el inicial; el resultado final fue 25/5. El primer intento de T10 (47 s) se excluyó porque Chivay ya estaba seleccionado.

**Seguimiento sugerido por Italo:** repetir la medición con otra persona para la revisión cruzada.
