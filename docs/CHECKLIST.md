# Checklist

## Pre-Setup (new users)
- [ ] `make configure` — interactive paste from iaedu.pt
- [ ] `make check` — verify plugin and config

## Pre-Commit

- [ ] `make lint` — ruff reports no errors
- [ ] `make format` — ruff format produces no changes
- [ ] `make build` — distribution builds without warnings
- [ ] `llm -m iaedu "test"` — returns a response
- [ ] No hardcoded secrets or placeholder URLs in source
- [ ] `CHANGELOG.md` updated if behaviour changed

## Pre-Release

- [ ] `make doctor` — all checks pass
- [ ] Version bumped in `pyproject.toml` and `CHANGELOG.md`
- [ ] `python3 -m build` produces clean sdist + wheel
- [ ] .env.example up to date with any new env vars
