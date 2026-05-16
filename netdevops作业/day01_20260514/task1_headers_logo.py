import requests
from pathlib import Path
def headers_from_txt(path: str | Path) -> dict[str, str]:
    """从 txt 读取每行 Key: Value，转成 requests 可用的 headers 字典。"""
    p = Path(path)
    headers: dict[str, str] = {}
    with open(p, "r", encoding="utf-8") as f:
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
def main() -> None:
    here = Path(__file__).resolve().parent
    header_txt = here / "http_header.txt"
    out_path = here / "logo.jpg"
    url = "https://qytsystem.qytang.com/static/images/logo.jpg"
    headers = headers_from_txt(header_txt)
    resp = requests.get(url, headers=headers, timeout=15, stream=True)
    resp.raise_for_status()
    out_path.write_bytes(resp.content)
    print(f"Downloaded {len(resp.content)} bytes -> {out_path}")
if __name__ == "__main__":
    main()
