#!/usr/bin/env python3
"""ai-dd: validadores deterministas del flujo, índice de estado y hook de guardia.

Uso:
  aidd.py validate [RUTA ...]      Valida specs (carpetas docs/specs/NNN-slug o archivos).
                                   Sin rutas valida todas. Código de salida 1 si hay errores.
  aidd.py status [--json]          Estado de todas las specs y siguiente paso sugerido.
  aidd.py hash RUTA                Huellas de spec/plan/tasks (las registra /analyze).
  aidd.py snapshot RUTA            Guarda una copia de spec/plan/tasks en .ai/cache/ (la usa /analyze).
  aidd.py changes RUTA [--since REF]
                                   Diff de spec/plan/tasks contra la última copia guardada o
                                   contra un commit (REF).
  aidd.py rotate RUTA KIND         Archiva en history/ la ronda o versión vigente
                                   (KIND: analysis | review | plan | tasks).
  aidd.py history RUTA [--write] [--migrate]
                                   Índice de rondas y versiones; --write escribe history/README.md;
                                   --migrate mueve a history/ los *.rN.md / *.vN.md sueltos.
  aidd.py review-pack RUTA [--base REF] [--head REF]
                                   Prepara el paquete compartido de /review en .ai/cache/review/:
                                   diff de código filtrado, alcance (archivos vs tareas) y contexto.
  aidd.py hook pre-tool            Hook PreToolUse: lee el evento JSON por stdin.

Solo usa la biblioteca estándar de Python 3.8+. Se copia a cada proyecto como .ai/bin/aidd.py
para que CI pueda ejecutarlo sin el plugin.
"""
import difflib
import hashlib
import shutil
import json
import os
import re
import subprocess
import sys

VERSION = "1.8.1"

SPEC_STATES = {"draft", "inferred", "approved", "implemented", "released"}
PLAN_STATES = {"draft", "approved", "blocked"}
TASKS_STATES = {"draft", "approved"}
VERDICTS = {"approved", "changes_requested", "blocked"}
FIXED_TASKS = ["T090", "T091", "T092", "T095", "T096", "T097", "T098"]
DEPLOY_TASKS = {"T095", "T096", "T097", "T098"}

TASK_RE = re.compile(r"^\s*- \[( |x|X)\] (T\d{3})\b(.*)$")
CA_DEF_RE = re.compile(r"^\s*- \[( |x|X)\] ((?:CA|AC)\d+)\b(.*)$")
CA_ID = r"(?:CA|AC)\d+"

# Vocabulario canónico en español e inglés (shared/vocabulary.md). Los documentos pueden usar
# cualquiera de los dos; el validador acepta ambos.
VOCAB = {
    "problem": ["Problema", "Problem"],
    "criteria": ["Criterios de aceptación", "Acceptance criteria"],
    "out_of_scope": ["Fuera de alcance", "Out of scope"],
    "security": ["Seguridad y privacidad", "Security and privacy"],
    "audit": ["Auditoría", "Audit"],
    "risk_coverage": ["Cobertura de riesgos", "Risk coverage"],
    "history": ["Historial", "History"],
    "constitution_check": ["Constitution Check"],
    "traceability": ["Trazabilidad", "Traceability"],
    "threat_model": ["Modelo de amenazas", "Threat model"],
    "rollout": ["Rollout"],
    "observability": ["Observabilidad", "Observability"],
    "accepted": ["Aceptados", "Accepted"],
    "deferred": ["Aceptados sin tarea", "Accepted without task"],
}
W = {
    "done_when": r"(?:hecho cuando|done when):",
    "covers": r"(?:cubre|covers):",
    "depends": r"(?:depende|depends(?: on)?):",
    "note": r"^\s+- (?:nota|note):",
    "abuse": r"\((?:abuso|abuse)\)",
    "not_applicable": r"\b(?:no aplica|not applicable|n/a)\b",
    "not_met": r"HOY NO SE CUMPLE|NOT MET TODAY",
    "clarify": r"\[(?:NECESITA ACLARACIÓN|NEEDS CLARIFICATION)\]",
    "accepted": r"\b(?:aceptad[oa]|accepted)\b",
    "partial": r"\b(?:parcial\w*|partial\w*)\b",
    "mitigated": r"\b(?:mitigad\w*|mitigated)\b",
    "out": r"\b(?:fuera|out)\b",
    "in": r"\b(?:dentro|in)\b",
    "risk_by_number": r"\b(?:riesgos?|risks?)\s+\d",
    "note_of": r"(?:nota de|note (?:on|for|of|in))",
}
PLACEHOLDER_RE = re.compile(r"\{\{[^}]*\}\}")
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)


# ---------------------------------------------------------------- utilidades

def read(path):
    """Lee UTF-8 (con o sin BOM). Si el archivo se guardó en ANSI (cp1252, habitual en editores de
    Windows), lo lee igualmente en lugar de fallar."""
    with open(path, "rb") as f:
        raw = f.read()
    for enc in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", "replace")


def frontmatter(text):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    data = {}
    if not m:
        return data
    for line in m.group(1).splitlines():
        mm = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if mm:
            val = mm.group(2).split(" #")[0].strip().strip('"').strip("'")
            data[mm.group(1)] = val
    return data


def body(text):
    return re.sub(r"^---\s*\n.*?\n---\s*\n", "", text, count=1, flags=re.S)


def section(text, title):
    """Contenido de la sección '## <title>' hasta la siguiente '## '. `title` puede ser una clave de
    VOCAB (acepta sus variantes en español e inglés) o un título literal."""
    if title in VOCAB:
        for t in VOCAB[title]:
            r = section(text, t)
            if r is not None:
                return r
        return None
    m = re.search(r"^##\s+" + re.escape(title) + r"\b.*?$(.*?)(?=^##\s|\Z)", text, re.M | re.S)
    return m.group(1) if m else None


def find_root(start):
    cur = os.path.abspath(start)
    while True:
        if os.path.isfile(os.path.join(cur, ".ai", "project.yaml")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            return None
        cur = parent


def yaml_scalar(text, key):
    m = re.search(r"^\s*" + re.escape(key) + r":\s*([^#\n]*)", text, re.M)
    return m.group(1).strip().strip('"').strip("'") if m else None


def yaml_list(text, key):
    m = re.search(r"^(\s*)" + re.escape(key) + r":\s*(.*)$", text, re.M)
    if not m:
        return []
    inline = m.group(2).split("#")[0].strip()
    if inline.startswith("["):
        return [x.strip().strip('"').strip("'") for x in inline.strip("[]").split(",") if x.strip()]
    items, indent = [], len(m.group(1))
    for line in text[m.end():].splitlines()[1:]:
        mm = re.match(r"^(\s*)-\s*(.+)$", line)
        if mm and len(mm.group(1)) > indent:
            items.append(mm.group(2).split("#")[0].strip().strip('"').strip("'"))
        elif line.strip():
            break
    return items


class Report:
    def __init__(self, label):
        self.label, self.errors, self.warnings = label, [], []

    def err(self, msg):
        self.errors.append(msg)

    def warn(self, msg):
        self.warnings.append(msg)

    def print(self):
        mark = "✗" if self.errors else ("!" if self.warnings else "✓")
        print(f"{mark} {self.label}")
        for e in self.errors:
            print(f"    error: {e}")
        for w in self.warnings:
            print(f"    aviso: {w}")


# ---------------------------------------------------------------- modelo

def load_spec_dir(d):
    spec = {"dir": d, "name": os.path.basename(os.path.normpath(d))}
    for kind in ("spec", "plan", "tasks", "review", "analysis"):
        p = os.path.join(d, kind + ".md")
        spec[kind] = read(p) if os.path.isfile(p) else None
    return spec


def spec_cas(spec_text):
    sec = section(body(spec_text), "criteria") or ""
    cas = []
    for line in sec.splitlines():
        m = CA_DEF_RE.match(line)
        if m:
            cas.append((m.group(2), m.group(1).lower() == "x", bool(re.search(W["abuse"], line, re.I))))
    return cas


def plan_threats(plan_text):
    sec = section(body(plan_text), "threat_model") or ""
    return sorted(set(re.findall(r"\|\s*(TM\d+)\s*\|", sec)), key=lambda x: int(x[2:]))


def parse_tasks(tasks_text):
    tasks = {}
    order = []
    for line in body(tasks_text).splitlines():
        m = TASK_RE.match(line)
        if not m:
            continue
        tid, rest = m.group(2), m.group(3)
        parts = [p.strip() for p in rest.split(" — ")]
        deps = re.findall(r"T\d{3}", (re.search(W["depends"] + r"\s*([^—]*)", rest, re.I) or [None, ""])[1] or "")
        covers = re.findall(CA_ID, (re.search(W["covers"] + r"\s*([^—]*)", rest, re.I) or [None, ""])[1] or "")
        files = parts[1] if len(parts) > 1 else ""
        tasks.setdefault(tid, []).append({
            "id": tid,
            "done": m.group(1).lower() == "x",
            "parallel": rest.lstrip().startswith("[P]"),
            "text": rest,
            "files": [f.strip(" `") for f in re.split(r",\s*", files) if f.strip()],
            "deps": deps,
            "covers": covers,
            "has_done_when": bool(re.search(W["done_when"], rest, re.I)),
        })
        order.append(tid)
    return tasks, order


def fingerprint(text):
    """Huella estable del contenido: ignora frontmatter, casillas marcadas y notas de avance."""
    if not text:
        return None
    lines = []
    for line in body(text).splitlines():
        if re.match(W["note"], line):
            continue
        lines.append(re.sub(r"^(\s*)- \[[xX]\]", r"\1- [ ]", line).rstrip())
    return hashlib.sha256("\n".join(lines).strip().encode("utf-8")).hexdigest()[:12]


def fingerprints(s):
    return {k + "_sha": fingerprint(s[k]) for k in ("spec", "plan", "tasks")}


def analysis_state(s):
    """None si no hay análisis; 'stale', 'fail' o 'pass'."""
    if not s["analysis"]:
        return None
    afm = frontmatter(s["analysis"])
    if any(afm.get(k) != v for k, v in fingerprints(s).items()):
        return "stale"
    return "pass" if afm.get("result") == "pass" else "fail"


def task_notes(tasks_text):
    """{tarea: texto de sus líneas '- nota:'}."""
    notes, cur = {}, None
    for line in body(tasks_text).splitlines():
        m = TASK_RE.match(line)
        if m:
            cur = m.group(2)
            continue
        if cur and re.match(W["note"], line):
            notes[cur] = notes.get(cur, "") + " " + line.strip()
        elif line.strip() and not line.startswith((" ", "\t")):
            cur = None
    return notes


ACCEPTED_NOTE_RE = re.compile(r"^\s*-\s*\*\*([A-Z]\d+):?\*\*:?\s*(?:→|->)\s*" + W["note_of"]
                              + r"\s+((?:T\d{3}(?:\s*(?:,|y|and)\s*)?)+)", re.I)
ROUND_FILE_RE = re.compile(r"^(analysis|review)\.r(\d+)\.md$|^(plan|tasks)\.v(\d+)\.md$")


def history_dir(d):
    return os.path.join(d, "history")


def analysis_texts(d):
    """analysis.md y sus rondas archivadas (en history/ o sueltas)."""
    out = []
    for base in (d, history_dir(d)):
        if not os.path.isdir(base):
            continue
        for f in sorted(os.listdir(base)):
            if f == "analysis.md" and base == d or re.match(r"^analysis\.r\d+\.md$", f):
                out.append(read(os.path.join(base, f)))
    return out


def accepted_as_notes(d):
    """{(hallazgo, tarea)} de los aceptados con formato '- **ID** → nota de Txxx'."""
    pairs = set()
    for text in analysis_texts(d):
        for line in (section(body(text), "accepted") or "").splitlines():
            m = ACCEPTED_NOTE_RE.match(line)
            if m:
                for t in re.findall(r"T\d{3}", m.group(2)):
                    pairs.add((m.group(1), t))
    return pairs


def rounds(s):
    a = frontmatter(s["analysis"]).get("round") if s["analysis"] else None
    r = frontmatter(s["review"]).get("round") if s["review"] else None
    parts = []
    if a:
        parts.append("a" + a)
    if r:
        parts.append("r" + r)
    return " ".join(parts) or None


def git(root, *args):
    env = dict(os.environ, GIT_OPTIONAL_LOCKS="0")
    try:
        p = subprocess.run(["git"] + list(args), cwd=root, capture_output=True, env=env)
    except OSError:
        return 127, ""
    return p.returncode, p.stdout.decode("utf-8", "replace")


RISK_DOCS = ("security.md", "observability.md", "deployment.md")
RISK_RE = r"(?:RS|OB|RD)\d+"


def load_risks(root):
    """{riesgo: [correcciones]} a partir de los documentos de riesgos del proyecto."""
    risks = {}
    for name in RISK_DOCS:
        p = os.path.join(root, "docs", name)
        if not os.path.isfile(p):
            continue
        for line in read(p).splitlines():
            m = re.match(r"^###\s+(" + RISK_RE + r")\b", line)
            if m:
                risks.setdefault(m.group(1), [])
                continue
            m = re.match(r"^\s*-\s+((" + RISK_RE + r")\.[a-z])\b", line)
            if m:
                risks.setdefault(m.group(2), [])
                if m.group(1) not in risks[m.group(2)]:
                    risks[m.group(2)].append(m.group(1))
    return {k: v for k, v in risks.items() if v}


def cited_risks(text, risks):
    ids = set(re.findall(r"\b(" + RISK_RE + r")(?:\.[a-z])?\b", text))
    return sorted(i for i in ids if i in risks)


def coverage_rows(spec_text):
    """{corrección: 'dentro' | 'fuera'} según la sección 'Cobertura de riesgos'."""
    sec = section(body(spec_text), "risk_coverage") or ""
    rows = {}
    for line in sec.splitlines():
        for cid in re.findall(r"\b((?:RS|OB|RD)\d+\.[a-z])\b", line):
            cells = [c.strip() for c in line.split("|")]
            idx = next((i for i, c in enumerate(cells) if cid in c), None)
            # Columna "Alcance / Scope": la celda siguiente a la de la corrección.
            rest = cells[idx + 1] if idx is not None and idx + 1 < len(cells) else line.split(cid, 1)[1]
            rows[cid] = "fuera" if re.search(W["out"], rest, re.I) else (
                "dentro" if re.search(W["in"], rest, re.I) else None)
    return rows


def mitigation_claims(text, risk):
    """Líneas que declaran mitigado el riesgo completo (no una corrección) sin decir 'parcial'."""
    out = []
    for line in text.splitlines():
        if re.search(r"\b" + risk + r"\b(?!\.[a-z])", line) and re.search(W["mitigated"], line, re.I) \
                and not re.search(W["partial"], line, re.I):
            out.append(line.strip()[:80])
    return out


def constitution_principles(root):
    p = os.path.join(root, "docs", "constitution.md")
    if not os.path.isfile(p):
        return None
    return re.findall(r"^###\s+(P\d+)\b", read(p), re.M)


# ---------------------------------------------------------------- validación

def validate_spec_dir(d, root):
    s = load_spec_dir(d)
    rep = Report(os.path.relpath(d, root) if root else d)
    if not s["spec"]:
        rep.err("falta spec.md")
        return rep
    principles = constitution_principles(root) if root else None

    # --- spec
    fm = frontmatter(s["spec"])
    st = fm.get("status")
    if st not in SPEC_STATES:
        rep.err(f"spec: status inválido o ausente ({st!r})")
    text = COMMENT_RE.sub("", s["spec"])
    if PLACEHOLDER_RE.search(text):
        rep.err("spec: quedan {{placeholders}} sin sustituir")
    cas = spec_cas(s["spec"])
    ids = [c[0] for c in cas]
    own = os.path.basename(os.path.normpath(d))[:3]
    extends = re.findall(r"\d{3}", fm.get("extends", ""))
    if extends and root:
        existing = {os.path.basename(x)[:3] for x in spec_dirs(root)}
        for n in extends:
            if n == own:
                rep.err("spec: extends se incluye a sí misma")
            elif n not in existing:
                rep.err(f"spec: extends apunta a {n}, que no existe en docs/specs/")
    if not cas:
        rep.err("spec: no hay criterios de aceptación numerados (CA1, CA2…)")
    dup = {i for i in ids if ids.count(i) > 1}
    if dup:
        rep.err(f"spec: criterios duplicados {sorted(dup)}")
    pending_q = len(re.findall(W["clarify"], text))
    if pending_q > 3:
        rep.err(f"spec: {pending_q} marcadores [NECESITA ACLARACIÓN] (máximo 3)")
    if st in {"approved", "implemented", "released"} and pending_q:
        rep.err("spec: aprobada con [NECESITA ACLARACIÓN] abiertos")
    for key in ("problem", "criteria", "out_of_scope"):
        if section(body(s["spec"]), key) is None:
            rep.err(f"spec: falta la sección '{' / '.join(VOCAB[key])}'")
    sec_sec = section(body(s["spec"]), "security")
    sensitive = sec_sec is not None and not re.search(W["not_applicable"], sec_sec, re.I)
    if sec_sec is None:
        (rep.warn if st == "inferred" else rep.err)("spec: falta la sección 'Seguridad y privacidad'")
    elif sensitive and not any(c[2] for c in cas):
        rep.warn("spec: la sección de seguridad no dice 'No aplica' y no hay criterios '(abuso)'")
    if sensitive and st != "inferred" and section(body(s["spec"]), "audit") is None:
        rep.warn("spec: toca datos sensibles o permisos pero no tiene sección 'Auditoría' "
                 "(eventos que deben registrarse)")
    for line in (section(body(s["spec"]), "criteria") or "").splitlines():
        m = CA_DEF_RE.match(line)
        if m and m.group(1).lower() == "x" and re.search(W["not_met"], line.upper()):
            rep.err(f"spec: {m.group(2)} está marcado [x] pero dice 'HOY NO SE CUMPLE'")
    if st in {"implemented", "released"}:
        open_cas = [c[0] for c in cas if not c[1]]
        if open_cas:
            rep.err(f"spec: estado {st} con criterios sin marcar {sorted(set(open_cas))}")

    # --- tamaño
    n_ext = len(re.findall(r"\d{3}", fm.get("extends", "")))
    if len(set(ids)) > 12 or n_ext > 4:
        rep.warn(f"spec: grande ({len(set(ids))} criterios, extiende {n_ext} specs); considera dividirla "
                 "antes de planear (más vueltas de /plan y /analyze)")

    # --- cobertura de riesgos
    risks = load_risks(root) if root else {}
    covered_all = {}
    if risks:
        cited = cited_risks(body(s["spec"]), risks)
        rows = coverage_rows(s["spec"])
        if cited and section(body(s["spec"]), "risk_coverage") is None:
            rep.err(f"spec: cita {cited} pero no tiene sección 'Cobertura de riesgos'")
        for r in cited:
            missing = [c for c in risks[r] if rows.get(c) is None]
            if missing:
                rep.err(f"spec: {r} tiene correcciones sin declarar dentro o fuera: {missing}")
            fuera = [c for c in risks[r] if rows.get(c) == "fuera"]
            covered_all[r] = not missing and not fuera
            if fuera and not re.search(W["partial"], section(body(s["spec"]), "problem") or "", re.I):
                rep.warn(f"spec: deja fuera {fuera} y el Problema no dice que atiende {r} parcialmente")
        no_hist = re.sub(r"^##\s+(?:Historial|History)\b.*?(?=^##\s|\Z)", "", body(s["spec"]), flags=re.M | re.S)
        if re.search(W["risk_by_number"], no_hist, re.I):
            rep.warn("spec: cita riesgos por número ('riesgo 1'); usa sus IDs (RS1…) y declara sus correcciones")
    for kind in ("plan", "tasks"):
        if s[kind] and risks:
            for r in cited_risks(body(s[kind]), risks):
                if covered_all.get(r):
                    continue
                for line in mitigation_claims(body(s[kind]), r):
                    rep.err(f"{kind}: declara {r} mitigado pero la spec no cubre todas sus correcciones: '{line}'")

    # --- plan
    threats = []
    if s["plan"]:
        pfm = frontmatter(s["plan"])
        pst = pfm.get("status")
        if pst not in PLAN_STATES:
            rep.err(f"plan: status inválido o ausente ({pst!r})")
        ptext = COMMENT_RE.sub("", s["plan"])
        if PLACEHOLDER_RE.search(ptext):
            rep.err("plan: quedan {{placeholders}} sin sustituir")
        if pst == "approved" and st not in {"approved", "implemented", "released"}:
            rep.err(f"plan: aprobado sobre una spec en estado {st}")
        cc = section(body(ptext), "constitution_check") or ""
        if principles is not None:
            missing = [p for p in principles if not re.search(r"\b" + p + r"\b", cc)]
            if missing:
                rep.err(f"plan: Constitution Check no evalúa {missing}")
        for line in cc.splitlines():
            if "❌" in line and not re.search(W["accepted"], line, re.I) and pst == "approved":
                rep.err("plan: aprobado con un ❌ sin aceptación registrada")
        trace = section(body(ptext), "traceability")
        if trace is None:
            rep.err("plan: falta la sección 'Trazabilidad'")
            trace = ""
        missing_ca = [c for c in ids if not re.search(r"\b" + c + r"\b", trace)]
        if missing_ca:
            rep.err(f"plan: criterios sin trazabilidad {missing_ca}")
        threats = plan_threats(s["plan"])
        missing_tm = [t for t in threats if not re.search(r"\b" + t + r"\b", trace)]
        if missing_tm:
            rep.err(f"plan: amenazas sin test en Trazabilidad {missing_tm}")
        if section(body(ptext), "threat_model") is None:
            rep.warn("plan: no tiene sección 'Modelo de amenazas'")
        if section(body(ptext), "rollout") is None:
            rep.err("plan: falta la sección 'Rollout'")
        ptype = yaml_scalar(read(os.path.join(root, ".ai", "project.yaml")), "type") if root else None
        if sensitive and ptype != "library" and section(body(ptext), "observability") is None:
            rep.warn("plan: la spec toca datos sensibles o permisos y el plan no tiene sección "
                     "'Observabilidad' (logs, eventos de auditoría, métricas)")

    # --- tasks
    if s["tasks"]:
        if not s["plan"]:
            rep.err("tasks: existe tasks.md sin plan.md")
        tfm = frontmatter(s["tasks"])
        tst = tfm.get("status")
        if tst not in TASKS_STATES:
            rep.err(f"tasks: status inválido o ausente ({tst!r})")
        if tst == "approved" and s["plan"] and frontmatter(s["plan"]).get("status") != "approved":
            rep.err("tasks: aprobado sobre un plan no aprobado")
        tasks, order = parse_tasks(s["tasks"])
        dups = [t for t, v in tasks.items() if len(v) > 1]
        if dups:
            rep.err(f"tasks: IDs duplicados {dups}")
        flat = {t: v[0] for t, v in tasks.items()}
        for fid in FIXED_TASKS:
            if fid not in flat:
                rep.err(f"tasks: falta la tarea fija {fid}")
        work = {t: v for t, v in flat.items() if int(t[1:]) < 90}
        bad_range = [t for t in flat if 93 <= int(t[1:]) <= 94 or int(t[1:]) == 99 or int(t[1:]) == 0]
        if bad_range:
            rep.warn(f"tasks: IDs en rango reservado sin uso definido {bad_range}")
        if not work:
            rep.err("tasks: no hay tareas de trabajo (T001–T089)")
        for t, v in work.items():
            if not v["has_done_when"]:
                rep.err(f"tasks: {t} sin 'hecho cuando:'")
            if len(v["files"]) > 3:
                rep.warn(f"tasks: {t} toca {len(v['files'])} archivos (máximo recomendado 3)")
            for dep in v["deps"]:
                if dep not in flat:
                    rep.err(f"tasks: {t} depende de {dep}, que no existe")
        # ciclos
        state = {}

        def visit(n, stack):
            state[n] = 1
            for dep in flat.get(n, {}).get("deps", []):
                if dep not in flat:
                    continue
                if state.get(dep) == 1:
                    rep.err(f"tasks: dependencia circular {' → '.join(stack + [n, dep])}")
                elif state.get(dep) is None:
                    visit(dep, stack + [n])
            state[n] = 2

        for n in flat:
            if state.get(n) is None:
                visit(n, [])
        covered = {c for v in work.values() for c in v["covers"]}
        uncovered = sorted({c for c in ids if c not in covered}, key=lambda x: int(x[2:]))
        if uncovered:
            rep.err(f"tasks: criterios sin tarea que los cubra {uncovered}")
        tbody = body(s["tasks"])
        missing_tm = [t for t in threats if not re.search(r"\b" + t + r"\b", tbody)]
        if missing_tm:
            rep.err(f"tasks: amenazas sin tareas {missing_tm}")
        par = [v for v in work.values() if v["parallel"] and not v["done"]]
        for i, a in enumerate(par):
            for b in par[i + 1:]:
                shared = set(a["files"]) & set(b["files"])
                if shared:
                    rep.warn(f"tasks: {a['id']} y {b['id']} son [P] y comparten {sorted(shared)}")
        if st in {"implemented", "released"}:
            open_t = [t for t, v in flat.items() if not v["done"] and t not in DEPLOY_TASKS]
            if open_t:
                rep.err(f"spec {st} con tareas abiertas {sorted(open_t)}")
        if st == "released" and "T098" in flat and not flat["T098"]["done"]:
            rep.err("spec released con T098 sin marcar")
        notes = task_notes(s["tasks"])
        for fid, tid in sorted(accepted_as_notes(d)):
            if tid not in flat:
                rep.err(f"analysis: el aceptado {fid} va como nota de {tid}, que no existe")
            elif flat[tid]["done"] and not re.search(r"\b" + fid + r"\b", notes.get(tid, "")):
                rep.err(f"tasks: {tid} está hecha sin la nota del aceptado {fid} (analysis → Aceptados)")
    elif st in {"implemented", "released"}:
        rep.err(f"spec {st} sin tasks.md")

    # --- analysis
    if s["analysis"]:
        ast = analysis_state(s)
        if frontmatter(s["analysis"]).get("result") not in {"pass", "fail"}:
            rep.err("analysis: result inválido o ausente (pass | fail)")
        elif ast == "stale" and st == "approved" and not (
                s["review"] and frontmatter(s["review"]).get("verdict") == "changes_requested"):
            rep.warn("analysis: desactualizado (spec, plan o tareas cambiaron después de /analyze)")

    # --- historial
    loose = sorted(f for f in os.listdir(d) if ROUND_FILE_RE.match(f))
    if loose:
        rep.warn(f"rondas o versiones anteriores sueltas {loose}: van en history/ "
                 "(python .ai/bin/aidd.py history <ruta> --migrate)")

    # --- review
    if s["review"]:
        rfm = frontmatter(s["review"])
        deferred = re.findall(r"^\s*-\s*\*\*(R\d+)", section(body(s["review"]), "deferred") or "", re.M)
        if deferred and st == "released" and root:
            rm = os.path.join(root, "docs", "roadmap.md")
            rtext = read(rm) if os.path.isfile(rm) else ""
            lost = [r for r in deferred if not re.search(re.escape(own) + r"/" + r + r"\b", rtext)]
            if lost:
                rep.warn(f"review: aceptados sin tarea que no están en el roadmap como {own}/Rn: {lost}")
        verdict = rfm.get("verdict")
        if verdict not in VERDICTS:
            rep.err(f"review: verdict inválido o ausente ({verdict!r})")
        if st == "released" and verdict != "approved":
            rep.err("spec released sin review aprobada")
        if st == "released" and rfm.get("human_signoff", "").startswith("pending"):
            rep.err("spec released con human_signoff pendiente")
    elif st == "released":
        rep.err("spec released sin review.md")
    return rep


def validate_roadmap(root):
    p = os.path.join(root, "docs", "roadmap.md")
    risks = load_risks(root)
    if not os.path.isfile(p) or not risks:
        return 0
    rep = Report("docs/roadmap.md")
    for line in read(p).splitlines():
        if not line.startswith("|"):
            continue
        num = (line.split("|") + ["", ""])[1].strip()
        for r in cited_risks(line, risks):
            missing = [c for c in risks[r] if not re.search(r"\b" + re.escape(c) + r"\b", line)]
            if missing:
                rep.err(f"objetivo {num}: cita {r} sin declarar las correcciones {missing} (dentro o fuera con destino)")
        if re.search(W["risk_by_number"], line, re.I):
            rep.warn(f"objetivo {num}: cita riesgos por número; usa sus IDs (RS1…) y todas sus correcciones")
    if rep.errors or rep.warnings:
        rep.print()
    return len(rep.errors)


def spec_dirs(root):
    base = os.path.join(root, "docs", "specs")
    if not os.path.isdir(base):
        return []
    return sorted(os.path.join(base, d) for d in os.listdir(base)
                  if re.match(r"^\d{3}-", d) and os.path.isdir(os.path.join(base, d)))


def cmd_validate(args):
    root = find_root(os.getcwd()) or os.getcwd()
    targets = []
    for a in args:
        a = os.path.abspath(a)
        targets.append(os.path.dirname(a) if os.path.isfile(a) else a)
    if not targets:
        targets = spec_dirs(root)
        if not targets:
            print("No hay specs en docs/specs/.")
            return 0
    seen, errors = set(), 0
    nums = {}
    for d in targets:
        if d in seen:
            continue
        seen.add(d)
        rep = validate_spec_dir(d, root)
        rep.print()
        errors += len(rep.errors)
        num = os.path.basename(d)[:3]
        nums.setdefault(num, []).append(os.path.basename(d))
    errors += validate_roadmap(root)
    for num, names in nums.items():
        if len(names) > 1:
            print(f"✗ número de spec repetido {num}: {names}")
            errors += 1
    print(f"\n{len(seen)} spec(s), {errors} error(es).")
    return 1 if errors else 0


# ---------------------------------------------------------------- estado

def next_step(s):
    st = frontmatter(s["spec"]).get("status") if s["spec"] else None
    pst = frontmatter(s["plan"]).get("status") if s["plan"] else None
    tst = frontmatter(s["tasks"]).get("status") if s["tasks"] else None
    verdict = frontmatter(s["review"]).get("verdict") if s["review"] else None
    signoff = frontmatter(s["review"]).get("human_signoff", "") if s["review"] else ""
    if st == "inferred":
        return "validar con /specify --edit"
    if st == "draft":
        return "/clarify y aprobar la spec"
    if st == "approved":
        if not s["plan"]:
            return "/plan"
        if pst == "blocked":
            return "resolver el bloqueo del plan (constitución)"
        if pst != "approved":
            return "aprobar el plan"
        if not s["tasks"]:
            return "/tasks"
        if tst != "approved":
            return "aprobar las tareas"
        ast = analysis_state(s)
        if ast == "stale" and verdict == "changes_requested":
            return "/implement (tareas de /review) y /review --rerun"
        if ast in (None, "stale"):
            return "/analyze" if ast is None else "/analyze (desactualizado)"
        if ast == "fail":
            return "corregir hallazgos de /analyze"
        return "/implement"
    if st == "implemented":
        if not s["review"] or verdict == "changes_requested":
            return "/review" if not s["review"] else "/implement y /review --rerun"
        if verdict == "blocked":
            return "resolver el bloqueo de la review"
        if signoff.startswith("pending"):
            return "firma humana de la review"
        return "/release"
    if st == "released":
        return "—"
    return "revisar spec.md"


def cmd_status(args):
    root = find_root(os.getcwd())
    if not root:
        print("No se encontró .ai/project.yaml (¿se ejecutó /init?).")
        return 1
    rows = []
    for d in spec_dirs(root):
        s = load_spec_dir(d)
        tasks, _ = parse_tasks(s["tasks"]) if s["tasks"] else ({}, [])
        work = [v[0] for t, v in tasks.items() if int(t[1:]) < 90]
        rows.append({
            "spec": s["name"],
            "status": frontmatter(s["spec"]).get("status") if s["spec"] else None,
            "plan": frontmatter(s["plan"]).get("status") if s["plan"] else None,
            "tasks": f"{sum(t['done'] for t in work)}/{len(work)}" if s["tasks"] else None,
            "review": frontmatter(s["review"]).get("verdict") if s["review"] else None,
            "rondas": rounds(s),
            "next": next_step(s),
        })
    if "--json" in args:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return 0
    if not rows:
        print("No hay specs todavía. Siguiente paso: /specify")
        return 0
    cols = ["spec", "status", "plan", "tasks", "review", "rondas", "next"]
    print("| " + " | ".join(cols) + " |")
    print("|" + "---|" * len(cols))
    for r in rows:
        print("| " + " | ".join(str(r[c] or "—") for c in cols) + " |")
    return 0


# ---------------------------------------------------------------- copias, historial y review

KINDS = ("spec.md", "plan.md", "tasks.md")
LOCKFILES = ("package-lock.json", "yarn.lock", "pnpm-lock.yaml", "bun.lockb", "composer.lock", "poetry.lock",
             "Pipfile.lock", "uv.lock", "Cargo.lock", "go.sum", "Gemfile.lock", "packages.lock.json",
             "pubspec.lock")


def spec_arg(args, usage):
    paths = [a for a in args if not a.startswith("--")]
    if not paths:
        print("Uso: aidd.py " + usage)
        return None, None
    d = os.path.abspath(paths[0])
    d = os.path.dirname(d) if os.path.isfile(d) else d
    return d, find_root(d) or os.getcwd()


def opt(args, name):
    if name in args:
        i = args.index(name)
        if i + 1 < len(args):
            return args[i + 1]
    return None


def cmd_snapshot(args):
    d, root = spec_arg(args, "snapshot docs/specs/NNN-slug")
    if not d:
        return 2
    cache = os.path.join(root, ".ai", "cache", "analysis", os.path.basename(d))
    os.makedirs(cache, exist_ok=True)
    for k in KINDS:
        if os.path.isfile(os.path.join(d, k)):
            shutil.copyfile(os.path.join(d, k), os.path.join(cache, k))
    code, head = git(root, "rev-parse", "HEAD")
    with open(os.path.join(cache, "COMMIT"), "w", encoding="utf-8") as f:
        f.write(head.strip() if code == 0 else "")
    print(os.path.relpath(cache, root).replace("\\", "/"))
    return 0


def cmd_changes(args):
    d, root = spec_arg(args, "changes docs/specs/NNN-slug [--since REF]")
    if not d:
        return 2
    since = opt(args, "--since")
    cache = os.path.join(root, ".ai", "cache", "analysis", os.path.basename(d))
    rel = os.path.relpath(d, root).replace("\\", "/")
    old_texts = {}
    if since:
        for k in KINDS:
            code, out = git(root, "show", f"{since}:{rel}/{k}")
            old_texts[k] = out if code == 0 else ""
        print(f"# base: commit {since}")
    else:
        if not os.path.isdir(cache):
            print("Sin copia previa: usa --since <commit del último análisis> o ejecuta un análisis completo.")
            return 3
        for k in KINDS:
            old = os.path.join(cache, k)
            old_texts[k] = read(old) if os.path.isfile(old) else ""
        s = load_spec_dir(d)
        if s["analysis"]:
            afm = frontmatter(s["analysis"])
            cached = {k[:-3] + "_sha": fingerprint(old_texts[k]) for k in KINDS}
            if any(afm.get(k) and afm.get(k) != v for k, v in cached.items()):
                print("# AVISO: la copia guardada no coincide con las huellas de analysis.md; usa "
                      "--since <commit del último análisis>.")
        cf = os.path.join(cache, "COMMIT")
        if os.path.isfile(cf) and read(cf).strip():
            print(f"# base: copia del commit {read(cf).strip()[:10]}")
    total = 0
    for k in KINDS:
        new = os.path.join(d, k)
        a = old_texts[k].splitlines()
        b = read(new).splitlines() if os.path.isfile(new) else []
        diff = list(difflib.unified_diff(a, b, f"anterior/{k}", f"actual/{k}", n=2, lineterm=""))
        if diff:
            total += sum(1 for x in diff if x[:1] in "+-" and x[:3] not in ("+++", "---"))
            print("\n".join(diff))
    print(f"\n# {total} líneas cambiadas desde el último análisis")
    return 0


def cmd_rotate(args):
    d, root = spec_arg(args, "rotate docs/specs/NNN-slug analysis|review|plan|tasks")
    kinds = [a for a in args[1:] if not a.startswith("--")]
    if not d or not kinds or kinds[0] not in ("analysis", "review", "plan", "tasks"):
        print("Uso: aidd.py rotate docs/specs/NNN-slug analysis|review|plan|tasks")
        return 2
    kind = kinds[0]
    src = os.path.join(d, kind + ".md")
    if not os.path.isfile(src):
        print(f"No existe {kind}.md: nada que archivar.")
        return 0
    h = history_dir(d)
    os.makedirs(h, exist_ok=True)
    if kind in ("analysis", "review"):
        n = frontmatter(read(src)).get("round") or "1"
        dst = os.path.join(h, f"{kind}.r{n}.md")
        if os.path.exists(dst):
            print(f"Ya existe {os.path.relpath(dst, root)}: sube 'round' antes de archivar.")
            return 1
        shutil.move(src, dst)
    else:
        n = 1 + sum(1 for f in os.listdir(h) if re.match(r"^" + kind + r"\.v\d+\.md$", f))
        dst = os.path.join(h, f"{kind}.v{n}.md")
        shutil.copyfile(src, dst)
    fix_links(dst, d)
    print(os.path.relpath(dst, root).replace("\\", "/"))
    return 0


def fix_links(moved, d):
    """En un archivo movido a history/, los enlaces relativos suben un nivel (salvo a otras rondas)."""
    text = read(moved)

    def sub(m):
        t = m.group(1)
        if re.match(r"^([a-z]+:|/|#)", t) or ("/" not in t and ROUND_FILE_RE.match(t.split("#")[0])):
            return m.group(0)
        return "](../" + t + ")"

    new = re.sub(r"\]\(([^)\s]+)\)", sub, text)
    if new != text:
        with open(moved, "w", encoding="utf-8", newline="\n") as f:
            f.write(new)


def history_rows(d):
    h = history_dir(d)
    rows = []
    for base in (h, d):
        if not os.path.isdir(base):
            continue
        for f in os.listdir(base):
            m = ROUND_FILE_RE.match(f)
            if not m:
                continue
            text = read(os.path.join(base, f))
            fm = frontmatter(text)
            kind = m.group(1) or m.group(3)
            num = int(m.group(2) or m.group(4))
            cm = re.search(r"Conteo[^:]*:\s*([^\n.]+)", text)
            rows.append({"file": os.path.relpath(os.path.join(base, f), d).replace("\\", "/"), "kind": kind,
                         "n": num, "date": fm.get("date", ""), "mode": fm.get("mode", ""),
                         "result": fm.get("result") or fm.get("verdict") or fm.get("status", ""),
                         "count": (cm.group(1).strip().rstrip(".") if cm else "")})
    s = load_spec_dir(d)
    for kind in ("analysis", "review"):
        if s[kind]:
            fm = frontmatter(s[kind])
            cm = re.search(r"Conteo[^:]*:\s*([^\n.]+)", s[kind])
            rows.append({"file": kind + ".md", "kind": kind, "n": int(fm.get("round") or 1),
                         "date": fm.get("date", ""), "mode": fm.get("mode", ""),
                         "result": fm.get("result") or fm.get("verdict", ""),
                         "count": (cm.group(1).strip().rstrip(".") if cm else "") + " (vigente)"})
    order = {"plan": 0, "tasks": 1, "analysis": 2, "review": 3}
    return sorted(rows, key=lambda r: (order[r["kind"]], r["n"]))


def cmd_history(args):
    d, root = spec_arg(args, "history docs/specs/NNN-slug [--write] [--migrate]")
    if not d:
        return 2
    if "--migrate" in args:
        h = history_dir(d)
        moved = []
        for f in sorted(os.listdir(d)):
            if ROUND_FILE_RE.match(f):
                os.makedirs(h, exist_ok=True)
                if os.path.exists(os.path.join(h, f)):
                    print(f"Ya existe history/{f}; no se mueve.")
                    continue
                shutil.move(os.path.join(d, f), os.path.join(h, f))
                fix_links(os.path.join(h, f), d)
                moved.append(f)
        for f in os.listdir(d):
            if f.endswith(".md") and moved:
                p = os.path.join(d, f)
                text = read(p)
                new = re.sub(r"\]\((" + "|".join(re.escape(m) for m in moved) + r")\)", r"](history/\1)", text)
                if new != text:
                    with open(p, "w", encoding="utf-8", newline="\n") as fh:
                        fh.write(new)
        print(f"Movidos a history/: {moved or 'ninguno'}")
    rows = history_rows(d)
    lines = [f"# Historial · {os.path.basename(d)}", "",
             "Rondas de /analyze y /review y versiones anteriores de plan y tareas. Nunca se borran; "
             "las skills no las leen salvo la ronda inmediatamente anterior.", "",
             "| Archivo | Tipo | N.º | Fecha | Modo | Resultado | Conteo |", "|---|---|---|---|---|---|---|"]
    for r in rows:
        f = r["file"]
        target = f[len("history/"):] if f.startswith("history/") else "../" + f
        lines.append(f"| [{os.path.basename(f)}]({target}) | {r['kind']} | {r['n']} | {r['date']} | {r['mode']} | "
                     f"{r['result']} | {r['count']} |")
    na = sum(1 for r in rows if r["kind"] == "analysis")
    nr = sum(1 for r in rows if r["kind"] == "review")
    lines += ["", f"Total: {na} rondas de /analyze, {nr} de /review."]
    out = "\n".join(lines) + "\n"
    if "--write" in args:
        os.makedirs(history_dir(d), exist_ok=True)
        with open(os.path.join(history_dir(d), "README.md"), "w", encoding="utf-8", newline="\n") as f:
            f.write(out)
        print(os.path.relpath(os.path.join(history_dir(d), "README.md"), root).replace("\\", "/"))
    else:
        print(out)
    return 0


def expand_braces(p):
    m = re.search(r"\{([^{}]*)\}", p)
    if not m:
        return [p]
    return [x for alt in m.group(1).split(",") for x in expand_braces(p[:m.start()] + alt.strip() + p[m.end():])]


def task_paths(tasks_text):
    """Rutas citadas en las tareas (campo de archivos y rutas entre comillas invertidas)."""
    tasks, _ = parse_tasks(tasks_text)
    out = {}
    for tid, vs in tasks.items():
        v = vs[0]
        cands = set(re.findall(r"`([^`\s]+/[^`\s]*|[^`\s]+\.[A-Za-z]{1,5})`", v["text"])) | set(v["files"])
        for c in cands:
            c = c.strip(" `").split(" ")[0]
            if "/" not in c and "." not in c:
                continue
            for e in expand_braces(c):
                out.setdefault(e.lstrip("./"), set()).add(tid)
    return out


def in_scope(f, paths, changed=(), root=None):
    import fnmatch
    hits = set()
    names = [os.path.basename(c) for c in changed]
    for p, tids in paths.items():
        exact = f == p or f.endswith("/" + p) or fnmatch.fnmatch(f, p) or (p.endswith("/") and f.startswith(p))
        # Rutas abreviadas con alias (`ApCtl/X.php`): se aceptan por nombre solo si la ruta citada no
        # existe tal cual y el nombre no se repite entre los cambiados (index.ts, page.tsx…).
        alias = ("." in os.path.basename(p) and os.path.basename(f) == os.path.basename(p)
                 and names.count(os.path.basename(f)) == 1
                 and not (root and os.path.exists(os.path.join(root, p))))
        if exact or alias:
            hits |= tids
    return hits


def impl_base(root, d, s):
    b = frontmatter(s["tasks"] or "").get("impl_base")
    if b:
        return b, "tasks.md → impl_base"
    rel = os.path.relpath(os.path.join(d, "tasks.md"), root).replace("\\", "/")
    code, out = git(root, "log", "--reverse", "--format=%H", "--", rel)
    if code != 0:
        return None, ""
    for h in out.split():
        c, text = git(root, "show", f"{h}:{rel}")
        if c == 0 and frontmatter(text).get("status") == "approved":
            return h[:10], "commit que aprobó tasks.md"
    return None, ""


def cmd_review_pack(args):
    d, root = spec_arg(args, "review-pack docs/specs/NNN-slug [--base REF] [--head REF]")
    if not d:
        return 2
    s = load_spec_dir(d)
    if not s["tasks"]:
        print("La spec no tiene tasks.md.")
        return 2
    base, why = (opt(args, "--base"), "--base") if opt(args, "--base") else impl_base(root, d, s)
    head = opt(args, "--head") or "HEAD"
    if not base:
        print("No se pudo determinar la base: pasa --base <commit en que se aprobaron las tareas>.")
        return 2
    code, _ = git(root, "rev-parse", "--verify", base)
    if code != 0:
        print(f"La base {base} no existe en git.")
        return 2
    rng = f"{base}..{head}"
    excl = [":(exclude)docs", ":(exclude).ai", ":(exclude,glob)**/*.md"] + \
           [f":(exclude,glob)**/{lf}" for lf in LOCKFILES]
    out_dir = os.path.join(root, ".ai", "cache", "review", os.path.basename(d))
    os.makedirs(out_dir, exist_ok=True)
    _, code_diff = git(root, "diff", "-U3", rng, "--", ".", *excl)
    _, names = git(root, "diff", "--name-status", rng, "--", ".", *excl)
    _, docs_stat = git(root, "diff", "--stat=120", rng, "--", "docs", ".ai", "*.md")
    _, locks = git(root, "diff", "--stat=120", rng, "--", *[f":(glob)**/{lf}" for lf in LOCKFILES])
    changed = [ln.split("\t")[-1] for ln in names.splitlines() if ln.strip()]
    paths = task_paths(s["tasks"])
    extra = [f for f in changed if not in_scope(f, paths, changed, root)]
    touched_tids = set()
    for f in changed:
        touched_tids |= in_scope(f, paths, changed, root)
    tasks, _ = parse_tasks(s["tasks"])
    untouched = sorted(t for t, v in tasks.items() if int(t[1:]) < 90 and t not in touched_tids
                       and any("/" in p for p in v[0]["files"]))

    def write(name, text):
        with open(os.path.join(out_dir, name), "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        return len(text.encode("utf-8"))

    sizes = {}
    sizes["code.diff"] = write("code.diff", code_diff)
    sizes["docs.stat"] = write("docs.stat", docs_stat or "(sin cambios de documentación)\n")
    sizes["deps.stat"] = write("deps.stat", locks or "(sin cambios en lockfiles)\n")
    scope = [f"# Alcance · {os.path.basename(d)} · {rng}", "",
             f"Base: {base} ({why}). Archivos de código cambiados: {len(changed)}.", "",
             "## Cambiados sin tarea que los cite (candidatos a alcance extra; verificar)", ""]
    scope += [f"- {f}" for f in extra] or ["- ninguno"]
    scope += ["", "## Tareas con rutas que no aparecen en el diff (¿sin implementar o solo docs?)", ""]
    scope += [f"- {t}" for t in untouched] or ["- ninguna"]
    scope += ["", "## Archivos cambiados", "", "```", names.strip(), "```"]
    sizes["scope.md"] = write("scope.md", "\n".join(scope) + "\n")
    cas = [ln.strip() for ln in (section(body(s["spec"] or ""), "criteria") or "").splitlines()
           if CA_DEF_RE.match(ln)]
    ctx = [f"# Contexto · {os.path.basename(d)}", "", "## Criterios de aceptación", ""] + cas
    for key in ("threat_model", "traceability", "observability"):
        sec = section(body(s["plan"] or ""), key)
        if sec:
            ctx += ["", "## " + VOCAB[key][0] + " (plan)", sec.strip()]
    sizes["context.md"] = write("context.md", "\n".join(ctx) + "\n")
    print(f"Paquete de review en {os.path.relpath(out_dir, root)}  (rango {rng}; base: {why})")
    for k, v in sizes.items():
        print(f"  {k:12} {v / 1024:8.1f} KB  ≈ {v // 4 // 1000}k tokens")
    print(f"  alcance: {len(changed)} archivos de código, {len(extra)} sin tarea, {len(untouched)} tareas sin diff")
    return 0


# ---------------------------------------------------------------- hook

DOC_PREFIXES = ("docs/", ".ai/")
DEFAULT_PROTECTED = (".git/hooks/", ".github/workflows/", ".gitlab-ci.yml", "azure-pipelines.yml",
                     "bitbucket-pipelines.yml", ".circleci/", ".claude/")
DEP_ADD_RE = re.compile(
    r"\b(npm\s+(i|install|add)\s+(?!-)[^\s-]|pnpm\s+(add|i|install)\s+(?!-)\S|yarn\s+add\s|bun\s+add\s|"
    r"pip3?\s+install\s+(?!-r\b|-e\b|\.)[^\s-]|uv\s+(add|pip\s+install)\s|poetry\s+add\s|pipenv\s+install\s+\S|"
    r"cargo\s+add\s|go\s+get\s|gem\s+install\s|composer\s+require\s|dotnet\s+add\s+\S+\s+package\s|"
    r"dotnet\s+add\s+package\s)")
DANGER_RE = [
    (re.compile(r"(curl|wget)[^|;&]*\|\s*(sudo\s+)?(ba|z)?sh\b"), "ejecuta un script remoto (curl | sh)"),
    (re.compile(r"\bsudo\b"), "usa sudo"),
    (re.compile(r"\bgit\s+push\b[^;&|]*(--force\b|\s-f\b|--force-with-lease\b)"), "hace force push"),
    (re.compile(r"\bgit\s+reset\s+--hard\b"), "descarta cambios con git reset --hard"),
    (re.compile(r"\b(DROP|TRUNCATE)\s+(TABLE|DATABASE|SCHEMA)\b", re.I), "borra datos (DROP/TRUNCATE)"),
]


def decide(decision, reason):
    if decision == "deny":
        sys.stderr.write("[ai-dd] " + reason + "\n")
        return 2
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": decision,
        "permissionDecisionReason": "[ai-dd] " + reason}}, ensure_ascii=False))
    return 0


def active_spec(root):
    for d in spec_dirs(root):
        s = load_spec_dir(d)
        if not (s["spec"] and s["tasks"]):
            continue
        if frontmatter(s["spec"]).get("status") == "approved" and frontmatter(s["tasks"]).get("status") == "approved":
            return os.path.basename(d)
    return None


SIGNING_EXT = (".keystore", ".jks", ".p12", ".p8", ".mobileprovision")


def is_protected(rel, extra):
    base = os.path.basename(rel)
    if base.startswith(".env") and base not in (".env.example", ".env.sample", ".env.template"):
        return True
    if base.lower().endswith(SIGNING_EXT) or base == "key.properties":
        return True  # claves de firma (Android/iOS)
    for p in DEFAULT_PROTECTED + tuple(extra):
        p = p.replace("\\", "/")
        if rel == p.rstrip("/") or rel.startswith(p if p.endswith("/") else p + "/") or rel == p:
            return True
    return False


def cmd_hook(args):
    if not args or args[0] != "pre-tool":
        return 0
    if os.environ.get("AIDD_ALLOW") == "1":
        return 0
    try:
        raw = sys.stdin.buffer.read() if hasattr(sys.stdin, "buffer") else sys.stdin.read().encode("utf-8")
        event = json.loads(raw.decode("utf-8-sig") or "{}")
    except ValueError:
        return 0
    root = find_root(event.get("cwd") or os.getcwd())
    if not root:
        return 0  # no es un proyecto ai-dd
    cfg = read(os.path.join(root, ".ai", "project.yaml"))
    mode = (yaml_scalar(cfg, "enforcement") or "warn").lower()
    if mode == "off":
        return 0
    soft = "deny" if mode == "block" else "ask"
    tool = event.get("tool_name", "")
    tin = event.get("tool_input", {}) or {}

    if tool == "Bash":
        cmd = tin.get("command", "")
        for rx, what in DANGER_RE:
            if rx.search(cmd):
                return decide("ask", f"El comando {what}. Requiere aprobación explícita (shared/agent-security.md §3).")
        if DEP_ADD_RE.search(cmd):
            return decide("ask", "El comando añade una dependencia. Verifica antes que el paquete existe, su "
                                 "antigüedad, reputación y licencia (shared/agent-security.md §2) y que el plan lo aprobó.")
        return 0

    path = tin.get("file_path") or tin.get("notebook_path")
    if not path:
        return 0
    try:
        rel = os.path.relpath(os.path.abspath(path), root).replace("\\", "/")
    except ValueError:
        return 0
    if rel.startswith(".."):
        return 0
    if is_protected(rel, yaml_list(cfg, "protected_paths")):
        return decide(soft, f"'{rel}' es una ruta protegida (shared/agent-security.md §4). Solo con aprobación "
                            "explícita y una tarea aprobada que lo indique.")
    if rel.startswith(DOC_PREFIXES) or rel.lower().endswith(".md"):
        return 0
    if active_spec(root):
        return 0
    return decide(soft, f"Se va a editar código ('{rel}') sin ninguna spec con tasks.md aprobado. "
                        "El flujo pide /specify → /plan → /tasks antes de implementar. Si es un cambio "
                        "menor fuera del flujo, apruébalo explícitamente.")


# ---------------------------------------------------------------- main

def force_utf8():
    """En Windows la consola suele usar cp1252: sin esto, ✓/✗/→ y los acentos rompen la salida."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass


def main(argv):
    force_utf8()
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__)
        return 0
    cmd, args = argv[1], argv[2:]
    if cmd == "--version":
        print(VERSION)
        return 0
    if cmd == "validate":
        return cmd_validate(args)
    if cmd == "status":
        return cmd_status(args)
    if cmd == "hash":
        if not args:
            print("Uso: aidd.py hash docs/specs/NNN-slug")
            return 2
        d = os.path.abspath(args[0])
        d = os.path.dirname(d) if os.path.isfile(d) else d
        for k, v in fingerprints(load_spec_dir(d)).items():
            print(f"{k}: {v}")
        return 0
    if cmd == "snapshot":
        return cmd_snapshot(args)
    if cmd == "changes":
        return cmd_changes(args)
    if cmd == "rotate":
        return cmd_rotate(args)
    if cmd == "history":
        return cmd_history(args)
    if cmd == "review-pack":
        return cmd_review_pack(args)
    if cmd == "hook":
        try:
            return cmd_hook(args)
        except Exception as exc:  # un fallo del hook nunca debe bloquear el trabajo
            sys.stderr.write(f"[ai-dd] hook: error interno ignorado: {exc}\n")
            return 0
    print(f"Comando desconocido: {cmd}\n")
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
