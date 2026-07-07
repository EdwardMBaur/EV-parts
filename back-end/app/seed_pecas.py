"""
Seed de peças — popula o catálogo com peças coerentes com o tema
(baterias, inversores, BMS, motores, conectores HV, carregadores, etc.),
cria um usuário fornecedor e monta a matriz de compatibilidade peça × veículo.

Requisitos: rodar `python -m app.seed` antes (categorias, veículos, admin).

Uso: python -m app.seed_pecas
"""
from decimal import Decimal

from app.database import SessionLocal, engine, Base
from app.models import Usuario, Categoria, Veiculo, Peca, MatrizCompatibilidade
from app.core.security import hash_password


FORNECEDOR = {
    "tipo_perfil": "fornecedor",
    "email": "desmanche.sul@evparts.com.br",
    "senha": "Fornecedor@123",
    "nome_razao_social": "EcoDesmanche EV Sul LTDA",
    "cpf_cnpj": "12345678000199",
    "telefone": "41999990000",
}

# Cada peça referencia categorias pelo nome e veículos por (modelo, ano).
# soh: só faz sentido em baterias/células; nas demais fica None.
PECAS = [
    {
        "nome_peca": "Módulo bateria ID.4 — 82 kWh",
        "categoria": "Baterias",
        "descricao": "Módulo de bateria de tração para plataforma MEB. Usável 77 kWh.",
        "preco": "12400.00",
        "estoque": 3,
        "codigo_oem": "1EA-915-105-D",
        "fabricante": "CATL / VW Group",
        "peso_kg": "493.00",
        "dimensoes": "82 kWh (usável: 77 kWh)",
        "voltagem": "352 V DC",
        "soh": 94,
        "cep": "80010000",
        "veiculos": [("ID.4 GTX", 2023, "2.4", "4.9"), ("ID.4 GTX", 2022, "2.4", "4.9")],
    },
    {
        "nome_peca": "Célula de bateria LFP 3.2V",
        "categoria": "Baterias",
        "descricao": "Célula prismática LFP para reparo e reconstrução de packs.",
        "preco": "840.00",
        "estoque": 40,
        "codigo_oem": "LFP-32-100AH",
        "fabricante": "BYD FinDreams",
        "peso_kg": "2.30",
        "dimensoes": "100 Ah · prismática",
        "voltagem": "3.2 V DC",
        "soh": 88,
        "cep": "81200100",
        "veiculos": [("Dolphin", 2023, None, None), ("Han EV", 2022, None, None)],
    },
    {
        "nome_peca": "Pack bateria Model 3 LR — 82 kWh",
        "categoria": "Baterias",
        "descricao": "Pack completo 2170 para Model 3 Long Range. Laudo de SoH incluso.",
        "preco": "31900.00",
        "estoque": 1,
        "codigo_oem": "1104420-00-F",
        "fabricante": "Panasonic / Tesla",
        "peso_kg": "478.00",
        "dimensoes": "82 kWh (usável: 78 kWh)",
        "voltagem": "355 V DC",
        "soh": 91,
        "cep": "01310100",
        "veiculos": [("Model 3 LR", 2022, "2022.20", "2023.44")],
    },
    {
        "nome_peca": "BMS — Controlador ID.4 v3.x",
        "categoria": "Módulos Eletrônicos",
        "descricao": "Battery Management System para packs MEB com firmware ≥ v3.0.",
        "preco": "3200.00",
        "estoque": 7,
        "codigo_oem": "1EA-915-181",
        "fabricante": "VW Group",
        "peso_kg": "1.80",
        "dimensoes": "220 × 160 × 45 mm",
        "voltagem": "12 V DC",
        "soh": None,
        "cep": "90040000",
        "veiculos": [("ID.4 GTX", 2023, "3.0", "4.9")],
    },
    {
        "nome_peca": "Inversor trifásico 150 kW",
        "categoria": "Inversores",
        "descricao": "Inversor de tração trifásico para motor traseiro. Refrigerado a líquido.",
        "preco": "8700.00",
        "estoque": 4,
        "codigo_oem": "1EA-900-556",
        "fabricante": "VW Group",
        "peso_kg": "9.40",
        "dimensoes": "310 × 250 × 120 mm",
        "voltagem": "400 V DC",
        "soh": None,
        "cep": "80230010",
        "veiculos": [("ID.4 GTX", 2023, "2.4", "4.9"), ("XC40 Recharge", 2023, None, None)],
    },
    {
        "nome_peca": "Inversor de tração Model Y 220 kW",
        "categoria": "Inversores",
        "descricao": "Unidade inversora de silício-carbeto (SiC) do eixo traseiro.",
        "preco": "11250.00",
        "estoque": 2,
        "codigo_oem": "1120980-00-C",
        "fabricante": "Tesla",
        "peso_kg": "8.10",
        "dimensoes": "300 × 240 × 130 mm",
        "voltagem": "400 V DC",
        "soh": None,
        "cep": "04538100",
        "veiculos": [("Model Y", 2023, "2023.6", "2024.20"), ("Model 3 LR", 2022, "2022.20", "2023.44")],
    },
    {
        "nome_peca": "Motor elétrico traseiro PSM 150 kW",
        "categoria": "Motores Elétricos",
        "descricao": "Motor síncrono de ímãs permanentes para tração traseira MEB.",
        "preco": "9900.00",
        "estoque": 3,
        "codigo_oem": "1EA-820-300",
        "fabricante": "VW Group",
        "peso_kg": "82.00",
        "dimensoes": "eixo traseiro · 150 kW",
        "voltagem": "400 V AC",
        "soh": None,
        "cep": "81050000",
        "veiculos": [("ID.4 GTX", 2023, None, None), ("ID.4 GTX", 2022, None, None)],
    },
    {
        "nome_peca": "Motor dianteiro ASM 80 kW",
        "categoria": "Motores Elétricos",
        "descricao": "Motor de indução assíncrono do eixo dianteiro (tração integral).",
        "preco": "7300.00",
        "estoque": 2,
        "codigo_oem": "1120890-00-A",
        "fabricante": "Tesla",
        "peso_kg": "61.00",
        "dimensoes": "eixo dianteiro · 80 kW",
        "voltagem": "400 V AC",
        "soh": None,
        "cep": "20031050",
        "veiculos": [("Model Y", 2023, None, None)],
    },
    {
        "nome_peca": "Conector HV — pack traseiro",
        "categoria": "Conectores HV",
        "descricao": "Conector de alta tensão original do pack traseiro. Blindado.",
        "preco": "1150.00",
        "estoque": 15,
        "codigo_oem": "5EA-971-100",
        "fabricante": "VW MEB",
        "peso_kg": "0.60",
        "dimensoes": "2 vias · 250 A",
        "voltagem": "500 V DC",
        "soh": None,
        "cep": "88010000",
        "veiculos": [("ID.4 GTX", 2023, None, None), ("ID.4 GTX", 2022, None, None), ("XC40 Recharge", 2023, None, None)],
    },
    {
        "nome_peca": "Chicote HV blindado 2m",
        "categoria": "Conectores HV",
        "descricao": "Cabo laranja de alta tensão blindado para interligação de módulos.",
        "preco": "620.00",
        "estoque": 22,
        "codigo_oem": "HV-CBL-2000",
        "fabricante": "Aptiv",
        "peso_kg": "1.40",
        "dimensoes": "2000 mm · 35 mm²",
        "voltagem": "600 V DC",
        "soh": None,
        "cep": "90230000",
        "veiculos": [("Dolphin", 2023, None, None), ("Han EV", 2022, None, None), ("Zoe R110", 2021, None, None)],
    },
    {
        "nome_peca": "Carregador de bordo OBC 11 kW",
        "categoria": "Carregadores OBC",
        "descricao": "On-board charger trifásico 11 kW com conversor DC/DC integrado.",
        "preco": "4450.00",
        "estoque": 5,
        "codigo_oem": "1EA-971-800",
        "fabricante": "VW Group",
        "peso_kg": "6.20",
        "dimensoes": "300 × 220 × 90 mm",
        "voltagem": "400 V DC",
        "soh": None,
        "cep": "80420000",
        "veiculos": [("ID.4 GTX", 2023, "2.4", "4.9"), ("XC40 Recharge", 2023, None, None)],
    },
    {
        "nome_peca": "Conversor DC/DC 2.5 kW",
        "categoria": "Carregadores OBC",
        "descricao": "Conversor de alta para baixa tensão (400V → 12V) para rede de bordo.",
        "preco": "1980.00",
        "estoque": 9,
        "codigo_oem": "DCDC-2500-12",
        "fabricante": "BYD FinDreams",
        "peso_kg": "3.10",
        "dimensoes": "240 × 180 × 70 mm",
        "voltagem": "400 V DC",
        "soh": None,
        "cep": "81330000",
        "veiculos": [("Dolphin", 2023, None, None), ("Han EV", 2022, None, None)],
    },
    {
        "nome_peca": "Sensor de temperatura do pack",
        "categoria": "Módulos Eletrônicos",
        "descricao": "Sensor NTC para monitoramento térmico de módulos de bateria.",
        "preco": "320.00",
        "estoque": 30,
        "codigo_oem": "5Q0-915-511",
        "fabricante": "VW MEB",
        "peso_kg": "0.05",
        "dimensoes": "NTC 10k",
        "voltagem": "5 V DC",
        "soh": None,
        "cep": "89201000",
        "veiculos": [
            ("ID.4 GTX", 2023, None, None),
            ("ID.4 GTX", 2022, None, None),
            ("XC40 Recharge", 2023, None, None),
            ("Zoe R110", 2021, None, None),
        ],
    },
    {
        "nome_peca": "Módulo VCU — Unidade de controle do veículo",
        "categoria": "Módulos Eletrônicos",
        "descricao": "Vehicle Control Unit responsável pela gestão de torque e energia.",
        "preco": "2750.00",
        "estoque": 6,
        "codigo_oem": "1EA-907-115",
        "fabricante": "VW Group",
        "peso_kg": "0.90",
        "dimensoes": "180 × 130 × 40 mm",
        "voltagem": "12 V DC",
        "soh": None,
        "cep": "80510000",
        "veiculos": [("ID.4 GTX", 2023, "3.0", "4.9"), ("ID.4 GTX", 2022, "3.0", "3.9")],
    },
    {
        "nome_peca": "Bomba d'água elétrica do sistema térmico",
        "categoria": "Refrig. Térmica",
        "descricao": "Bomba elétrica de circulação do circuito de arrefecimento da bateria.",
        "preco": "890.00",
        "estoque": 12,
        "codigo_oem": "5QE-965-561",
        "fabricante": "Pierburg",
        "peso_kg": "1.10",
        "dimensoes": "Ø90 × 110 mm",
        "voltagem": "12 V DC",
        "soh": None,
        "cep": "83005000",
        "veiculos": [("ID.4 GTX", 2023, None, None), ("XC40 Recharge", 2023, None, None)],
    },
    {
        "nome_peca": "Chiller de bateria (trocador de calor)",
        "categoria": "Refrig. Térmica",
        "descricao": "Trocador de calor refrigerante/líquido para condicionamento do pack.",
        "preco": "1620.00",
        "estoque": 4,
        "codigo_oem": "1EA-816-411",
        "fabricante": "Hanon Systems",
        "peso_kg": "2.40",
        "dimensoes": "260 × 90 × 60 mm",
        "voltagem": None,
        "soh": None,
        "cep": "90520000",
        "veiculos": [("ID.4 GTX", 2023, None, None), ("Model 3 LR", 2022, None, None)],
    },
    {
        "nome_peca": "Pinça de freio regenerativo dianteira",
        "categoria": "Suspensão e Freios",
        "descricao": "Pinça de freio compatível com frenagem regenerativa. Lado esquerdo.",
        "preco": "780.00",
        "estoque": 10,
        "codigo_oem": "5QM-615-123",
        "fabricante": "TRW",
        "peso_kg": "3.60",
        "dimensoes": "disco Ø358 mm",
        "voltagem": None,
        "soh": None,
        "cep": "80320000",
        "veiculos": [("ID.4 GTX", 2023, None, None), ("XC40 Recharge", 2023, None, None)],
    },
    {
        "nome_peca": "Amortecedor dianteiro adaptativo",
        "categoria": "Suspensão e Freios",
        "descricao": "Amortecedor com controle eletrônico DCC para plataforma MEB.",
        "preco": "1340.00",
        "estoque": 8,
        "codigo_oem": "1EA-413-031",
        "fabricante": "ZF Sachs",
        "peso_kg": "4.20",
        "dimensoes": "dianteiro · DCC",
        "voltagem": "12 V DC",
        "soh": None,
        "cep": "88301000",
        "veiculos": [("ID.4 GTX", 2023, None, None), ("ID.4 GTX", 2022, None, None)],
    },
    {
        "nome_peca": "Módulo de bateria Zoe 52 kWh",
        "categoria": "Baterias",
        "descricao": "Módulo de bateria para Renault Zoe R110. SoH verificado em laudo.",
        "preco": "6900.00",
        "estoque": 2,
        "codigo_oem": "295B1-5MA0A",
        "fabricante": "LG Energy Solution",
        "peso_kg": "310.00",
        "dimensoes": "52 kWh (usável: 50 kWh)",
        "voltagem": "400 V DC",
        "soh": 83,
        "cep": "80630000",
        "veiculos": [("Zoe R110", 2021, "1.8", "1.9")],
    },
    {
        "nome_peca": "Carregador rápido DC — módulo de potência 25 kW",
        "categoria": "Carregadores OBC",
        "descricao": "Módulo de potência para infraestrutura de recarga rápida DC.",
        "preco": "5300.00",
        "estoque": 3,
        "codigo_oem": "DCFC-PM-25K",
        "fabricante": "Delta Electronics",
        "peso_kg": "18.00",
        "dimensoes": "rack 3U · 25 kW",
        "voltagem": "500 V DC",
        "soh": None,
        "cep": "01452000",
        "veiculos": [("Model Y", 2023, None, None), ("Model 3 LR", 2022, None, None)],
    },
]


def _get_fornecedor(db):
    forn = db.query(Usuario).filter(Usuario.email == FORNECEDOR["email"]).first()
    if forn:
        return forn
    forn = Usuario(
        tipo_perfil=FORNECEDOR["tipo_perfil"],
        email=FORNECEDOR["email"],
        senha_hash=hash_password(FORNECEDOR["senha"]),
        nome_razao_social=FORNECEDOR["nome_razao_social"],
        cpf_cnpj=FORNECEDOR["cpf_cnpj"],
        telefone=FORNECEDOR["telefone"],
        ativo="S",
    )
    db.add(forn)
    db.flush()
    return forn


def _veiculo_id(db, modelo, ano):
    v = db.query(Veiculo).filter(Veiculo.modelo == modelo, Veiculo.ano_fabricacao == ano).first()
    return v.id_veiculo if v else None


def seed_pecas():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    criadas, puladas = 0, 0
    try:
        fornecedor = _get_fornecedor(db)
        categorias = {c.nome_categoria: c.id_categoria for c in db.query(Categoria).all()}

        for item in PECAS:
            if db.query(Peca).filter(Peca.codigo_oem == item["codigo_oem"]).first():
                puladas += 1
                continue

            id_categoria = categorias.get(item["categoria"])
            if id_categoria is None:
                print(f"⚠️  Categoria '{item['categoria']}' não encontrada — pulando '{item['nome_peca']}'")
                continue

            peca = Peca(
                id_fornecedor=fornecedor.id_usuario,
                id_categoria=id_categoria,
                nome_peca=item["nome_peca"],
                descricao=item["descricao"],
                preco=Decimal(item["preco"]),
                estoque=item["estoque"],
                codigo_oem=item["codigo_oem"],
                fabricante=item["fabricante"],
                peso_kg=Decimal(item["peso_kg"]) if item["peso_kg"] else None,
                dimensoes=item["dimensoes"],
                voltagem=item["voltagem"],
                estado_saude_soh=item["soh"],
                cep_localizacao=item["cep"],
                ativo="S",
            )
            db.add(peca)
            db.flush()

            for modelo, ano, sw_min, sw_max in item["veiculos"]:
                id_veiculo = _veiculo_id(db, modelo, ano)
                if id_veiculo is None:
                    print(f"⚠️  Veículo '{modelo} {ano}' não encontrado — compat. ignorada")
                    continue
                db.add(MatrizCompatibilidade(
                    id_peca=peca.id_peca,
                    id_veiculo=id_veiculo,
                    versao_sw_min=sw_min,
                    versao_sw_max=sw_max,
                ))
            criadas += 1

        db.commit()
        print(f"✅ Seed de peças concluído — {criadas} criadas, {puladas} já existentes.")
    except Exception as e:
        db.rollback()
        print(f"❌ Erro no seed de peças: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_pecas()
