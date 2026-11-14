# Herramienta de acopio y tablero

Alternativa local: LibreOffice Calc (formato ODS, LibreOffice bajo MPL 2.0 y licencias complementarias) junto con una vista HTML local que lee el mismo conjunto de CSV/JSON y muestra filtros por corte, área y responsable. Grist Desktop no estaba disponible como ejecutable en el entorno de preparación. No se contabilizó una revisión cronometrada de 20 min ni una instalación fallida de 30 min. Se usa Calc como alternativa operativa.

**En Calc.** La conversión y la reapertura usaron LibreOfficeDev 26.8.0.0.alpha0. El archivo PANVIZ_Evaluacion.ods agrupa Criterios, Evidencias, Pruebas, Hallazgos, Acciones, Trazabilidad y los cortes Antes/Después. Las fórmulas recalculan los indicadores usando los registros. El campo con_evidencia se alimenta de la validación de rutas del generador. Las capturas incluidas son renderizaciones de las dos hojas del tablero. La validación del archivo ODS se hace al abrir/convertir con LibreOffice.

**En el tablero local.** Desde /evaluacion seleccionar corte, área y responsable. El indicador conserva el denominador del corte y los filtros ajustan criterios, barras y debilidades. Los IDs E abren el registro y la ruta relativa dentro del paquete. Los CSV se exportan con UTF-8 BOM para facilitar el uso en Calc.

**Acopio.** El formulario local exige criterio, descripción, ruta/enlace y autor. Guarda el borrador por navegador y exporta un CSV. El responsable propuesto consolida esos CSV, valida origen y duplicados y actualiza el índice. Limitación: este formulario no es multiusuario y requiere consolidación explícita. Para importación manual en Calc, abrir un CSV de exportaciones con codificación UTF-8 y separador coma.

**Verificación de preparación.** Se ejecutaron los casos técnicos del API local, el generador de CSV/JSON y la conversión a ODS. La prueba interactiva en navegador y el uso cronometrado por los integrantes se reservan para el equipo; documentar edición, duración real y observaciones en la sesión de cierre.


## Actualizar las hojas de datos

El tablero HTML se actualiza ejecutando generar.py. Para sincronizar el ODS, abrir cada CSV como hoja aparte, seleccionar la codificación UTF-8 y copiar las columnas por nombre a la hoja que corresponda conservando su orden. En Criterios, mantener con_evidencia en la última columna: 1 para una lista con evidencia enlazada y 0 para una lista vacía. Las fórmulas de los dos paneles se refieren al intervalo de filas del corte. Si se agrega una fila a Hallazgos, extender el intervalo de esa hoja en las fórmulas de ambos cortes. Guardar una nueva copia ODS y actualizar las dos capturas si cambia el corte.
