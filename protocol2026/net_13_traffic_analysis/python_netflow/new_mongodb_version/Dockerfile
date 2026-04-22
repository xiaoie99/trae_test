# syntax=docker/dockerfile:1
FROM python:3.11.9-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY mongo_config.py netflow_parser_v9.py netflow_server.py report_html.py reporter_app.py ./

EXPOSE 2055/udp
EXPOSE 8080

CMD ["python", "netflow_server.py"]
