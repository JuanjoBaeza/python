import asyncio
import os
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client

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

async def consultar_anthropic(session, pregunta, contexto="", modelo="claude-3-7-sonnet-latest"):
    """Función helper para consultar Anthropic"""
    try:
        params = {"pregunta": pregunta, "modelo": modelo}
        if contexto:
            params["contexto"] = contexto
            
        result = await session.call_tool("consulta_anthropic", params)
        return result
    except Exception as e:
        return f"Error al consultar Anthropic: {e}"

async def analizar_texto_anthropic(session, texto, tipo_analisis="general"):
    """Función helper para analizar texto con Anthropic"""
    try:
        result = await session.call_tool("analizar_texto_anthropic", {
            "texto": texto,
            "tipo_analisis": tipo_analisis
        })
        return result
    except Exception as e:
        return f"Error al analizar texto: {e}"

async def traducir_texto(session, texto, idioma_destino):
    """Función helper para traducir texto"""
    try:
        result = await session.call_tool("traducir_texto", {
            "texto": texto,
            "idioma_destino": idioma_destino
        })
        return result
    except Exception as e:
        return f"Error en traducción: {e}"

async def generar_codigo(session, descripcion, lenguaje="python"):
    """Función helper para generar código"""
    try:
        result = await session.call_tool("generar_codigo", {
            "descripcion": descripcion,
            "lenguaje": lenguaje
        })
        return result
    except Exception as e:
        return f"Error al generar código: {e}"

async def main():

    # Verificar que la API key esté configurada
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ Error: ANTHROPIC_API_KEY no encontrada en variables de entorno")
        print("💡 Ejecuta: export ANTHROPIC_API_KEY='tu-api-key'")
        return

    # Configuración del servidor MCP
    spec = ServerSpec(
        command="python3",
        args=["3_server_anthropic.py"],
        env=None,
        cwd=None
    )

    async with stdio_client(spec) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # Inicializar la sesión
            await session.initialize()

            # Listar herramientas disponibles
            tools = await session.list_tools()
            print("=== Herramientas Anthropic disponibles ===")
            for tool in tools.tools:
                print(f"🔧 {tool.name}: {tool.description}")
            print()

            # 1. Consulta básica a Anthropic
            print("=== Consulta básica a Anthropic ===")
            pregunta1 = "¿Cuáles son las ventajas de usar Python para machine learning?"
            respuesta1 = await consultar_anthropic(session, pregunta1)
            print(f"🤖 Pregunta: {pregunta1}")
            print(f"💡 Respuesta: {respuesta1}")
            print()

            # 2. Consulta con contexto
            print("=== Consulta con contexto ===")
            pregunta2 = "¿Cómo puedo optimizar este código?"
            contexto2 = """
            Tengo una función que procesa grandes volúmenes de datos en Python usando pandas.
            La función actual tarda mucho en ejecutarse y quiero hacerla más eficiente.
            """
            respuesta2 = await consultar_anthropic(session, pregunta2, contexto2)
            print(f"🤖 Pregunta: {pregunta2}")
            print(f"📋 Contexto: {contexto2.strip()}")
            print(f"💡 Respuesta: {respuesta2}")
            print()

            # 3. Análisis de texto
            print("=== Análisis de texto ===")
            texto_analizar = """
            El aprendizaje automático está transformando la industria tecnológica. 
            Las empresas están adoptando modelos de IA para mejorar sus productos y servicios.
            Python se ha convertido en el lenguaje líder para el desarrollo de ML debido a su ecosistema de librerías.
            """
            
            analisis = await analizar_texto_anthropic(session, texto_analizar, "resumen")
            print("📊 Análisis de texto:")
            print(analisis)
            print()

            # 4. Traducción
            print("=== Traducción ===")
            texto_traducir = "El machine learning es una tecnología fascinante que está cambiando el mundo."
            traduccion = await traducir_texto(session, texto_traducir, "inglés")
            print(f"🌐 Texto original: {texto_traducir}")
            print(f"🔤 Traducción: {traduccion}")
            print()

            # 5. Generación de código
            print("=== Generación de código ===")
            descripcion_codigo = "Una función que calcula el factorial de un número de forma recursiva"
            codigo = await generar_codigo(session, descripcion_codigo, "python")
            print(f"💻 Descripción: {descripcion_codigo}")
            print(f"📝 Código generado:\n{codigo}")
            print()

            # 6. Listar modelos disponibles
            try:
                modelos = await session.call_tool("listar_modelos_anthropic", {})
                print("=== Modelos Anthropic disponibles ===")
                print(modelos)
            except Exception as e:
                print(f"⚠️ No se pudo listar modelos: {e}")

if __name__ == "__main__":
    asyncio.run(main())