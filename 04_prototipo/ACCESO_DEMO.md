# Acceso local de demostración

El servidor normal requiere inicio de sesión. Ejecutar:

```powershell
py -3 .\04_prototipo\panviz.py --version v2 --port 8765
```

Abrir http://127.0.0.1:8765/. El servidor redirige a `/login`.

| Cuenta de demostración | Contraseña | Permisos |
|---|---|---|
| lector | LecturaPANVIZ!26 | Consultar registros, filtrar y revisar el tablero/evidencias. No importa, corrige ni publica. |
| publicador | PublicaPANVIZ!26 | Consultar, importar, corregir y publicar localmente. |

Las credenciales anteriores son públicas y ficticias, creadas exclusivamente para la demostración académica. No contienen datos personales. El servidor guarda hashes PBKDF2 de las contraseñas. Las sesiones se mantienen en memoria y expiran tras una hora; se invalidan al cerrar sesión o reiniciar el servidor. La cookie es HttpOnly y SameSite=Strict. No usa Secure porque el escenario es HTTP en localhost. La cuenta autorizada se resuelve desde la sesión del servidor, independientemente de cualquier rol enviado en el cuerpo de la solicitud.

## Demostración con ambas cuentas

1. Iniciar como **publicador**, cargar y validar la muestra: 24 aceptados y 6 rechazados.
2. Consultar Chivay con la muestra original: 6, repartidos 3/3.
3. Corregir P026 y validar: 25 aceptados y 5 rechazados.
4. Cerrar sesión e iniciar como **lector**. El estado importado se conserva, porque pertenece al piloto y no al navegador.
5. Pulsar **Intentar publicar**. Debe devolver 403 y conservar el conjunto publicado. El botón permanece disponible para demostrar el rechazo del servidor; importar y editar quedan deshabilitados.
6. Abrir el tablero y el acta con la cuenta de lector.

El usuario ya no cambia de rol mediante una lista editable. Usa **Cerrar sesión** para cambiar de cuenta.

## Pruebas y alcance

```powershell
py -3 .\05_pruebas\probar_acceso.py
```

Las pruebas verifican acceso anónimo, credenciales incorrectas, cookie, lectura, escritura, intento de falsificar rol, publicación, cierre de sesión y comprobación de origen. Guardan un resultado separado en `05_pruebas/resultados/acceso_local.json`. No modifican los resultados históricos de v1/v2 ni convierten los doce casos anteriores en pruebas de autenticación.

`medir.py` usa `--modo-pruebas` para conservar la regresión histórica del control por roles simulados. Ese modo se activa explícitamente y omite el inicio de sesión; debe reservarse a la suite local. La ejecución normal mantiene el acceso protegido. La suite histórica sigue sobrescribiendo sus JSON de resultados: guarda los registros humanos antes de repetirla.

El acceso añadido corresponde a un prototipo local y cuentas compartidas de demostración. No es identidad verificada de usuarios ni despliegue de producción. A03 continúa abierta para el siguiente ciclo, otra muestra y controles de identidad más amplios.
