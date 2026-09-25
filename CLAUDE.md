# Repo del plugin ai-dd

Este repositorio **es** el plugin; no es un proyecto que use el flujo.

- Lee `README.md` → "Mantenimiento" antes de cambiar cualquier skill.
- Reglas compartidas entre skills: solo en `shared/contract.md`.
- Al cambiar plantillas o contrato: sube la versión en `.claude-plugin/plugin.json` y en
  `skills/init/SKILL.md`, y añade entrada en `CHANGELOG.md`.
- Las skills se escriben como instrucciones para el agente, en español, en imperativo.
- Antes de cada commit que toque `scripts/` o plantillas: `python tests/run.py` sin fallos.
- Un hallazgo de un proyecto real no se convierte en regla sin un caso de prueba de otro tipo o
  idioma en `tests/fixtures/` (ver README → Mantenimiento). Títulos y marcadores nuevos que lea el
  validador van en `shared/vocabulary.md` y en `VOCAB`/`W` de `aidd.py`, en español e inglés.
- Mantén cada `SKILL.md` por debajo de ~3 000 palabras; el detalle va en `references/`.
