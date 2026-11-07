# RepoSignal

RepoSignal is an evidence-based auditor for public GitHub repository-maintenance signals.

It helps maintainers find concrete improvements—such as missing documentation, missing community files, repository metadata gaps, and accidentally tracked runtime artifacts.

## What it is not

RepoSignal does **not** decide whether a developer is “real” or “fake,” verify identity, infer intent, rank people, or make hiring recommendations. Public repository signals are incomplete and context-dependent; review the linked evidence and make human decisions separately.

## Quick start

```bash
python -m pip install -e .
reposignal audit owner/repository
```

Write a Markdown report to a file:

```bash
reposignal audit owner/repository --output reposignal-report.md
```

## First-release checks

- Repository description and topics
- README, license, security policy, and contribution guide
- `.github` configuration directory
- Common runtime artifacts accidentally committed at the repository root

## Development

```bash
python -m pip install pytest
pytest
```

## Roadmap

1. Check links and quick-start commands in README files.
2. Add workflow and dependency-health checks.
3. Publish a GitHub Action and JSON/SARIF output.

## License

MIT. See [LICENSE](LICENSE).
