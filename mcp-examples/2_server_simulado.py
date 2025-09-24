from mcp.server.fastmcp import FastMCP

# Crea el servidor
mcp = FastMCP("demo-server")

# Ejemplo: añade una herramienta
@mcp.tool()
def saluda(nombre: str) -> str:
    """Devuelve un saludo personalizado"""
    return f"¡Hola {nombre}!"

# Ejemplo: añade una herramienta más compleja para consultas LLM
@mcp.tool()
def consulta_llm(pregunta: str, contexto: str = "") -> str:
    """
    Realiza una consulta a un modelo de lenguaje simulando un LLM.
    
    Args:
        pregunta: La pregunta o consulta a realizar
        contexto: Información contextual adicional (opcional)
    """
    # Simulación de respuesta de LLM
    respuestas_base = {
        "¿Cuáles son las mejores prácticas para desarrollo Python?": 
        "Las mejores prácticas incluyen: usar type hints, escribir tests, seguir PEP8, usar virtual environments, y documentar el código adecuadamente.",
        
        "¿Qué es Python?":
        "Python es un lenguaje de programación interpretado, de alto nivel y multipropósito. Es conocido por su sintaxis clara y legible.",
        
        "Explica el concepto de async/await":
        "Async/await permite programación asíncrona en Python. 'async' define funciones asíncronas y 'await' pausa la ejecución hasta que una operación se complete.",
        
        "¿Cómo funciona MCP?":
        "MCP (Model Context Protocol) es un protocolo para comunicación entre aplicaciones y modelos de lenguaje, permitiendo exponer herramientas y recursos de forma estandarizada."
    }
    
    # Buscar respuesta predefinida o generar una genérica
    if pregunta in respuestas_base:
        respuesta = respuestas_base[pregunta]
    else:
        respuesta = f"Respuesta simulada a: '{pregunta}'. En implementación real, conectaría con un LLM real."
    
    if contexto:
        respuesta = f"Contexto proporcionado: {contexto}\n\n{respuesta}"
    
    return respuesta

# Herramienta para análisis de texto
@mcp.tool()
def analizar_texto(texto: str, tipo_analisis: str = "general") -> str:
    """
    Analiza un texto con diferentes tipos de análisis.
    
    Args:
        texto: El texto a analizar
        tipo_analisis: Tipo de análisis ('general', 'sentimiento', 'resumen')
    """
    texto_preview = texto[:100] + "..." if len(texto) > 100 else texto
    
    if tipo_analisis == "sentimiento":
        return f"Análisis de sentimiento: '{texto_preview}' - Resultado: Positivo (análisis simulado)"
    elif tipo_analisis == "resumen":
        return f"Resumen: '{texto_preview}' - Resumen simulado: Texto analizado contiene aproximadamente {len(texto.split())} palabras."
    else:
        return f"Análisis general: '{texto_preview}' - Longitud: {len(texto)} caracteres, Palabras aproximadas: {len(texto.split())}"

# Ejemplo: añade un recurso
@mcp.resource("example://texto")
def texto_ejemplo() -> str:
    return "Este es un recurso de ejemplo servido por MCP."

# Punto de entrada
if __name__ == "__main__":
    mcp.run(transport="stdio")