from flask import Blueprint, render_template
from web_front.utils import login_required
from web_front.models import Router, DeviceType, LoginCredential, Interface, User, OSPFProcess

main_bp = Blueprint('main', __name__)

# 首页
@main_bp.route('/')
@login_required
def index():
    # 从应用上下文中获取数据库会话
    from flask import current_app
    db_session = current_app.extensions['db_session']
    
    routers_count = db_session.query(Router).count()
    devicetypes_count = db_session.query(DeviceType).count()
    credentials_count = db_session.query(LoginCredential).count()
    interfaces_count = db_session.query(Interface).count()
    users_count = db_session.query(User).count()
    ospf_count = db_session.query(OSPFProcess).count()
    
    return render_template('index.html', 
                          routers_count=routers_count,
                          devicetypes_count=devicetypes_count,
                          credentials_count=credentials_count,
                          interfaces_count=interfaces_count,
                          users_count=users_count,
                          ospf_count=ospf_count) 