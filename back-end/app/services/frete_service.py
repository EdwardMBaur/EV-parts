from decimal import Decimal
from typing import List, Optional
from app.schemas.logistica import FreteModalidade, FreteResponse


HIGH_VOLTAGE_THRESHOLD = 48


def _is_carga_perigosa(voltagem: Optional[str]) -> bool:
    if not voltagem:
        return False
    try:
        v = float("".join(c for c in voltagem if c.isdigit() or c == "."))
        return v >= HIGH_VOLTAGE_THRESHOLD
    except (ValueError, TypeError):
        return False


def calcular_frete(
    cep_origem: str,
    cep_destino: str,
    peso_kg: Decimal,
    voltagem: Optional[str] = None,
    valor_declarado: Optional[Decimal] = None,
) -> FreteResponse:
    """
    Simulates intelligent freight routing for heavy/dangerous EV components.
    In production this should call a logistics partner API (e.g., Braspress, Rodonaves).
    
    Current implementation uses a rule-based heuristic model:
    - Distance factor estimated by first 2 digits of CEP (region code)
    - Hazardous-cargo surcharge applied when high voltage
    - Returns 2 modalities: fracionado (economy) and expresso (premium)
    """
    perigosa = _is_carga_perigosa(voltagem)

    origem_regiao = int(cep_origem[:2])
    destino_regiao = int(cep_destino[:2])
    distancia_relativa = abs(origem_regiao - destino_regiao)

    base_km = 300 + distancia_relativa * 40 

    taxa_base = Decimal("0.008") if not perigosa else Decimal("0.018")

    peso = Decimal(str(peso_kg))
    km = Decimal(str(base_km))

    custo_base = peso * km * taxa_base
    custo_seguro = (valor_declarado or Decimal("0")) * Decimal("0.005")

    fracionado_valor = (custo_base + custo_seguro + Decimal("120")).quantize(Decimal("0.01"))
    expresso_valor = (custo_base * Decimal("1.9") + custo_seguro + Decimal("80")).quantize(Decimal("0.01"))

    prazo_fracionado = max(5, 7 + distancia_relativa // 10)
    prazo_expresso = max(2, 3 + distancia_relativa // 20)

    modalidades: List[FreteModalidade] = [
        FreteModalidade(
            nome="Carga Fracionada",
            codigo="carga_fracionada",
            prazo_dias=prazo_fracionado,
            valor=fracionado_valor,
            descricao="Transporte rodoviário consolidado — ideal para peças de até 300 kg",
        ),
        FreteModalidade(
            nome="Expresso Especializado",
            codigo="expresso",
            prazo_dias=prazo_expresso,
            valor=expresso_valor,
            descricao="Veículo exclusivo com motorista habilitado para cargas ADR — prioridade total",
        ),
    ]

    aviso = None
    if perigosa:
        aviso = (
            f"⚡ Carga perigosa detectada ({voltagem}). Aplicados requisitos ADR/IMDG "
            "para transporte de baterias de alta tensão. Motorista habilitado obrigatório."
        )

    return FreteResponse(
        cep_origem=cep_origem,
        cep_destino=cep_destino,
        modalidades=modalidades,
        aviso_carga_especial=aviso,
    )
