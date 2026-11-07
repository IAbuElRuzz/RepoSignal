from reposignal.models import AuditReport, Finding, Severity
from reposignal.render import render_markdown


def test_report_explicitly_rejects_person_scoring() -> None:
    text = render_markdown(
        AuditReport("acme/widget", (Finding("readme", Severity.GOOD, "README is present", "Found README.md."),))
    )

    assert "does not verify identity" in text
    assert "hiring decisions" in text
