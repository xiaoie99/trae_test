import sys, os, hashlib, time, datetime, re
# ---- 1. 复用第12天的 qytang_multicmd ----
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from day12_20260406.day12_task1_multicmd import qytang_multicmd
# ---- 2. SQLAlchemy ORM ----
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
engine = create_engine('sqlite:///router_config.db',
                       connect_args={'check_same_thread': False})
Base = declarative_base()
Session = sessionmaker(bind=engine)
class RouterConfig(Base):
    """路由器配置备份模型"""
    __tablename__ = 'router_config'
    id            = Column(Integer, primary_key=True)
    router_ip     = Column(String(64),    nullable=False, index=True)
    router_config = Column(String(99999), nullable=False)
    config_hash   = Column(String(500),   nullable=False)
    record_time   = Column(DateTime, default=datetime.datetime.now)
    def __repr__(self):
        return (f"{self.__class__.__name__}("
                f"路由器IP地址: {self.router_ip} | "
                f"配置Hash: {self.config_hash} | "
                f"记录时间: {self.record_time})")
Base.metadata.create_all(engine, checkfirst=True)
# ---- 3. 工具函数 ----
def get_show_run(host, username, password):
    """获取配置并计算 hash"""
    raw = qytang_multicmd(host, username, password,
                          ['terminal length 0', 'show running-config'],
                          verbose=False)
    # 将列表中的输出合并为一个字符串
    raw_text = '\n'.join(raw)
    match = re.search(r'(hostname[\s\S]+end)', raw_text)
    config = match.group(1) if match else raw_text  # 从 match 中取出配置文本
    config_hash = hashlib.sha256(config.encode('utf-8')).hexdigest()   # 对配置文本做 SHA256
    return config, config_hash
def save_config(host, config, config_hash):
    """写入数据库（使用独立 session，避免事务残留）"""
    with Session() as session:
        record = RouterConfig(router_ip=host, router_config=config, config_hash=config_hash)
        session.add(record)
        session.commit()
def get_latest_two_hashes(host):
    """查询最近两条记录"""
    with Session() as session:
        results = (session.query(RouterConfig)
                   .filter(RouterConfig.router_ip == host)            # 按 router_ip 过滤
                   .order_by(RouterConfig.id.desc())
                   .limit(2)
                   .all())
        return results
# ---- 4. 主循环 ----
if __name__ == '__main__':
    host     = '10.10.1.200'       # 换成自己的路由器
    username = 'admin'
    password = 'qwert@12345'
    print(f"[*] 开始监控 {host} 的配置变化，每 5 秒采集一次...\n")
    while True:
        config, config_hash = get_show_run(host, username, password)
        save_config(host, config, config_hash)
        records = get_latest_two_hashes(host)
        if len(records) < 2:
            print(f"本次采集的HASH:{config_hash}")
        elif records[0].config_hash == records[1].config_hash:
            print(f"本次采集的HASH:{config_hash}")    # 配置无变化，打印本次 hash
        else:
            print("==========配置发生变化==========")    # 配置有变化，打印告警及前后两次 hash
            print(f"  THE MOST RECENT HASH  {records[0].config_hash}")
            print(f"  THE LAST HASH         {records[1].config_hash}")
        time.sleep(5)