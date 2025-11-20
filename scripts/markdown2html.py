import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

import mistune
from jinja2 import Environment, FileSystemLoader, Template
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound

# 版本号
VERSION = "6.0.0-jinja2-engine"


def load_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def strip_html(html_content):
    """移除 HTML 标签，用于生成纯文本摘要"""
    html_content = html_content.replace("<br>", " ").replace("<br/>", " ")
    clean_text = re.sub(r"<[^>]+>", "", html_content)
    return " ".join(clean_text.split())


def parse_front_matter(full_text):
    """解析 Front Matter (YAML)"""
    lines = full_text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, full_text

    metadata = {}
    body_start_index = 0
    found_end = False

    for i in range(1, len(lines)):
        line = lines[i].strip()
        if line == "---":
            body_start_index = i + 1
            found_end = True
            break

        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip()

            # 处理列表格式
            if val.startswith("[") and val.endswith("]"):
                inner = val[1:-1]
                items = [item.strip().strip("\"'") for item in inner.split(",")]
                # 这里直接存储为列表，而不是字符串！方便 Jinja2 遍历
                val = items
            elif (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                val = val[1:-1]

            metadata[key] = val

    if not found_end:
        return {}, full_text

    body = "\n".join(lines[body_start_index:])
    return metadata, body


class HighlightRenderer(mistune.HTMLRenderer):
    def block_code(self, code, info=None):
        if not info:
            return f"<pre><code>{mistune.escape(code)}</code></pre>"
        try:
            lexer = get_lexer_by_name(info, stripall=True)
        except ClassNotFound:
            return f"<pre><code>{mistune.escape(code)}</code></pre>"
        formatter = HtmlFormatter(wrapcode=True, cssclass="highlight")
        return highlight(code, lexer, formatter)

    def table(self, text):
        return f'<div class="table-wrapper"><table>{text}</table></div>'


def get_markdown_parser():
    return mistune.create_markdown(
        renderer=HighlightRenderer(), plugins=["table", "url", "strikethrough", "task_lists", "math"]
    )


def update_readme(readme_path, post_count):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    readme_template = """# Blog...

This is a simple static self based on GitHub Issue and Page.
| :alarm_clock: Late updated | :page_facing_up: posts |
| -------------------------- | ---------------------- |
| {time}                     | {num_posts}            |

---
*Powered by `issue2markdowns.py` and `markdown2html.py`* in `scripts`.
"""

    new_content = readme_template.format(time=current_time, num_posts=post_count)
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Updated README: Time={current_time}, Posts={post_count}")


def process_single_file(input_path, output_dir, jinja_template):
    """
    处理单个 Markdown 文件
    这里不再进行字符串拼接，而是准备数据字典，传给 Jinja2 渲染
    """
    output_filename = input_path.stem + ".html"
    output_path = output_dir / output_filename

    # 1. 解析 Markdown
    raw_content = load_file(input_path)
    metadata, full_markdown_body = parse_front_matter(raw_content)

    # 2. 提取摘要逻辑
    summary_content = ""
    body_content = full_markdown_body
    split_token = "<!--more-->"
    has_manual_summary = False

    if split_token and split_token in full_markdown_body:
        parts = full_markdown_body.split(split_token, 1)
        if len(parts) == 2:
            summary_content = parts[0].strip()
            body_content = parts[1].strip()
            has_manual_summary = True

    # 3. Markdown 转 HTML
    parser = get_markdown_parser()
    html_body = parser(body_content)

    html_summary = ""  # 用于文章页展示的 HTML 摘要
    summary_text_plain = ""  # 用于首页列表的纯文本摘要

    if has_manual_summary:
        html_summary = parser(summary_content)
        summary_text_plain = strip_html(html_summary)
    else:
        full_html = parser(full_markdown_body)
        clean_text = strip_html(full_html)
        summary_text_plain = clean_text[:200] + "..."

    # 4. 准备渲染数据 (Context)
    # 注意：tags 如果是字符串，尝试分割成列表，方便模板循环
    tags = metadata.get("tags", [])
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",") if t.strip()]

    context = {
        "title": metadata.get("title", input_path.stem),
        "date": metadata.get("date", ""),
        "author": metadata.get("author", ""),
        "tags": tags,
        "summary_html": html_summary,  # 传给模板判断是否显示
        "content": html_body,
    }

    # 5. Jinja2 渲染
    final_html = jinja_template.render(**context)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_html)

    print(f"Generated: {output_filename}")

    # 6. 返回用于生成首页的数据对象
    return {
        "title": context["title"],
        "date": context["date"] or "1970-01-01",
        "url": output_filename,
        "tags": tags,
        "summary_text": summary_text_plain,
    }


def generate_index_page(articles, output_dir, jinja_template):
    """生成首页"""
    # 按日期降序
    articles.sort(key=lambda x: x["date"], reverse=True)

    # 直接将文章列表传给模板，让模板处理循环生成 HTML
    final_html = jinja_template.render(articles=articles)

    with open(output_dir / "index.html", "w", encoding="utf-8") as f:
        f.write(final_html)

    print(f"Generated Index: {output_dir / 'index.html'}")


def build_site(input_dir, output_dir, tpl_article_path, tpl_index_path):
    input_path = Path(input_dir)
    output_path = Path(output_dir)

    if not input_path.exists():
        print(f"Error: Input directory '{input_dir}' does not exist.", file=sys.stderr)
        sys.exit(1)

    output_path.mkdir(parents=True, exist_ok=True)

    # --- Jinja2 模板加载 ---
    # 我们直接读取文件内容创建 Template 对象，这样可以保持传参路径的灵活性
    # 也可以使用 FileSystemLoader，但为了兼容传入任意路径，直接读取更直接
    try:
        article_template_str = load_file(tpl_article_path)
        index_template_str = load_file(tpl_index_path)

        tpl_article = Template(article_template_str)
        tpl_index = Template(index_template_str)
    except Exception as e:
        print(f"Error loading templates: {e}", file=sys.stderr)
        sys.exit(1)

    articles_metadata = []
    md_files = list(input_path.glob("*.md"))

    if not md_files:
        print(f"No markdown files found in '{input_dir}'.")
        return

    print(f"Found {len(md_files)} markdown files. Building site...")

    for md_file in md_files:
        meta = process_single_file(md_file, output_path, tpl_article)
        articles_metadata.append(meta)

    generate_index_page(articles_metadata, output_path, tpl_index)
    print("\nBuild Complete! 🎉")
    return articles_metadata


def main():
    parser = argparse.ArgumentParser(description="Static Site Generator (Markdown to HTML)")
    parser.add_argument("--input_dir", default="../content")
    parser.add_argument("--output_dir", default="../docs")
    parser.add_argument("--template-article", default="template_article.html", help="Article template path")
    parser.add_argument("--template-index", default="template_index.html", help="Index template path")
    parser.add_argument("--readme", default="../readme.md")
    args = parser.parse_args()

    print(f"SSG Generator v{VERSION}")
    articles_metadata = build_site(args.input_dir, args.output_dir, args.template_article, args.template_index)
    if args.readme:
        update_readme(args.readme, len(articles_metadata))


if __name__ == "__main__":
    main()
