from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from web_front.utils import login_required
from web_front.forms import InterfaceForm
from web_front.models import Interface, Router

interfaces_bp = Blueprint('interfaces', __name__, url_prefix='/interfaces')

@interfaces_bp.route('/router/<int:router_id>')
@login_required
def interfaces(router_id):
    db_session = current_app.extensions['db_session']
    router = db_session.query(Router).get(router_id)
    if not router:
        flash('路由器不存在', 'danger')
        return redirect(url_for('routers.routers'))
    
    interfaces = db_session.query(Interface).filter_by(router_id=router_id).all()
    return render_template('interfaces.html', interfaces=interfaces, router=router)

@interfaces_bp.route('/router/<int:router_id>/add', methods=['GET', 'POST'])
@login_required
def add_interface(router_id):
    db_session = current_app.extensions['db_session']
    router = db_session.query(Router).get(router_id)
    if not router:
        flash('路由器不存在', 'danger')
        return redirect(url_for('routers.routers'))
    
    form = InterfaceForm()
    if form.validate_on_submit():
        interface = Interface(
            router_id=router_id,
            interface_name=form.interface_name.data,
            ip=form.ip.data,
            mask=form.mask.data
        )
        db_session.add(interface)
        db_session.commit()
        flash('接口添加成功', 'success')
        return redirect(url_for('interfaces.interfaces', router_id=router_id))
    return render_template('interface_form.html', form=form, router=router, title="添加接口")

@interfaces_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_interface(id):
    db_session = current_app.extensions['db_session']
    interface = db_session.query(Interface).get(id)
    if not interface:
        flash('接口不存在', 'danger')
        return redirect(url_for('routers.routers'))
    
    form = InterfaceForm(obj=interface)
    if form.validate_on_submit():
        interface.interface_name = form.interface_name.data
        interface.ip = form.ip.data
        interface.mask = form.mask.data
        db_session.commit()
        flash('接口更新成功', 'success')
        return redirect(url_for('interfaces.interfaces', router_id=interface.router_id))
    return render_template('interface_form.html', form=form, router=interface.router, title="编辑接口")

@interfaces_bp.route('/delete/<int:id>')
@login_required
def delete_interface(id):
    db_session = current_app.extensions['db_session']
    interface = db_session.query(Interface).get(id)
    if not interface:
        flash('接口不存在', 'danger')
        return redirect(url_for('routers.routers'))
    
    router_id = interface.router_id
    db_session.delete(interface)
    db_session.commit()
    flash('接口已删除', 'success')
    return redirect(url_for('interfaces.interfaces', router_id=router_id)) 