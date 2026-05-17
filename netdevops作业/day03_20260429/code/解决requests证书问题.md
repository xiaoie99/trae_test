# 解决 requests 证书校验问题

## 微软证书服务器 vs Linux 替代方案

作业里的「微软证书服务器申请证书」是在 Windows AD CS 上签发**企业根 CA + 服务器证书**，本质是 PKI（公钥基础设施）流程，与操作系统无关。

在 Linux 上可以用下面两种方式**等价模拟**，不必搭建 Windows 证书服务器。

| 方式 | 说明 | 课件参考 |
|------|------|----------|
| **cfssl**（推荐，与老师 cfssl 文档一致） | 自建 CA，再签发 `fastapi.netdevops.com` 证书 | `netdevops课件/.../restapi_4_fastapi/linux签发证书.md` |
| **openssl**（更简单） | 下面脚本已用于生成本作业目录中的证书 | 本节命令 |

本作业目录已包含用 **openssl** 生成的：

- `code/ca.crt` — 根证书（相当于企业根 CA）
- `code/fastapi/fastapi.crt` — 服务器证书
- `code/fastapi/fastapi.key` — 服务器私钥

如需重新生成，在 Linux 上执行：

```bash
mkdir -p /opt/certs && cd /opt/certs
# 1. 生成根 CA（相当于微软「企业根 CA」）
openssl genrsa -out ca.key 4096
openssl req -new -x509 -days 3650 -key ca.key -out ca.crt \
  -subj "/C=CN/ST=beijing/L=beijing/O=qytang/CN=qytca"
# 2. 生成服务器私钥与 CSR
openssl genrsa -out fastapi.key 2048
openssl req -new -key fastapi.key -out fastapi.csr \
  -subj "/C=CN/ST=beijing/L=beijing/O=qytang/OU=qytangnetdevops/CN=fastapi.netdevops.com"
# 3. 用根 CA 签发服务器证书（SAN 必须包含访问域名）
cat > fastapi.ext <<EOF
subjectAltName=DNS:fastapi.netdevops.com,IP:127.0.0.1
EOF
openssl x509 -req -days 3650 -in fastapi.csr -CA ca.crt -CAkey ca.key \
  -CAcreateserial -out fastapi.crt -extfile fastapi.ext
```

将 `fastapi.crt`、`fastapi.key` 放入 `code/fastapi/`，`ca.crt` 放入 `code/` 供客户端校验。

---

## 客户端如何让 requests 信任证书（禁止 verify=False）

`day3_client.py` 使用：

```python
requests.post(url, json=obj, verify=CA_CERT)  # CA_CERT 指向 code/ca.crt
```

这样**会校验证书**，且信任自签根 CA。

### 方式 A：代码里指定根证书（本作业已采用）

与 `verify='ca.crt'` 路径等价，最简单。

### 方式 B：写入系统 / Python certifi 信任库（课件「加载企业级根证书」）

```bash
# 系统级（Rocky/RHEL）
cp code/ca.crt /etc/pki/ca-trust/source/anchors/labca.crt
update-ca-trust extract

# 或写入 venv 的 certifi（课件 spider 文档做法）
python3 -c "import certifi; print(certifi.where())"
cat code/ca.crt >> $(python3 -c "import certifi; print(certifi.where())")
```

之后 `requests.post(url, verify=True)` 也可通过校验。

---

## 你需要自己完成的操作

1. **no_proxy 必须包含本地域名**（否则会走 `http_proxy`，HTTPS 握手失败报 `UNEXPECTED_EOF`）：
   ```bash
   export no_proxy="localhost,127.0.0.1,10.10.0.0/16,fastapi.netdevops.com"
   export NO_PROXY="$no_proxy"
   ```
   `day3_client.py` 已自动追加 `fastapi.netdevops.com`；也可写入 `~/.bashrc` 永久生效。

2. **/etc/hosts** 增加解析（把域名指到跑 docker 的机器 IP）：
   ```
   127.0.0.1  fastapi.netdevops.com
   ```
   若 Docker 在远程主机，改为该主机 IP。

3. **启动服务**（在 `code` 目录）：
   ```bash
   cd /python_basic/netdevops作业/day03_20260429/code
   docker compose up -d --build
   ```
   首次构建较慢；容器内已 `yum install net-tools`，可直接执行 `ifconfig`。

4. **运行客户端**：
   ```bash
   python3 day3_client.py
   ```

5. **Swagger 测试**：浏览器打开 `https://fastapi.netdevops.com/docs`，对 `POST /cmd` 执行 `{"cmd":"pwd"}`，响应里 `cmd_result` 为 base64，解码后即为命令输出。

6. 若 443 端口被占用，可改 `docker-compose.yaml` 为 `"8443:443"`，同时把客户端 `server_ip` 改为 `fastapi.netdevops.com:8443`。

---

## Windows 浏览器访问虚拟机（去掉「不安全」）

场景：FastAPI 跑在 Linux 虚拟机，用 Windows 上的 Chrome/Edge 打开 `https://fastapi.netdevops.com/docs`。

### 步骤 1：把根证书拷到 Windows

在虚拟机里证书路径：

`/python_basic/netdevops作业/day03_20260429/code/ca.crt`

用 WinSCP、共享文件夹、`scp` 等拷到 Windows 任意目录，例如 `C:\certs\ca.crt`。

### 步骤 2：Windows 导入根证书（信任 CA）

1. 双击 `ca.crt`，或运行 `certmgr.msc`
2. 选 **本地计算机** → **将所有的证书都放入下列存储** → **浏览**
3. 选 **受信任的根证书颁发机构** → 确定 → 下一步 → 完成
4. 安全警告点 **是**

或 PowerShell（管理员）：

```powershell
Import-Certificate -FilePath "C:\certs\ca.crt" -CertStoreLocation Cert:\LocalMachine\Root
```

### 步骤 3：Windows 配置 hosts（域名指向虚拟机 IP）

用管理员记事本编辑 `C:\Windows\System32\drivers\etc\hosts`，增加一行（IP 改成你虚拟机实际地址，例如 `10.10.1.205`）：

```
10.10.1.205  fastapi.netdevops.com
```

查看虚拟机 IP：在 Linux 里执行 `hostname -I` 或 `ip addr`。

### 步骤 4：关闭浏览器后重新打开

访问：`https://fastapi.netdevops.com/docs`

地址栏应显示锁标志，不再提示「不安全」。

**注意：**

- 必须用域名 `fastapi.netdevops.com` 访问，不要直接用 `https://10.10.1.205`，否则证书域名不匹配仍会报错。
- 虚拟机防火墙需放行 443 端口。
- 若映射的是 `8443:443`，访问 `https://fastapi.netdevops.com:8443/docs`，hosts 不变。
