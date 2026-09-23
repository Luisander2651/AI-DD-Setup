# Repo del plugin ai-dd

Este repositorio **es** el plugin; no es un proyecto que use el flujo.

- Lee `README.md` → "Mantenimiento" antes de cambiar cualquier skill.
- Reglas compartidas entre skills: solo en `shared/contract.md`.
- Al cambiar plantillas o contrato: sube la versión en `.claude-plugin/plugin.json` y en
  `skills/init/SKILL.md`, y añade entrada en `CHANGELOG.md`.
- Las skills se escriben como instrucciones para el agente, en español, en imperativo.
- Mantén cada `SKILL.md` por debajo de ~3 000 palabras; el detalle va en `references/`.
