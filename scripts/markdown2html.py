import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

import mistune
from jinja2 import Environment, FileSystemLoader
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound

# 版本号
VERSION = "6.2.0-light-mode-only"


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

            if val.startswith("[") and val.endswith("]"):
                inner = val[1:-1]
                items = [item.strip().strip("\"'") for item in inner.split(",")]
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
    output_filename = input_path.stem + ".html"
    output_path = output_dir / output_filename

    # 1. 解析 Markdown
    raw_content = load_file(input_path)
    metadata, full_markdown_body = parse_front_matter(raw_content)

    # 2. 提取摘要
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

    # 3. 转 HTML
    parser = get_markdown_parser()
    html_body = parser(body_content)

    html_summary = ""
    summary_text_plain = ""

    if has_manual_summary:
        html_summary = parser(summary_content)
        summary_text_plain = strip_html(html_summary)
    else:
        full_html = parser(full_markdown_body)
        clean_text = strip_html(full_html)
        summary_text_plain = clean_text[:200] + "..."

    # 4. 生成代码高亮 CSS (仅保留亮色模式，例如 'xcode' 或 'friendly')
    formatter = HtmlFormatter(style="xcode", cssclass="highlight")
    pygments_css = formatter.get_style_defs(".highlight")

    # 5. 准备 Context
    tags = metadata.get("tags", [])
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",") if t.strip()]

    context = {
        "title": metadata.get("title", input_path.stem),
        "date": metadata.get("date", ""),
        "author": metadata.get("author", ""),
        "tags": tags,
        "summary_html": html_summary,
        "content": html_body,
        "pygments_css": pygments_css,  # 简化变量名
    }

    final_html = jinja_template.render(**context)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_html)

    print(f"Generated: {output_filename}")

    return {
        "title": context["title"],
        "date": context["date"] or "1970-01-01",
        "url": output_filename,
        "tags": tags,
        "summary_text": summary_text_plain,
    }


def generate_index_page(articles, output_dir, jinja_template):
    articles.sort(key=lambda x: x["date"], reverse=True)
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

    article_tpl_path = Path(tpl_article_path).resolve()
    index_tpl_path = Path(tpl_index_path).resolve()

    if not article_tpl_path.exists() or not index_tpl_path.exists():
        print(f"Error: Templates not found.", file=sys.stderr)
        sys.exit(1)

    template_dirs = list(set([str(article_tpl_path.parent), str(index_tpl_path.parent)]))

    try:
        env = Environment(loader=FileSystemLoader(template_dirs))
        tpl_article = env.get_template(article_tpl_path.name)
        tpl_index = env.get_template(index_tpl_path.name)
    except Exception as e:
        print(f"Error loading templates: {e}", file=sys.stderr)
        sys.exit(1)

    articles_metadata = []
    md_files = list(input_path.glob("*.md"))

    if not md_files:
        print(f"No markdown files found.", file=sys.stderr)
        return

    print(f"Found {len(md_files)} markdown files. Building site...")

    for md_file in md_files:
        meta = process_single_file(md_file, output_path, tpl_article)
        articles_metadata.append(meta)

    generate_index_page(articles_metadata, output_path, tpl_index)
    print("\nBuild Complete! 🎉")
    return articles_metadata


def main():
    parser = argparse.ArgumentParser(description="Static Site Generator")
    parser.add_argument("--input_dir", default="../content")
    parser.add_argument("--output_dir", default="../docs")
    parser.add_argument("--template-article", default="templates/article.html")
    parser.add_argument("--template-index", default="templates/index.html")
    parser.add_argument("--readme", default="../readme.md")
    args = parser.parse_args()

    print(f"SSG Generator v{VERSION}")
    articles_metadata = build_site(args.input_dir, args.output_dir, args.template_article, args.template_index)

    if args.readme and articles_metadata is not None:
        update_readme(args.readme, len(articles_metadata))


if __name__ == "__main__":
    main()
