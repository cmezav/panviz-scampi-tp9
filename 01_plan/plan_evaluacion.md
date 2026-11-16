# Plan de evaluación TP9

**Propósito.** Identificar brechas verificables y evaluar un incremento local de PANVIZ mediante una autoevaluación académica inspirada en SCAMPI C, con CMMI-DEV v1.3 como modelo histórico. Los estados de la matriz son docentes. El alcance excluye la operación epidemiológica real, certificación, madurez organizacional, autenticación de producción, rendimiento bajo carga y decisiones clínicas.

**Unidad y muestra.** Un micropiloto con dos flujos: F1 captura/importación y validación, y F2 consolidación, visualización y publicación local. Muestra intencional fija de 30 registros sintéticos con seis inválidos conocidos, cuatro distritos y dos grupos etarios. Se usan el mismo CSV, oráculos, 24 criterios y 12 casos en dos cortes. Seleccionar artefactos de ambos flujos y priorizar riesgos de conteo y publicación. La muestra no representa una organización.

**Roles simulados.** Patrocinador propuesto: responsable de vigilancia (representado por E1 si confirma). Usuario simulado propuesto: analista de vigilancia (E4 si confirma, sin ayuda del desarrollador). Rotación propuesta E2→E1, E3→E2, E4→E3, E5→E4, E1→E5. Los revisores son integrantes del grupo y la independencia es limitada.

**Tres decisiones de la lectura aplicada.** (1) §2.2: diagnóstico formativo de baja formalidad, alcance acotado y sin calificación de madurez. (2) §2.3, tabla 2: preparar inventario, examinar, documentar y verificar artefactos, confirmar hallazgos preliminares, reportar y archivar. (3) §2.4: fijar muestra y cobertura antes de ejecutar, seleccionar de forma intencional por riesgo y declarar por qué los resultados no se generalizan.

**Levantamiento.** Acordar estándar y alcance, recoger artefactos, repetir pruebas, revisar evidencia por otra persona, contrastar dos entrevistas de cinco minutos, registrar discrepancias y decidir hallazgos. Guardar versión, fecha, autor real, revisor, resultado y ruta. La validación humana de v2 consta en la [sesión E38](../06_evidencias/pruebas_usuario/sesion_2026-11-15.md) y la [aceptación de Italo](../06_evidencias/entrevistas/Acta_02_validacion.md).

**Confidencialidad.** Solo identificadores sintéticos. Excluir datos de pacientes, cuentas reales, credenciales y contactos de capturas y actas. Desidentificar registros de entrevista antes de compartirlos. El prototipo corre en localhost.

**Criterios de decisión.** Evidenciado: se observa cumplimiento completo en la muestra. Parcial: hay soporte útil y falta un aspecto identificable. No evidenciado: falta soporte o el resultado contradice el criterio. No evaluable: un límite de muestra o acceso impide juzgar. Una plantilla vacía prueba la preparación del instrumento, no su ejecución. Los hallazgos técnicos se registran como preliminares hasta corroboración del equipo.
