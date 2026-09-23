#!/usr/bin/env python3
"""ai-dd: validadores deterministas del flujo, índice de estado y hook de guardia.

Uso:
  aidd.py validate [RUTA ...]      Valida specs (carpetas docs/specs/NNN-slug o archivos).
                                   Sin rutas valida todas. Código de salida 1 si hay errores.
  aidd.py status [--json]          Estado de todas las specs y siguiente paso sugerido.
  aidd.py hook pre-tool            Hook PreToolUse: lee el evento JSON por stdin.

Solo usa la biblioteca estándar de Python 3.8+. Se copia a cada proyecto como .ai/bin/aidd.py
para que CI pueda ejecutarlo sin el plugin.
"""
import json
import os
import re
import sys

VERSION = "1.4.0"

SPEC_STATES = {"draft", "inferred", "approved", "implemented", "released"}
PLAN_STATES = {"draft", "approved", "blocked"}
TASKS_STATES = {"draft", "approved"}
VERDICTS = {"approved", "changes_requested", "blocked"}
FIXED_TASKS = ["T090", "T091", "T092", "T095", "T096", "T097", "T098"]
DEPLOY_TASKS = {"T095", "T096", "T097", "T098"}

TASK_RE = re.compile(r"^\s*- \[( |x|X)\] (T\d{3})\b(.*)$")
CA_DEF_RE = re.compile(r"^\s*- \[( |x|X)\] (CA\d+)\b(.*)$")
PLACEHOLDER_RE = re.compile(r"\{\{[^}]*\}\}")
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)


# ---------------------------------------------------------------- utilidades

def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


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
    """Contenido de la sección '## <title>' hasta la siguiente '## '."""
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
    for kind in ("spec", "plan", "tasks", "review"):
        p = os.path.join(d, kind + ".md")
        spec[kind] = read(p) if os.path.isfile(p) else None
    return spec


def spec_cas(spec_text):
    sec = section(body(spec_text), "Criterios de aceptación") or ""
    cas = []
    for line in sec.splitlines():
        m = CA_DEF_RE.match(line)
        if m:
            cas.append((m.group(2), m.group(1).lower() == "x", "(abuso)" in line))
    return cas


def plan_threats(plan_text):
    sec = section(body(plan_text), "Modelo de amenazas") or ""
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
        deps = re.findall(r"T\d{3}", (re.search(r"depende:\s*([^—]*)", rest) or [None, ""])[1] or "")
        covers = re.findall(r"CA\d+", (re.search(r"cubre:\s*([^—]*)", rest) or [None, ""])[1] or "")
        files = parts[1] if len(parts) > 1 else ""
        tasks.setdefault(tid, []).append({
            "id": tid,
            "done": m.group(1).lower() == "x",
            "parallel": rest.lstrip().startswith("[P]"),
            "text": rest,
            "files": [f.strip(" `") for f in re.split(r",\s*", files) if f.strip()],
            "deps": deps,
            "covers": covers,
            "has_done_when": "hecho cuando:" in rest,
        })
        order.append(tid)
    return tasks, order


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
    if not cas:
        rep.err("spec: no hay criterios de aceptación numerados (CA1, CA2…)")
    dup = {i for i in ids if ids.count(i) > 1}
    if dup:
        rep.err(f"spec: criterios duplicados {sorted(dup)}")
    pending_q = len(re.findall(r"\[NECESITA ACLARACIÓN\]", text))
    if pending_q > 3:
        rep.err(f"spec: {pending_q} marcadores [NECESITA ACLARACIÓN] (máximo 3)")
    if st in {"approved", "implemented", "released"} and pending_q:
        rep.err("spec: aprobada con [NECESITA ACLARACIÓN] abiertos")
    for title in ("Problema", "Criterios de aceptación", "Fuera de alcance"):
        if section(body(s["spec"]), title) is None:
            rep.err(f"spec: falta la sección '{title}'")
    sec_sec = section(body(s["spec"]), "Seguridad y privacidad")
    if sec_sec is None:
        (rep.warn if st == "inferred" else rep.err)("spec: falta la sección 'Seguridad y privacidad'")
    elif "no aplica" not in sec_sec.lower() and not any(c[2] for c in cas):
        rep.warn("spec: la sección de seguridad no dice 'No aplica' y no hay criterios '(abuso)'")
    if st in {"implemented", "released"}:
        open_cas = [c[0] for c in cas if not c[1]]
        if open_cas:
            rep.err(f"spec: estado {st} con criterios sin marcar {sorted(set(open_cas))}")

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
        cc = section(body(ptext), "Constitution Check") or ""
        if principles is not None:
            missing = [p for p in principles if not re.search(r"\b" + p + r"\b", cc)]
            if missing:
                rep.err(f"plan: Constitution Check no evalúa {missing}")
        for line in cc.splitlines():
            if "❌" in line and "aceptado" not in line and pst == "approved":
                rep.err("plan: aprobado con un ❌ sin aceptación registrada")
        trace = section(body(ptext), "Trazabilidad")
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
        if section(body(ptext), "Modelo de amenazas") is None:
            rep.warn("plan: no tiene sección 'Modelo de amenazas'")
        if section(body(ptext), "Rollout") is None:
            rep.err("plan: falta la sección 'Rollout'")

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
    elif st in {"implemented", "released"}:
        rep.err(f"spec {st} sin tasks.md")

    # --- review
    if s["review"]:
        rfm = frontmatter(s["review"])
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
        if not os.path.isfile(os.path.join(s["dir"], "analysis.md")):
            return "/analyze"
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
            "next": next_step(s),
        })
    if "--json" in args:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return 0
    if not rows:
        print("No hay specs todavía. Siguiente paso: /specify")
        return 0
    cols = ["spec", "status", "plan", "tasks", "review", "next"]
    print("| " + " | ".join(cols) + " |")
    print("|" + "---|" * len(cols))
    for r in rows:
        print("| " + " | ".join(str(r[c] or "—") for c in cols) + " |")
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


def is_protected(rel, extra):
    base = os.path.basename(rel)
    if base.startswith(".env") and base not in (".env.example", ".env.sample", ".env.template"):
        return True
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
        event = json.loads(sys.stdin.read() or "{}")
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

def main(argv):
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
