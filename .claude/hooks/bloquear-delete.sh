#!/usr/bin/env bash
# Hook PreToolUse: bloquea comandos de Bash con DELETE o DROP.
comando=$(jq -r '.tool_input.command // ""')
if echo "$comando" | grep -qiE '\b(DELETE|DROP)\b'; then
  echo "Bloqueado por el hook: en esta mesa de ayuda no se borran tickets (DELETE/DROP)." >&2
  exit 2
fi
exit 0
