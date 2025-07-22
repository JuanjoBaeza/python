import requests
import json

# Reemplaza esto con tu propia API Key
API_KEY = "xxxxxxxxxxxxxxxxxxxxxxx"
MODEL = "models/gemini-1.5-flash"

url = f"https://generativelanguage.googleapis.com/v1/models?key={API_KEY}"

# URL base para generar contenido
API_URL = f"https://generativelanguage.googleapis.com/v1/{MODEL}:generateContent?key={API_KEY}"

response = requests.get(url)

if response.ok:
    modelos = response.json().get("models", [])
    print("✅ Modelos disponibles para tu API key:\n")
    for modelo in modelos:
        print(f"- {modelo['name']}")
else:
    print("❌ Error al obtener modelos:", response.status_code)
    print(response.text)

def generar_respuesta(prompt):
    """
    Envía un prompt de texto a Gemini y devuelve la respuesta generada.
    """
    headers = {
        "Content-Type": "application/json"
    }

    # Payload de solicitud
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    # Realiza la solicitud POST
    response = requests.post(API_URL, headers=headers, json=data)

    # Maneja la respuesta
    if response.ok:
        resultado = response.json()
        return resultado["candidates"][0]["content"]["parts"][0]["text"]
    else:
        print("❌ Error:", response.status_code)
        print(response.text)
        return None

# Ejemplo de uso
if __name__ == "__main__":
    prompt = "Resume brevemente la Segunda Guerra Mundial."
    respuesta = generar_respuesta(prompt)
    if respuesta:
        print("\n🧠 Gemini responde:\n")
        print(respuesta)