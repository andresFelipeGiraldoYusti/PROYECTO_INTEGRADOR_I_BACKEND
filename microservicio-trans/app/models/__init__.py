# app/models/__init__.py

# Importa Base
from db.session import Base

# Importa todos los modelos aquí
from . import users
from . import mfa_devices
from . import mfa_session
from . import product_type
from . import risk_policies
from . import suppliers
from . import totp_configurations
from . import transactions
