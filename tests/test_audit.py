from reposignal.audit import audit_repository
from reposignal.models import Severity


def test_audit_reports_missing_maintenance_files_and_runtime_artifacts() -> None:
    report = audit_repository(
        {"full_name": "acme/widget", "description": "Useful widget", "topics": ["python"]},
        [{"name": "README.md"}, {"name": "bot.log"}, {"name": ".github"}],
    )

    findings = {finding.identifier: finding for finding in report.findings}

    assert findings["description"].severity is Severity.GOOD
    assert findings["license"].severity is Severity.REVIEW
    assert findings["runtime-artifacts"].evidence == "Found: bot.log."
    assert report.health_score == 52
