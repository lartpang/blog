# -*- coding: utf-8 -*-
import argparse
import copy
import json
import math
import os
import re
import shutil
import time
import urllib
from collections import OrderedDict
from datetime import datetime, timedelta, timezone

import requests
from feedgen.feed import FeedGenerator
from github import Github
from github.Issue import Issue
from github.Repository import Repository
from jinja2 import Environment, FileSystemLoader

from constant import I18N, ICONS, NEWLINE_CHAR

__VERSION__ = "2.0.0"

# Predefined Paths
GITHUB_WORKSPACE = os.environ.get("GITHUB_WORKSPACE")
USER_CONFIG_FILE = os.path.join(GITHUB_WORKSPACE, "config.json")
BLOG_BASE_FILE = os.path.join(GITHUB_WORKSPACE, "blogBase.json")
README_FILE = os.path.join(GITHUB_WORKSPACE, "README.md")
BACKUP_DIR = os.path.join(GITHUB_WORKSPACE, "backup")
DOCS_DIR = os.path.join(GITHUB_WORKSPACE, "docs")

POST_DIR = os.path.join(DOCS_DIR, "post")
RSS_XML_FILE = os.path.join(DOCS_DIR, "rss.xml")
POST_LIST_FILE = os.path.join(DOCS_DIR, "postList.json")


class Convertor:
    def __init__(self, github_token, repo_name, issue_number):
        self.github_token = github_token
        self.repo_name = repo_name
        self.issue_number = issue_number
        self.old_feed_string = ""
        self.repo: Repository = Github(login_or_token=github_token).get_repo(self.repo_name)
        self.label_color_info = {l.name: "#" + l.color for l in self.repo.get_labels()}

        self.initialize_config()

    def initialize_config(self):
        self.blogBase = {
            # For the single page with a unique label. e.g. "about, link"
            "sub_page_labels": [],
            "start_site": "",
            "filingNum": "",
            "max_posts_per_page": 15,
            "comment_label_color": "#006b75",
            "year_colors": ["#bc4c00", "#0969da", "#1f883d", "#A333D0"],
            "i18n": "CN",
            "theme_mode": "manual",
            "day_theme": "light",
            "night_theme": "dark",
            "script": "",
            "style": "",
            "bottom_text": "",
            "show_source": 1,
            "icons": {},
            "UTC": +8,
            "rss_split": "sentence",
            "extra_links": {},
            # should not be overrode
            "posts": OrderedDict(),  # 文章post页面信息 postListJson
            "sub_pages": OrderedDict(),  # 独立网页页面信息 singeListJson
            "label_color_info": self.label_color_info,
            "home_url": f"https://{self.repo.owner.login}.github.io",
            "author": self.repo.owner.login,
        }

        # 加载用户自定义的html格式的脚本和样式
        with open(USER_CONFIG_FILE, "r", encoding="utf-8") as f:
            user_cfg = json.load(f)
        if user_cfg["script"].endswith(".html"):
            with open(
                os.path.join(GITHUB_WORKSPACE, user_cfg["script"]),
                mode="r",
                encoding="utf-8",
            ) as f:
                user_cfg["script"] = f.read() + NEWLINE_CHAR
        if user_cfg["style"].endswith(".html"):
            with open(
                os.path.join(GITHUB_WORKSPACE, user_cfg["style"]),
                mode="r",
                encoding="utf-8",
            ) as f:
                user_cfg["style"] = f.read() + NEWLINE_CHAR
        self.blogBase.update(user_cfg)

        # self.blogBase.setdefault("displayTitle", self.blogBase["title"])
        self.blogBase.setdefault("faviconUrl", self.blogBase["avatar_url"])
        self.blogBase.setdefault("og_image", self.blogBase["avatar_url"])

        if self.repo.name.lower() != f"{self.repo.owner.login}.github.io":
            # 非user.github.io仓库
            self.blogBase["home_url"] += f"/{self.repo.name}"
        print("GitHub Pages URL: ", self.blogBase["home_url"])

        self.i18n = I18N.get(self.blogBase["i18n"], "EN")
        self.TZ = timezone(timedelta(hours=self.blogBase["UTC"]))

    @staticmethod
    def generate_post_description(issueBody: str = None):
        """Generate the post description corresponding to the issue.
        Due to the complexity of the post description, it is not implemented yet.

        Args:
            issueBody (str, optional): Issue body. Defaults to None.
        """
        postDescription = ""
        return postDescription

    def render_html(self, template, blogBase, icon, html, posts=None):
        file_loader = FileSystemLoader("templates")
        env = Environment(loader=file_loader)
        template = env.get_template(template)

        posts = posts or {}
        output = template.render(blogBase=blogBase, posts=posts, i18n=self.i18n, IconList=icon)
        with open(html, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"create {html} with template {template}")

    def markdown2html(self, mdstr: str):
        try:
            response = requests.post(
                "https://api.github.com/markdown",
                json={"text": mdstr, "mode": "gfm"},
                headers={"Authorization": f"token {self.github_token}"},
            )
            response.raise_for_status()  # Raises an exception if status code is not 200
            return response.text
        except requests.RequestException as e:
            raise Exception("markdown2html error: {}".format(e))

    # TODO: Maybe we should use the separated functions to handle the post and sub_page html files.
    def create_post_html(self, post_cfg: dict):
        with open(post_cfg["md_path"], "r", encoding="utf-8") as f:
            post_body = self.markdown2html(f.read())

        # Import mathjax for supporting the math formulas
        if "<math-renderer" in post_body:
            post_body = re.sub(r"<math-renderer.*?>", "", post_body)
            post_body = re.sub(r"</math-renderer>", "", post_body)
            post_cfg["script"] += "".join(
                [
                    '<script>MathJax = {tex: {inlineMath: [["$", "$"]]}};</script>',
                    '<script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>',
                ]
            )

        assert "post_title" in post_cfg, post_cfg.keys()
        # fmt: off
        post_info = {
            "show_source": self.blogBase["show_source"],
            "start_site": self.blogBase["start_site"],
            "og_image": post_cfg["og_image"],
            "post_title": post_cfg["post_title"],
            "description": post_cfg["description"],
            "post_url": post_cfg["post_url"],
            "post_source_url": post_cfg["post_source_url"],
            "post_body": post_body,
            "num_comments": post_cfg["num_comments"],
            "style": post_cfg["style"],
            "script": post_cfg["script"],
            "top": post_cfg["top"],
            "repo_name": self.repo_name,
            "highlight": int("highlight" in post_body),
            "bottom_text": "" if post_cfg["post_type"] == "sub_page" else self.blogBase["bottom_text"],
        }
        # fmt: on

        post_icons = {k: ICONS[k] for k in ["sun", "moon", "sync", "home", "github"]}
        self.render_html("post.html", post_info, post_icons, post_cfg["html_dir"])
        print(f'{post_cfg["post_title"]} > {post_cfg["html_dir"]} > {post_info["post_url"]}')

    def create_index_html(self):
        base_icons = ["sun", "moon", "sync", "search", "rss", "upload", "post"]
        index_icons = {
            k: ICONS.get(k, "link") for k in base_icons + self.blogBase["sub_page_labels"]
        }
        # overwrite the icons with the user defined icons
        index_icons.update(self.blogBase["icons"])

        all_post_infos = sorted(
            self.blogBase["posts"].items(),
            key=lambda x: (x[1]["top"], x[1]["created_time"]),
            reverse=True,
        )
        max_posts_per_page = self.blogBase["max_posts_per_page"]
        num_pages = math.ceil(len(all_post_infos) / max_posts_per_page)
        for page_idx in range(num_pages):
            start_idx = page_idx * max_posts_per_page
            end_idx = (page_idx + 1) * max_posts_per_page
            curr_posts = OrderedDict(all_post_infos[start_idx:end_idx])
            print(f"Post Range={(start_idx, end_idx)} Number of Posts:{len(curr_posts)}")

            if page_idx == 0:
                # the total number of posts is less than max_posts_per_page
                post_html = os.path.join(DOCS_DIR, "index.html")
                self.blogBase["prevUrl"] = "disabled"
                if page_idx + 1 < num_pages:  # there is a next page
                    self.blogBase["nextUrl"] = "/page1.html"
                else:  # current page is the last page with a full list
                    self.blogBase["nextUrl"] = "disabled"
            else:
                post_html = os.path.join(DOCS_DIR, f"page{page_idx}.html")
                if page_idx == 1:
                    self.blogBase["prevUrl"] = "/index.html"
                else:
                    self.blogBase["prevUrl"] = f"/page{page_idx-1}.html"
                if page_idx + 1 < num_pages:  # there is a next page
                    self.blogBase["nextUrl"] = f"/page{page_idx+1}.html"
                else:  # current page is the last page with a full list
                    self.blogBase["nextUrl"] = "disabled"
            self.render_html("plist.html", self.blogBase, index_icons, post_html, curr_posts)

        # create tag page
        tag_icons = {k: ICONS[k] for k in ["sun", "moon", "sync", "home", "search", "post"]}
        tag_html = os.path.join(DOCS_DIR, "tag.html")
        self.render_html("tag.html", self.blogBase, tag_icons, tag_html, curr_posts)

    def create_feed_xml(self):
        feed = FeedGenerator()
        feed.title(self.blogBase["title"])
        feed.description(self.blogBase["sub_title"])
        feed.link(href=self.blogBase["home_url"])
        feed.image(url=self.blogBase["avatar_url"], title="avatar", link=self.blogBase["home_url"])
        feed.copyright(self.blogBase["title"])
        feed.managingEditor(self.blogBase["title"])
        feed.webMaster(self.blogBase["title"])
        feed.ttl("60")

        # fmt: off
        # NOTE: Only list posts, not sub_pages
        for post_info in sorted(self.blogBase["posts"].values(), key=lambda x: x["created_time"], reverse=False):
            item = feed.add_item()
            item.guid(post_info["post_url"], permalink=True)
            item.title(post_info["post_title"])
            item.description(post_info["description"])
            item.link(href=post_info["post_url"])
            item.pubDate(time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime(post_info["created_time"])))
        # fmt: on

        if self.old_feed_string != "":
            new_feed_xml = os.path.join(DOCS_DIR, "new.xml")

            feed.rss_file(new_feed_xml)
            with open(new_feed_xml, "r", encoding="utf-8") as f:
                new = f.read()
            os.remove(new_feed_xml)

            # compare old and new xml files
            new = re.sub(r"<lastBuildDate>.*?</lastBuildDate>", "", new)
            old = re.sub(r"<lastBuildDate>.*?</lastBuildDate>", "", self.old_feed_string)

            if new == old:
                print("====== rss xml no update ======")
                with open(RSS_XML_FILE, "w", encoding="utf-8") as f:
                    f.write(self.old_feed_string)
                return

        print("====== create rss xml ======")
        feed.rss_file(RSS_XML_FILE)

    def create_file_name(self, issue: Issue, useLabel: bool = False):
        if useLabel:
            fileName = issue.labels[0].name
        else:
            fileName = str(issue.number).rjust(4, "0")  # 000X
        return re.sub(r"[<>:/\\|?*\"]|[\0-\31]", "-", fileName)

    def update_post_info(self, issue: Issue) -> dict:
        """Update the posts and sub_pages based on the issue information.

        Args:
            issue (Issue): issue object.

        Returns:
            dict: post information.
        """
        # TODO: 这里只考虑了标签列表中的第一个标签
        if issue.labels[0].name in self.blogBase["sub_page_labels"]:
            post_type = "sub_pages"
            html_name = self.create_file_name(issue, useLabel=True)
            html_path = os.path.join(DOCS_DIR, f"{html_name}.html")
        else:
            post_type = "posts"
            html_name = self.create_file_name(issue, useLabel=False)
            html_path = os.path.join(POST_DIR, f"{html_name}.html")

        # fmt: off
        post_cfg = {
            "html_dir": html_path,
            "labels": [label.name for label in issue.labels],
            "labelColor": self.label_color_info[issue.labels[0].name],
            "post_type": post_type,
            "post_title": issue.title,
            "post_url": self.blogBase["home_url"] + "/" + urllib.parse.quote(os.path.relpath(html_path, start=DOCS_DIR)),
            "post_source_url": "https://github.com/" + self.repo_name + "/issues/" + str(issue.number),
            "num_comments": issue.get_comments().totalCount,
            "num_words": len(issue.body),
            "description": self.generate_post_description(issue.body),
        }
        # fmt: on

        post_cfg["top"] = 0
        for event in issue.get_events():
            if event.event == "pinned":
                post_cfg["top"] = 1
            # elif event.event == "unpinned":
            #     post_cfg["top"] = 0

        # Parse and import the customized settings from the specific comment of the post body
        # format: <!-- myconfig:{key1:value1,key2:value2,...} -->
        print("Parse and import customized settings...")
        custom_post_cfg = {}
        for cfg in re.findall(r"<!--\s*myconfig:{([^}]*?)}\s*-->", issue.body, flags=re.MULTILINE):
            custom_post_cfg.update(json.loads(cfg))
        print("Customized settings: ", custom_post_cfg)

        # fmt: off
        post_cfg["created_time"] = custom_post_cfg.get("timestamp", int(time.mktime(issue.created_at.timetuple())))
        post_cfg["style"] = self.blogBase["style"] + custom_post_cfg.get("style", "")
        post_cfg["script"] = self.blogBase["script"] + custom_post_cfg.get("script", "")
        post_cfg["og_image"] = custom_post_cfg.get("og_image", self.blogBase["og_image"])

        thisTime = datetime.fromtimestamp(post_cfg["created_time"]).astimezone(self.TZ)
        post_cfg["created_date"] = thisTime.strftime("%Y-%m-%d")
        post_cfg["dateLabelColor"] = self.blogBase["year_colors"][int(thisTime.year) % len(self.blogBase["year_colors"])]
        # fmt: on

        md_name = re.sub(r"[<>:/\\|?*\"]|[\0-\31]", "-", issue.title)
        md_path = os.path.join(BACKUP_DIR, md_name + ".md")
        post_cfg["md_path"] = md_path
        if issue.body is not None:
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(issue.body)

        # self.blogBase[post_type][f"P{issue.number}"] = post_cfg
        return post_cfg

    def update_all_posts(self):
        print("====== start create all posts html ======")

        for _dir in [BACKUP_DIR, DOCS_DIR, POST_DIR]:
            if os.path.exists(_dir):
                shutil.rmtree(_dir)
        for _dir in [BACKUP_DIR, DOCS_DIR, POST_DIR]:
            os.mkdir(_dir)

        # Only use the open issues
        for issue in self.repo.get_issues(state="open"):
            if len(issue.labels) < 1:
                continue

            post_cfg = self.update_post_info(issue)
            self.blogBase[post_cfg["post_type"]][f"P{issue.number}"] = post_cfg
            self.create_post_html(post_cfg)

        self.create_index_html()
        self.create_feed_xml()
        print("====== create all posts html end ======")

    def update_single_post(self, number: str):
        print("====== start create single post html ======")

        issue = self.repo.get_issue(int(number))
        if len(issue.labels) < 1:
            return

        post_cfg = self.update_post_info(issue)
        self.blogBase[post_cfg["post_type"]][f"P{number}"] = post_cfg
        self.create_post_html(post_cfg)

        self.create_index_html()
        self.create_feed_xml()
        print("====== create single post html end ======")

    def update_blog_base(self):
        if not os.path.exists(BLOG_BASE_FILE):
            print("blogBase is not exists, run_all")
            self.update_all_posts()
        else:
            if os.path.exists(RSS_XML_FILE):
                with open(RSS_XML_FILE, "r", encoding="utf-8") as f:
                    self.old_feed_string = f.read()

            if self.issue_number == "0" or self.issue_number == "":
                print(f"issue_number=={self.issue_number}, run_all")
                self.update_all_posts()
            else:
                print("blogBase is exists and issue_number!=0, run_one")
                with open(BLOG_BASE_FILE, "r", encoding="utf-8") as f:
                    old_blog_base = json.load(f)

                for key, value in old_blog_base.items():
                    self.blogBase[key] = value

                self.update_single_post(self.issue_number)

        with open(BLOG_BASE_FILE, "w", encoding="utf-8") as f:
            json.dump(self.blogBase, f, indent=2)

    def update_post_list_json(self):
        print("====== create postList.json file ======")

        sorted_post_infos = OrderedDict(
            sorted(
                self.blogBase["posts"].items(),
                key=lambda x: x[1]["created_time"],
                reverse=True,
            )
        )

        num_comments = 0
        num_words = 0
        useless_keys = [
            "description",
            "post_source_url",
            "html_dir",
            "created_time",
            "script",
            "style",
            "top",
            "og_image",
        ]
        for i in sorted_post_infos:
            for k in useless_keys:
                if k in sorted_post_infos[i]:
                    del sorted_post_infos[i][k]

            if "num_comments" in sorted_post_infos[i]:
                num_comments = num_comments + sorted_post_infos[i]["num_comments"]
                del sorted_post_infos[i]["num_comments"]

            if "num_words" in sorted_post_infos[i]:
                num_words = num_words + sorted_post_infos[i]["num_words"]
                del sorted_post_infos[i]["num_words"]

        sorted_post_infos["label_color_info"] = self.label_color_info

        with open(POST_LIST_FILE, mode="w", encoding="utf-8") as f:
            json.dump(sorted_post_infos, f, indent=2)
        return num_comments, num_words

    def update_readme_md(self, num_comments, num_words):
        print("====== update readme file ======")

        readme = NEWLINE_CHAR.join(
            [
                f'# {self.blogBase["title"]} :link: {self.blogBase["home_url"]}',
                "This is a simple static self based on GitHub Issue and Page.",
                "| :alarm_clock: Late updated                            | :page_facing_up: Articles                                                | :speech_balloon: Comments | :hibiscus: Words |",
                "| ----------------------------------------------------- | ------------------------------------------------------------------------ | ------------------------- | ---------------- |",
                f"|{datetime.now(self.TZ).strftime('%Y-%m-%d %H:%M:%S')} | [{len(self.blogBase['posts']) - 1}]({self.blogBase['home_url']}/tag.html)| {num_comments}            | {num_words}      |",
                "---",
                "*Powered by `issue2md.py` in [scripts](./scripts), which is modified from [Gmeek](https://github.com/Meekdai/Gmeek)*",
            ]
        )
        with open(README_FILE, "w", encoding="utf-8") as f:
            f.write(readme)


def main():
    parser = argparse.ArgumentParser(description="Convertor: GitHub Issue -> Markdown -> HTML")
    parser.add_argument("github_token", help="github_token")
    parser.add_argument("repo_name", help="repo_name")
    parser.add_argument("--issue_number", help="issue_number", default=0, required=False)
    args = parser.parse_args()

    blog = Convertor(args.github_token, args.repo_name, args.issue_number)
    blog.update_blog_base()
    num_comments, num_words = blog.update_post_list_json()
    if os.environ.get("GITHUB_EVENT_NAME") != "schedule":
        blog.update_readme_md(num_comments, num_words)


if __name__ == "__main__":
    main()
