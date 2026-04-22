#!/usr/bin/env python3
# -*- coding=utf-8 -*-
from web_front import create_app

app, db_session = create_app()
app.extensions['db_session'] = db_session

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 