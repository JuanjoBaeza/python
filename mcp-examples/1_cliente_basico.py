import asyncio

# -------------------------------------------------------------
# 1. Definimos un spec completo con todos los atributos que stdio_client necesita.
class ServerSpec:
    def __init__(self, command: str, args=None, env=None, cwd=None, 
                 encoding="utf-8", encoding_error_handler="strict", 
                 line_endings="\n", bufsize=0):
        """
        :param command: comando a ejecutar (ej.: "python")
        :param args: lista de argumentos opcionales
        :param env: diccionario de variables de entorno (opcional)
        :param cwd: directorio de trabajo donde lanzar el proceso (opcional)
        :param encoding: codificación para la comunicación (por defecto utf-8)
        :param encoding_error_handler: manejador de errores de codificación
        :param line_endings: terminaciones de línea
        :param bufsize: tamaño del buffer
        """
        self.command = command
        self.args = list(args) if args else []
        self.env = env
        self.cwd = cwd
        self.encoding = encoding
        self.encoding_error_handler = encoding_error_handler
        self.line_endings = line_endings
        self.bufsize = bufsize

# -------------------------------------------------------------
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client


async def main():
    # Usamos el spec local con todos los atributos requeridos
    spec = ServerSpec(
        command="python3",
        args=["1_server_basico.py"],
        env=None,
        cwd=None,
        encoding="utf-8",
        encoding_error_handler="strict",
        line_endings="\n",
        bufsize=0
    )

    async with stdio_client(spec) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("Herramientas disponibles:")
            for tool in tools.tools:
                print(f"- {tool.name}: {tool.description}")

            result = await session.call_tool("saluda", {"nombre": "Juanjo"})
            print("Resultado:", result)


if __name__ == "__main__":
    asyncio.run(main())