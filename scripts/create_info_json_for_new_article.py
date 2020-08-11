import os
import time
import json


def get_time_about_file(filepath):
    return time.ctime(os.path.getctime(filepath)), time.ctime(os.path.getmtime(filepath))


md_root = "../markdown_new"


def create_article_info(root: str) -> list:
    all_article_info = []
    for dirpath, dirnames, filenames in os.walk(root):
        print(f" ==>> 正在处理{dirpath}")
        for filename in filenames:

            filepath = os.path.join(dirpath, filename)
            created_time, modified_time = get_time_about_file(filepath)
            all_article_info.append(
                {
                    "file_name": filename,
                    "path": "./" + os.path.relpath(filepath, start=os.path.dirname(root)),
                    "created_time": created_time,
                    "modified_time": modified_time,
                }
            )
    return all_article_info


with open("old_article_info.json", encoding="utf-8", mode="r") as f:
    all_article_info = json.load(f)

all_article_info.extend(create_article_info(md_root))
with open("new_article_info.json", encoding="utf-8", mode="w") as f:
    json.dump(
        sorted(all_article_info, key=lambda file_dict: file_dict["modified_time"], reverse=True),
        f,
        indent=2,
    )
