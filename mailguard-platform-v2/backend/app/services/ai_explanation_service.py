import ssl

import httpx
import truststore

from app.core.config import settings

# Groq perdor nje API te ngjashem me OpenAI (chat completions)
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

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
windows_ssl_context = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)


# Kerkon nga Groq nje shpjegim me fjale: pse emaili mori kete etikete.
# Shfaqet te seksioni "Why? (AI explanation)" i faqes Scanner.
# Kthen None nese s'ka API key ose Groq deshton - skanimi vazhdon normalisht.
async def explain_scan_result(subject: str, body: str, predicted_label: str,
                              confidence_score: float) -> str | None:
    if not settings.GROQ_API_KEY:
        return None

    prompt = PROMPT_TEMPLATE.format(
        label=predicted_label,
        confidence=round(confidence_score * 100, 1),
        subject=subject or "(no subject)",
        body=body,
    )

    try:
        async with httpx.AsyncClient(timeout=15, verify=windows_ssl_context) as http_client:
            response = await http_client.post(
                GROQ_API_URL,
                headers={"Authorization": f"Bearer {settings.GROQ_API_KEY}"},
                json={
                    "model": settings.GROQ_MODEL,
                    "messages": [{"role": "user", "content": prompt}],
                },
            )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception:
        return None
