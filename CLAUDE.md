# Mesa de ayuda (demo)

- Los tickets viven en SQLite: `data/tickets.db`, tabla `tickets`.
- Columnas: id, titulo, descripcion, cliente, creado, estado (pendiente|clasificado), criticidad, nota.
- Consulta con `sqlite3 data/tickets.db "SELECT id, titulo FROM tickets WHERE estado = 'pendiente';"`
- Para volver al estado inicial (40 pendientes): `./scripts/reset.sh`
- Nunca borres tickets.
