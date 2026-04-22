### 下面的报错,需要降级pysnmp到6.1.4
```shell
(protocol2022) [root@AIOps pyats]# pyats parse "show ip ospf nei" --testbed-file ../top.yaml --output ./pyats_files/netdevops_ospf_nei_snapshot
Traceback (most recent call last):
  File "/root/.virtualenvs/protocol2022/bin/pyats", line 8, in <module>
    sys.exit(main())
             ^^^^^^
  File "src/pyats/cli/__main__.py", line 35, in pyats.cli.__main__.main
  File "src/pyats/cli/core.py", line 38, in pyats.cli.core.CLI.__init__
  File "src/pyats/cli/core.py", line 79, in pyats.cli.core.CLI.load_commands
  File "/root/.virtualenvs/protocol2022/lib64/python3.11/site-packages/pkg_resources/__init__.py", line 2470, in load
    self.require(*args, **kwargs)
  File "/root/.virtualenvs/protocol2022/lib64/python3.11/site-packages/pkg_resources/__init__.py", line 2493, in require
    items = working_set.resolve(reqs, env, installer, extras=self.extras)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/root/.virtualenvs/protocol2022/lib64/python3.11/site-packages/pkg_resources/__init__.py", line 800, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (pysnmp 7.1.16 (/root/.virtualenvs/protocol2022/lib/python3.11/site-packages), Requirement.parse('pysnmp<6.2,>=6.1.4'), {'genie.libs.sdk'})
```

### C8Kv1配置
```shell
router ospf 1
 router-id 1.1.1.1
 network 1.1.1.0 0.0.0.255 area 0
 network 10.1.1.0 0.0.0.255 area 0
!
interface GigabitEthernet2
 ip address 10.1.1.1 255.255.255.0
!
interface Loopback0
 ip address 1.1.1.1 255.255.255.0
```

### C8Kv2配置
```shell
router ospf 1
 router-id 2.2.2.2
 network 2.2.2.0 0.0.0.255 area 0
 network 10.1.1.0 0.0.0.255 area 0
!
interface GigabitEthernet2
 ip address 10.1.1.2 255.255.255.0
!
interface Loopback0
 ip address 2.2.2.2 255.255.255.0
```

### 制造快照(show ip ospf nei)
```shell
pyats parse "show ip ospf nei" --testbed-file ../top.yaml --output ./pyats_files/ospf_nei_snapshot
```

### 制造快照(show ip route ospf)
```shell
pyats parse "show ip route ospf" --testbed-file ../top.yaml --output ./pyats_files/ip_route_ospf_snapshot
```

### C8Kv1配置
```shell
router ospf 1
 router-id 1.1.1.1
 network 1.1.1.0 0.0.0.255 area 0
 network 10.1.1.0 0.0.0.255 area 0
 network 11.1.1.0 0.0.0.255 area 0
!
interface GigabitEthernet2
 ip address 10.1.1.1 255.255.255.0
!
interface Loopback0
 ip address 1.1.1.1 255.255.255.0
!
interface Loopback1
 ip address 11.1.1.1 255.255.255.0
```

### C8Kv2配置
```shell
router ospf 1
 router-id 22.2.2.2
 network 2.2.2.0 0.0.0.255 area 0
 network 10.1.1.0 0.0.0.255 area 0
 network 22.2.2.0 0.0.0.255 area 0
!
interface GigabitEthernet2
 ip address 10.1.1.2 255.255.255.0
!
interface Loopback0
 ip address 2.2.2.2 255.255.255.0
!
interface Loopback1
 ip address 22.2.2.2 255.255.255.0
```

### 制造快照(show ip ospf nei)
```shell
pyats parse "show ip ospf nei" --testbed-file ../top.yaml --output ./pyats_files/netdevops_ospf_nei_snapshot
```

### 快照对比(show ip ospf nei) <尝试去改router-id制造diff>
```shell
pyats diff ./pyats_files/ospf_nei_snapshot ./pyats_files/netdevops_ospf_nei_snapshot 
```

### 制造快照(show ip route ospf)
```shell
pyats parse "show ip route ospf" --testbed-file ../top.yaml --output ./pyats_files/netdevops_ip_route_ospf_snapshot
```

### 快照对比(show ip route ospf) <只是让宣告的网络不同即可>
```shell
pyats diff ./pyats_files/ip_route_ospf_snapshot ./pyats_files/netdevops_ip_route_ospf_snapshot 
```