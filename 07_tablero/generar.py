"""Genera exportaciones y datos reproducibles para PANVIZ_Evaluacion."""
import argparse
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPORT = ROOT / "07_tablero/exportaciones"
EVIDENCE = [
 ("E01","Plan de evaluación","01_plan/plan_evaluacion.md","Común"),
 ("E02","Estándar del proceso","02_procesos/estandar_v1.md","Común"),
 ("E03","Adaptación y diseño","02_procesos/adaptacion.md","F1 y F2"),
 ("E04","Plantillas de control","02_procesos/plantillas.md","Común"),
 ("E05","Cambio y mejora del proceso","02_procesos/mejora_v2.md","F1 y F2"),
 ("E06","Requisitos y catálogo","03_requisitos_riesgos/requisitos.md","F1 y F2"),
 ("E07","Registro de cinco riesgos","03_requisitos_riesgos/riesgos.csv","F1 y F2"),
 ("E08","Muestra sintética de 30","04_prototipo/datos/muestra.csv","F1"),
 ("E09","Oráculo de resumen","04_prototipo/datos/oraculo_resumen.csv","F2"),
 ("E10","Oráculo de rechazos","04_prototipo/datos/oraculo_rechazos.csv","F1"),
 ("E11","Regla base experimental","04_prototipo/versiones/v1.py","F1"),
 ("E12","Regla de calendario corregida","04_prototipo/versiones/v2.py","F1"),
 ("E13","Implementación y permiso local","04_prototipo/panviz.py","F1 y F2"),
 ("E14","Vista y edición de CSV","04_prototipo/index.html","F1 y F2"),
 ("E15","Casos y criterios de prueba","05_pruebas/casos.csv","F1 y F2"),
 ("E16","Suite de medición repetible","05_pruebas/medir.py","F1 y F2"),
 ("E17","Ejecución registrada antes","05_pruebas/resultados/v1.json","F1 y F2"),
 ("E18","Ejecución registrada después","05_pruebas/resultados/v2.json","F1 y F2"),
 ("E19","Protocolo de interacción","05_pruebas/protocolo_usuario.md","F1 y F2"),
 ("E20","Plan de aportes y revisión","01_plan/aportes.csv","Común"),
 ("E21","Comunicación de hallazgos","06_evidencias/hallazgos.csv","Común"),
 ("E22","Plan de mejora priorizado","06_evidencias/acciones.csv","Común"),
 ("E23","Ruta de sustentación y cierre","01_plan/entrega_exposicion.md","Común"),
 ("E24","Vista del tablero y formulario CSV","07_tablero/index.html","Común"),
 ("E25","Captura del tablero antes","07_tablero/capturas/antes.png","Común"),
 ("E26","Captura del tablero después","07_tablero/capturas/despues.png","Común"),
 ("E27","Acta de uso del proceso","06_evidencias/entrevistas/Acta_01_uso_proceso.md","Común"),
 ("E28","Diferencia en la regla de calendario","05_pruebas/diff_regla_fecha.txt","F1"),
 ("E29","Acta de validación de resultados","06_evidencias/entrevistas/Acta_02_validacion.md","F1 y F2"),
 ("E30","Registro de revisión cruzada","06_evidencias/revision_cruzada/registro.md","Común"),
 ("E31","Verificación de la herramienta","07_tablero/herramienta.md","Común"),
 ("E32","Plan de acopio e indexación","06_evidencias/acopio.md","Común"),
 ("E33","Captura T09: P026 corregido","06_evidencias/pruebas_usuario/T09_p026_corregido.png","F1"),
 ("E34","Captura T10: resumen de Chivay","06_evidencias/pruebas_usuario/T10_resumen_chivay.png","F2"),
]
PENDING = {"E27", "E29", "E30"}
V2_ONLY = {"E05","E12","E18","E26","E28","E33","E34"}
V1_ONLY = {"E11","E17","E25"}
CRITERIA = [
 ("OPD","E1","Estándar y plantillas versionados","E02 E04","E02 E04","E","E","Proceso y tres plantillas localizables."),
 ("OPD","E1","Estándar aplicado en ambos flujos","E03 E13","E03 E13","E","E","Flujos comparten controles y tienen adaptación documentada."),
 ("OPD","E1","Revisión y aprobación del estándar por otro integrante","","","N","N","Falta corroboración y aprobación registradas."),
 ("OPD","E1","Lección incorporada al proceso revisado","","E05 E28","N","E","Antes no se incorporaba la lección. Después se registra el caso negativo y la regresión."),
 ("IPM","E1","Plan integrado con alcance y roles","E01 E20","E01 E20","E","E","Plan y roles propuestos explícitos; aprobación se verifica en C07."),
 ("IPM","E1","Adaptación aplicada a captura y consolidación","E03 E17","E03 E18","E","E","Los resultados permiten verificar ejecución de ambos flujos."),
 ("IPM","E1","Revisión del plan y resolución de discrepancias","","","N","N","Acta de revisión e interacción del equipo pendientes."),
 ("IPM","E5","Seguimiento integrado antes y después","E17 E24","E17 E18 E24","P","E","En v1 existe un corte; v2 incorpora comparación reproducible."),
 ("RD","E2","Seis requisitos medibles vinculados a pruebas","E06 E15","E06 E15","E","E","Cada requisito apunta a una prueba observable."),
 ("RD","E2","Resultados cumplen aceptación funcional de datos","E09 E10 E17","E09 E10 E18","P","E","v1: 4/6 motivos coinciden y consolidado difiere. v2: 6/6 y totales exactos."),
 ("RD","E2","Requisitos contrastados por otro integrante","","","N","N","Falta revisión nominal de requisitos y trazabilidad."),
 ("RD","E2","Mejora mantiene trazabilidad hacia oráculo y regla","E06 E10 E17","E06 E10 E18 E28","P","E","v1 describe regla pero no satisface el calendario; v2 incorpora corrección."),
 ("RSKM","E2","Cinco riesgos con respuesta y rol responsable","E07","E07","E","E","Cinco disparadores, responsables propuestos y respuestas."),
 ("RSKM","E4","Controles de fecha y publicación ejecutados","E07 E17","E07 E18","P","E","Control local de permiso en ambas; calendario falla en v1."),
 ("RSKM","E2","Riesgos revisados por otra persona","","","N","N","Falta revisión cruzada registrada."),
 ("RSKM","E2","Cambio y riesgo tienen una acción seguida","E21 E22","E05 E21 E22","P","E","El riesgo de fecha pasa de reproducido a corregido; otros se mantienen abiertos."),
 ("VER","E4","Plan con 12 casos y esperado independiente","E09 E10 E15","E09 E10 E15","E","E","Hay dos casos para cada característica."),
 ("VER","E4","Suite técnica ejecutada con evidencia reproducible","E16 E17","E16 E18","E","E","Diez casos técnicos ejecutados por versión, incluidos los fallidos."),
 ("VER","E4","Revisión por pares de evidencia de verificación","","","N","N","Falta revisión humana del log y los pasos."),
 ("VER","E4","Regresión posterior al cambio aprobada","E17","E18 E28","N","E","T12 falla en la base experimental y pasa tras el cambio."),
 ("VAL","E4","Protocolo con dos escenarios y condiciones de observación","E19","E19","E","E","Tareas, cronometraje, condiciones y criterio de aceptación definidos."),
 ("VAL","E4","Dos tareas ejecutadas con usuario simulado","","E18 E19 E33 E34","N","E","v1: sin ejecución con usuario. v2: resultados registrados y capturas enlazadas para T09 y T10."),
 ("VAL","E4","Usuario y revisor corroboran el resultado","","","N","N","No existe un acta confirmada por participantes."),
 ("VAL","E4","Seguimiento de aceptación y adopción en ciclos posteriores","","","X","X","La muestra cubre un piloto; falta observación de ciclos posteriores."),
]
LINKS = [
 ("R01","C10","E10 E17 E18","T01","H01","A01"),
 ("R01","C18","E15 E16 E17 E18","T03","H04","A03"),
 ("R02","C18","E15 E16 E17 E18","T05 T06","H04","A03"),
 ("R03","C10","E09 E17 E18","T02","H01","A01"),
 ("R03","C18","E16 E17 E18","T04","H04","A03"),
 ("R04","C14","E07 E13 E17 E18","T07 T08","H03","A03"),
 ("R05","C22","E18 E19 E33 E34","T09 T10","H02","A02"),
 ("R06","C20","E05 E17 E18 E28","T11 T12","H01","A01"),
]
STATES = {"E":"Evidenciado","P":"Parcial","N":"No evidenciado","X":"No evaluable"}


def read_csv(path):
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def save_csv(path, rows):
    with path.open("w",encoding="utf-8-sig",newline="") as f:
        writer = csv.DictWriter(f,fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def generate():
    EXPORT.mkdir(exist_ok=True)
    tests = {v:json.loads((ROOT/f"05_pruebas/resultados/{v}.json").read_text(encoding="utf-8")) for v in ("v1","v2")}
    date = tests["v2"]["fecha_utc"][:10]
    index = []
    for key, title, path, flow in EVIDENCE:
        f = ROOT/path
        if not f.is_file() and key not in {"E25","E26","E31"}:
            raise FileNotFoundError(path)
        index.append(dict(id=key,descripcion=title,tipo=f.suffix.strip("."),ruta=path,
            version="v1" if key in V1_ONLY else "v2" if key in V2_ONLY else "TP9",
            fecha=date,autor="Ejecución técnica automatizada" if key in {"E17","E18","E25","E26"} else "Preparación del paquete TP9",
            revisor="Pendiente de revisión nominal",flujo=flow,
            validez="Plantilla pendiente" if key in PENDING else "Pendiente" if not f.is_file() else "Disponible",
            sha256=hashlib.sha256(f.read_bytes()).hexdigest() if f.is_file() else ""))
    idx={x["id"]:x for x in index}
    criteria = []
    cases = read_csv(ROOT/"05_pruebas/casos.csv")
    all_tests, stats = [], []
    findings = read_csv(ROOT/"06_evidencias/hallazgos.csv")
    actions = read_csv(ROOT/"06_evidencias/acciones.csv")
    for pos,v in enumerate(("v1","v2")):
        subset=[]
        for n,(area,owner,desc,e1,e2,a,b,why) in enumerate(CRITERIA,1):
            evidence = (e1,e2)[pos].split()
            assert all(idx[e]["validez"]=="Disponible" for e in evidence)
            subset.append(dict(corte=v,id=f"C{n:02}",area=area,descripcion=desc,responsable=owner,
                               estado=STATES[(a,b)[pos]],justificacion=why,evidencia=" ".join(evidence)))
        criteria.extend(subset)
        test_list=[]
        for row in cases:
            t=tests[v]["pruebas"][row["id"]]
            evidence_id = "E19" if t["resultado"] == "No ejecutada" else "E17" if v == "v1" else "E18"
            if row["id"] in {"T09", "T10"} and isinstance(t.get("detalle"), dict):
                evidence_id = t["detalle"].get("evidencia_id") or evidence_id
            test_list.append(dict(corte=v,**row,observado=t["observado"],duracion_ms=t["duracion_ms"],
                                  resultado=t["resultado"],evidencia=evidence_id))
        all_tests.extend(test_list)
        cnt=lambda tag: sum(r["resultado"]==tag for r in test_list)
        done=len(test_list)-cnt("No ejecutada")
        stats.append(dict(corte=v,cobertura_n=sum(bool(c["evidencia"]) for c in subset),cobertura_d=24,
                          evidenciados_n=sum(c["estado"]=="Evidenciado" for c in subset),evidenciados_d=24,
                          ejecutadas_n=done,ejecutadas_d=12,aprobadas_n=cnt("Aprobada"),aprobadas_d=done,
                          pendientes=cnt("No ejecutada"),fallidas=cnt("Fallida"),
                          debilidades_abiertas=sum(h["tipo"]=="Debilidad" and h[f"estado_{v}"]=="Abierta" for h in findings)))
    links=[dict(zip(("requisito","criterio","evidencia","pruebas","hallazgo","accion"),r)) for r in LINKS]
    for name, data in (("criterios",criteria),("evidencias",index),("pruebas",all_tests),("hallazgos",findings),("acciones",actions),("indicadores",stats),("trazabilidad",links)):
        save_csv(EXPORT/f"{name}.csv",data)
    data=dict(criterios=criteria,evidencias=index,pruebas=all_tests,hallazgos=findings,acciones=actions,
              indicadores=stats,trazabilidad=links)
    (EXPORT/"evaluacion.json").write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(stats,ensure_ascii=False))
    return data


if __name__=="__main__":
    generate()
