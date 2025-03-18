# -*- coding: utf-8 -*-
import argparse
import json
import os
import re
import shutil
from collections import OrderedDict
from datetime import datetime

from github import Github
from github.Issue import Issue
from github.Repository import Repository

__VERSION__ = "1.0.0"

NEWLINE_CHAR = "\r\n"

# Predefined Paths
GITHUB_WORKSPACE = os.environ.get("GITHUB_WORKSPACE")

README_FILE = os.path.join(GITHUB_WORKSPACE, "README.md")
POST_DIR = os.path.join(GITHUB_WORKSPACE, "content", "posts")
POST_INFOS = os.path.join(GITHUB_WORKSPACE, "scripts", "posts.json")


class Convertor:
    def __init__(self, github_token, repo_name, issue_number):
        self.github_token = github_token
        self.repo_name = repo_name
        self.issue_number = issue_number
        self.repo: Repository = Github(login_or_token=github_token).get_repo(self.repo_name)

        if not os.path.exists(POST_INFOS):
            self.post_infos = {}
        else:
            with open(POST_INFOS, "r", encoding="utf-8") as f:
                # {issue_number: issue_info}
                self.post_infos = json.load(f, object_pairs_hook=OrderedDict)

    def get_post_info_from_issue(self, issue: Issue):
        if len(issue.labels) < 1:
            return
        if issue.body is None:
            return

        issue_info = {
            "issue_number": issue.number,
            "title": issue.title,
            "created_date": issue.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "tags": [label.name for label in issue.labels],
            "original_link": issue.html_url,
            "md_name": re.sub(r"[<>:/\\|?*\"]|[\0-\31]", " ", issue.title),
            "body": issue.body,
        }
        return issue_info

    def export_post(self, issue_info: dict, post_id: int):
        # YAML Front Matter
        tags = ", ".join([f'"{tag}"' for tag in issue_info["tags"]])
        yaml_fm = NEWLINE_CHAR.join(
            [
                "---",
                f'title: "{issue_info["title"]}"',
                f"date: {issue_info['created_date']}",
                f"tags: [{tags}]",
                "---",
                "",
                "<!--more-->",
                "",
                f"> <{issue_info['original_link']}>",
                "",
                "",
            ]
        )
        md_file = str(post_id).rjust(4, "0") + "-" + issue_info["md_name"] + ".md"
        with open(os.path.join(POST_DIR, md_file), "w", encoding="utf-8") as f:
            f.write(yaml_fm)
            f.write(issue_info["body"])
        return

    def export_all_posts(self):
        if os.path.exists(POST_DIR):
            shutil.rmtree(POST_DIR)
        os.mkdir(POST_DIR)

        post_infos = OrderedDict()
        # only use the open issues
        for issue in self.repo.get_issues(state="open"):
            issue_info = self.get_post_info_from_issue(issue)
            if issue_info is not None:
                post_infos[issue_info["issue_number"]] = issue_info
                self.export_post(issue_info, post_id=len(post_infos))
        return post_infos

    def export_specific_post(self, number: str):
        issue = self.repo.get_issue(int(number))
        issue_info = self.get_post_info_from_issue(issue)
        if issue_info is not None:
            post_info = issue_info
            self.export_post(post_info, post_id=len(self.post_infos) + 1)
            return post_info

    def update_blog_info(self):
        if not self.post_infos or self.issue_number == "0" or self.issue_number == "":
            self.post_infos = self.export_all_posts()
        else:
            self.post_infos[self.issue_number] = self.export_specific_post(self.issue_number)

        with open(POST_INFOS, "w", encoding="utf-8") as f:
            json.dump(self.post_infos, f, indent=2)

    def update_readme_md(self):
        print(" update readme file ")

        readme = NEWLINE_CHAR.join(
            [
                "# Blog...",
                "This is a simple static self based on GitHub Issue and Page.",
                "| :alarm_clock: Late updated                            | :page_facing_up: posts |",
                "| ----------------------------------------------------- | ------------------------- |",
                f"|{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {len(self.post_infos)} |",
                "---",
                "*Powered by `issue2markdowns.py`*",
            ]
        )
        with open(README_FILE, "w", encoding="utf-8") as f:
            f.write(readme)


def main():
    parser = argparse.ArgumentParser(description="Convertor: GitHub Issues -> Markdown files")
    parser.add_argument("github_token", help="github_token")
    parser.add_argument("repo_name", help="repo_name")
    parser.add_argument("--issue_number", help="issue_number", default=0, required=False)
    args = parser.parse_args()

    blog = Convertor(args.github_token, args.repo_name, args.issue_number)
    blog.update_blog_info()
    blog.update_readme_md()


if __name__ == "__main__":
    main()
