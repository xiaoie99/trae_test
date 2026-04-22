from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from web_front.utils import login_required
from web_front.forms import RouterForm
from web_front.models import Router, LoginCredential, DeviceType

routers_bp = Blueprint('routers', __name__, url_prefix='/routers')

@routers_bp.route('/')
@login_required
def routers():
    db_session = current_app.extensions['db_session']
    routers = db_session.query(Router).all()
    return render_template('routers.html', routers=routers)

@routers_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_router():
    db_session = current_app.extensions['db_session']
    form = RouterForm()
    # 获取所有登录凭证和设备类型
    form.login_credential_id.choices = [(c.id, c.credential_name) for c in db_session.query(LoginCredential).all()]
    form.device_type_id.choices = [(d.id, d.device_type) for d in db_session.query(DeviceType).all()]
    
    if form.validate_on_submit():
        router = Router(
            routername=form.routername.data,
            ip=form.ip.data,
            login_credential_id=form.login_credential_id.data,
            device_type_id=form.device_type_id.data
        )
        db_session.add(router)
        db_session.commit()
        flash('路由器添加成功', 'success')
        return redirect(url_for('routers.routers'))
    return render_template('router_form.html', form=form, title="添加路由器")

@routers_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_router(id):
    db_session = current_app.extensions['db_session']
    router = db_session.query(Router).get(id)
    if not router:
        flash('路由器不存在', 'danger')
        return redirect(url_for('routers.routers'))
    
    form = RouterForm(obj=router)
    form.login_credential_id.choices = [(c.id, c.credential_name) for c in db_session.query(LoginCredential).all()]
    form.device_type_id.choices = [(d.id, d.device_type) for d in db_session.query(DeviceType).all()]
    
    if form.validate_on_submit():
        router.routername = form.routername.data
        router.ip = form.ip.data
        router.login_credential_id = form.login_credential_id.data
        router.device_type_id = form.device_type_id.data
        db_session.commit()
        flash('路由器更新成功', 'success')
        return redirect(url_for('routers.routers'))
    return render_template('router_form.html', form=form, title="编辑路由器")

@routers_bp.route('/delete/<int:id>')
@login_required
def delete_router(id):
    db_session = current_app.extensions['db_session']
    router = db_session.query(Router).get(id)
    if router:
        db_session.delete(router)
        db_session.commit()
        flash('路由器已删除', 'success')
    else:
        flash('路由器不存在', 'danger')
    return redirect(url_for('routers.routers')) 