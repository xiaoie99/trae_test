from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, IPAddress, ValidationError, InputRequired

class LoginForm(FlaskForm):
    """用户登录表单"""
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('登录')

class DeviceTypeForm(FlaskForm):
    """设备类型表单"""
    device_type = StringField('设备类型', validators=[DataRequired()], 
                            description="例如：cisco_ios, juniper_junos")
    submit = SubmitField('保存')

class CredentialForm(FlaskForm):
    """登录凭证表单"""
    credential_name = StringField('凭证名称', validators=[DataRequired()], 
                                description="例如：管理员凭证, 监控凭证")
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('保存')

class RouterForm(FlaskForm):
    """路由器表单"""
    routername = StringField('路由器名称', validators=[DataRequired()])
    ip = StringField('IP地址', validators=[DataRequired(), IPAddress()])
    login_credential_id = SelectField('登录凭证', coerce=int, validators=[DataRequired()])
    device_type_id = SelectField('设备类型', coerce=int, validators=[DataRequired()])
    submit = SubmitField('保存')

class InterfaceForm(FlaskForm):
    """接口表单"""
    interface_name = StringField('接口名称', validators=[DataRequired()], 
                              description="例如：GigabitEthernet0/0, Loopback0")
    ip = StringField('IP地址', validators=[DataRequired(), IPAddress()])
    mask = StringField('子网掩码', validators=[DataRequired()], 
                    description="例如：255.255.255.0")
    submit = SubmitField('保存')
    
    def validate_mask(self, field):
        """验证子网掩码格式"""
        parts = field.data.split('.')
        if len(parts) != 4:
            raise ValidationError('子网掩码必须是四段式格式')
        for part in parts:
            try:
                num = int(part)
                if num < 0 or num > 255:
                    raise ValidationError('子网掩码每段数值必须在0-255之间')
            except ValueError:
                raise ValidationError('子网掩码必须是数字')

class UserForm(FlaskForm):
    """路由器用户表单"""
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    priv = IntegerField('权限级别', validators=[DataRequired()], 
                      description="例如：15表示管理员权限")
    submit = SubmitField('保存')
    
    def validate_priv(self, field):
        """验证权限级别在有效范围内"""
        if field.data < 0 or field.data > 15:
            raise ValidationError('权限级别必须在0-15之间')

class OSPFProcessForm(FlaskForm):
    """OSPF进程表单"""
    processid = IntegerField('进程ID', validators=[DataRequired()], 
                          description="例如：1")
    routerid = StringField('路由器ID', validators=[DataRequired(), IPAddress()], 
                        description="例如：1.1.1.1")
    submit = SubmitField('保存')

class AreaForm(FlaskForm):
    """OSPF区域表单"""
    area_id = IntegerField('区域ID', validators=[InputRequired()], 
                        description="例如：0表示骨干区域")
    submit = SubmitField('保存')
    
    def validate_area_id(self, field):
        """验证区域ID在有效范围内"""
        if field.data is None:
            raise ValidationError('区域ID不能为空')
        if field.data < 0 or field.data > 4294967295:
            raise ValidationError('区域ID必须在0-4294967295之间')

class NetworkForm(FlaskForm):
    """OSPF网络表单"""
    network = StringField('网络地址', validators=[DataRequired(), IPAddress()], 
                       description="例如：192.168.1.0")
    wildmask = StringField('通配符掩码', validators=[DataRequired()], 
                        description="例如：0.0.0.255")
    submit = SubmitField('保存')
    
    def validate_wildmask(self, field):
        """验证通配符掩码格式"""
        parts = field.data.split('.')
        if len(parts) != 4:
            raise ValidationError('通配符掩码必须是四段式格式')
        for part in parts:
            try:
                num = int(part)
                if num < 0 or num > 255:
                    raise ValidationError('通配符掩码每段数值必须在0-255之间')
            except ValueError:
                raise ValidationError('通配符掩码必须是数字')