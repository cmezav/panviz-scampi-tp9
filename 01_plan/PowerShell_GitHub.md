# Crear y publicar el repositorio desde PowerShell

Extraer Equipo03_PANVIZ.zip y entrar en la carpeta que contiene README.md. El identificador 03 sigue el trabajo anterior; cámbialo si el docente asignó otro número.

## 1. Comprobar herramientas

En PowerShell, comprobar que están disponibles Git, Python 3.10 o posterior y GitHub CLI. Si falta Git o GitHub CLI en Windows, instalarlos con los comandos opcionales y reabrir PowerShell.

```powershell
git --version
py -3 --version
gh --version
# Solo si faltan:
# winget install --id Git.Git -e
# winget install --id GitHub.cli -e
```

## 2. Preparar en local

Ejecutar desde la raíz recién extraída. Usar nombre y correo reales o el correo noreply de la cuenta GitHub. Los dos commits documentan la publicación de versiones del paquete. Son creados al ejecutar estos comandos.

```powershell
Set-Location "C:\ruta\a\Equipo03_PANVIZ"
git init -b main
git config --local user.name (Read-Host "Nombre para commits")
git config --local user.email (Read-Host "Correo de commits o noreply")
git config --local core.autocrlf false

git add -- .gitignore .gitattributes 04_prototipo/panviz.py 04_prototipo/index.html 04_prototipo/datos 04_prototipo/versiones/v1.py
git commit -m "test: conservar linea base experimental PANVIZ TP9"
git tag -a tp9-v1-experimento -m "Regla incompleta intencional para comparar resultados"

git add .
git status --short
git commit -m "feat: corregir calendario y documentar evaluacion SCAMPI del piloto"
git tag -a tp9-v2-corregida -m "Regla de calendario corregida y verificacion tecnica"
git log --oneline --decorate -2
```

Publica el corte incluido para conservar la concordancia entre informe, tablero y logs. Si quieres repetir las pruebas, usa una copia aparte o un clon de verificación. Los tiempos locales pueden variar. Publica únicamente artefactos que el equipo haya autorizado compartir.

## 3. Crear el remoto con GitHub CLI

```powershell
gh auth login --hostname github.com --git-protocol https --web
gh auth status
gh auth setup-git
gh repo create panviz-scampi-tp9 --private --source=. --remote=origin --push
git push origin --tags
git remote -v
git ls-remote --heads --tags origin
gh repo view --web
```

Si ya creaste un remoto vacío desde GitHub, sustituye gh repo create por estos comandos, con tu usuario u organización:

```powershell
git remote add origin https://github.com/TU_USUARIO/panviz-scampi-tp9.git
git push -u origin main
git push origin --tags
```

El repositorio privado requiere acceso del docente. Para habilitarlo, invítalo desde Settings → Collaborators de ese repositorio. Si el grupo acuerda publicar el código, primero confirme qué documentos, nombres y actas pueden ser públicos. No clonar sobre ni empujar cambios al repositorio ajeno del TP8.
