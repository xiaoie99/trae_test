from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from web_front.utils import login_required
from web_front.forms import UserForm
from web_front.models import User, Router

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('/router/<int:router_id>')
@login_required
def users(router_id):
    db_session = current_app.extensions['db_session']
    router = db_session.query(Router).get(router_id)
    if not router:
        flash('路由器不存在', 'danger')
        return redirect(url_for('routers.routers'))
    
    users = db_session.query(User).filter_by(router_id=router_id).all()
    return render_template('users.html', users=users, router=router)

@users_bp.route('/router/<int:router_id>/add', methods=['GET', 'POST'])
@login_required
def add_user(router_id):
    db_session = current_app.extensions['db_session']
    router = db_session.query(Router).get(router_id)
    if not router:
        flash('路由器不存在', 'danger')
        return redirect(url_for('routers.routers'))
    
    form = UserForm()
    if form.validate_on_submit():
        user = User(
            router_id=router_id,
            username=form.username.data,
            password=form.password.data,
            priv=form.priv.data
        )
        db_session.add(user)
        db_session.commit()
        flash('用户添加成功', 'success')
        return redirect(url_for('users.users', router_id=router_id))
    return render_template('user_form.html', form=form, router=router, title="添加用户")

@users_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    db_session = current_app.extensions['db_session']
    user = db_session.query(User).get(id)
    if not user:
        flash('用户不存在', 'danger')
        return redirect(url_for('routers.routers'))
    
    form = UserForm(obj=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.password = form.password.data
        user.priv = form.priv.data
        db_session.commit()
        flash('用户更新成功', 'success')
        return redirect(url_for('users.users', router_id=user.router_id))
    return render_template('user_form.html', form=form, router=user.router, title="编辑用户")

@users_bp.route('/delete/<int:id>')
@login_required
def delete_user(id):
    db_session = current_app.extensions['db_session']
    user = db_session.query(User).get(id)
    if not user:
        flash('用户不存在', 'danger')
        return redirect(url_for('routers.routers'))
    
    router_id = user.router_id
    db_session.delete(user)
    db_session.commit()
    flash('用户已删除', 'success')
    return redirect(url_for('users.users', router_id=router_id)) 