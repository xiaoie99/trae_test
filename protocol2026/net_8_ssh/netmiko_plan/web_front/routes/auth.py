from flask import Blueprint, render_template, redirect, url_for, flash, session
from web_front.forms import LoginForm

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# 登录页面
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        # 简单的用户验证，实际应用中应使用数据库存储用户
        if username == 'admin' and password == 'admin':
            session['logged_in'] = True
            session['username'] = username
            flash('登录成功', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('用户名或密码错误', 'danger')
    return render_template('login.html', form=form)

# 登出
@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('已登出', 'success')
    return redirect(url_for('auth.login')) 