#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于亁颐堂NetDevOps课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主VIP, 让我们聊点高级的
# https://vip.qytang.com/


# SQLAlchemy相关导入
from sqlalchemy import create_engine  # 创建数据库引擎
from sqlalchemy.orm import declarative_base, relationship  # ORM基类和关系函数

# 数据库列类型和外键
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
import datetime  # 处理日期时间
from pathlib import Path  # 处理文件路径
import os  # 操作系统接口

# 获取当前文件的路径
current_file_path = Path(__file__).resolve()

# 获取当前文件所在的目录路径
current_dir = current_file_path.parent

# 定义SQLite数据库文件的路径
db_filename = f'{current_dir}{os.sep}config-devices-info-db{os.sep}router_config_sqlite3.db'

# 创建SQLAlchemy基类，所有模型类都将继承此类
Base = declarative_base()

# B站录像
# https://www.bilibili.com/video/BV1z6o9YeEUh


class Router(Base):
    """路由器表：核心表，存储路由器基本信息"""
    __tablename__ = 'router'  # 数据库表名

    id = Column(Integer, primary_key=True)  # 主键ID
    routername = Column(String(64), nullable=False, index=True)  # 路由器名称，建立索引
    ip = Column(String(64), nullable=False, index=True)  # 路由器IP地址，建立索引
    
    # ~~~关联LoginCredential~~~
    login_credential_id = Column(Integer, ForeignKey("login_credential.id", ondelete='CASCADE'), nullable=True)  # 外键，关联登录凭证
    login_credential = relationship('LoginCredential', back_populates="router", passive_deletes=True)  # 建立双向关系
    
    # ~~~关联DeviceType~~~
    device_type_id = Column(Integer, ForeignKey("device_type.id", ondelete='CASCADE'), nullable=True)  # 外键，关联设备类型
    device_type = relationship('DeviceType', back_populates="router", passive_deletes=True)  # 建立双向关系
    
    # ~~~关联Interface~~~
    # 一对多关系，一台路由器有多个接口
    interface = relationship('Interface', back_populates="router", passive_deletes=True)
    
    # ~~~关联OSPFProcess~~~
    # 一对一关系(uselist=False)，一台路由器只有一个OSPF进程
    ospf_process = relationship('OSPFProcess', back_populates="router", uselist=False, passive_deletes=True)
    
    # ~~~关联CPUUsage~~~
    # 一对多关系，一台路由器有多条CPU使用记录
    cpu_usage = relationship('CPUUsage', back_populates="router", passive_deletes=True)
    
    # ~~~关联User~~~
    # 一对多关系，一台路由器可以有多个用户账号
    user = relationship('User', back_populates="router", passive_deletes=True)
    
    def to_dict(self):
        """将对象转换为字典，用于Jinja2模板渲染和JSON序列化"""
        return {
            'device_ip': self.ip,
            'username': self.login_credential.username,
            'password': self.login_credential.password,
            'device_type': self.device_type.device_type,
            'interfaces_list': [interface.to_dict() for interface in self.interface] if self.interface else [],
            'ospf_dict': self.ospf_process.to_dict() if self.ospf_process else None,
            'create_users_list': [user.to_dict() for user in self.user] if self.user else [],
        }
    def __repr__(self):
        """对象的字符串表示，用于日志和调试"""
        return f"{self.__class__.__name__}({self.routername})"


class DeviceType(Base):
    """设备类型表：存储网络设备的类型信息（如cisco_ios, juniper_junos等）"""
    __tablename__ = 'device_type'

    id = Column(Integer, primary_key=True)  # 主键ID
    device_type = Column(String(64), nullable=False)  # 设备类型名称
    # 一对多关系，一种设备类型可以对应多台路由器
    router = relationship('Router', back_populates="device_type", passive_deletes=True)

    def __repr__(self):
        """对象的字符串表示"""
        return f"{self.__class__.__name__}({self.device_type})"


class LoginCredential(Base):
    """登录凭证表：存储设备的登录认证信息"""
    __tablename__ = 'login_credential'

    id = Column(Integer, primary_key=True)  # 主键ID
    credential_name = Column(String(64), nullable=False)  # 凭证名称
    username = Column(String(64), nullable=False)  # 用户名
    password = Column(String(64), nullable=False)  # 密码
    # 一对多关系，一组凭证可以被多台路由器使用
    router = relationship('Router', back_populates="login_credential", passive_deletes=True)

    def __repr__(self):
        """对象的字符串表示"""
        return f"{self.__class__.__name__}(Credential: {self.credential_name} "\
               f"| Username: {self.username} " \
               f"| Password: {self.password})"


class User(Base):
    """用户表：存储路由器上配置的用户账号"""
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)  # 主键ID
    router_id = Column(Integer, ForeignKey("router.id", ondelete='CASCADE'), nullable=False)  # 外键，关联路由器
    username = Column(String(64), nullable=False)  # 用户名
    password = Column(String(64), nullable=False)  # 密码
    priv = Column(Integer, nullable=False)  # 权限级别
    # 多对一关系，多个用户属于一台路由器
    router = relationship('Router', back_populates="user", passive_deletes=True)

    def to_dict(self):
        """将对象转换为字典"""
        return {
            'username': self.username,
            'password': self.password,
            'priv': self.priv
        }
        
    def __repr__(self):
        """对象的字符串表示"""
        return f"{self.__class__.__name__}(Router: {self.router.routername} "\
               f"| Username: {self.username} " \
               f"| Password: {self.password} " \
               f"| Priv: {self.priv})"
               
               
class Interface(Base):
    """接口表：存储路由器的网络接口信息"""
    __tablename__ = 'interface'

    id = Column(Integer, primary_key=True)  # 主键ID
    router_id = Column(Integer, ForeignKey("router.id", ondelete='CASCADE'), nullable=False)  # 外键，关联路由器
    interface_name = Column(String(64), nullable=False)  # 接口名称，如GigabitEthernet0/0
    ip = Column(String(64), nullable=False)  # IP地址
    mask = Column(String(64), nullable=False)  # 子网掩码
    # 多对一关系，多个接口属于一台路由器
    router = relationship('Router', back_populates="interface", passive_deletes=True)

    def to_dict(self):
        """将对象转换为字典"""
        return {
            'interface_name': self.interface_name,
            'ip': self.ip,
            'mask': self.mask
        }

    def __repr__(self):
        """对象的字符串表示"""
        return f"{self.__class__.__name__}(Router: {self.router.routername} "\
               f"| Interface_name: {self.interface_name} " \
               f"| IP: {self.ip} / {self.mask})"


class CPUUsage(Base):
    """CPU使用率表：存储路由器CPU使用情况的历史记录"""
    __tablename__ = 'cpu_usage'

    id = Column(Integer, primary_key=True)  # 主键ID
    router_id = Column(Integer, ForeignKey("router.id", ondelete='CASCADE'), nullable=False)  # 外键，关联路由器
    cpu_useage_percent = Column(Integer, nullable=False)  # CPU使用百分比
    cpu_useage_datetime = Column(DateTime(timezone='Asia/Chongqing'), default=datetime.datetime.now)  # 记录时间
    # 多对一关系，多条CPU记录属于一台路由器
    router = relationship('Router', back_populates="cpu_usage", passive_deletes=True)

    def __repr__(self):
        """对象的字符串表示"""
        return f"{self.__class__.__name__}(Router: {self.router.routername} " \
               f"| Datetime: {self.cpu_useage_datetime} " \
               f"| Percent: {self.cpu_useage_percent})"


class OSPFProcess(Base):
    """OSPF进程表：存储路由器的OSPF路由进程信息"""
    __tablename__ = 'ospf_process'

    id = Column(Integer, primary_key=True)  # 主键ID
    router_id = Column(Integer, ForeignKey("router.id", ondelete='CASCADE'), nullable=False)  # 外键，关联路由器
    processid = Column(Integer, nullable=False)  # OSPF进程ID
    routerid = Column(String(64), nullable=False)  # OSPF路由器ID
    # 多对一关系，OSPF进程属于一台路由器
    router = relationship('Router', back_populates="ospf_process", passive_deletes=True)
    # 一对多关系，一个OSPF进程有多个区域
    area = relationship('Area', back_populates="ospf_process", passive_deletes=True)

    def to_dict(self):
        """将对象转换为字典，包含完整的OSPF配置"""
        ospf_dict = {'process_id': self.processid,
                     'router_id': self.routerid,}
        network_list = []
        # 遍历所有区域和网络，构建配置信息
        for area in self.area:
            for network in area.ospf_network:
                network_list.append({
                    'network': network.network,
                    'wildcard_mask': network.wildmask,
                    'area': area.area_id
                })
        ospf_dict['network_list'] = network_list
        return ospf_dict

    def __repr__(self):
        """对象的字符串表示"""
        return f"{self.__class__.__name__}(Router: {self.router.routername} " \
               f"| Process: {self.processid})"


class Area(Base):
    """OSPF区域表：存储OSPF进程中配置的区域信息"""
    __tablename__ = 'area'

    id = Column(Integer, primary_key=True)  # 主键ID
    ospfprocess_id = Column(Integer, ForeignKey("ospf_process.id", ondelete='CASCADE'), nullable=False)  # 外键，关联OSPF进程
    area_id = Column(Integer, nullable=False)  # 区域ID，如0表示骨干区域
    # 多对一关系，多个区域属于一个OSPF进程
    ospf_process = relationship('OSPFProcess', back_populates="area", passive_deletes=True)
    # 一对多关系，一个区域包含多个网络
    ospf_network = relationship('OSPFNetwork', back_populates="area", passive_deletes=True)

    def __repr__(self):
        """对象的字符串表示"""
        return f"{self.__class__.__name__}(Router: {self.ospf_process.router.routername} " \
               f"| Process: {self.ospf_process.processid} " \
               f"| Area: {self.area_id})"


class OSPFNetwork(Base):
    """OSPF网络表：存储OSPF区域中配置的网络信息"""
    __tablename__ = 'ospf_network'

    id = Column(Integer, primary_key=True)  # 主键ID
    area_id = Column(Integer, ForeignKey("area.id", ondelete='CASCADE'), nullable=False)  # 外键，关联区域
    network = Column(String(64), nullable=False)  # 网络地址
    wildmask = Column(String(64), nullable=False)  # 通配符掩码
    # 多对一关系，多个网络属于一个区域
    area = relationship('Area', back_populates="ospf_network", passive_deletes=True)

    def __repr__(self):
        """对象的字符串表示，包含完整路径信息"""
        return f"{self.__class__.__name__}(Router: {self.area.ospf_process.router.routername} " \
               f"| Process: {self.area.ospf_process.processid} " \
               f"| Area: {self.area.area_id} " \
               f"| Network: {self.network}/{self.wildmask})"


if __name__ == '__main__':
    # 如果数据库文件已存在则删除，确保每次运行创建全新的数据库
    if os.path.exists(db_filename):
        os.remove(db_filename)

    # 创建SQLite数据库引擎
    # check_same_thread=False允许在多线程环境中使用同一连接
    engine = create_engine(f'sqlite:///{db_filename}?check_same_thread=False',
                            # echo=True  # 设置为True可以显示SQL语句，用于调试
                            )
    # 创建所有表，checkfirst=True表示如果表已存在则不重复创建
    Base.metadata.create_all(engine, checkfirst=True)
