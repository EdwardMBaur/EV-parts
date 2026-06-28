"""
Seed script — populates the database with initial categories,
sample vehicles and an admin user for local development.

Run with: python -m app.seed
"""
from app.database import SessionLocal, engine, Base
from app.models import *
from app.core.security import hash_password


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        categorias_data = [
            {"nome_categoria": "Baterias", "descricao": "Módulos, pacotes e células de bateria"},
            {"nome_categoria": "Inversores", "descricao": "Inversores de frequência e controladores de tração"},
            {"nome_categoria": "Módulos Eletrônicos", "descricao": "BMS, ECU e módulos de controle"},
            {"nome_categoria": "Motores Elétricos", "descricao": "Motores de tração e auxiliares"},
            {"nome_categoria": "Conectores HV", "descricao": "Conectores e cabos de alta tensão"},
            {"nome_categoria": "Carregadores OBC", "descricao": "On-board chargers e conversores DC/DC"},
            {"nome_categoria": "Suspensão e Freios", "descricao": "Componentes mecânicos adaptados para EVs"},
            {"nome_categoria": "Refrig. Térmica", "descricao": "Sistemas de resfriamento de baterias e eletrônicos"},
        ]
        for cat_data in categorias_data:
            if not db.query(Categoria).filter(Categoria.nome_categoria == cat_data["nome_categoria"]).first():
                db.add(Categoria(**cat_data))

        veiculos_data = [
            {"montadora": "Volkswagen", "modelo": "ID.4 GTX", "ano_fabricacao": 2023, "versao_software": "3.1.2", "vin_prefixo": "WVWZZZE1ZP"},
            {"montadora": "Volkswagen", "modelo": "ID.4 GTX", "ano_fabricacao": 2022, "versao_software": "3.0.0", "vin_prefixo": "WVWZZZE1ZN"},
            {"montadora": "BYD", "modelo": "Dolphin", "ano_fabricacao": 2023, "versao_software": "2.5.0", "vin_prefixo": "LGXCE4DB0P"},
            {"montadora": "BYD", "modelo": "Han EV", "ano_fabricacao": 2022, "versao_software": "2.0.1", "vin_prefixo": "LGXCE4AE0N"},
            {"montadora": "Tesla", "modelo": "Model 3 LR", "ano_fabricacao": 2022, "versao_software": "2022.36", "vin_prefixo": "5YJ3E1EA4N"},
            {"montadora": "Tesla", "modelo": "Model Y", "ano_fabricacao": 2023, "versao_software": "2023.6", "vin_prefixo": "7SAYGDEE4P"},
            {"montadora": "Renault", "modelo": "Zoe R110", "ano_fabricacao": 2021, "versao_software": "1.8.0", "vin_prefixo": "VF1AG000M6"},
            {"montadora": "Volvo", "modelo": "XC40 Recharge", "ano_fabricacao": 2023, "versao_software": "P8.0", "vin_prefixo": "YV1XZBRE0P"},
        ]
        for v_data in veiculos_data:
            if not db.query(Veiculo).filter(
                Veiculo.montadora == v_data["montadora"],
                Veiculo.modelo == v_data["modelo"],
                Veiculo.ano_fabricacao == v_data["ano_fabricacao"],
            ).first():
                db.add(Veiculo(**v_data))

        if not db.query(Usuario).filter(Usuario.email == "admin@evparts.com.br").first():
            admin = Usuario(
                tipo_perfil="admin",
                email="admin@evparts.com.br",
                senha_hash=hash_password("Admin@123"),
                nome_razao_social="EV.parts Admin",
                cpf_cnpj="00000000000",
                ativo="S",
            )
            db.add(admin)

        db.commit()
        print("✅ Seed concluído com sucesso!")

    except Exception as e:
        db.rollback()
        print(f"❌ Erro no seed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
