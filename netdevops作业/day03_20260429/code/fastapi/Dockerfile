FROM        rockylinux:9.3.20231119
USER        root
RUN         /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone
RUN         yum install -y python3.12 python3.12-devel python3.12-pip gcc net-tools
RUN         mkdir /qytangfastapi
WORKDIR     /qytangfastapi
COPY        requirements.txt .
RUN         pip3.12 install -r requirements.txt
COPY        main.py .
COPY        fastapi.key .
COPY        fastapi.crt .
CMD gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:443 --keyfile=fastapi.key --certfile=fastapi.crt
