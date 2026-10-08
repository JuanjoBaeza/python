from openai import OpenAI

# Arrancar previamente la aplicacion LM Studio y e iniciar el servidor local

client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")

completion = client.chat.completions.create(
  model="local-model", # this field is currently unused
  messages=[
    {"role": "system", "content": "¿De que trata Blade Runner 2049?"},
  ],
  temperature=0.7,
)

msg = completion.choices[0].message

print(msg.content)