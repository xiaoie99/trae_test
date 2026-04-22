from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from web_front.utils import login_required
from web_front.forms import AreaForm
from web_front.models import Area, OSPFProcess

areas_bp = Blueprint('areas', __name__, url_prefix='/areas')

@areas_bp.route('/ospf/<int:ospf_id>')
@login_required
def areas(ospf_id):
    db_session = current_app.extensions['db_session']
    ospf_process = db_session.query(OSPFProcess).get(ospf_id)
    if not ospf_process:
        flash('OSPF进程不存在', 'danger')
        return redirect(url_for('routers.routers'))
    
    areas = db_session.query(Area).filter_by(ospfprocess_id=ospf_id).all()
    return render_template('areas.html', areas=areas, ospf_process=ospf_process)

@areas_bp.route('/ospf/<int:ospf_id>/add', methods=['GET', 'POST'])
@login_required
def add_area(ospf_id):
    db_session = current_app.extensions['db_session']
    ospf_process = db_session.query(OSPFProcess).get(ospf_id)
    if not ospf_process:
        flash('OSPF进程不存在', 'danger')
        return redirect(url_for('routers.routers'))
    
    form = AreaForm()
    if form.validate_on_submit():
        area = Area(
            ospfprocess_id=ospf_id,
            area_id=form.area_id.data
        )
        db_session.add(area)
        db_session.commit()
        flash('OSPF区域添加成功', 'success')
        return redirect(url_for('areas.areas', ospf_id=ospf_id))
    return render_template('area_form.html', form=form, ospf_process=ospf_process, title="添加OSPF区域")

@areas_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_area(id):
    db_session = current_app.extensions['db_session']
    area = db_session.query(Area).get(id)
    if not area:
        flash('OSPF区域不存在', 'danger')
        return redirect(url_for('routers.routers'))
    
    form = AreaForm(obj=area)
    if form.validate_on_submit():
        area.area_id = form.area_id.data
        db_session.commit()
        flash('OSPF区域更新成功', 'success')
        return redirect(url_for('areas.areas', ospf_id=area.ospfprocess_id))
    return render_template('area_form.html', form=form, ospf_process=area.ospf_process, title="编辑OSPF区域")

@areas_bp.route('/delete/<int:id>')
@login_required
def delete_area(id):
    db_session = current_app.extensions['db_session']
    area = db_session.query(Area).get(id)
    if not area:
        flash('OSPF区域不存在', 'danger')
        return redirect(url_for('routers.routers'))
    
    ospf_id = area.ospfprocess_id
    db_session.delete(area)
    db_session.commit()
    flash('OSPF区域已删除', 'success')
    return redirect(url_for('areas.areas', ospf_id=ospf_id)) 