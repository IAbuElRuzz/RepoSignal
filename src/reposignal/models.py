"""Domain models for transparent, repository-scoped audit reports."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class Severity(StrEnum):
    INFO = "info"
    REVIEW = "review"
    GOOD = "good"


@dataclass(frozen=True)
class Finding:
    identifier: str
    severity: Severity
    title: str
    evidence: str
    recommendation: str | None = None


@dataclass(frozen=True)
class AuditReport:
    repository: str
    findings: tuple[Finding, ...]

    @property
    def health_score(self) -> int:
        """Return a repository-hygiene score, never a score for a person."""
        score = 100
        score -= sum(finding.severity is Severity.REVIEW for finding in self.findings) * 12
        return max(score, 0)
