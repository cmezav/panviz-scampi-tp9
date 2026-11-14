# Mejora incorporada al estándar v2

La regla experimental v1 solo exigía el formato de fecha. Con la misma muestra admitió dos fechas con forma ISO imposibles en el calendario. La v2 comprueba formato y fecha de calendario. Se conserva v1 identificada como experimento y el diff de un módulo. La vista es común.

**Lección de verificación.** Un cambio en una regla del catálogo incluye caso positivo, límite y negativo del dominio, además de la regresión del flujo consumidor. Conservar referencia esperada, resultado observado, versión y entorno.

**CR09-01.** Motivo: falla inducida observada en T01, T02, T11 y T12. Implementación: v2 añade comprobación de calendario. Revisión humana y aprobación del estándar: pendientes. El experimento y el parche son reproducibles.
