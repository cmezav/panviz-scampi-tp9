"""Ejecuta T01–T08, T11 y T12 contra el servidor de cada versión."""
import csv
import hashlib
import json
import platform
import subprocess
import sys
import time
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
PROTOTYPE = ROOT / "04_prototipo"
OUTPUT = ROOT / "05_pruebas" / "resultados"
SAMPLE_PATH = PROTOTYPE / "datos" / "muestra.csv"
SAMPLE = SAMPLE_PATH.read_bytes()
DISTRICTS = ("Cayma", "Cercado", "Chivay", "Yanque")


def csv_rows(name):
    with (PROTOTYPE / "datos" / name).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


REJECTED = [dict(r, linea=int(r["linea"])) for r in csv_rows("oraculo_rechazos.csv")]
TOTALS = [dict(r, total=int(r["total"])) for r in csv_rows("oraculo_resumen.csv")]


@contextmanager
def instance(version, state):
    args = [sys.executable, str(PROTOTYPE / "panviz.py"), "--version", version, "--port", "0", "--state", str(state)]
    child = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        line = child.stdout.readline()
        if not line.startswith("PANVIZ "):
            raise RuntimeError(child.stderr.read())
        yield line.split()[-1]
    finally:
        child.terminate()
        child.wait(timeout=5)


def request(url, path, data=None):
    start = time.perf_counter_ns()
    req = Request(url + path, data=data)
    try:
        result = urlopen(req, timeout=5)
    except HTTPError as error:
        result = error
    with result:
        body = result.read()
        return result.code, body, (time.perf_counter_ns() - start) / 1_000_000


def api(url, path, data=None):
    code, body, ms = request(url, path, data)
    return code, json.loads(body), ms


def record(rows, test, ok, observed, start, raw=None):
    rows[test] = {"resultado": "Aprobada" if ok else "Fallida", "observado": observed,
                  "duracion_ms": round((time.perf_counter_ns() - start) / 1_000_000, 3), "detalle": raw}


def evaluate(version):
    results = {}
    with TemporaryDirectory(prefix=f"panviz-{version}-") as tmp:
        state = Path(tmp)
        with instance(version, state) as url:
            start = time.perf_counter_ns()
            code, data, _ = api(url, "/api/importar", SAMPLE)
            rejections = [{k:r[k] for k in ("linea","id","motivo")} for r in data["rechazados"]]
            record(results, "T01", code == 200 and rejections == REJECTED and len(data["aceptados"]) == 24,
                   f"{len(rejections)}/6 inválidos rechazados, {len(data['aceptados'])} aceptados", start, rejections)

            start = time.perf_counter_ns()
            _, summary, _ = api(url, "/api/resumen")
            counts = {d: sum(r["total"] for r in summary["totales"] if r["distrito"] == d) for d in DISTRICTS}
            record(results, "T02", summary["totales"] == TOTALS,
                   ", ".join(f"{d} {n}" for d,n in counts.items()), start, summary["totales"])

            start = time.perf_counter_ns()
            timings = [api(url, "/api/importar", SAMPLE) for _ in range(3)]
            ms = [round(x[2], 3) for x in timings]
            record(results,"T03",all(t[0] == 200 for t in timings) and max(ms) <= 2000,
                   f"máx. {max(ms):.3f} ms, tres repeticiones",start,ms)

            start = time.perf_counter_ns()
            timings = [api(url, "/api/resumen?distrito=" + quote("Cayma")) for _ in range(3)]
            ms = [round(x[2], 3) for x in timings]
            record(results,"T04",all(t[0] == 200 and all(r["distrito"] == "Cayma" for r in t[1]["totales"]) for t in timings) and max(ms) <= 2000,
                   f"máx. {max(ms):.3f} ms, tres repeticiones",start,ms)

            start = time.perf_counter_ns()
            c1, one, _ = api(url, "/api/importar", SAMPLE)
            c2, two, _ = api(url, "/api/importar", SAMPLE)
            ids = [r["id"] for r in two["aceptados"]]
            record(results,"T05",c1==c2==200 and one==two and len(ids)==len(set(ids)),
                   f"{len(one['aceptados'])} → {len(ids)} aceptados, {len(set(ids))} IDs únicos",start,ids)

            start = time.perf_counter_ns()
            _, original, _ = api(url, "/api/resumen")
            persisted = (state / "importacion.json").read_bytes()
        with instance(version, state) as url:
            code, reopened, _ = api(url, "/api/resumen")
            same = (state / "importacion.json").read_bytes() == persisted
            record(results,"T06",code==200 and original==reopened and same,
                   f"{len(reopened['aceptados'])} aceptados recuperados; archivo persistido idéntico",start,
                   {"sha256":hashlib.sha256(persisted).hexdigest()})

            start = time.perf_counter_ns()
            code, error, _ = api(url, "/api/publicar", b'{"rol":"lector"}')
            record(results,"T07",code==403 and not (state/"publicado.json").exists(),
                   f"HTTP {code}; no se creó publicación",start,error)

            start = time.perf_counter_ns()
            ok, _, _ = api(url, "/api/publicar", b'{"rol":"publicador_simulado"}')
            saved = (state/"publicado.json").read_bytes()
            api(url, "/api/importar", SAMPLE + b"P999,Cayma,2026-11-14,Infantil,Pendiente\n")
            denied, _, _ = api(url, "/api/publicar", b'{"rol":"lector"}')
            after = (state/"publicado.json").read_bytes()
            log = [json.loads(s) for s in (state/"accesos.jsonl").read_text(encoding="utf-8").splitlines()]
            record(results,"T08",ok==200 and denied==403 and after==saved and not log[-1]["permitido"],
                   f"publicador HTTP {ok}; lector HTTP {denied}; publicación idéntica: {saved == after}",start,
                   {"antes":hashlib.sha256(saved).hexdigest(),"despues":hashlib.sha256(after).hexdigest(),"log":log})

            start = time.perf_counter_ns()
            _, page, _ = request(url, "/")
            original_view = (PROTOTYPE / "index.html").read_bytes()
            code, filtered, _ = api(url, "/api/importar", SAMPLE)
            rejects_invalid = any(r["id"] == "P025" and r["motivo"] == "Fecha inválida" for r in filtered["rechazados"])
            record(results,"T11",code==200 and rejects_invalid and page==original_view,
                   f"P025 rechazada por calendario: {rejects_invalid}; misma vista: {page == original_view}",start,
                   {"sha256_vista":hashlib.sha256(page).hexdigest(),"regla":f"versiones/{version}.py"})

            start = time.perf_counter_ns()
            denied, _, _ = api(url, "/api/publicar", b'{"rol":"lector"}')
            _, final, _ = api(url, "/api/resumen")
            achieved = [{k:r[k] for k in ("linea","id","motivo")} for r in final["rechazados"]]
            record(results,"T12",denied==403 and final["totales"]==TOTALS and achieved==REJECTED,
                   f"totales iguales al oráculo: {final['totales']==TOTALS}; rechazos: {len(achieved)}; lector HTTP {denied}",start,
                   {"totales":final["totales"], "rechazos":achieved, "lector":denied})
    for t in ("T09","T10"):
        results[t] = dict(resultado="No ejecutada",observado="Sesión de usuario simulado pendiente",duracion_ms=None,detalle=None)
    return dict(version=version,fecha_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),
                entorno={"python":sys.version.split()[0],"sistema":platform.platform(),"equipo":platform.machine(),
                         "procesador":platform.processor() or "no reportado",
                         "medicion":"perf_counter_ns; HTTP loopback; operación completa incluyendo serialización; una ejecución de suite"},
                datos_sha256=hashlib.sha256(SAMPLE).hexdigest(), pruebas=dict(sorted(results.items())))


def main():
    if len(sys.argv) > 1:
        versions = sys.argv[1:]
        if any(v not in {"v1","v2"} for v in versions):
            raise SystemExit("Use v1 o v2")
    else:
        versions = ("v1", "v2")
    OUTPUT.mkdir(exist_ok=True)
    for version in versions:
        package = evaluate(version)
        out = OUTPUT / f"{version}.json"
        out.write_text(json.dumps(package,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        print(version, {state:sum(x["resultado"]==state for x in package["pruebas"].values())
                        for state in ("Aprobada","Fallida","No ejecutada")})


if __name__ == "__main__":
    main()
