# Import all blueprint modules
from web_front.routes.auth import auth_bp
from web_front.routes.devicetypes import devicetypes_bp
from web_front.routes.credentials import credentials_bp
from web_front.routes.routers import routers_bp
from web_front.routes.interfaces import interfaces_bp
from web_front.routes.users import users_bp
from web_front.routes.ospf import ospf_bp
from web_front.routes.areas import areas_bp
from web_front.routes.networks import networks_bp
from web_front.routes.main import main_bp

# List of all blueprints
blueprints = [
    auth_bp,
    devicetypes_bp,
    credentials_bp,
    routers_bp,
    interfaces_bp,
    users_bp,
    ospf_bp,
    areas_bp,
    networks_bp,
    main_bp
]
