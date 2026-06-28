import httpx
from typing import Optional
from app.config import settings


async def buscar_cep(cep: str) -> Optional[dict]:
    """
    Queries ViaCEP API to auto-fill address from a Brazilian ZIP code.
    Returns None if CEP not found or invalid.
    """
    cep_clean = "".join(filter(str.isdigit, cep))
    if len(cep_clean) != 8:
        return None

    url = f"{settings.CEP_API_URL}/{cep_clean}/json/"
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()
            if data.get("erro"):
                return None
            return {
                "cep": data.get("cep", "").replace("-", ""),
                "logradouro": data.get("logradouro", ""),
                "bairro": data.get("bairro", ""),
                "cidade": data.get("localidade", ""),
                "estado": data.get("uf", ""),
                "ibge": data.get("ibge"),
                "ddd": data.get("ddd"),
            }
    except (httpx.HTTPError, Exception):
        return None
