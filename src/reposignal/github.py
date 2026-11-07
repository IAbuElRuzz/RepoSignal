"""Small, dependency-free client for public GitHub repository data."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class GitHubClientError(RuntimeError):
    """Raised when public GitHub data cannot be obtained."""


@dataclass
class GitHubClient:
    base_url: str = "https://api.github.com"
    timeout_seconds: int = 15

    def get_repository(self, owner: str, repository: str) -> dict[str, Any]:
        return self._get_json(f"/repos/{owner}/{repository}")

    def get_root_contents(self, owner: str, repository: str) -> list[dict[str, Any]]:
        payload = self._get_json(f"/repos/{owner}/{repository}/contents")
        if not isinstance(payload, list):
            raise GitHubClientError("GitHub returned an unexpected repository contents response.")
        return payload

    def _get_json(self, path: str) -> Any:
        request = Request(
            f"{self.base_url}{path}",
            headers={"Accept": "application/vnd.github+json", "User-Agent": "RepoSignal/0.1"},
        )
        try:
            with urlopen(request, timeout=self.timeout_seconds) as response:
                return json.load(response)
        except HTTPError as error:
            if error.code == 404:
                raise GitHubClientError("Repository not found or is not public.") from error
            raise GitHubClientError(f"GitHub API request failed with HTTP {error.code}.") from error
        except (URLError, TimeoutError, json.JSONDecodeError) as error:
            raise GitHubClientError("Could not retrieve public GitHub data.") from error
