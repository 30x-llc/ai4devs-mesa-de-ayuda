# mesa-de-ayuda · demo de Claude Code en 5 actos

[![CI](https://github.com/30x-llc/ai4devs-mesa-de-ayuda/actions/workflows/ci.yml/badge.svg)](https://github.com/30x-llc/ai4devs-mesa-de-ayuda/actions/workflows/ci.yml)

Repo de práctica de la Nivelación 2 de AI for Developers (30X, 11-nov-2026).

Los datos son sintéticos: 40 tickets de soporte de una app ficticia, "Caja Fácil", guardados en SQLite. La tarea es la misma en los 5 actos, y en cada acto agregas una pieza de Claude Code para ver qué cambia.

## Requisitos

- [Claude Code](https://code.claude.com/docs), versión 2.1.322 o posterior (la de la clase).
- `python3`, `sqlite3`, `jq` y [`uv`](https://docs.astral.sh/uv/).
- WSL2 si usas Windows, porque el sandbox de Claude Code corre solo en macOS y Linux.

## Inicio rápido

```bash
git clone https://github.com/30x-llc/ai4devs-mesa-de-ayuda.git mesa-de-ayuda && cd mesa-de-ayuda && git checkout acto-0 && ./scripts/reset.sh && claude
```

`./scripts/reset.sh` crea la base con 40 tickets pendientes. Dentro de Claude Code escribe el prompt fijo:

```
Haz el triage de los tickets pendientes
```

Para gastar menos, agrega: "En esta prueba procesa solo los 15 primeros (ids 1 a 15)."

## Los 5 actos

Cada acto es un tag de git. Cada tag suma 1 pieza al anterior.

| Tag | Pieza que agrega | Archivos | Qué observar |
|---|---|---|---|
| `acto-0` | Ninguna | `scripts/seed.py`, `scripts/reset.sh` | Cómo encuentra los datos y qué criterio usa |
| `acto-1` | Memoria del proyecto | `CLAUDE.md` | Cuántos turnos usa y cuántos tokens ocupa la memoria |
| `acto-2` | Servidor MCP con 2 herramientas | `mcp/servidor.py`, `.mcp.json` | Qué herramientas usa y cuántas llamadas hace |
| `acto-3` | Skill | `.claude/skills/triage/SKILL.md` | Si 2 corridas iguales dan el mismo resultado |
| `acto-4` | Regla de permisos y hook | `.claude/settings.json`, `.claude/hooks/bloquear-delete.sh` | Qué pasa cuando un pedido intenta algo prohibido |

## Cómo pasar de un acto a otro

Sal de Claude Code con `/exit`. Luego cambia de tag y vuelve a crear la base:

```bash
git checkout acto-1 && ./scripts/reset.sh && rm -f .claude/settings.local.json
claude
```

Repite con `acto-2`, `acto-3` y `acto-4`. En el acto 2, Claude Code te pide aprobar el servidor `mesa-de-ayuda`. Apruébalo.

Para ver qué archivos cambian entre 2 actos:

```bash
git diff acto-1 acto-2 --stat
git diff acto-1 acto-2
```

## Mira qué entra al contexto

En cada acto escribe `/context` antes del prompt. Anota los tokens de "Memory files", "MCP tools" y "Skills". Compara las cifras entre actos.

Para medir turnos y costo sin interfaz:

```bash
claude -p "Haz el triage de los tickets pendientes" --output-format json | jq '{num_turns, total_cost_usd}'
```

Si tienes skills, MCP o hooks personales, agrega `--setting-sources project --strict-mcp-config --mcp-config .mcp.json`. En los actos 0 y 1 usa `--mcp-config '{"mcpServers":{}}'`. Así la comparación usa solo lo que trae el repo.

## Costo

El ensayo del profesor costó unos 4 USD en 23 corridas. Eso da unos 0,18 USD por corrida.

## Seguridad

- Todos los datos son inventados. Ningún ticket, cliente o monto es real.
- `secretos-falsos/` guarda un valor falso a propósito. El acto 4 lo usa para probar la regla de permisos.
- Un ticket trae una prompt injection a propósito. Mira qué hace el agente con ella.
- Lee cada hook, script y servidor MCP antes de copiarlo a tus repos. Corren con tus permisos.

Para probar el hook del acto 4 sin modelo:

```bash
echo '{"tool_input":{"command":"DROP TABLE prueba"}}' | .claude/hooks/bloquear-delete.sh; echo "exit=$?"
```

El hook sale con código 2 y Claude Code bloquea el comando.

## En tu propio repo, con otras herramientas

Haz estos cambios fuera de esta demo. Dentro de la demo, cada acto debe tener solo sus piezas.

- **Codex, Cursor y OpenCode** leen `AGENTS.md`. Copia ahí el contenido de tu `CLAUDE.md`.
- **Skills:** el formato `SKILL.md` es un estándar abierto ([agentskills.io](https://agentskills.io)). Cada herramienta busca las skills en su propia carpeta. Revisa su documentación.
- **MCP:** Codex lo configura en `~/.codex/config.toml`, Cursor en `.cursor/mcp.json` y OpenCode en `opencode.json`.

## Licencia

[MIT](LICENSE) · 30X LLC
