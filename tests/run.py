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
        if exp["errors"] == 0 and "warnings_contains" in exp and not exp["warnings_contains"]:
            check(f"{name}: sin avisos", not warns, out)


def scenario_review_pack():
    print("review-pack (rutas con el mismo nombre, alias, docs fuera del diff):")
    with tempfile.TemporaryDirectory() as tmp:
        for d in (".ai", "docs/specs/001-x", "app/login", "app/admin", "src/Controllers"):
            os.makedirs(os.path.join(tmp, d))
        open(os.path.join(tmp, ".ai/project.yaml"), "w").write("type: frontend\n")
        open(os.path.join(tmp, "docs/specs/001-x/spec.md"), "w").write(
            "---\nstatus: approved\n---\n## Criterios de aceptación\n- [x] CA1 x\n")
        open(os.path.join(tmp, "docs/specs/001-x/tasks.md"), "w", encoding="utf-8").write(
            "---\nstatus: approved\n---\n"
            "- [x] T001 a — `app/login/page.tsx` — hecho cuando: y — cubre: CA1\n"
            "- [x] T002 b — `Ctl/SaveThingController.php` — hecho cuando: y — cubre: CA1\n")
        for f in ("app/login/page.tsx", "app/admin/page.tsx", "src/Controllers/SaveThingController.php"):
            open(os.path.join(tmp, f), "w").write("a\n")
        git(tmp, "init", "-q")
        git(tmp, "add", "-A")
        git(tmp, "commit", "-qm", "base")
        for f in ("app/login/page.tsx", "app/admin/page.tsx", "src/Controllers/SaveThingController.php",
                  "docs/specs/001-x/spec.md"):
            open(os.path.join(tmp, f), "a").write("b\n")
        git(tmp, "commit", "-qam", "change")
        code, out = run(["review-pack", "docs/specs/001-x", "--base", "HEAD~1"], tmp)
        scope = open(os.path.join(tmp, ".ai/cache/review/001-x/scope.md"), encoding="utf-8").read()
        extra = scope.split("## Cambiados sin tarea")[1].split("## Tareas")[0]
        check("admin/page.tsx no se da por cubierto por login/page.tsx", "app/admin/page.tsx" in extra, scope)
        check("alias Ctl/…Controller.php cubre la ruta real", "SaveThingController" not in extra, scope)
        diff = open(os.path.join(tmp, ".ai/cache/review/001-x/code.diff"), encoding="utf-8").read()
        check("docs/ queda fuera del diff de código", "spec.md" not in diff and "page.tsx" in diff)


def scenario_history():
    print("history / rotate:")
    with tempfile.TemporaryDirectory() as tmp:
        d = os.path.join(tmp, "docs/specs/001-x")
        os.makedirs(d)
        os.makedirs(os.path.join(tmp, ".ai"))
        open(os.path.join(tmp, ".ai/project.yaml"), "w").write("type: backend\n")
        open(os.path.join(d, "analysis.r1.md"), "w").write("---\nround: 1\nresult: fail\n---\n[x](../../x.md)\n")
        open(os.path.join(d, "analysis.md"), "w").write("---\nround: 2\nresult: pass\n---\n[r1](analysis.r1.md)\n")
        run(["history", "docs/specs/001-x", "--migrate", "--write"], tmp)
        check("la ronda suelta pasa a history/", os.path.isfile(os.path.join(d, "history/analysis.r1.md")))
        check("el enlace del vigente apunta a history/",
              "](history/analysis.r1.md)" in open(os.path.join(d, "analysis.md")).read())
        check("los enlaces relativos del archivado suben un nivel",
              "](../../../x.md)" in open(os.path.join(d, "history/analysis.r1.md")).read())
        run(["rotate", "docs/specs/001-x", "analysis"], tmp)
        check("rotate mueve la ronda vigente", os.path.isfile(os.path.join(d, "history/analysis.r2.md"))
              and not os.path.exists(os.path.join(d, "analysis.md")))
        check("history/README.md existe", os.path.isfile(os.path.join(d, "history/README.md")))


def scenario_hook():
    print("hook:")
    with tempfile.TemporaryDirectory() as tmp:
        os.makedirs(os.path.join(tmp, ".ai"))
        open(os.path.join(tmp, ".ai/project.yaml"), "w").write("type: mobile\nworkflow:\n  enforcement: warn\n")

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


if __name__ == "__main__":
    fixtures()
    scenario_review_pack()
    scenario_history()
    scenario_hook()
    print(f"\n{'OK' if not FAILS else str(len(FAILS)) + ' FALLO(S)'}")
    sys.exit(1 if FAILS else 0)
