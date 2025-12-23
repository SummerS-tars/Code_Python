"""在线数据抓取服务

从高德地图接口获取地铁线路数据，生成符合项目格式的 CSV。
"""

from __future__ import annotations

import csv
import os
from collections import defaultdict
from typing import Dict, List, Optional, Tuple

CITY_CODE = "3100"  # 上海
API_URL = f"http://map.amap.com/service/subway?_1469083453978&srhdata={CITY_CODE}_drw_{{city}}.json"
DEFAULT_CITY = "shanghai"


class FetchError(Exception):
    """抓取或处理数据时发生的异常"""


class DataFetcher:
    LOOP_LINES = ["4号线"]

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

    def _fix_topology(self, lines: List[Dict]) -> List[Tuple[str, List[Dict]]]:
        """修复拓扑：闭合环线、分叉重命名并返回标准结构"""

        seen_lines: Dict[str, List[List[str]]] = {}
        fixed: List[Tuple[str, List[Dict]]] = []

        for line in lines:
            line_name = line.get("ln")
            stations = line.get("st", []) or []
            if not line_name or not stations:
                continue

            stations_fixed: List[Dict] = list(stations)
            station_names = [str(st.get("n") or "") for st in stations_fixed]

            # 环线闭合：首尾不同则追加起点副本
            if line_name in self.LOOP_LINES and station_names:
                if station_names[0] != station_names[-1]:
                    first_copy = dict(stations_fixed[0])
                    first_copy["_loop_closure"] = True
                    stations_fixed.append(first_copy)
                    station_names.append(str(first_copy.get("n") or ""))

            # 分叉线路：同名不同序列的重命名
            base_name = line_name.split("(")[0].strip()
            existing_sequences = seen_lines.get(base_name, [])
            final_line_name = line_name
            if existing_sequences:
                is_same_sequence = any(seq == station_names for seq in existing_sequences)
                if not is_same_sequence:
                    suffix_index = len(existing_sequences)
                    suffix = "(支线)" if suffix_index == 1 else f"(支线{suffix_index})"
                    final_line_name = f"{base_name}{suffix}"
            seen_lines.setdefault(base_name, []).append(station_names)

            fixed.append((final_line_name, stations_fixed))

        return fixed

    def process(self, data: Dict) -> List[Dict[str, str]]:
        """将 JSON 转为 CSV 行列表

        返回字段：站点ID, 线路名, 站名, 可换乘站点ID
        """
        if not data or "l" not in data:
            raise FetchError("数据格式不正确：缺少 'l' 字段")

        fixed_lines = self._fix_topology(data["l"])
        csv_rows: List[Dict[str, str]] = []
        station_name_map: Dict[str, List[int]] = defaultdict(list)
        all_stations: List[Dict[str, object]] = []
        dedupe_seen: set[Tuple[str, str]] = set()

        current_id = 1
        for line_name, stations in fixed_lines:
            for st in stations:
                st_name = st.get("n")
                if not st_name:
                    continue
                is_loop_closure = bool(st.get("_loop_closure"))
                key = (line_name, st_name)
                if key in dedupe_seen and not is_loop_closure:
                    continue
                dedupe_seen.add(key)

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
