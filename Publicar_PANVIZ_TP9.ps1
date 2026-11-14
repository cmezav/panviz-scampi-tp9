#requires -Version 5.1
[CmdletBinding()]
param(
    [string]$Ruta = (Get-Location).Path,
    [ValidatePattern('^[a-zA-Z0-9_.-]+$')]
    [string]$Repositorio = 'panviz-scampi-tp9',
    [switch]$SoloLocal,
    [switch]$SoloPublicar,
    [switch]$HacerPublicoExistente
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $false

function Invoke-Checked {
    param([string]$Program, [string[]]$Arguments)
    & $Program @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "$Program fallo con codigo $LASTEXITCODE. Comando: $($Arguments -join ' ')"
    }
}

if ($SoloLocal -and ($SoloPublicar -or $HacerPublicoExistente)) {
    throw 'Usa -SoloLocal para preparar los commits o -SoloPublicar para publicar.'
}

$commits = @(
    @{ Message = 'chore: definir atributos e ignorar archivos locales'; Paths = @('.gitignore', '.gitattributes') }
    @{ Message = 'data: agregar muestra sintetica y oraculos de verificacion'; Paths = @('04_prototipo/datos') }
    @{ Message = 'test: conservar la regla experimental de fecha'; Paths = @('04_prototipo/versiones/v1.py') }
    @{ Message = 'feat: implementar importacion resumen y publicacion local'; Paths = @('04_prototipo/panviz.py') }
    @{ Message = 'feat: agregar interfaz local de importacion y consulta'; Paths = @('04_prototipo/index.html'); Tag = 'tp9-v1-experimento' }
    @{ Message = 'docs: definir alcance muestra y criterios de evaluacion'; Paths = @('01_plan/plan_evaluacion.md') }
    @{ Message = 'docs: registrar las responsabilidades y la revision propuestas'; Paths = @('01_plan/aportes.csv') }
    @{ Message = 'docs: definir el proceso comun y sus plantillas'; Paths = @('02_procesos/estandar_v1.md', '02_procesos/plantillas.md') }
    @{ Message = 'docs: registrar la adaptacion a los dos flujos'; Paths = @('02_procesos/adaptacion.md') }
    @{ Message = 'docs: establecer requisitos y riesgos del piloto'; Paths = @('03_requisitos_riesgos') }
    @{ Message = 'test: definir doce casos y el protocolo de usuario'; Paths = @('05_pruebas/casos.csv', '05_pruebas/protocolo_usuario.md') }
    @{ Message = 'test: conservar el resultado de la linea base'; Paths = @('05_pruebas/resultados/v1.json') }
    @{ Message = 'fix: validar el calendario y registrar la mejora'; Paths = @('04_prototipo/versiones/v2.py', '02_procesos/mejora_v2.md', '05_pruebas/diff_regla_fecha.txt') }
    @{ Message = 'test: agregar la suite reproducible y el corte corregido'; Paths = @('05_pruebas/medir.py', '05_pruebas/resultados/v2.json'); Tag = 'tp9-v2-corregida' }
    @{ Message = 'docs: definir el acopio y la revision de evidencias'; Paths = @('06_evidencias/acopio.md', '06_evidencias/revision_cruzada') }
    @{ Message = 'docs: preparar las actas de las dos entrevistas'; Paths = @('06_evidencias/entrevistas') }
    @{ Message = 'docs: registrar hallazgos y acciones priorizadas'; Paths = @('06_evidencias/hallazgos.csv', '06_evidencias/acciones.csv') }
    @{ Message = 'feat: implementar indicadores y exportaciones reproducibles'; Paths = @('07_tablero/generar.py', '07_tablero/exportaciones') }
    @{ Message = 'feat: agregar tablero con filtros y formulario de evidencias'; Paths = @('07_tablero/index.html') }
    @{ Message = 'docs: agregar hoja Calc y documentar su actualizacion'; Paths = @('07_tablero/PANVIZ_Evaluacion.ods', '07_tablero/herramienta.md') }
    @{ Message = 'docs: conservar las capturas de ambos cortes'; Paths = @('07_tablero/capturas') }
    @{ Message = 'docs: incorporar el respaldo de la demostracion'; Paths = @('07_tablero/demostracion.mp4', '01_plan/entrega_exposicion.md') }
    @{ Message = 'docs: integrar el informe de la revision SCAMPI'; Paths = @('08_informe/Reporte_TP9_SCAMPI_PANVIZ.docx') }
    @{ Message = 'docs: explicar como ejecutar y reproducir PANVIZ'; Paths = @('README.md') }
    @{ Message = 'chore: automatizar la publicacion y documentar GitHub'; Paths = @('01_plan/PowerShell_GitHub.md', 'Publicar_PANVIZ_TP9.ps1') }
)

Push-Location -LiteralPath $Ruta
try {
    Get-Command git -ErrorAction Stop | Out-Null
    if (-not $SoloLocal) { Get-Command gh -ErrorAction Stop | Out-Null }

    if (-not $SoloPublicar) {
        if (Test-Path -LiteralPath '.git') {
            throw 'Ya existe un repositorio local. Usa -SoloPublicar para mantener su historial o extrae una copia limpia para crear los 25 commits.'
        }
        foreach ($step in $commits) {
            foreach ($file in $step.Paths) {
                if (-not (Test-Path -LiteralPath $file)) {
                    throw "Falta $file. Extrae el ZIP actualizado y ejecuta desde la carpeta Equipo03_PANVIZ."
                }
            }
        }

        Invoke-Checked git @('init', '-b', 'main')
        $gitName = & git config --get user.name
        if ([string]::IsNullOrWhiteSpace($gitName)) {
            $gitName = Read-Host 'Nombre real para los commits'
        }
        $gitEmail = & git config --get user.email
        if ([string]::IsNullOrWhiteSpace($gitEmail)) {
            $gitEmail = Read-Host 'Correo de GitHub o noreply para los commits'
        }
        if ([string]::IsNullOrWhiteSpace($gitName) -or [string]::IsNullOrWhiteSpace($gitEmail)) {
            throw 'Configura user.name y user.email y vuelve a extraer el ZIP para iniciar en una carpeta nueva.'
        }
        Invoke-Checked git @('config', '--local', 'user.name', $gitName)
        Invoke-Checked git @('config', '--local', 'user.email', $gitEmail)
        Invoke-Checked git @('config', '--local', 'core.autocrlf', 'false')

        foreach ($step in $commits) {
            $paths = [string[]]$step.Paths
            Invoke-Checked git (@('add', '--') + $paths)
            Invoke-Checked git (@('commit', '-m', $step.Message, '--') + $paths)
            if ($step.ContainsKey('Tag')) {
                Invoke-Checked git @('tag', '-a', $step.Tag, '-m', $step.Message)
            }
        }
        Invoke-Checked git @('rev-list', '--count', 'HEAD')
    }

    if ($SoloLocal) { return }
    if (-not (Test-Path -LiteralPath '.git')) { throw 'La carpeta no tiene repositorio Git.' }

    Invoke-Checked git @('rev-parse', '--verify', 'refs/heads/main')
    & gh auth status --hostname github.com
    if ($LASTEXITCODE -ne 0) {
        Invoke-Checked gh @('auth', 'login', '--hostname', 'github.com', '--git-protocol', 'https', '--web')
    }
    Invoke-Checked gh @('auth', 'setup-git', '--hostname', 'github.com')

    if ((Invoke-Checked git @('remote')) -contains 'origin') {
        $origin = Invoke-Checked git @('remote', 'get-url', 'origin')
        if ($origin -notmatch '^(?:https://github\.com/|git@github\.com:)([A-Za-z0-9-]+/[A-Za-z0-9_.-]+?)(?:\.git)?/?$') {
            throw 'origin debe apuntar a un repositorio de github.com.'
        }
        $fullName = $Matches[1]
        if (($fullName.Split('/')[1]) -ne $Repositorio) {
            throw "origin apunta a $fullName. Usa -Repositorio con su nombre exacto si ese es el repositorio del TP9."
        }
        $remote = Invoke-Checked gh @('repo', 'view', $fullName, '--json', 'visibility,url') | ConvertFrom-Json
        if ($remote.visibility -ne 'PUBLIC') {
            if (-not $HacerPublicoExistente) {
                throw "El remoto $fullName es privado o interno. Usa -SoloPublicar -HacerPublicoExistente para publicar ese repositorio."
            }
            Invoke-Checked gh @('repo', 'edit', $fullName, '--visibility', 'public', '--accept-visibility-change-consequences')
        }
    } else {
        $account = Invoke-Checked gh @('api', 'user', '--hostname', 'github.com', '--jq', '.login')
        $fullName = "$account/$Repositorio"
        Invoke-Checked gh @('repo', 'create', $fullName, '--public', '--source', '.', '--remote', 'origin')
    }

    Invoke-Checked git @('push', '-u', 'origin', 'main')
    Invoke-Checked git @('push', 'origin', '--tags')
    Invoke-Checked gh @('repo', 'view', $fullName, '--json', 'visibility,url', '--jq', '.visibility + " " + .url')
} finally {
    Pop-Location
}
