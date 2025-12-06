from core.config import settings
from db.session import engine, SessionLocal
from sqlalchemy import text


def test_connection():
    print(">>> Probando conexión a la base de datos...")
    print(">>> SQLALCHEMY_DATABASE_URL =", settings.SQLALCHEMY_DATABASE_URL)

    # 1) Probar conexión directa con el engine
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            row = result.fetchone()
            print(">>> Resultado SELECT 1:", row[0])
    except Exception as e:
        print("❌ Error al conectar usando engine.connect():")
        print(repr(e))
        return

    # 2) Probar creación de sesión
    try:
        db = SessionLocal()
        result = db.execute(text("SELECT 1"))
        row = result.fetchone()
        print(">>> Resultado SELECT 1 vía SessionLocal:", row[0])
    except Exception as e:
        print("❌ Error al usar SessionLocal():")
        print(repr(e))
        return
    finally:
        try:
            db.close()
        except Exception:
            pass

    print("✅ Conexión a la base de datos OK.")


if __name__ == "__main__":
    test_connection()