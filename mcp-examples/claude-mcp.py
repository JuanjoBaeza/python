# ────────────────────────────────────────────────────────
#  mcp/claude.py   (Modelo‑Contexto‑Protocolo)
# ────────────────────────────────────────────────────────
from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from typing import Any, Iterable, List, Protocol

logger = logging.getLogger(__name__)

# ------------------------------------------------------------------
#  Modelo – un mensaje de chat (texto + rol)
# ------------------------------------------------------------------
@dataclass(frozen=True)
class ClaudeMessage:
    role: str                     # "user" | "assistant"
    content: str                  # Texto del mensaje
    metadata: dict[str, Any] = field(default_factory=dict)   # opcional


# ------------------------------------------------------------------
#  Protocolo – interfaz genérica de chat
# ------------------------------------------------------------------
class ChatProtocol(Protocol):
    """
    Cualquier backend que implemente este protocolo debe proveer:
        * `ask(messages: Iterable[ClaudeMessage]) -> str`
    """
    def ask(self, messages: Iterable[ClaudeMessage]) -> str:
        ...


# ------------------------------------------------------------------
#  Contexto – wrapper del SDK de Anthropic
# ------------------------------------------------------------------
class ClaudeContext:
    """
    Maneja la creación y el cierre de la conexión a Claude‑3‑Opus.
    Se puede usar como *context manager* o simplemente invocar `ask`.
    """

    def __init__(
        self,
        api_key: str | None = None,
        # Para pruebas en local descomentar abajo y comentar linea de arriba
        # estableciendo variable de entorno en powershell $Env:API_KEY = "XXXXXXX"
        # api_key = "XXXXXXXX",
        model: str = "claude-3-opus-latest",
        max_tokens: int = 4_096,
    ):
        """
        :param api_key:   Si no se pasa, se busca en ANTHROPIC_API_KEY.
        :param model:     Modelo a usar (default «claude‑3‑opus‑latest»).
        :param max_tokens: Máximo de tokens que puede devolver Claude.
        """
        if not api_key:
            import os
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError(
                    "No se encontró API key. "
                    "Exporta ANTHROPIC_API_KEY antes de usar."
                )

        # Lazy‑import para que el módulo no cargue la dependencia hasta
        # que realmente se use.
        from anthropic import Anthropic

        self._client = Anthropic(api_key=api_key)
        self.model = model
        self.max_tokens = max_tokens

    # ------------------------------------------------------------------
    #  Context manager (opcional)
    # ------------------------------------------------------------------
    def __enter__(self) -> "ClaudeContext":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # El SDK no necesita cerrar nada explícitamente,
        # pero si hubiera un pool de conexiones se haría aquí.
        pass

    # ------------------------------------------------------------------
    #  Método principal
    # ------------------------------------------------------------------
    def ask(self, messages: Iterable[ClaudeMessage]) -> str:
        """
        Envía una lista de `ClaudeMessage` al backend y devuelve el texto de la respuesta.

        Se encarga de convertir los mensajes a la estructura que espera Anthropic,
        llamar al SDK y extraer el contenido textual sin importar si es dict o objeto.
        """
        # 1️⃣ Preparamos el payload
        payload = [
            {"role": msg.role, "content": msg.content} for msg in messages
        ]

        try:
            resp = self._client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                messages=payload,
            )
            return self._extract_text(resp)

        except Exception as exc:          # pragma: no cover
            logger.exception("Error al consultar Claude")
            raise RuntimeError(f"Claude error: {exc}") from exc

    # ------------------------------------------------------------------
    #  Extractor interno – compatible con SDK ≥0.5 y <0.5
    # ------------------------------------------------------------------
    @staticmethod
    def _extract_text(resp: Any) -> str:
        """
        Devuelve el texto concatenado de la respuesta.

        La función es muy robusta y funciona tanto con:
            * `resp.content` (SDK 0.5+)
            * `resp.message.content` (SDK <0.5)
        """
        texts: List[str] = []

        # --- SDK 0.5+ ---------------------------------------------------
        if hasattr(resp, "content") and isinstance(resp.content, list):
            for block in resp.content:
                # Caso dict
                if isinstance(block, dict):
                    if block.get("type") == "text":
                        txt = block.get("text", "")
                        if txt:
                            texts.append(txt)
                else:  # objeto (TextBlock, ImageBlock, …)
                    t_type = getattr(block, "type", None)
                    if t_type == "text":
                        txt = getattr(block, "text", "")
                        if txt:
                            texts.append(txt)

        # --- SDK <0.5 ----------------------------------------------------
        elif hasattr(resp, "message"):
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

        # --- Fallback simple -------------------------------------------
        if not texts and hasattr(resp, "text"):
            txt = getattr(resp, "text")
            if isinstance(txt, str) and txt.strip():
                texts.append(txt)

        if not texts:      # pragma: no cover
            raise RuntimeError("Claude response had no usable text content.")

        return "".join(texts)


# ------------------------------------------------------------------
#  Uso de ejemplo (puede ir en tests o en la propia CLI)
# ------------------------------------------------------------------
if __name__ == "__main__":
    import os

    # Si quieres usar el contexto como 'with', simplemente haz:
    with ClaudeContext() as ctx:
        prompt = input("Escribe tu pregunta: ")
        msg = ClaudeMessage(role="user", content=prompt)
        reply = ctx.ask([msg])
        print("\nRespuesta:", reply)

