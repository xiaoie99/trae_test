from bs4 import BeautifulSoup
import requests
import os
from pathlib import Path
from math import pi, cos, sin
from bokeh.plotting import figure, output_file, save
from bokeh.transform import cumsum
from bokeh.palettes import Category10
from bokeh.models import ColumnDataSource, LabelSet, Range1d
from dotenv import load_dotenv
import pandas as pd
# 从项目根目录 .env 加载 USERNAME / PASSWORD
load_dotenv(Path(__file__).resolve().parents[2] / ".env")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
header = os.path.join(os.path.dirname(__file__), "http_header.txt")
login_url = "https://qytsystem.qytang.com/accounts/login/"
homework_url = "https://qytsystem.qytang.com/python_enhance/python_enhance_homework"
OUTPUTS_DIR = Path(__file__).resolve().parent / "outputs"
def get_header(header_file=header):
    headers = {}
    with open(header_file, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line:
                continue
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            if not key:
                continue
            headers[key] = value
    return headers
def get_response(url=homework_url, username=username, password=password):
    if not username or not password:
        raise RuntimeError("未找到 USERNAME/PASSWORD，请在 /python_basic/.env 中配置或 export 环境变量")
    headers = get_header(header)
    if "Referer" not in headers:
        headers["Referer"] = login_url
    client = requests.session()
    login_html = client.get(login_url, headers=headers)
    soup = BeautifulSoup(login_html.text, "lxml")
    token_input = soup.find("input", {"name": "csrfmiddlewaretoken"})
    if token_input is None:
        raise RuntimeError("登录页未找到 csrfmiddlewaretoken，请检查 http_header.txt")
    token = token_input.get("value")
    data = {"username": username, "password": password, "csrfmiddlewaretoken": token}
    post_headers = dict(headers)
    post_headers["Referer"] = login_url
    post_headers["Origin"] = "https://qytsystem.qytang.com"
    post_headers["Content-Type"] = "application/x-www-form-urlencoded"
    post_headers["Sec-Fetch-Site"] = "same-origin"
    result = client.post(login_url, headers=post_headers, data=data)
    print(f"Login result: {result.status_code}")
    if result.status_code != 200:
        raise RuntimeError(f"登录失败 HTTP {result.status_code}，请检查账号密码和 http_header.txt")
    homework = client.get(url, headers=headers)
    homework_soup = BeautifulSoup(homework.text, "lxml")
    if homework_soup.find("table") is None:
        raise RuntimeError("作业页未找到表格，可能账号密码错误或登录未成功")
    return homework_soup
def bokeh_bing(name_list, count_list, bing_name, save_name=None):
    """使用 Bokeh 绘制饼状图并保存为 HTML 文件。"""
    data_dict = dict(zip(name_list, [float(c) for c in count_list]))
    data = (
        pd.Series(data_dict)
        .reset_index(name="bytes")
        .rename(columns={"index": "application"})
    )
    data["angle"] = data["bytes"] / data["bytes"].sum() * 2 * pi
    data["start_angle"] = data["angle"].cumsum().shift(1, fill_value=0)
    data["end_angle"] = data["angle"].cumsum()
    data["mid_angle"] = (data["start_angle"] + data["end_angle"]) / 2
    num = len(data_dict)
    if num <= 2:
        data["color"] = Category10[3][:num]
    elif num <= 10:
        data["color"] = Category10[num]
    else:
        data["color"] = (Category10[10] * ((num // 10) + 1))[:num]
    data["percentage"] = (
        (data["bytes"] / data["bytes"].sum() * 100).round(2).astype(str) + "%"
    )
    data["slice_label"] = data["application"].astype(str)
    outside_radius = 0.7
    data["label_x"] = outside_radius * data["mid_angle"].map(cos)
    data["label_y"] = 1 + outside_radius * data["mid_angle"].map(sin)
    data["pct_label"] = data["percentage"].astype(str)
    inside_radius = 0.23
    data["pct_x"] = inside_radius * data["mid_angle"].map(cos)
    data["pct_y"] = 1 + inside_radius * data["mid_angle"].map(sin)
    source = ColumnDataSource(data)
    p = figure(
        height=520,
        width=800,
        title=bing_name,
        toolbar_location="right",
        tools="hover,pan,wheel_zoom,box_zoom,reset,save",
        tooltips="@application: @bytes (@percentage)",
        x_range=Range1d(-1.4, 1.4),
        y_range=Range1d(-0.2, 2.2),
    )
    p.wedge(
        x=0,
        y=1,
        radius=0.4,
        start_angle=cumsum("angle", include_zero=True),
        end_angle=cumsum("angle"),
        line_color="white",
        fill_color="color",
        legend_field="application",
        source=source,
    )
    labels = LabelSet(
        x="label_x",
        y="label_y",
        text="slice_label",
        text_align="center",
        text_baseline="middle",
        text_font_size="11pt",
        source=source,
    )
    p.add_layout(labels)
    pct_labels = LabelSet(
        x="pct_x",
        y="pct_y",
        text="pct_label",
        text_align="center",
        text_baseline="middle",
        text_font_size="11pt",
        text_color="white",
        source=source,
    )
    p.add_layout(pct_labels)
    p.axis.axis_label = None
    p.axis.visible = False
    p.grid.grid_line_color = None
    p.title.text_font_size = "16pt"
    p.title.align = "center"
    p.legend.label_text_font_size = "12pt"
    p.legend.location = "center_right"
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    output_filename = save_name if save_name else str(OUTPUTS_DIR / f"{bing_name}.html")
    output_file(output_filename, title=bing_name)
    save(p)
    print(f"[*] Bokeh 饼状图已生成: {output_filename}")
def _normalize_cell_text(s: str) -> str:
    return " ".join((s or "").split())
def extract_course_and_grade_counts(soup):
    """从作业页面表格中提取课程和成绩列并统计数量。"""
    table = soup.find("table")
    if table is None:
        raise RuntimeError("No <table> found in response HTML.")
    header_row = table.find("tr")
    if header_row is None:
        raise RuntimeError("No table header row (<tr>) found.")
    headers = [
        _normalize_cell_text(th.get_text())
        for th in header_row.find_all(["th", "td"])
    ]
    if not headers:
        raise RuntimeError("Could not parse table headers.")
    try:
        course_idx = headers.index("课程")
    except ValueError as e:
        raise RuntimeError(f'Column "课程" not found. Headers: {headers}') from e
    try:
        grade_idx = headers.index("成绩")
    except ValueError as e:
        raise RuntimeError(f'Column "成绩" not found. Headers: {headers}') from e
    course_counts = {}
    grade_counts = {}
    for tr in table.find_all("tr")[1:]:
        tds = tr.find_all("td")
        if not tds:
            continue
        if course_idx < len(tds):
            course = _normalize_cell_text(tds[course_idx].get_text())
            if course:
                course_counts[course] = course_counts.get(course, 0) + 1
        if grade_idx < len(tds):
            grade = _normalize_cell_text(tds[grade_idx].get_text())
            if grade:
                grade_counts[grade] = grade_counts.get(grade, 0) + 1
    return course_counts, grade_counts
def _dict_to_lists_sorted(d):
    items = sorted(d.items(), key=lambda kv: (-kv[1], kv[0]))
    return [k for k, _ in items], [v for _, v in items]
if __name__ == "__main__":
    soup = get_response(homework_url)
    course_counts, grade_counts = extract_course_and_grade_counts(soup)
    course_names, course_vals = _dict_to_lists_sorted(course_counts)
    grade_names, grade_vals = _dict_to_lists_sorted(grade_counts)
    print("课程统计:", dict(zip(course_names, course_vals)))
    print("成绩统计:", dict(zip(grade_names, grade_vals)))
    bokeh_bing(
        course_names,
        course_vals,
        "课程作业分布图",
        save_name=str(OUTPUTS_DIR / "课程作业分布图.html"),
    )
    bokeh_bing(
        grade_names,
        grade_vals,
        "课程分数分布图",
        save_name=str(OUTPUTS_DIR / "课程分数分布图.html"),
    )
