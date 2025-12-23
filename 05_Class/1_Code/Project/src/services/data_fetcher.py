"""在线数据抓取服务

从高德地图接口获取地铁线路数据，生成符合项目格式的 CSV。
"""

from __future__ import annotations

import csv
import os
from collections import defaultdict
from typing import Dict, List, Optional

CITY_CODE = "3100"  # 上海
API_URL = f"http://map.amap.com/service/subway?_1469083453978&srhdata={CITY_CODE}_drw_{{city}}.json"
DEFAULT_CITY = "shanghai"


class FetchError(Exception):
    """抓取或处理数据时发生的异常"""


class DataFetcher:
    def __init__(self, city: str = DEFAULT_CITY):
        self.city = city

    def _ensure_requests(self):
        try:
            import requests  # type: ignore
            return requests
        except ImportError as exc:  # pragma: no cover - 环境缺依赖时提示
            raise FetchError("缺少 requests 库，请先安装: pip install requests") from exc

    def fetch_raw(self) -> Dict:
        """拉取原始 JSON 数据"""
        requests = self._ensure_requests()
        url = API_URL.format(city=self.city)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        try:
            resp = requests.get(url, headers=headers, timeout=15)
            resp.raise_for_status()
            return resp.json()
        except Exception as exc:
            raise FetchError(f"获取数据失败: {exc}") from exc

    def process(self, data: Dict) -> List[Dict[str, str]]:
        """将 JSON 转为 CSV 行列表

        返回字段：站点ID, 线路名, 站名, 可换乘站点ID
        """
        if not data or "l" not in data:
            raise FetchError("数据格式不正确：缺少 'l' 字段")

        lines = data["l"]
        csv_rows: List[Dict[str, str]] = []
        station_name_map: Dict[str, List[int]] = defaultdict(list)
        all_stations: List[Dict[str, object]] = []

        current_id = 1
        for line in lines:
            line_name = line.get("ln")
            stations = line.get("st", [])
            for st in stations:
                st_name = st.get("n")
                station_obj = {
                    "id": current_id,
                    "line": line_name,
                    "name": st_name,
                    "transfer_ids": []  # type: ignore[list-item]
                }
                all_stations.append(station_obj)
                station_name_map[st_name].append(current_id)
                current_id += 1

        # 计算换乘
        for ids in station_name_map.values():
            if len(ids) > 1:
                for s_id in ids:
                    station_obj = next(s for s in all_stations if s["id"] == s_id)
                    station_obj["transfer_ids"] = [str(tid) for tid in ids if tid != s_id]

        # 组装 CSV 行
        for st in all_stations:
            transfer_str = "/".join(st["transfer_ids"])  # type: ignore[index]
            csv_rows.append({
                "站点ID": str(st["id"]),
                "线路名": str(st["line"]),
                "站名": str(st["name"]),
                "可换乘站点ID": transfer_str,
            })
        return csv_rows

    def save_to_csv(self, rows: List[Dict[str, str]], output_path: str) -> None:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        headers = ["站点ID", "线路名", "站名", "可换乘站点ID"]
        with open(output_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)

    def fetch_and_save(self, output_path: str) -> None:
        data = self.fetch_raw()
        rows = self.process(data)
        self.save_to_csv(rows, output_path)


__all__ = ["DataFetcher", "FetchError"]
