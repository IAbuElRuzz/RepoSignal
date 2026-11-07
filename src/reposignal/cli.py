"""Command-line interface for RepoSignal."""

from __future__ import annotations

import argparse
import logging
import sys

from .audit import audit_repository
from .github import GitHubClient, GitHubClientError
from .render import render_markdown


def parse_repository(value: str) -> tuple[str, str]:
    parts = value.split("/")
    if len(parts) != 2 or not all(parts):
        raise argparse.ArgumentTypeError("Repository must use owner/repository format.")
    return parts[0], parts[1]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Audit public GitHub repository-maintenance signals.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    audit = subparsers.add_parser("audit", help="Audit one public repository.")
    audit.add_argument("repository", type=parse_repository, help="Public repository as owner/repository")
    audit.add_argument("--output", type=argparse.FileType("w"), default=sys.stdout, help="Write Markdown to this file")
    return parser


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    args = build_parser().parse_args(argv)
    owner, repository_name = args.repository
    client = GitHubClient()
    try:
        report = audit_repository(client.get_repository(owner, repository_name), client.get_root_contents(owner, repository_name))
    except GitHubClientError as error:
        logging.error("Audit failed: %s", error)
        return 2
    args.output.write(render_markdown(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
