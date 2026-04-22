#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from flask import Flask, Response, request
from report_html import generate_report_html

app = Flask(__name__)


@app.get('/')
def index():
	range_key = request.args.get('range', '1h')  # 15m,30m,1h,3h,6h,24h
	html = generate_report_html(range_key)
	return Response(html, mimetype='text/html; charset=utf-8')


if __name__ == '__main__':
	host = os.environ.get('REPORT_HOST', '0.0.0.0')
	port = int(os.environ.get('REPORT_PORT', '8080'))
	app.run(host=host, port=port)
