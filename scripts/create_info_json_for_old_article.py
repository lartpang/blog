import os
import time
import json


def get_time_about_file(filepath):
    return time.ctime(os.path.getctime(filepath)), time.ctime(os.path.getmtime(filepath))


md_root = "../markdown_cleaned"


def create_article_info(root: str) -> dict:
    all_article_info = []
    for dirpath, dirnames, filenames in os.walk(root):
        print(f" ==>> 正在处理{dirpath}")
        for filename in filenames:
            filepath = "./" + os.path.relpath(
                os.path.join(dirpath, filename), start=os.path.dirname(root)
            )
            created_time, modified_time = get_time_about_file(os.path.join(dirpath, filename))
            all_article_info.append(
                {
                    "file_name": filename,
                    "path": filepath,
                    "created_time": created_time,
                    "modified_time": modified_time,
                }
            )
    return all_article_info


all_article_info = create_article_info(md_root)
with open("old_article_info.json", encoding="utf-8", mode="w") as f:
    json.dump(
        sorted(all_article_info, key=lambda file_dict: file_dict["modified_time"], reverse=True),
        f,
        indent=2,
    )
