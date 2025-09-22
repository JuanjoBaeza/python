# --------------------------------------------------------------
#  Claude‑3‑Opus helper – version robusta (SDK ≥0.5)
# --------------------------------------------------------------

import logging
from typing import Any, List

logger = logging.getLogger(__name__)

def _extract_text_from_response(resp: Any) -> str:
    """
    Extrae todo el texto presente en la respuesta de Claude.

    - Si los bloques son diccionarios → usa .get().
    - Si los bloques son objetos (TextBlock, ImageBlock, …) → lee atributos.
    - Si no hay bloques de tipo 'text', lanza RuntimeError.
    """
    # 1️⃣ Respuesta moderna (SDK ≥0.5)
    if hasattr(resp, "content") and isinstance(resp.content, list):
        texts: List[str] = []

        for block in resp.content:
            # Caso dict
            if isinstance(block, dict):
                if block.get("type") == "text":
                    txt = block.get("text", "")
                    if txt:
                        texts.append(txt)

            # Caso objeto (TextBlock, ImageBlock, …)
            else:
                t_type = getattr(block, "type", None)
                if t_type == "text":
                    txt = getattr(block, "text", "")
                    if txt:
                        texts.append(txt)

        if texts:
            return "".join(texts)

    # 2️⃣ Versión antigua (SDK <0.5) – resp.message.content
    if hasattr(resp, "message"):
        msg = getattr(resp, "message")
        if hasattr(msg, "content") and isinstance(msg.content, list):
            for block in msg.content:
                if isinstance(block, dict):
                    if block.get("type") == "text":
                        txt = block.get("text", "")
                        if txt:
                            texts.append(txt)
                else:
                    t_type = getattr(block, "type", None)
                    if t_type == "text":
                        txt = getattr(block, "text", "")
                        if txt:
                            texts.append(txt)

            if texts:
                return "".join(texts)

    # 3️⃣ Fallback directo (.text) – solo en algunas versiones muy antiguas
    if hasattr(resp, "text"):
        txt = getattr(resp, "text")
        if isinstance(txt, str) and txt.strip():
            return txt

    raise RuntimeError("Claude response had no usable text content.")


def ask_claude_opus(
    client: Any,
    user_text: str,
    *,
    model: str = "claude-3-opus-latest",
    max_tokens: int = 4_096,
) -> str:
    """
    Envia un mensaje a Claude‑3‑Opus y devuelve el texto de la respuesta.
    """
    try:
        resp = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": user_text}],
        )
        return _extract_text_from_response(resp)

    except Exception as exc:
        logger.exception("Failed to get Claude response")
        raise RuntimeError(f"Could not retrieve Claude reply: {exc}") from exc


# --------------------------------------------------------------
#  Ejemplo de uso
# --------------------------------------------------------------

if __name__ == "__main__":
    import os

    # -----------------------------------------
    # 1️⃣ Cargar la clave desde variable de entorno (recomendado)
    # -----------------------------------------
    
    # Usar cualquiera de las dos opciones:
    # API_KEY = os.getenv("ANTHROPIC_API_KEY")
    # API_KEY = "XXXXXXXXXXXXXXXXXXX"
    
    if not API_KEY:
        raise RuntimeError(
            "No se encontró la variable ANTHROPIC_API_KEY. "
            "Exporta tu clave antes de ejecutar."
        )

    from anthropic import Anthropic

    client = Anthropic(api_key=API_KEY)

    # -----------------------------------------
    # 2️⃣ Texto que queremos preguntar
    # -----------------------------------------
    user_msg = (
        "Explícame brevemente qué es la programación orientada a objetos."
    )

    # -----------------------------------------
    # 3️⃣ Llamar al helper y mostrar resultado
    # -----------------------------------------
    respuesta = ask_claude_opus(client, user_msg)

    print("\nRespuesta de Claude 3 Opus:")
    print(respuesta)
