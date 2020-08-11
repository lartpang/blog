import os
import json
from os import curdir
from collections import defaultdict

file_text_template = """
# Go!!!

> Lart Pang (Youwei Pang)
>
> © 2020•Lart Pang's Articles...

## My Articles
{text_str}
"""

subsection_title_template = "\n\n### {subsection_title}\n\n"
list_item_template = "* [{title}]({rel_file_path})"

with open("./new_article_info.json", encoding="utf-8", mode="r") as f:
    article_info = json.load(f)

dirname_dict = defaultdict(list)
for article_dict in article_info:
    curr_dirname = os.path.basename(os.path.dirname(article_dict["path"]))
    dirname_dict[curr_dirname].append(
        list_item_template.format(
            title=article_dict["file_name"], rel_file_path=article_dict["path"],
        )
    )

text_str = ""
for subsec_title, article_list in dirname_dict.items():
    subsec_title = subsection_title_template.format(subsection_title=subsec_title)
    text_str += subsec_title + "\n".join(article_list)
file_text = file_text_template.format(text_str=text_str)

with open("../README.md", encoding="utf-8", mode="w") as f:
    f.write(file_text)
