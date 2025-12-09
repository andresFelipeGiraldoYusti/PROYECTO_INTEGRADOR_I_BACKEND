from datetime import datetime
from app.db.session import Base, SessionLocal, engine
from app.models.product_type import ProductTypes
from app.models.suppliers import Suppliers
from app.models.users import Users
from app.models.risk_policies import RiskPolicies
from app.models.transactions import (
    Transactions,
    VerificationStatus,
    MFAStatus,
)

def seed_product_types(db):
    product_types = [
        ProductTypes(name="Servicios", description="Servicios generales"),
        ProductTypes(name="Equipos electrónicos", description="Tecnología y hardware"),
        ProductTypes(name="Papelería", description="Insumos de oficina"),
        ProductTypes(name="Transporte", description="Logística y movilidad"),
        ProductTypes(name="Consultoría", description="Servicios profesionales"),
        ProductTypes(name="Software", description="Licencias y herramientas digitales"),
        ProductTypes(name="Mobiliario", description="Muebles de oficina"),
        ProductTypes(name="Seguridad", description="Servicios de vigilancia"),
        ProductTypes(name="Limpieza", description="Aseo empresarial"),
        ProductTypes(name="Marketing", description="Promoción y publicidad"),
    ]
    db.add_all(product_types)

# -------------------------------------------------------------------
# 🔹 SEED: SUPPLIERS
# -------------------------------------------------------------------
def seed_suppliers(db):
    suppliers = [
        Suppliers(nit="900111222", legal_name="Proveedor Servicios S.A.", comercial_name="ServiPlus"),
        Suppliers(nit="800555444", legal_name="Electro Mundo LTDA", comercial_name="ElectroMundo"),
        Suppliers(nit="901333444", legal_name="Industrias Prima S.A.", comercial_name="PrimaCorp"),
        Suppliers(nit="805777333", legal_name="Papelería Global S.A.S.", comercial_name="GlobalPaper"),
        Suppliers(nit="900888777", legal_name="Consultoría Experta S.A.S.", comercial_name="ConExpert"),
        Suppliers(nit="901555222", legal_name="Logística Express S.A.", comercial_name="LogiExpress"),
        Suppliers(nit="800111999", legal_name="SoftSolutions S.A.S.", comercial_name="SoftSol"),
        Suppliers(nit="900666123", legal_name="AseoPro SAS", comercial_name="AseoPro"),
        Suppliers(nit="901222555", legal_name="Muebles Alfa S.A.S.", comercial_name="AlfaMuebles"),
        Suppliers(nit="805444777", legal_name="Seguridad Total LTDA", comercial_name="SegurTotal"),
    ]
    db.add_all(suppliers)

# -------------------------------------------------------------------
# 🔹 SEED: USERS
# -------------------------------------------------------------------
def seed_users(db):
    users = [
        Users(email="jlopez@empresa.com", full_name="Juan López", dapartment="Finanzas",
              phone_number="3001111111", username="jlopez", password_hash="hash"),
        Users(email="mgarcia@empresa.com", full_name="Marta García", dapartment="Compras",
              phone_number="3002222222", username="mgarcia", password_hash="hash"),
        Users(email="arodriguez@empresa.com", full_name="Ana Rodríguez", dapartment="TI",
              phone_number="3003333333", username="arodriguez", password_hash="hash"),
        Users(email="pbernal@empresa.com", full_name="Pablo Bernal", dapartment="Logística",
              phone_number="3004444444", username="pbernal", password_hash="hash"),
        Users(email="cruiz@empresa.com", full_name="Camilo Ruiz", dapartment="Compras",
              phone_number="3005555555", username="cruiz", password_hash="hash"),
        Users(email="mlopera@empresa.com", full_name="María Lopera", dapartment="Finanzas",
              phone_number="3006666666", username="mlopera", password_hash="hash"),
        Users(email="jrendon@empresa.com", full_name="Julio Rendón", dapartment="TI",
              phone_number="3007777777", username="jrendon", password_hash="hash"),
        Users(email="glopera@empresa.com", full_name="Gloria Lopera", dapartment="Gerencia",
              phone_number="3008888888", username="glopera", password_hash="hash"),
        Users(email="fgomez@empresa.com", full_name="Felipe Gómez", dapartment="Auditoría",
              phone_number="3009999999", username="fgomez", password_hash="hash"),
        Users(email="acastro@empresa.com", full_name="Andrea Castro", dapartment="Logística",
              phone_number="3010000000", username="acastro", password_hash="hash"),
    ]
    db.add_all(users)

# -------------------------------------------------------------------
# 🔹 SEED: RISK POLICIES (USA product_type_id y supplier_id reales)
# -------------------------------------------------------------------
def seed_risk_policies(db):
    risk_policies = [
    RiskPolicies(rol="Analista", amount=0,        product_type_id=1, supplier_id=1, mfa_action="SKIP_MFA"),
    RiskPolicies(rol="Analista", amount=50000,    product_type_id=1, supplier_id=1, mfa_action="SKIP_MFA"),
    RiskPolicies(rol="Analista", amount=100000,   product_type_id=1, supplier_id=1, mfa_action="SKIP_MFA"),
    RiskPolicies(rol="Analista", amount=150000,   product_type_id=1, supplier_id=1, mfa_action="SKIP_MFA"),

    RiskPolicies(rol="Analista", amount=200000,   product_type_id=1, supplier_id=1, mfa_action="REQUIRE_MFA"),
    RiskPolicies(rol="Analista", amount=250000,   product_type_id=1, supplier_id=1, mfa_action="REQUIRE_MFA"),
    RiskPolicies(rol="Analista", amount=300000,   product_type_id=1, supplier_id=1, mfa_action="REQUIRE_MFA"),
    RiskPolicies(rol="Analista", amount=350000,   product_type_id=1, supplier_id=1, mfa_action="REQUIRE_MFA"),

    RiskPolicies(rol="Analista", amount=400000,   product_type_id=1, supplier_id=1, mfa_action="REQUIRE_MFA"),
    RiskPolicies(rol="Analista", amount=500000,   product_type_id=1, supplier_id=1, mfa_action="REQUIRE_MFA"),

    RiskPolicies(rol="Jefe",     amount=600000,   product_type_id=1, supplier_id=1, mfa_action="REQUIRE_MFA"),
    RiskPolicies(rol="Jefe",     amount=700000,   product_type_id=1, supplier_id=1, mfa_action="REQUIRE_MFA"),
    RiskPolicies(rol="Jefe",     amount=800000,   product_type_id=1, supplier_id=1, mfa_action="REQUIRE_MFA"),
    RiskPolicies(rol="Jefe",     amount=900000,   product_type_id=1, supplier_id=1, mfa_action="REQUIRE_MFA"),

    RiskPolicies(rol="Gerente",  amount=1000000,  product_type_id=1, supplier_id=1, mfa_action="ALWAYS_MFA"),
    RiskPolicies(rol="Gerente",  amount=2000000,  product_type_id=1, supplier_id=1, mfa_action="ALWAYS_MFA"),
    RiskPolicies(rol="Gerente",  amount=3000000,  product_type_id=1, supplier_id=1, mfa_action="ALWAYS_MFA"),
    RiskPolicies(rol="Gerente",  amount=5000000,  product_type_id=1, supplier_id=1, mfa_action="ALWAYS_MFA"),
    RiskPolicies(rol="Gerente",  amount=8000000,  product_type_id=1, supplier_id=1, mfa_action="ALWAYS_MFA"),
    RiskPolicies(rol="Gerente",  amount=10000000, product_type_id=1, supplier_id=1, mfa_action="ALWAYS_MFA"),
]

    db.add_all(risk_policies)



# -------------------------------------------------------------------
# 🔹 SEED: TRANSACTIONS (10 registros)
# -------------------------------------------------------------------
def seed_transactions(db):
    txs = [
        Transactions(user_id=1, product_type_id=1, supplier_id=1, amount=450000,
                     verification_status=VerificationStatus.SUCCESS, mfa_status=MFAStatus.NOT_REQUIRED),
        Transactions(user_id=2, product_type_id=2, supplier_id=2, amount=1500000,
                     verification_status=VerificationStatus.NEEDS_ADDITIONAL_CHECKS, mfa_status=MFAStatus.PENDING),
        Transactions(user_id=3, product_type_id=3, supplier_id=3, amount=200000,
                     verification_status=VerificationStatus.SUCCESS, mfa_status=MFAStatus.NOT_REQUIRED),
        Transactions(user_id=4, product_type_id=4, supplier_id=4, amount=300000,
                     verification_status=VerificationStatus.FAILED, mfa_status=MFAStatus.NOT_REQUIRED),
        Transactions(user_id=5, product_type_id=5, supplier_id=5, amount=6000000,
                     verification_status=VerificationStatus.NEEDS_ADDITIONAL_CHECKS, mfa_status=MFAStatus.PENDING),
        Transactions(user_id=6, product_type_id=6, supplier_id=6, amount=700000,
                     verification_status=VerificationStatus.SUCCESS, mfa_status=MFAStatus.NOT_REQUIRED),
        Transactions(user_id=7, product_type_id=7, supplier_id=7, amount=1200000,
                     verification_status=VerificationStatus.SUCCESS, mfa_status=MFAStatus.NOT_REQUIRED),
        Transactions(user_id=8, product_type_id=8, supplier_id=8, amount=400000,
                     verification_status=VerificationStatus.FAILED, mfa_status=MFAStatus.NOT_REQUIRED),
        Transactions(user_id=9, product_type_id=9, supplier_id=9, amount=800000,
                     verification_status=VerificationStatus.SUCCESS, mfa_status=MFAStatus.NOT_REQUIRED),
        Transactions(user_id=10, product_type_id=10, supplier_id=10, amount=9500000,
                     verification_status=VerificationStatus.NEEDS_ADDITIONAL_CHECKS, mfa_status=MFAStatus.PENDING),
    ]
    db.add_all(txs)

# -------------------------------------------------------------------
# 🔹 EXECUTION
# -------------------------------------------------------------------
def main():
    Base.metadata.create_all(engine)
    db = SessionLocal()

    try:
        #seed_product_types(db)
        #seed_suppliers(db)
        #db.commit()

        #seed_users(db)
        #db.commit()

        seed_risk_policies(db)
        db.commit()

        #seed_transactions(db)
        #db.commit()

        print("✅ Datos insertados correctamente en la base Neon.")

    except Exception as e:
        db.rollback()
        print("❌ Error al insertar datos:", e)

    finally:
        db.close()


if __name__ == "__main__":
    main()
