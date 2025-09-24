from mcp.server.fastmcp import FastMCP

# Crea el servidor
mcp = FastMCP("demo-server")

# Ejemplo: añade una herramienta
@mcp.tool()
def saluda(nombre: str) -> str:
    """Devuelve un saludo personalizado"""
    return f"¡Hola {nombre}!"

# Ejemplo: añade un recurso
@mcp.resource("example://texto")
def texto_ejemplo() -> str:
    return "Este es un recurso de ejemplo servido por MCP."

# Punto de entrada
if __name__ == "__main__":
    mcp.run()