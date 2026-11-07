"""Markdown rendering for auditable, shareable reports."""

from __future__ import annotations

from .models import AuditReport, Severity


def render_markdown(report: AuditReport) -> str:
    lines = [
        f"# RepoSignal report: {report.repository}",
        "",
        f"**Repository hygiene score: {report.health_score}/100**",
        "",
        "> This report evaluates public repository-maintenance signals only. It does not verify identity, decide whether a developer is real or fake, or support hiring decisions.",
        "",
    ]
    for severity in (Severity.REVIEW, Severity.GOOD, Severity.INFO):
        selected = [finding for finding in report.findings if finding.severity is severity]
        if not selected:
            continue
        lines.extend([f"## {severity.value.title()} signals", ""])
        for finding in selected:
            lines.append(f"- **{finding.title}** — {finding.evidence}")
            if finding.recommendation:
                lines.append(f"  Recommendation: {finding.recommendation}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"
