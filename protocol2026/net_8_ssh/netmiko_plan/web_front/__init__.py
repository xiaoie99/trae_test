from flask import Flask
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os
import sys
from pathlib import Path

# 获取当前文件的路径
current_file_path = Path(__file__).resolve()

# 获取当前文件所在的目录路径
parent_dir = current_file_path.parent.parent
sys.path.append(str(parent_dir))

# 导入数据库模型
from netmiko_3_config_db_0_create_db import (
    Base, db_filename
)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'qytang-netdevops-secret-key'
    csrf = CSRFProtect(app)

    # 连接到数据库
    engine = create_engine(f'sqlite:///{db_filename}?check_same_thread=False')
    db_session = scoped_session(sessionmaker(autocommit=False,
                                            autoflush=False,
                                            bind=engine))

    # 确保数据库表存在
    Base.metadata.create_all(bind=engine)

    # 确保关闭数据库会话
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    # 注册蓝图
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

    app.register_blueprint(auth_bp)
    app.register_blueprint(devicetypes_bp)
    app.register_blueprint(credentials_bp)
    app.register_blueprint(routers_bp)
    app.register_blueprint(interfaces_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(ospf_bp)
    app.register_blueprint(areas_bp)
    app.register_blueprint(networks_bp)
    app.register_blueprint(main_bp)

    return app, db_session
