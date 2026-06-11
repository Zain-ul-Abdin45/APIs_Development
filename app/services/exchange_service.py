import httpx
from app.config import settings

# Reuse a single AsyncClient across requests — avoids TCP handshake overhead
_http_client: httpx.AsyncClient | None = None


def get_http_client() -> httpx.AsyncClient:
    global _http_client
    if _http_client is None or _http_client.is_closed:
        _http_client = httpx.AsyncClient(
            base_url=settings.exchange_rate_api_base,
            timeout=httpx.Timeout(5.0),
            headers={"Authorization": f"Bearer {settings.exchange_rate_api_key}"}
            if settings.exchange_rate_api_key
            else {},
        )
    return _http_client


async def get_exchange_rate(from_currency: str, to_currency: str = "EUR") -> float:
    client = get_http_client()
    response = await client.get(
        "/live",
        params={"source": from_currency, "currencies": to_currency},
    )
    response.raise_for_status()
    data = response.json()
    key = f"{from_currency}{to_currency}"
    return data.get("quotes", {}).get(key, 1.0)


async def close_http_client():
    global _http_client
    if _http_client and not _http_client.is_closed:
        await _http_client.aclose()
        _http_client = None
