# -*- coding: utf-8 -*-
import json
from collections import defaultdict
from pathlib import Path


def find_and_save_duplicate_datakeys(src_filename: str,
                                     dst_filename: str = "duplicates.json") -> None:
    """
    读取 src_filename，查找 datakey 重复的对象，
    并将这些对象写入 dst_filename（UTF-8，带缩进）。
    """
    try:
        # 1️⃣  读取原始 JSON
        with open(src_filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 2️⃣  按 datakey 分组
        groups: dict[str, list[dict]] = defaultdict(list)
        for item in data:
            if isinstance(item, dict):
                key = item.get("datakey")
                if key is not None:
                    groups[key].append(item)

        # 3️⃣  收集出现 >1 次的 datakey 对应的对象
        duplicates: list[dict] = [
            obj for objs in groups.values() if len(objs) > 1 for obj in objs
        ]

        if not duplicates:
            print("✅ 没有重复的 datakey。不会生成新文件。")
            return

        # 4️⃣  写出新 JSON 文件
        Path(dst_filename).write_text(
            json.dumps(duplicates, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"✅ 已找到 {len(duplicates)} 条重复记录，已写入 {dst_filename}")

    except Exception as e:
        print(f"❌ 处理失败：{e}")


if __name__ == "__main__":
    # 默认读取当前目录的 data.json，输出 duplicates.json
    find_and_save_duplicate_datakeys("matched_result.json")
