#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# Pygal 饼状图生成工具：SVG → cairosvg → PNG（支持邮件内嵌）
import pygal
import os
from pathlib import Path
import cairosvg
# 输出目录：当前文件上两级目录下的 outputs/
OUTPUTS_DIR = Path(__file__).resolve().parent.parent / 'outputs'
def pygal_pie(name_list, count_list, title, save_name=None):
    """使用 Pygal 绘制交互式饼状图，并返回 PNG 路径用于邮件内嵌。"""
    from pygal.style import Style
    custom_style = Style(
        font_family='Noto Sans CJK SC'  # 中文字体，否则中文乱码
    )
    pie_chart = pygal.Pie(inner_radius=0.4, title=title, style=custom_style)
    for name, count in zip(name_list, count_list):
        pie_chart.add(name, count)
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    png_filename = save_name if save_name else str(OUTPUTS_DIR / f"{title}.png")
    cairosvg.svg2png(bytestring=pie_chart.render(), write_to=png_filename)
    print(f"[*] Pygal 饼状图已生成 PNG: {png_filename}")
    return png_filename
if __name__ == '__main__':
    names = ['INFO', 'WARNING', 'ERROR', 'CRITICAL']
    counts = [150, 45, 12, 3]
    pygal_pie(names, counts, 'SYSLOG严重级别分布图测试')
