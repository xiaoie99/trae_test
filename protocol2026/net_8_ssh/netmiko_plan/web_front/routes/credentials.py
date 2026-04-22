from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from web_front.utils import login_required
from web_front.forms import CredentialForm
from web_front.models import LoginCredential

credentials_bp = Blueprint('credentials', __name__, url_prefix='/credentials')

@credentials_bp.route('/')
@login_required
def credentials():
    db_session = current_app.extensions['db_session']
    credentials = db_session.query(LoginCredential).all()
    return render_template('credentials.html', credentials=credentials)

@credentials_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_credential():
    db_session = current_app.extensions['db_session']
    form = CredentialForm()
    if form.validate_on_submit():
        credential = LoginCredential(
            credential_name=form.credential_name.data,
            username=form.username.data,
            password=form.password.data
        )
        db_session.add(credential)
        db_session.commit()
        flash('登录凭证添加成功', 'success')
        return redirect(url_for('credentials.credentials'))
    return render_template('credential_form.html', form=form, title="添加登录凭证")

@credentials_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_credential(id):
    db_session = current_app.extensions['db_session']
    credential = db_session.query(LoginCredential).get(id)
    if not credential:
        flash('登录凭证不存在', 'danger')
        return redirect(url_for('credentials.credentials'))
    
    form = CredentialForm(obj=credential)
    if form.validate_on_submit():
        credential.credential_name = form.credential_name.data
        credential.username = form.username.data
        credential.password = form.password.data
        db_session.commit()
        flash('登录凭证更新成功', 'success')
        return redirect(url_for('credentials.credentials'))
    return render_template('credential_form.html', form=form, title="编辑登录凭证")

@credentials_bp.route('/delete/<int:id>')
@login_required
def delete_credential(id):
    db_session = current_app.extensions['db_session']
    credential = db_session.query(LoginCredential).get(id)
    if credential:
        db_session.delete(credential)
        db_session.commit()
        flash('登录凭证已删除', 'success')
    else:
        flash('登录凭证不存在', 'danger')
    return redirect(url_for('credentials.credentials')) 