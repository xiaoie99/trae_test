from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from web_front.utils import login_required
from web_front.forms import OSPFProcessForm
from web_front.models import OSPFProcess, Router

ospf_bp = Blueprint('ospf', __name__, url_prefix='/ospf')

@ospf_bp.route('/router/<int:router_id>')
@login_required
def ospf(router_id):
    db_session = current_app.extensions['db_session']
    router = db_session.query(Router).get(router_id)
    if not router:
        flash('路由器不存在', 'danger')
        return redirect(url_for('routers.routers'))
    
    ospf_process = db_session.query(OSPFProcess).filter_by(router_id=router_id).first()
    return render_template('ospf.html', ospf_process=ospf_process, router=router)

@ospf_bp.route('/router/<int:router_id>/add', methods=['GET', 'POST'])
@login_required
def add_ospf(router_id):
    db_session = current_app.extensions['db_session']
    router = db_session.query(Router).get(router_id)
    if not router:
        flash('路由器不存在', 'danger')
        return redirect(url_for('routers.routers'))
    
    # 检查是否已存在OSPF进程
    existing_ospf = db_session.query(OSPFProcess).filter_by(router_id=router_id).first()
    if existing_ospf:
        flash('该路由器已有OSPF进程，请编辑现有进程', 'warning')
        return redirect(url_for('ospf.ospf', router_id=router_id))
    
    form = OSPFProcessForm()
    if form.validate_on_submit():
        ospf_process = OSPFProcess(
            router_id=router_id,
            processid=form.processid.data,
            routerid=form.routerid.data
        )
        db_session.add(ospf_process)
        db_session.commit()
        flash('OSPF进程添加成功', 'success')
        return redirect(url_for('ospf.ospf', router_id=router_id))
    return render_template('ospf_form.html', form=form, router=router, title="添加OSPF进程")

@ospf_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_ospf(id):
    db_session = current_app.extensions['db_session']
    ospf_process = db_session.query(OSPFProcess).get(id)
    if not ospf_process:
        flash('OSPF进程不存在', 'danger')
        return redirect(url_for('routers.routers'))
    
    form = OSPFProcessForm(obj=ospf_process)
    if form.validate_on_submit():
        ospf_process.processid = form.processid.data
        ospf_process.routerid = form.routerid.data
        db_session.commit()
        flash('OSPF进程更新成功', 'success')
        return redirect(url_for('ospf.ospf', router_id=ospf_process.router_id))
    return render_template('ospf_form.html', form=form, router=ospf_process.router, title="编辑OSPF进程")

@ospf_bp.route('/delete/<int:id>')
@login_required
def delete_ospf(id):
    db_session = current_app.extensions['db_session']
    ospf_process = db_session.query(OSPFProcess).get(id)
    if not ospf_process:
        flash('OSPF进程不存在', 'danger')
        return redirect(url_for('routers.routers'))
    
    router_id = ospf_process.router_id
    db_session.delete(ospf_process)
    db_session.commit()
    flash('OSPF进程已删除', 'success')
    return redirect(url_for('ospf.ospf', router_id=router_id)) 