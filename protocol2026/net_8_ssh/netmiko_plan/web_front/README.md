# Netmiko Web Front

这是一个基于Flask的网络设备管理平台，用于管理和配置网络设备的前端接口。

## 项目结构

```
web_front/
├── __init__.py             # 应用初始化
├── forms.py                # 表单定义
├── models/                 # 数据模型
├── routes/                 # 路由模块
│   ├── __init__.py
│   ├── auth.py             # 认证相关路由
│   ├── main.py             # 主页相关路由
│   ├── devicetypes.py      # 设备类型管理
│   ├── credentials.py      # 登录凭证管理
│   ├── routers.py          # 路由器管理
│   ├── interfaces.py       # 接口管理
│   ├── users.py            # 用户管理
│   ├── ospf.py             # OSPF进程管理
│   ├── areas.py            # OSPF区域管理
│   └── networks.py         # OSPF网络管理
├── static/                 # 静态文件
├── templates/              # 模板文件
├── utils.py                # 工具函数
├── run.py                  # 应用启动脚本
└── requirements.txt        # 依赖包
```

## 功能模块

1. 认证模块 - 用户登录与登出
2. 设备类型管理 - 添加、编辑、删除设备类型
3. 登录凭证管理 - 添加、编辑、删除登录凭证
4. 路由器管理 - 添加、编辑、删除路由器设备
5. 接口管理 - 添加、编辑、删除路由器接口
6. 用户管理 - 添加、编辑、删除路由器用户
7. OSPF管理 - 添加、编辑、删除OSPF进程
8. OSPF区域管理 - 添加、编辑、删除OSPF区域
9. OSPF网络管理 - 添加、编辑、删除OSPF网络

## 安装与运行

1. 安装依赖包
   ```
   pip install -r requirements.txt
   ```

2. 运行应用
   ```
   python run.py
   ```

3. 访问网址
   ```
   http://127.0.0.1:5000
   ```

## 默认管理员账户

- 用户名: admin
- 密码: admin

## B站录像
  B站链接: https://www.bilibili.com/video/BV1z6o9YeEUh

## 更多信息

- 亁颐堂官网: www.qytang.com
- 教主VIP: https://vip.qytang.com
