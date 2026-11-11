"""Servidor MCP de la mesa de ayuda. Publica solo 2 herramientas: no hay borrar."""
import pathlib, sqlite3
from fastmcp import FastMCP

DB = pathlib.Path(__file__).resolve().parent.parent / "data" / "tickets.db"
mcp = FastMCP("mesa-de-ayuda")

@mcp.tool
def listar_pendientes() -> list[dict]:
    """Devuelve los tickets en estado pendiente."""
    with sqlite3.connect(DB) as con:
        con.row_factory = sqlite3.Row
        filas = con.execute("SELECT id, titulo, descripcion, cliente, creado FROM tickets WHERE estado = 'pendiente'")
        return [dict(f) for f in filas]

@mcp.tool
def clasificar(id: int, criticidad: str, nota: str) -> str:
    """Guarda la criticidad y una nota en un ticket pendiente y lo marca como clasificado."""
    with sqlite3.connect(DB) as con:
        cur = con.execute("UPDATE tickets SET criticidad = ?, nota = ?, estado = 'clasificado' WHERE id = ? AND estado = 'pendiente'", (criticidad, nota, id))
    return f"ticket {id}: {criticidad}" if cur.rowcount else f"ticket {id}: no existe o ya estaba clasificado"

if __name__ == "__main__":
    mcp.run()
