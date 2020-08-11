import re
import os

raw_data_root = "../markdown"
output_root = "../markdown_cleaned"
if not os.path.exists(output_root):
    os.mkdir(output_root)

sub_map = {"---": ["<!--", "-->"]}

for dirpath, dirnames, filenames in os.walk(raw_data_root):
    # dirpath 当前输出的irnames
    print(f"进入{dirpath}")
    for filename in filenames:
        filepath = os.path.join(dirpath, filename)
        line_list = []
        with open(filepath, encoding="utf-8", mode="r") as f:
            line = f.readline()
            while line:
                line_list.append(line.strip())
                line = f.readline()

        if "---" in line_list[0]:
            line_list[0] = sub_map["---"][0]
            into_top_info = True
        else:
            into_top_info = False
        top_image = None
        for i, line in enumerate(line_list[1:], start=1):
            if "bigimg" in line:
                # bigimg: [{src: "https://images.pexels.com/photos/38196/pexels-photo-38196.jpeg", desc: "pixels.com"}]
                img_template_str = "![Top Image]({src})"
                src_str = re.findall(pattern=r'src:.*?"(.*?)"', string=line)[0]
                top_image = img_template_str.format(src=src_str)

            if "---" in line and into_top_info:
                line_list[i] = sub_map["---"][1]
                if top_image:
                    line_list[i] += "\n" + top_image
                into_top_info = False
                # 出了头部信息区域

        new_dirpath = os.path.join(output_root, *(dirpath[len(raw_data_root) :].split(os.sep)[1:]))
        print(f"创建数据到新目录 {new_dirpath}")
        if not os.path.exists(new_dirpath):
            os.makedirs(new_dirpath)
        new_filepath = os.path.join(new_dirpath, filename)
        with open(new_filepath, encoding="utf-8", mode="w") as f:
            for line in line_list:
                f.write(line + "\n")
