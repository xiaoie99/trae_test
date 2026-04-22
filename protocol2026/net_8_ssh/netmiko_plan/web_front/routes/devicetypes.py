from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from web_front.utils import login_required
from web_front.forms import DeviceTypeForm
from web_front.models import DeviceType

devicetypes_bp = Blueprint('devicetypes', __name__, url_prefix='/devicetypes')

@devicetypes_bp.route('/')
@login_required
def devicetypes():
    db_session = current_app.extensions['db_session']
    devicetypes = db_session.query(DeviceType).all()
    return render_template('devicetypes.html', devicetypes=devicetypes)

@devicetypes_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_devicetype():
    db_session = current_app.extensions['db_session']
    form = DeviceTypeForm()
    if form.validate_on_submit():
        devicetype = DeviceType(device_type=form.device_type.data)
        db_session.add(devicetype)
        db_session.commit()
        flash('设备类型添加成功', 'success')
        return redirect(url_for('devicetypes.devicetypes'))
    return render_template('devicetype_form.html', form=form, title="添加设备类型")

@devicetypes_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_devicetype(id):
    db_session = current_app.extensions['db_session']
    devicetype = db_session.query(DeviceType).get(id)
    if not devicetype:
        flash('设备类型不存在', 'danger')
        return redirect(url_for('devicetypes.devicetypes'))
    
    form = DeviceTypeForm(obj=devicetype)
    if form.validate_on_submit():
        devicetype.device_type = form.device_type.data
        db_session.commit()
        flash('设备类型更新成功', 'success')
        return redirect(url_for('devicetypes.devicetypes'))
    return render_template('devicetype_form.html', form=form, title="编辑设备类型")

@devicetypes_bp.route('/delete/<int:id>')
@login_required
def delete_devicetype(id):
    db_session = current_app.extensions['db_session']
    devicetype = db_session.query(DeviceType).get(id)
    if devicetype:
        db_session.delete(devicetype)
        db_session.commit()
        flash('设备类型已删除', 'success')
    else:
        flash('设备类型不存在', 'danger')
    return redirect(url_for('devicetypes.devicetypes')) 