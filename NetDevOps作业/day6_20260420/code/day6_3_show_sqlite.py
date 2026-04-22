#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
from datetime import datetime, timedelta

import numpy as np
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from code.day6_1_create_db import InternfaceMonitor, engine
from code.tools.day6_bokeh_line import bokeh_line

Session = sessionmaker(bind=engine)


def show_speed_from_db(minutes=10):
    session = Session()
    cutoff = datetime.now() - timedelta(minutes=minutes)

    combos = (
        session.query(InternfaceMonitor.device_ip, InternfaceMonitor.interface_name)
        .distinct()
        .all()
    )

    in_speed_lines = []
    out_speed_lines = []

    for device_ip, interface_name in combos:
        records = (
            session.query(InternfaceMonitor)
            .filter(
                InternfaceMonitor.device_ip == device_ip,
                InternfaceMonitor.interface_name == interface_name,
                InternfaceMonitor.record_datetime >= cutoff,
            )
            .order_by(InternfaceMonitor.record_datetime)
            .all()
        )
        if len(records) < 2:
            continue

        in_arr = np.array([r.in_bytes for r in records], dtype=np.int64)
        out_arr = np.array([r.out_bytes for r in records], dtype=np.int64)
        time_arr = np.array([r.record_datetime for r in records], dtype="datetime64[s]")

        diff_in = np.diff(in_arr)
        diff_out = np.diff(out_arr)
        diff_secs = np.diff(time_arr).astype(np.int64)

        valid = (diff_secs > 0) & (diff_in > 0) & (diff_out > 0)
        in_kbps = np.round((diff_in[valid] * 8) / (1000 * diff_secs[valid]), 2)
        out_kbps = np.round((diff_out[valid] * 8) / (1000 * diff_secs[valid]), 2)

        clean_times = np.array([r.record_datetime for r in records[1:]])[valid].tolist()
        if not clean_times:
            continue

        label = f"{device_ip}:{interface_name}"
        in_speed_lines.append([clean_times, in_kbps.tolist(), f"RX:{label}"])
        out_speed_lines.append([clean_times, out_kbps.tolist(), f"TX:{label}"])
        print(f"[*] {label}: {len(clean_times)} 个有效速率点")

    session.close()

    if in_speed_lines:
        bokeh_line(in_speed_lines, title="接口入向速率 (RX)", y_label="速度 (kbps)")
    if out_speed_lines:
        bokeh_line(out_speed_lines, title="接口出向速率 (TX)", y_label="速度 (kbps)")


if __name__ == "__main__":
    show_speed_from_db(minutes=10)
