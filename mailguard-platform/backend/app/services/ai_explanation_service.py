import ssl

import httpx
import truststore

from app.core.config import settings

# Groq perdor nje API te ngjashem me OpenAI (chat completions)
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

PROMPT_TEMPLATE = (
    "Ti je nje asistent sigurie qe shpjegon rezultatet e nje modeli Machine "
    "Learning per skanim email-esh. Modeli e ka klasifikuar emailin e "
    "meposhtem si '{label}' me {confidence}% siguri.\n\n"
    "Subject: {subject}\n"
    "Body: {body}\n\n"
    "Shpjego ne 2-3 fjali te shkurtra, ne shqip, pse ky email duket si "
    "'{label}', duke u referuar te fjale ose fraza konkrete nga teksti kur "
    "eshte e mundur. Mos e perserit numrin e sigurise."
)

# Perdor certifikatat e Windows (rrjeti i shkolles nderpret HTTPS)
_ssl_context = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)


# Kerkon nje shpjegim me fjale nga Groq per rezultatin e skanimit
async def get_explanation(subject: str, body: str, predicted_label: str, confidence_score: float) -> str | None:
    # Nese s'ka API key te konfiguruar, thjesht anashkalohet (skanimi vazhdon normalisht)
    if not settings.GROQ_API_KEY:
        return None

    prompt = PROMPT_TEMPLATE.format(
        label=predicted_label,
        confidence=round(confidence_score * 100, 1),
        subject=subject or "(no subject)",
        body=body,
    )

    try:
        async with httpx.AsyncClient(timeout=15, verify=_ssl_context) as client:
            response = await client.post(
                GROQ_URL,
                headers={"Authorization": f"Bearer {settings.GROQ_API_KEY}"},
                json={
                    "model": settings.GROQ_MODEL,
                    "messages": [{"role": "user", "content": prompt}],
                },
            )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    except Exception:
        # Nese Groq nuk pergjigjet ose API key eshte gabim, skanimi nuk deshton
        return None
