"""Rules for evaluating public repository-maintenance signals."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from .models import AuditReport, Finding, Severity

ESSENTIAL_FILES = {
    "README.md": ("readme", "README is present", "Explain the project, audience, and quick start."),
    "LICENSE": ("license", "License is present", "Add a recognized license so reuse terms are clear."),
    "SECURITY.md": ("security", "Security policy is present", "Add SECURITY.md with a reporting route."),
    "CONTRIBUTING.md": ("contributing", "Contribution guide is present", "Add CONTRIBUTING.md for collaborators."),
}
RUNTIME_ARTIFACT_SUFFIXES = (".log", ".pyc")
RUNTIME_ARTIFACT_NAMES = {"followers.txt", "follower_counter.txt", "current_page.txt"}


def audit_repository(repository: dict[str, Any], contents: Iterable[dict[str, Any]]) -> AuditReport:
    """Audit one public repository; never infer whether a person is genuine."""
    file_names = {str(item.get("name", "")) for item in contents}
    findings: list[Finding] = []

    if repository.get("description"):
        findings.append(Finding("description", Severity.GOOD, "Repository description is present", "GitHub metadata includes a description."))
    else:
        findings.append(Finding("description", Severity.REVIEW, "Repository description is missing", "GitHub metadata has no description.", "Add a concise statement of the user problem solved."))

    topics = repository.get("topics") or []
    if topics:
        findings.append(Finding("topics", Severity.GOOD, "Repository topics are present", f"Topics: {', '.join(topics)}."))
    else:
        findings.append(Finding("topics", Severity.REVIEW, "Repository topics are missing", "GitHub metadata has no topics.", "Add accurate search topics for the language, domain, and use case."))

    for filename, (identifier, good_title, recommendation) in ESSENTIAL_FILES.items():
        if filename in file_names:
            findings.append(Finding(identifier, Severity.GOOD, good_title, f"Found {filename}."))
        else:
            findings.append(Finding(identifier, Severity.REVIEW, f"{filename} is missing", f"No root-level {filename} was found.", recommendation))

    if ".github" in file_names:
        findings.append(Finding("github-directory", Severity.GOOD, "GitHub configuration directory is present", "Found .github at the repository root."))
    else:
        findings.append(Finding("github-directory", Severity.INFO, "No GitHub configuration directory found", "No root-level .github directory was found.", "Consider issue templates or workflow documentation when the project is ready."))

    artifacts = sorted(
        filename for filename in file_names if filename.endswith(RUNTIME_ARTIFACT_SUFFIXES) or filename in RUNTIME_ARTIFACT_NAMES
    )
    if artifacts:
        findings.append(Finding("runtime-artifacts", Severity.REVIEW, "Runtime artifacts are tracked", f"Found: {', '.join(artifacts)}.", "Ignore generated state and logs unless they are intentional fixtures."))

    if repository.get("archived"):
        findings.append(Finding("archived", Severity.INFO, "Repository is archived", "GitHub marks this repository as archived."))

    return AuditReport(repository=str(repository.get("full_name", "unknown repository")), findings=tuple(findings))
