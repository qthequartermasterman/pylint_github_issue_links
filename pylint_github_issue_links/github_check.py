from __future__ import annotations

from typing import TYPE_CHECKING, List

from astroid import nodes

from pylint.checkers import BaseRawFileChecker

import requests
import re


if TYPE_CHECKING:
    from pylint.lint import PyLinter

def get_issue_data(link:str) -> dict:
    link = link.replace("www.", "")
    if 'api.github.com/repos/' not in link:
        link = link.replace("github.com/", "api.github.com/repos/")
    resp = requests.get(link)
    return resp.json()

def check_issue_closed(issue_data:dict) -> bool:
    return issue_data["state"] == "closed"

def get_links_from_line(line:bytes) -> List[str]:
    return re.findall(
        r'((?:https?://)?(?:www.)?(?:api.)?github.com/\S+/issues/\S+)',
        str(line),
    )


class GitHubIssueChecker(BaseRawFileChecker):
    name = "linked-closed-github-issue"
    msgs = {
        "G9000": (
            "Linked GitHub issue is closed.",
            "linked-closed-github-issue",
            (
                "Used when a GitHub issue is linked, but the issue is closed."
            ),
        )
    }
    options = ()

    def process_module(self, node: nodes.Module) -> None:
        with node.stream() as stream:
            for line_num, line in enumerate(stream):
                links = get_links_from_line(line)
                for link in links:
                    issue_data = get_issue_data(link)
                    if check_issue_closed(issue_data):
                        self.add_message("linked-closed-github-issue", line=line_num+1)


def register(linter: PyLinter) -> None:
    linter.register_checker(GitHubIssueChecker(linter))