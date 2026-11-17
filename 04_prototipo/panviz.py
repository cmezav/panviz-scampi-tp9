"""Microprototipo local PANVIZ TP9. Python 3.10+, sin dependencias externas."""
import argparse
import csv
import importlib
import io
import json
from collections import Counter
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from tempfile import NamedTemporaryFile
from urllib.parse import parse_qs, urlparse, unquote

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FIELDS = ("id", "distrito", "fecha", "grupo_etario", "estado_validacion")
REQUIRED = FIELDS[:-1]
DISTRICTS = ("Cayma", "Cercado", "Chivay", "Yanque")
GROUPS = ("Infantil", "Adulto mayor")
MAX_BYTES = 250_000


def write_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, delete=False) as tmp:
        json.dump(obj, tmp, ensure_ascii=False, indent=2)
    Path(tmp.name).replace(path)


def validar(source, version):
    rule = importlib.import_module(f"versiones.{version}").fecha_valida
    reader = csv.DictReader(io.StringIO(source.lstrip("\ufeff")), strict=True)
    if tuple(reader.fieldnames or ()) != FIELDS:
        raise ValueError("Columnas esperadas: " + ", ".join(FIELDS))
    accepted, rejected, seen = [], [], set()
    for row in reader:
        if None in row or any(value is None for value in row.values()):
            raise ValueError("Cantidad de columnas inválida en línea " + str(reader.line_num))
        row = {key: value.strip() for key, value in row.items()}
        if any(not row[key] for key in REQUIRED):
            reason = "Campo obligatorio vacío"
        elif not rule(row["fecha"]):
            reason = "Fecha inválida"
        elif row["id"] in seen:
            reason = "ID duplicado"
        elif row["distrito"] not in DISTRICTS or row["grupo_etario"] not in GROUPS:
            reason = "Valor fuera del catálogo"
        else:
            seen.add(row["id"])
            accepted.append(dict(row, estado_validacion="Aceptado"))
            continue
        rejected.append(dict(row, estado_validacion="Rechazado", linea=reader.line_num, motivo=reason))
    return {"aceptados": accepted, "rechazados": rejected}


def resumen(records, district=""):
    totals = Counter((r["distrito"], r["grupo_etario"]) for r in records if not district or r["distrito"] == district)
    return [dict(distrito=d, grupo_etario=g, total=n) for (d, g), n in sorted(totals.items())]


class Pilot:
    def __init__(self, version, state):
        self.version, self.state = version, Path(state)
        self.state.mkdir(parents=True, exist_ok=True)

    def current(self):
        path = self.state / "importacion.json"
        return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"aceptados": [], "rechazados": []}

    def load(self, source):
        data = validar(source, self.version)
        write_json(self.state / "importacion.json", data)
        return data

    def publish(self, role):
        allowed = role == "publicador_simulado"
        log = dict(fecha=datetime.now(timezone.utc).isoformat(), rol=role, permitido=allowed, version=self.version)
        with (self.state / "accesos.jsonl").open("a", encoding="utf-8") as f:
            f.write(json.dumps(log, ensure_ascii=False) + "\n")
        if not allowed:
            return 403, {"mensaje": "Publicación denegada para este rol de simulación."}
        records = self.current()["aceptados"]
        if not records:
            return 409, {"mensaje": "Importe un conjunto aceptado antes de publicar."}
        write_json(self.state / "publicado.json", {"aceptados": records, "resumen": resumen(records)})
        return 200, {"mensaje": f"Publicación local guardada con {len(records)} registros aceptados."}


def handler(pilot):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def respond(self, code, body, content_type="application/json; charset=utf-8"):
            payload = body if isinstance(body, bytes) else json.dumps(body, ensure_ascii=False).encode()
            self.send_response(code)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(payload)

        def do_GET(self):
            url = urlparse(self.path)
            if url.path == "/api/resumen":
                district = parse_qs(url.query).get("distrito", [""])[0]
                data = pilot.current()
                self.respond(200, {"version": pilot.version, "totales": resumen(data["aceptados"], district), **data})
                return
            if url.path == "/api/publicado":
                path = pilot.state / "publicado.json"
                self.respond(200, json.loads(path.read_text(encoding="utf-8")) if path.exists() else {})
                return
            paths = {
                "/": (HERE / "index.html", "text/html; charset=utf-8"),
                "/evaluacion": (ROOT / "07_tablero" / "index.html", "text/html; charset=utf-8"),
            }
            if url.path in paths:
                path, mime = paths[url.path]
                if path.is_file():
                    self.respond(200, path.read_bytes(), mime)
                else:
                    self.respond(404, {"mensaje": "Vista no incluida en esta versión"})
                return
            if url.path.startswith("/artefacto/"):
                rel = unquote(url.path.removeprefix("/artefacto/"))
                path = (ROOT / rel).resolve()
                allowed_roots = {"01_plan","02_procesos","03_requisitos_riesgos","04_prototipo","05_pruebas","06_evidencias","07_tablero"}
                if path.is_relative_to(ROOT) and rel.split("/")[0] in allowed_roots and path.is_file() and not any(p.startswith(".") for p in Path(rel).parts):
                    types = {".md":"text/plain; charset=utf-8",".csv":"text/plain; charset=utf-8",".json":"text/plain; charset=utf-8",
                             ".txt":"text/plain; charset=utf-8",".py":"text/plain; charset=utf-8",".html":"text/plain; charset=utf-8",".png":"image/png"}
                    mime = types.get(path.suffix)
                    if mime:
                        self.respond(200, path.read_bytes(), mime)
                        return
            self.respond(404, {"mensaje": "Recurso inexistente"})

        def do_POST(self):
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if length < 0 or length > MAX_BYTES:
                    self.respond(413, {"mensaje": "Tamaño no permitido"})
                    return
                raw = self.rfile.read(length).decode("utf-8")
                if self.path == "/api/importar":
                    data = pilot.load(raw)
                    self.respond(200, {"version": pilot.version, **data})
                elif self.path == "/api/publicar":
                    body = json.loads(raw)
                    if not isinstance(body, dict):
                        raise ValueError("Se esperaba un objeto de publicación")
                    self.respond(*pilot.publish(body.get("rol", "")))
                else:
                    self.respond(404, {"mensaje": "Recurso inexistente"})
            except (ValueError, csv.Error) as error:
                self.respond(400, {"mensaje": str(error)})
    return Handler


# PANVIZ_LOGIN_HANDLER
_legacy_handler = handler

def handler(pilot, require_login=True):
    base = _legacy_handler(pilot)
    if not require_login:
        return base
    from acceso import protect
    return protect(base, pilot, HERE)


def main():
    p = argparse.ArgumentParser()
    versions = tuple(v for v in ("v1", "v2") if (HERE / "versiones" / f"{v}.py").is_file())
    p.add_argument("--version", choices=versions, default=versions[-1])
    p.add_argument("--port", type=int, default=8765)
    p.add_argument("--state", type=Path)
    p.add_argument("--modo-pruebas", action="store_true", help="Solo suite histórica local: omitir inicio de sesión")
    args = p.parse_args()
    state = args.state or HERE / ".estado" / args.version
    with HTTPServer(("127.0.0.1", args.port), handler(Pilot(args.version, state), require_login=not args.modo_pruebas)) as server:
        port = server.server_address[1]
        print(f"PANVIZ {args.version} http://127.0.0.1:{port}", flush=True)
        server.serve_forever()


if __name__ == "__main__":
    main()
