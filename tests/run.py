#!/usr/bin/env python3
"""Pruebas del validador y del script sobre proyectos que no se parecen entre sí.

Uso: python tests/run.py            (desde la raíz del plugin; solo biblioteca estándar)

Cada carpeta de tests/fixtures/ es un proyecto mínimo de un tipo, stack e idioma distintos con su
expected.json: número exacto de errores y fragmentos que deben aparecer en errores o avisos. Los
escenarios de abajo prueban review-pack, history/rotate y el hook con repos git temporales.
Todo cambio del plugin que salga de un proyecto real debe seguir pasando aquí.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
AIDD = os.path.join(os.path.dirname(HERE), "scripts", "aidd.py")
FAILS = []

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass


def run(args, cwd, stdin=None):
    p = subprocess.run([sys.executable, AIDD] + args, cwd=cwd, input=stdin, capture_output=True,
                       env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    return p.returncode, p.stdout.decode("utf-8", "replace") + p.stderr.decode("utf-8", "replace")


def check(name, cond, detail=""):
    print(("  ok   " if cond else "  FAIL ") + name)
    if not cond:
        FAILS.append(name)
        if detail:
            print("       " + detail.replace("\n", "\n       "))


def git(cwd, *args):
    subprocess.run(["git", "-c", "user.email=t@t", "-c", "user.name=t"] + list(args), cwd=cwd,
                   check=True, capture_output=True)


def fixtures():
    print("Proyectos de prueba:")
    base = os.path.join(HERE, "fixtures")
    for name in sorted(os.listdir(base)):
        src = os.path.join(base, name)
        exp = json.load(open(os.path.join(src, "expected.json"), encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            dst = os.path.join(tmp, name)
            shutil.copytree(src, dst)
            _, out = run(["validate"], dst)
        errors = [l for l in out.splitlines() if "error:" in l or l.startswith("✗ número")]
        warns = [l for l in out.splitlines() if "aviso:" in l]
        check(f"{name}: {exp['errors']} error(es)", len(errors) == exp["errors"], out)
        for frag in exp.get("contains", []):
            check(f"{name}: error '{frag}'", any(frag in e for e in errors), out)
        for frag in exp.get("warnings_contains", []):
            check(f"{name}: aviso '{frag}'", any(frag in w for w in warns), out)
        for frag in exp.get("warnings_not_contains", []):
            check(f"{name}: sin aviso ni error '{frag}'", not any(frag in x for x in warns + errors), out)
        if exp["errors"] == 0 and "warnings_contains" in exp and not exp["warnings_contains"]:
            check(f"{name}: sin avisos", not warns, out)


def scenario_review_pack():
    print("review-pack (rutas con el mismo nombre, alias, docs fuera del diff):")
    with tempfile.TemporaryDirectory() as tmp:
        for d in (".ai", "docs/specs/001-x", "app/login", "app/admin", "src/Controllers"):
            os.makedirs(os.path.join(tmp, d))
        open(os.path.join(tmp, ".ai/project.yaml"), "w", encoding="utf-8").write("type: frontend\n")
        open(os.path.join(tmp, "docs/specs/001-x/spec.md"), "w", encoding="utf-8").write(
            "---\nstatus: approved\n---\n## Criterios de aceptación\n- [x] CA1 x\n")
        open(os.path.join(tmp, "docs/specs/001-x/tasks.md"), "w", encoding="utf-8").write(
            "---\nstatus: approved\n---\n"
            "- [x] T001 a — `app/login/page.tsx` — hecho cuando: y — cubre: CA1\n"
            "- [x] T002 b — `Ctl/SaveThingController.php` — hecho cuando: y — cubre: CA1\n")
        for f in ("app/login/page.tsx", "app/admin/page.tsx", "src/Controllers/SaveThingController.php"):
            open(os.path.join(tmp, f), "w", encoding="utf-8").write("a\n")
        git(tmp, "init", "-q")
        git(tmp, "add", "-A")
        git(tmp, "commit", "-qm", "base")
        for f in ("app/login/page.tsx", "app/admin/page.tsx", "src/Controllers/SaveThingController.php",
                  "docs/specs/001-x/spec.md"):
            open(os.path.join(tmp, f), "a", encoding="utf-8").write("b\n")
        git(tmp, "commit", "-qam", "change")
        code, out = run(["review-pack", "docs/specs/001-x", "--base", "HEAD~1"], tmp)
        check("review-pack termina sin error", code == 0, out)
        if code != 0:
            return
        scope = open(os.path.join(tmp, ".ai/cache/review/001-x/scope.md"), encoding="utf-8").read()
        extra = scope.split("## Cambiados sin tarea")[1].split("## Tareas")[0]
        check("admin/page.tsx no se da por cubierto por login/page.tsx", "app/admin/page.tsx" in extra, scope)
        check("alias Ctl/…Controller.php cubre la ruta real", "SaveThingController" not in extra, scope)
        diff = open(os.path.join(tmp, ".ai/cache/review/001-x/code.diff"), encoding="utf-8").read()
        check("docs/ queda fuera del diff de código", "spec.md" not in diff and "page.tsx" in diff)


def scenario_review_pack_generated():
    print("review-pack (rutas con punto, código generado por comando, --base en un rerun):")
    with tempfile.TemporaryDirectory() as tmp:
        for d in (".ai", "docs/specs/001-x", "gen/proto", "svc"):
            os.makedirs(os.path.join(tmp, d))
        open(os.path.join(tmp, ".ai/project.yaml"), "w", encoding="utf-8").write("type: backend\nlanguage: en\n")
        open(os.path.join(tmp, "docs/specs/001-x/spec.md"), "w", encoding="utf-8").write(
            "---\nstatus: approved\n---\n## Acceptance criteria\n- [x] AC1 x\n")
        tasks = ("---\nstatus: approved\n---\n"
                 "- [x] T001 a — .pre-commit-config.yaml, .golangci.yml — done when: y\n"
                 "- [x] T002 b — gen/ (generated by `buf generate`) — done when: y\n"
                 "- [x] T003 c — gen/proto/api.pb.go, svc/server.go — done when: y — covers: AC1\n")
        open(os.path.join(tmp, "docs/specs/001-x/tasks.md"), "w", encoding="utf-8").write(tasks)
        open(os.path.join(tmp, "svc/server.go"), "w", encoding="utf-8").write("package svc\n")
        git(tmp, "init", "-q")
        git(tmp, "add", "-A")
        git(tmp, "commit", "-qm", "base")
        for f in (".pre-commit-config.yaml", ".golangci.yml", "gen/proto/api.pb.go", "gen/proto/other.pb.go",
                  "gen/proto/third.pb.go", "svc/server.go"):
            open(os.path.join(tmp, f), "a", encoding="utf-8").write("// generated-or-not\n")
        git(tmp, "add", "-A")
        git(tmp, "commit", "-qm", "impl")
        code, out = run(["review-pack", "docs/specs/001-x", "--base", "HEAD~1"], tmp)
        check("review-pack termina sin error", code == 0, out)
        if code != 0:
            return
        cache = os.path.join(tmp, ".ai/cache/review/001-x")
        scope = open(os.path.join(cache, "scope.md"), encoding="utf-8").read()
        extra = scope.split("## Cambiados sin tarea")[1].split("## ")[0]
        check("rutas que empiezan por punto se reconocen", ".pre-commit-config.yaml" not in extra
              and ".golangci.yml" not in extra, scope)
        diff = open(os.path.join(cache, "code.diff"), encoding="utf-8").read()
        check("lo generado por comando queda fuera de code.diff", "other.pb.go" not in diff, diff[:400])
        check("un archivo generado que cita una tarea sí entra", "api.pb.go" in diff and "server.go" in diff)
        check("scope.md lista lo generado", "gen/: 3 archivos" in scope, scope)
        # rerun: una tarea nueva (añadida por /review) sin diff, y las anteriores no cuentan
        open(os.path.join(tmp, "docs/specs/001-x/tasks.md"), "a", encoding="utf-8").write(
            "- [ ] T004 d — svc/limits.go — done when: y — covers: AC1\n")
        git(tmp, "commit", "-qam", "review tasks")
        code, out = run(["review-pack", "docs/specs/001-x", "--base", "HEAD~1"], tmp)
        scope = open(os.path.join(cache, "scope.md"), encoding="utf-8").read()
        untouched = scope.split("## Tareas con rutas")[1].split("## ")[0]
        check("--base: solo cuentan las tareas nuevas", "T004" in untouched and "T003" not in untouched, scope)


def scenario_status():
    print("status (siguiente paso):")
    with tempfile.TemporaryDirectory() as tmp:
        d = os.path.join(tmp, "docs/specs/001-x")
        os.makedirs(d)
        os.makedirs(os.path.join(tmp, ".ai"))
        open(os.path.join(tmp, ".ai/project.yaml"), "w", encoding="utf-8").write("type: library\nlanguage: en\n")
        w = lambda f, t: open(os.path.join(d, f), "w", encoding="utf-8").write(t)
        w("spec.md", "---\nstatus: approved\n---\n## Acceptance criteria\n- [ ] AC1 x\n")
        w("plan.md", "---\nstatus: approved\n---\n")
        w("tasks.md", "---\nstatus: draft\n---\n- [ ] T001 a — x.py — done when: y — covers: AC1\n")
        w("analysis.md", "---\nresult: fail\nround: 1\n---\n")
        _, out = run(["status", "--json"], tmp)
        _, h = run(["hash", "docs/specs/001-x"], tmp)
        fm = "".join(f"{l}\n" for l in h.strip().splitlines())
        w("analysis.md", "---\nresult: fail\nround: 1\n" + fm + "---\n")
        _, out = run(["status", "--json"], tmp)
        check("análisis fail con tareas en draft → corregir hallazgos", "corregir hallazgos" in out, out)
        w("spec.md", "---\nstatus: implemented\n---\n## Acceptance criteria\n- [x] AC1 x\n")
        w("tasks.md", "---\nstatus: approved\n---\n- [x] T001 a — x.py — done when: y — covers: AC1\n"
                      "- [x] T090 a\n- [x] T091 b\n- [x] T092 c\n- [ ] T095 d\n")
        w("review.md", "---\nverdict: changes_requested\nround: 1\n---\n")
        _, out = run(["status", "--json"], tmp)
        check("review con cambios y sin tareas abiertas → /review --rerun",
              '"next": "/review --rerun"' in out, out)
        os.remove(os.path.join(d, "review.md"))
        w("spec.md", "---\nstatus: approved\n---\n## Acceptance criteria\n- [ ] AC1 x\n")
        w("tasks.md", "---\nstatus: approved\n---\n"
                      "- [-] T001 old — x.py — done when: y — covers: AC1 — obsolete: replaced by T002 (2026-10-02)\n"
                      "- [ ] T002 a — x.py — done when: y — covers: AC1\n"
                      "  - blocked: 2026-10-02 — bytes or characters — /plan 001 --fix\n")
        _, h = run(["hash", "docs/specs/001-x"], tmp)
        w("analysis.md", "---\nresult: pass\nround: 2\n" + "".join(f"{l}\n" for l in h.strip().splitlines()) + "---\n")
        _, out = run(["status", "--json"], tmp)
        check("tarea bloqueada → status propone la skill del bloqueo",
              '"next": "T002 bloqueada: /plan 001 --fix"' in out, out)
        check("las tareas obsoletas no cuentan en el progreso", '"tasks": "0/1"' in out, out)


def scenario_history():
    print("history / rotate:")
    with tempfile.TemporaryDirectory() as tmp:
        d = os.path.join(tmp, "docs/specs/001-x")
        os.makedirs(d)
        os.makedirs(os.path.join(tmp, ".ai"))
        open(os.path.join(tmp, ".ai/project.yaml"), "w", encoding="utf-8").write("type: backend\n")
        open(os.path.join(d, "analysis.r1.md"), "w", encoding="utf-8").write("---\nround: 1\nresult: fail\n---\n[x](../../x.md)\n")
        open(os.path.join(d, "analysis.md"), "w", encoding="utf-8").write("---\nround: 2\nresult: pass\n---\n[r1](analysis.r1.md)\n")
        run(["history", "docs/specs/001-x", "--migrate", "--write"], tmp)
        check("la ronda suelta pasa a history/", os.path.isfile(os.path.join(d, "history/analysis.r1.md")))
        check("el enlace del vigente apunta a history/",
              "](history/analysis.r1.md)" in open(os.path.join(d, "analysis.md"), encoding="utf-8").read())
        check("los enlaces relativos del archivado suben un nivel",
              "](../../../x.md)" in open(os.path.join(d, "history/analysis.r1.md"), encoding="utf-8").read())
        run(["rotate", "docs/specs/001-x", "analysis"], tmp)
        check("rotate mueve la ronda vigente", os.path.isfile(os.path.join(d, "history/analysis.r2.md"))
              and not os.path.exists(os.path.join(d, "analysis.md")))
        check("history/README.md existe", os.path.isfile(os.path.join(d, "history/README.md")))


def scenario_encoding():
    print("codificación (archivos guardados en ANSI/cp1252 en Windows):")
    with tempfile.TemporaryDirectory() as tmp:
        d = os.path.join(tmp, "docs/specs/001-x")
        os.makedirs(d)
        os.makedirs(os.path.join(tmp, ".ai"))
        open(os.path.join(tmp, ".ai/project.yaml"), "w", encoding="utf-8").write("type: backend\n")
        spec = ("---\nstatus: draft\n---\n## Problema\nx\n## Criterios de aceptación\n- [ ] CA1 Sesión\n"
                "## Fuera de alcance\nx\n## Seguridad y privacidad\nNo aplica.\n")
        open(os.path.join(d, "spec.md"), "w", encoding="cp1252").write(spec)
        code, out = run(["validate"], tmp)
        check("spec en cp1252 se valida sin errores", code == 0 and "0 error(es)" in out, out)
        open(os.path.join(d, "spec.md"), "w", encoding="utf-8-sig").write(spec)
        code, out = run(["validate"], tmp)
        check("spec en UTF-8 con BOM se valida sin errores", code == 0 and "0 error(es)" in out, out)


def scenario_hook():
    print("hook:")
    with tempfile.TemporaryDirectory() as tmp:
        os.makedirs(os.path.join(tmp, ".ai"))
        open(os.path.join(tmp, ".ai/project.yaml"), "w", encoding="utf-8").write("type: mobile\nworkflow:\n  enforcement: warn\n")

        def hook(ev):
            ev["cwd"] = tmp
            return run(["hook", "pre-tool"], tmp, json.dumps(ev).encode())[1]

        for f in ("android/app/release.keystore", "ios/dist.p12", "android/key.properties", ".env"):
            out = hook({"tool_name": "Write", "tool_input": {"file_path": os.path.join(tmp, f)}})
            check(f"protege {f}", "ruta protegida" in out, out)
        out = hook({"tool_name": "Write", "tool_input": {"file_path": os.path.join(tmp, ".env.example")}})
        check(".env.example no es ruta protegida", "ruta protegida" not in out, out)
        out = hook({"tool_name": "Edit", "tool_input": {"file_path": os.path.join(tmp, "src/app/app.ts")}})
        check("editar código sin spec activa pide aprobación", "sin ninguna spec" in out, out)
        out = hook({"tool_name": "Bash", "tool_input": {"command": "npm install left-padd"}})
        check("añadir dependencia pide verificación", "añade una dependencia" in out, out)
        out = hook({"tool_name": "Bash", "tool_input": {"command": "npx cap sync"}})
        check("comandos normales pasan", out.strip() == "", out)
        for f in ("AGENTS.md", "CLAUDE.md"):
            out = hook({"tool_name": "Edit", "tool_input": {"file_path": os.path.join(tmp, f),
                                                            "old_string": "a", "new_string": "b"}})
            check(f"{f} pide aprobación", "instrucciones del agente" in out and '"ask"' in out, out)
        out = hook({"tool_name": "Edit", "tool_input": {"file_path": os.path.join(tmp, "pyproject.toml"),
                    "old_string": "dependencies = [\n]", "new_string": "dependencies = [\n]\nhttpx-utils = \"0.3.1\""}})
        check("añadir una dependencia editando el manifiesto pide verificación", "dependencias" in out, out)
        out = hook({"tool_name": "Edit", "tool_input": {"file_path": os.path.join(tmp, "pyproject.toml"),
                    "old_string": 'version = "0.1.0"', "new_string": 'version = "0.2.0"'}})
        check("subir la versión del propio paquete no cuenta como dependencia", "dependencias" not in out, out)
        out = hook({"tool_name": "Write", "tool_input": {"file_path": os.path.join(tmp, "go.mod"),
                    "content": "module x\n\ngo 1.22\n\nrequire github.com/acme/yaml v1.4.0\n"}})
        check("escribir go.mod con require pide verificación", "dependencias" in out, out)
        out = hook({"tool_name": "Edit", "tool_input": {"file_path": os.path.join(tmp, "requirements.txt"),
                    "old_string": "flask==3.0.0", "new_string": "flask==3.0.0\nrequestz"}})
        check("añadir una línea sin versión a requirements.txt pide verificación", "dependencias" in out, out)
        out = hook({"tool_name": "Edit", "tool_input": {"file_path": os.path.join(tmp, "Gemfile"),
                    "old_string": "", "new_string": 'gem "railz", "~> 7.1"'}})
        check("añadir una gema pide verificación", "dependencias" in out, out)
    with tempfile.TemporaryDirectory() as tmp:
        os.makedirs(os.path.join(tmp, ".ai"))
        open(os.path.join(tmp, ".ai/project.yaml"), "w", encoding="utf-8").write(
            "type: backend\nworkflow:\n  enforcement: block\n")
        ev = {"tool_name": "Edit", "cwd": tmp, "tool_input": {"file_path": os.path.join(tmp, "package.json"),
              "old_string": "{", "new_string": '{\n  "left-padd": "1.0.0",'}}
        code, out = run(["hook", "pre-tool"], tmp, json.dumps(ev).encode())
        check("modo block sin spec activa: añadir dependencia en el manifiesto se deniega", code == 2, out)
        ev = {"tool_name": "Edit", "cwd": tmp, "tool_input": {"file_path": os.path.join(tmp, "AGENTS.md"),
              "old_string": "a", "new_string": "b"}}
        code, out = run(["hook", "pre-tool"], tmp, json.dumps(ev).encode())
        check("modo block: AGENTS.md pregunta (no deniega, /init lo escribe)", code == 0 and '"ask"' in out, out)


def scenario_design_templates():
    print("plantillas de diseño:")
    base = os.path.join(os.path.dirname(HERE), "skills", "init", "templates", "design")
    html = open(os.path.join(base, "option.html"), encoding="utf-8").read()
    import re as _re
    ext = _re.findall(r"""(?:src|href)\s*=\s*["'](?:https?:)?//[^"']+|@import|url\(\s*["']?(?:https?:)?//""", html)
    check("option.html no carga nada externo (se abre sin red)", not ext, str(ext))
    check("option.html calcula el contraste en la página", "function ratio" in html or "const ratio" in html)
    for name in ("system.md", "brief.md", "creative-direction.md", "anti-cliches.md", "option.html"):
        check(f"existe templates/design/{name}", os.path.isfile(os.path.join(base, name)))


def scenario_closed_specs():
    print("specs cerradas, enmiendas y riesgos citados en Rollout:")
    with tempfile.TemporaryDirectory() as tmp:
        os.makedirs(os.path.join(tmp, ".ai"))
        os.makedirs(os.path.join(tmp, "docs"))
        open(os.path.join(tmp, ".ai/project.yaml"), "w", encoding="utf-8").write("type: mobile\nlanguage: en\n")
        open(os.path.join(tmp, "docs/constitution.md"), "w", encoding="utf-8").write(
            "---\nversion: 1.1.0\n---\n### P1 Tests first\n### P2 Only design tokens\n"
            "## Amendments\n| Version | Date | Change | Reason |\n|---|---|---|---|\n"
            "| 1.0.0 | 2026-01-01 | Initial | /init |\n| 1.1.0 | 2026-02-01 | P2 added (MINOR) | /init --upgrade |\n")
        open(os.path.join(tmp, "docs/deployment.md"), "w", encoding="utf-8").write(
            "## Known risks\n### RD1 · High — No kill switch\n- RD1.a Staged rollout\n- RD1.b Hotfix path\n")

        def spec(num, status, plan_fm, plan_extra=""):
            d = os.path.join(tmp, f"docs/specs/{num}-x")
            os.makedirs(d)
            mark = "x" if status in ("implemented", "released") else " "
            open(os.path.join(d, "spec.md"), "w", encoding="utf-8").write(
                f"---\nstatus: {status}\n---\n## Problem\nx\n## Acceptance criteria\n- [{mark}] AC1 x\n"
                "## Out of scope\nNothing\n## Security and privacy\nNot applicable\n")
            if status == "implemented":
                open(os.path.join(d, "tasks.md"), "w", encoding="utf-8").write(
                    "---\nstatus: approved\n---\n- [x] T001 a — x.py — done when: y — covers: AC1\n"
                    "- [x] T090 a\n- [x] T091 b\n- [x] T092 c\n- [ ] T095 d\n")
            open(os.path.join(d, "plan.md"), "w", encoding="utf-8").write(
                f"---\nstatus: approved\n{plan_fm}---\n## Constitution Check\n| Principle | Result |\n|---|---|\n"
                "| P1 | ✅ |\n## Threat model\nNone\n## Traceability\nAC1 → test\n"
                "## Rollout\nRollback per RD1 (context only).\n" + plan_extra)

        spec("001", "implemented", "constitution_version: 1.0.0\n")
        spec("002", "approved", "")
        spec("003", "implemented", "")
        spec("004", "approved", "constitution_version: 1.0.0\n", "## Risks\nRD1 mitigated by staged rollout\n")
        _, out = run(["validate"], tmp)
        block = lambda n: out.split(f"docs/specs/{n}-x", 1)[1].split("docs/specs/", 1)[0]
        check("plan con constitution_version anterior: no se le exige el principio añadido después",
              "P2" not in block("001"), out)
        check("plan sin constitution_version en spec abierta: exige todos los principios",
              "error: plan: Constitution Check no evalúa ['P2']" in block("002"), out)
        check("plan sin constitution_version en spec cerrada: aviso heredado, no error",
              "no evalúa" not in block("003") and "heredado" in block("003"), out)
        check("riesgo citado solo en Rollout: sin aviso", "RD1" not in block("001") + block("002"), out)
        check("riesgo declarado fuera de Rollout: aviso", "cita ['RD1']" in block("004"), out)
        _, out = run(["validate", "--all"], tmp)
        check("validate --all muestra los heredados", "heredado: plan: Constitution Check" in out, out)


def scenario_release_status():
    print("status durante /release:")
    with tempfile.TemporaryDirectory() as tmp:
        d = os.path.join(tmp, "docs/specs/001-x")
        os.makedirs(d)
        os.makedirs(os.path.join(tmp, ".ai"))
        open(os.path.join(tmp, ".ai/project.yaml"), "w", encoding="utf-8").write("type: mobile\nlanguage: en\n")
        w = lambda f, t: open(os.path.join(d, f), "w", encoding="utf-8").write(t)
        w("spec.md", "---\nstatus: implemented\n---\n## Acceptance criteria\n- [x] AC1 x\n")
        w("plan.md", "---\nstatus: approved\n---\n")
        w("review.md", "---\nverdict: approved\nround: 1\nhuman_signoff: me 2026-10-03\n---\n")
        base = "---\nstatus: approved\n---\n- [x] T001 a — x.py — done when: y — covers: AC1\n- [x] T090 a\n- [x] T091 b\n- [x] T092 c\n"
        w("tasks.md", base + "- [ ] T095 staging\n  - blocked: 2026-10-03 — sign and upload the AAB, check on device — /release 001\n- [ ] T096 approve\n")
        _, out = run(["status", "--json"], tmp)
        check("T095 bloqueada → status dice qué falta", "T095 bloqueada: sign and upload the AAB" in out, out)
        w("tasks.md", base + "- [x] T095 staging\n- [ ] T096 approve\n")
        _, out = run(["status", "--json"], tmp)
        check("T095 hecha → aprobación humana (T096)", "aprobación humana para producción (T096)" in out, out)


def scenario_design_contrast_rule():
    print("system.md: regla de contraste:")
    with tempfile.TemporaryDirectory() as tmp:
        os.makedirs(os.path.join(tmp, ".ai"))
        os.makedirs(os.path.join(tmp, "docs/design"))
        open(os.path.join(tmp, ".ai/project.yaml"), "w", encoding="utf-8").write(
            "type: frontend\nlanguage: en\ndesign:\n  status: draft\n  source: chosen\n"
            "  system: docs/design/system.md\n  html: docs/design/system.html\n")
        open(os.path.join(tmp, "docs/design/system.html"), "w", encoding="utf-8").write("<html></html>")
        open(os.path.join(tmp, "docs/design/system.md"), "w", encoding="utf-8").write(
            "---\nstatus: draft\nsource: chosen\n---\n## Color\n| Token | Light | Dark | Use | Contrast light · dark |\n|---|---|---|---|---|\n"
            "| `--color-text` | `#111111` | `#eeeeee` | Text | 18.9:1 · 17.0:1 |\n"
            "| `--color-warning-bg` | `#fff3d6` | `#3a2d10` | Warning background | — |\n"
            "| `--color-danger` | `#b3261e` | `#ff8f86` | Errors | 6.0 · 8.2 |\n")
        _, out = run(["validate"], tmp)
        check("un fondo (-bg) no se trata como color de texto", "--color-warning-bg" not in out, out)
        check("contraste sin ':1' sigue avisando", "--color-danger es color de texto" in out, out)


def scenario_templates():
    print("templates (huellas de docs/templates/):")
    with tempfile.TemporaryDirectory() as tmp:
        os.makedirs(os.path.join(tmp, ".ai"))
        os.makedirs(os.path.join(tmp, "docs/templates"))
        for n, t in (("spec.md", "# Spec\r\nbody  \r\n"), ("plan.md", "# Plan\n")):
            open(os.path.join(tmp, "docs/templates", n), "w", encoding="utf-8", newline="").write(t)
        open(os.path.join(tmp, ".ai/project.yaml"), "w", encoding="utf-8").write("type: cli\nlanguage: en\n")
        _, y = run(["templates", "--yaml"], tmp)
        open(os.path.join(tmp, ".ai/project.yaml"), "a", encoding="utf-8").write(y)
        open(os.path.join(tmp, "docs/templates/plan.md"), "a", encoding="utf-8").write("## Our own section\n")
        open(os.path.join(tmp, "docs/templates/tasks.md"), "w", encoding="utf-8").write("# Tasks\n")
        _, out = run(["templates"], tmp)
        check("plantilla igual a la registrada → sin cambios", "| spec.md |" in out and "sin cambios" in out.split("| spec.md |")[1].split("\n")[0], out)
        check("plantilla editada → personalizada", "personalizada" in out.split("| plan.md |")[1].split("\n")[0], out)
        check("plantilla sin huella → sin registro", "sin registro" in out.split("| tasks.md |")[1].split("\n")[0], out)
        open(os.path.join(tmp, "docs/templates/spec.md"), "w", encoding="utf-8").write("# Spec\nbody\n")
        _, out = run(["templates"], tmp)
        check("los finales de línea no cuentan como personalización", "sin cambios" in out.split("| spec.md |")[1].split("\n")[0], out)


if __name__ == "__main__":
    fixtures()
    scenario_review_pack()
    scenario_review_pack_generated()
    scenario_status()
    scenario_history()
    scenario_encoding()
    scenario_hook()
    scenario_design_templates()
    scenario_closed_specs()
    scenario_release_status()
    scenario_design_contrast_rule()
    scenario_templates()
    print(f"\n{'OK' if not FAILS else str(len(FAILS)) + ' FALLO(S)'}")
    sys.exit(1 if FAILS else 0)
