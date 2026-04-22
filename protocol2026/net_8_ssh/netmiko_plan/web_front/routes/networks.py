from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from web_front.utils import login_required
from web_front.forms import NetworkForm
from web_front.models import OSPFNetwork, Area

networks_bp = Blueprint('networks', __name__, url_prefix='/networks')

@networks_bp.route('/area/<int:area_id>')
@login_required
def networks(area_id):
    db_session = current_app.extensions['db_session']
    area = db_session.query(Area).get(area_id)
    if not area:
        flash('OSPF区域不存在', 'danger')
        return redirect(url_for('routers.routers'))
    
    networks = db_session.query(OSPFNetwork).filter_by(area_id=area_id).all()
    return render_template('networks.html', networks=networks, area=area)

@networks_bp.route('/area/<int:area_id>/add', methods=['GET', 'POST'])
@login_required
def add_network(area_id):
    db_session = current_app.extensions['db_session']
    area = db_session.query(Area).get(area_id)
    if not area:
        flash('OSPF区域不存在', 'danger')
        return redirect(url_for('routers.routers'))
    
    form = NetworkForm()
    if form.validate_on_submit():
        network = OSPFNetwork(
            area_id=area_id,
            network=form.network.data,
            wildmask=form.wildmask.data
        )
        db_session.add(network)
        db_session.commit()
        flash('OSPF网络添加成功', 'success')
        return redirect(url_for('networks.networks', area_id=area_id))
    return render_template('network_form.html', form=form, area=area, title="添加OSPF网络")

@networks_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_network(id):
    db_session = current_app.extensions['db_session']
    network = db_session.query(OSPFNetwork).get(id)
    if not network:
        flash('OSPF网络不存在', 'danger')
        return redirect(url_for('routers.routers'))
    
    form = NetworkForm(obj=network)
    if form.validate_on_submit():
        network.network = form.network.data
        network.wildmask = form.wildmask.data
        db_session.commit()
        flash('OSPF网络更新成功', 'success')
        return redirect(url_for('networks.networks', area_id=network.area_id))
    return render_template('network_form.html', form=form, area=network.area, title="编辑OSPF网络")

@networks_bp.route('/delete/<int:id>')
@login_required
def delete_network(id):
    db_session = current_app.extensions['db_session']
    network = db_session.query(OSPFNetwork).get(id)
    if not network:
        flash('OSPF网络不存在', 'danger')
        return redirect(url_for('routers.routers'))
    
    area_id = network.area_id
    db_session.delete(network)
    db_session.commit()
    flash('OSPF网络已删除', 'success')
    return redirect(url_for('networks.networks', area_id=area_id)) 