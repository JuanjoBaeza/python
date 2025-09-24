import os
from mcp.server.fastmcp import FastMCP
import anthropic

# Crea el servidor
mcp = FastMCP("anthropic-server")

# Configuración de Anthropic, cambiar segun se necesite origen de la API KEY
# ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ANTHROPIC_API_KEY = "NNNNNNNN"
if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY no encontrada en las variables de entorno")

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

@mcp.tool()
def consulta_anthropic(pregunta: str, contexto: str = "", modelo: str = "claude-3-7-sonnet-latest") -> str:
    """
    Consulta al modelo Anthropic Claude con una pregunta y contexto opcional.
    
    Args:
        pregunta: La pregunta o consulta a realizar
        contexto: Información contextual adicional (opcional)
        modelo: Modelo de Anthropic a usar (por defecto: claude-3-7-sonnet-latest)
    """
    try:
        # Construir el mensaje
        if contexto:
            mensaje = f"Contexto: {contexto}\n\nPregunta: {pregunta}"
        else:
            mensaje = pregunta

        # Realizar la consulta a Anthropic
        response = client.messages.create(
            model=modelo,
            max_tokens=1000,
            temperature=0.7,
            messages=[{
                "role": "user",
                "content": mensaje
            }]
        )
        
        return response.content[0].text
        
    except anthropic.APIConnectionError as e:
        return f"Error de conexión con Anthropic: {e}"
    except anthropic.RateLimitError as e:
        return f"Límite de tasa excedido: {e}"
    except anthropic.APIStatusError as e:
        return f"Error de API HTTP {e.status_code}: {e}"
    except Exception as e:
        return f"Error inesperado: {e}"

@mcp.tool()
def analizar_texto_anthropic(texto: str, tipo_analisis: str = "general") -> str:
    """
    Analiza un texto usando Anthropic Claude.
    
    Args:
        texto: El texto a analizar
        tipo_analisis: Tipo de análisis ('general', 'sentimiento', 'resumen', 'correccion')
    """
    try:
        prompt_map = {
            "general": f"Analiza este texto y proporciona un análisis general:\n\n{texto}",
            "sentimiento": f"Analiza el sentimiento de este texto y explica tu razonamiento:\n\n{texto}",
            "resumen": f"Proporciona un resumen conciso de este texto:\n\n{texto}",
            "correccion": f"Revisa y corrige este texto si es necesario, explicando los cambios:\n\n{texto}"
        }
        
        prompt = prompt_map.get(tipo_analisis, f"Analiza este texto:\n\n{texto}")

        response = client.messages.create(
            model="claude-3-7-sonnet-latest",
            max_tokens=800,
            temperature=0.3,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        return response.content[0].text
        
    except Exception as e:
        return f"Error al analizar el texto: {e}"

@mcp.tool()
def listar_modelos_anthropic() -> str:
    """Lista los modelos disponibles de Anthropic"""
    try:
        # Anthropic no tiene endpoint para listar modelos, así que devolvemos los conocidos
        modelos = [
            "claude-opus-4-1-20250805",
            "claude-3-7-sonnet-latest", 
            "claude-3-5-haiku-latest"
        ]
        return "Modelos Anthropic disponibles:\n" + "\n".join(f"- {modelo}" for modelo in modelos)
    except Exception as e:
        return f"Error al listar modelos: {e}"

@mcp.tool()
def traducir_texto(texto: str, idioma_destino: str) -> str:
    """
    Traduce texto usando Anthropic Claude.
    
    Args:
        texto: Texto a traducir
        idioma_destino: Idioma objetivo (ej: 'inglés', 'francés', 'alemán')
    """
    try:
        prompt = f"Traduce el siguiente texto al {idioma_destino}. Mantén el tono y estilo original:\n\n{texto}"

        response = client.messages.create(
            model="claude-3-7-sonnet-latest",
            max_tokens=1000,
            temperature=0.2,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        return response.content[0].text
        
    except Exception as e:
        return f"Error en la traducción: {e}"

@mcp.tool()
def generar_codigo(descripcion: str, lenguaje: str = "python") -> str:
    """
    Genera código basado en una descripción usando Anthropic.
    
    Args:
        descripcion: Descripción del código a generar
        lenguaje: Lenguaje de programación (python, javascript, etc.)
    """
    try:
        prompt = f"""Genera código en {lenguaje} basado en esta descripción:
        
        {descripcion}
        
        Proporciona solo el código, sin explicaciones adicionales, a menos que sea necesario para claridad."""

        response = client.messages.create(
            model="claude-3-7-sonnet-latest",
            max_tokens=1500,
            temperature=0.3,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        return response.content[0].text
        
    except Exception as e:
        return f"Error al generar código: {e}"

# Punto de entrada
if __name__ == "__main__":
    mcp.run(transport="stdio")