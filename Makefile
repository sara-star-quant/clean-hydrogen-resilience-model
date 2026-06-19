PY ?= python3.14
VENV ?= model/.venv
PYTEST ?= $(VENV)/bin/pytest
PYRIGHT ?= $(VENV)/bin/pyright

.PHONY: help install test test-fast test-perf coverage lint scan render summary publish-check clean precommit-install

help:
	@echo "Common targets:"
	@echo "  make install          create venv and install dev deps"
	@echo "  make test             run the full pytest suite (incl perf and regression)"
	@echo "  make test-fast        run pytest fast subset (CI-friendly, ~3s)"
	@echo "  make test-perf        run pytest perf marks only"
	@echo "  make coverage         run pytest with coverage report (gate at 80 percent)"
	@echo "  make lint             run pyright strict and the non-ASCII scanner"
	@echo "  make scan             run the non-ASCII scanner alone"
	@echo "  make render           regenerate report tables and chart PNGs via electicity render-all"
	@echo "  make summary          emit the machine-readable JSON summary"
	@echo "  make publish-check    full pre-publish check: tests + lint + scan + grep for secrets"
	@echo "  make precommit-install install the pre-commit and pre-push git hooks"
	@echo "  make clean            remove caches"

install:
	$(PY) -m venv $(VENV)
	$(VENV)/bin/pip install --upgrade pip
	$(VENV)/bin/pip install -e "model[dev]"

test:
	cd model && $(PWD)/$(PYTEST) -q

test-fast:
	cd model && $(PWD)/$(PYTEST) -q -m "not perf and not regression"

test-perf:
	cd model && $(PWD)/$(PYTEST) -q -m perf

coverage:
	cd model && $(PWD)/$(PYTEST) -q -m "not perf and not regression" --cov=electicity_model --cov-report=term --cov-fail-under=80

lint:
	$(PYRIGHT) --project pyrightconfig.json
	$(PY) docs/scan_non_ascii.py

scan:
	$(PY) docs/scan_non_ascii.py

render:
	$(VENV)/bin/electicity render-all

summary:
	$(VENV)/bin/electicity summary --out model/_summary.json

publish-check: lint test-fast
	@echo "--- secret scan ---"
	@! grep -rni "password\|api_key\|secret_key\|aws_access" --include="*.py" --include="*.md" --include="*.yaml" . | grep -v ".venv\|node_modules\|.idea" || (echo "secret-shaped strings found, review manually" && false)
	@echo "--- absolute /Users path scan ---"
	@! grep -rn "/Users/peterz" --include="*.md" --include="*.py" --include="*.yaml" --include="*.html" . | grep -v ".venv\|node_modules\|.idea\|CHANGELOG.md\|grep -rn \"/Users/\"" || (echo "absolute /Users paths found in committed files" && false)
	@echo "--- TODO marker scan ---"
	@grep -rn "TODO" --include="*.md" . | grep -v ".venv\|node_modules" || true
	@echo "publish-check passed."

precommit-install:
	pip install pre-commit
	pre-commit install
	pre-commit install --hook-type pre-push
	@echo "git hooks installed."

clean:
	rm -rf $(VENV) .pytest_cache .mypy_cache .pyright .coverage htmlcov
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	find . -type d -name "*.egg-info" -prune -exec rm -rf {} +
