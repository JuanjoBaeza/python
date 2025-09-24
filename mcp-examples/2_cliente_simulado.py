import asyncio
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client

# Definimos ServerSpec basado en lo que necesita stdio_client
class ServerSpec:
    def __init__(self, command: str, args=None, env=None, cwd=None):
        self.command = command
        self.args = list(args) if args else []
        self.env = env
        self.cwd = cwd
        # Atributos que stdio_client espera
        self.encoding = "utf-8"
        self.encoding_error_handler = "strict"
        self.line_endings = "\n"
        self.bufsize = 0

async def consultar_llm(session, pregunta, contexto=""):
    """Función helper para consultar al LLM a través del servidor MCP"""
    try:
        if contexto:
            result = await session.call_tool("consulta_llm", {
                "pregunta": pregunta,
                "contexto": contexto
            })
        else:
            result = await session.call_tool("consulta_llm", {
                "pregunta": pregunta
            })
        return result
    except Exception as e:
        return f"Error al consultar el LLM: {e}"

async def analizar_texto_con_llm(session, texto, tipo_analisis="general"):
    """Función helper para analizar texto usando el LLM"""
    try:
        result = await session.call_tool("analizar_texto", {
            "texto": texto,
            "tipo_analisis": tipo_analisis
        })
        return result
    except Exception as e:
        return f"Error al analizar el texto: {e}"

async def main():
    # Configuración del servidor MCP
    spec = ServerSpec(
        command="python3",
        args=["2_server_simulado.py"],
        env=None,
        cwd=None
    )

    async with stdio_client(spec) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # Inicializar la sesión
            await session.initialize()

            # Listar herramientas disponibles
            tools = await session.list_tools()
            print("=== Herramientas disponibles ===")
            for tool in tools.tools:
                print(f"- {tool.name}: {tool.description}")
            print()

            # 1. Probar el saludo básico
            print("=== Prueba de saludo ===")
            try:
                result = await session.call_tool("saluda", {"nombre": "Juanjo"})
                print(f"Resultado: {result}")
            except Exception as e:
                print(f"Error con saluda: {e}")
            print()

            # 2. Consulta al LLM simple
            print("=== Consulta LLM simple ===")
            pregunta1 = "¿Cuáles son las mejores prácticas para desarrollo Python?"
            respuesta1 = await consultar_llm(session, pregunta1)
            print(f"Pregunta: {pregunta1}")
            print(f"Respuesta: {respuesta1}")
            print()

            # 3. Consulta al LLM con contexto
            print("=== Consulta LLM con contexto ===")
            pregunta2 = "¿Cómo puedo mejorar este código?"
            contexto = "Tengo una función que procesa datos y quiero hacerla más eficiente"
            respuesta2 = await consultar_llm(session, pregunta2, contexto)
            print(f"Pregunta: {pregunta2}")
            print(f"Contexto: {contexto}")
            print(f"Respuesta: {respuesta2}")
            print()

            # 4. Análisis de texto (si la herramienta existe)
            print("=== Análisis de texto ===")
            texto_analizar = """
            El Machine Learning Protocol (MCP) es un estándar emergente para la comunicación 
            entre aplicaciones y modelos de lenguaje. Proporciona una forma estandarizada 
            de exponer herramientas y recursos a los LLMs.
            """
            
            try:
                # Análisis general
                analisis_general = await analizar_texto_con_llm(session, texto_analizar, "general")
                print("Análisis general:")
                print(analisis_general)
                print()
            except Exception as e:
                print(f"Herramienta 'analizar_texto' no disponible: {e}")
                print()

            # 5. Probar múltiples consultas rápidas
            print("=== Múltiples consultas ===")
            preguntas_rapidas = [
                "¿Qué es Python?",
                "Explica el concepto de async/await",
                "¿Cómo funciona MCP?"
            ]

            for i, pregunta in enumerate(preguntas_rapidas, 1):
                respuesta = await consultar_llm(session, pregunta)
                print(f"Consulta {i}: {pregunta}")
                print(f"Respuesta {i}: {respuesta}")
                print()

if __name__ == "__main__":
    asyncio.run(main())