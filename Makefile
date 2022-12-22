.PHONY: help
help:
	echo "`help` is not implemented yet."


.PHONY: linted
linted:
	isort core/ models/ migrations/ app/ tests/
	mypy .
	flake8 .


.PHONY: tested
tested:
	coverage run -m pytest tests/ -vv --durations=6

.PHONY: coverage-report
coverage-report:
	coverage report -m --skip-covered

.PHONY: coverage-html-report
coverage-html-report:
	coverage report -m --precision=2 --directory=tests/coverage-report-pages/

.PHONY: coverage-erased
coverage-erased:
	coverage erase


.PHONY: new-migration
new-migration:
	alembic revision --autogenerate -m ${message}

.PHONY: migrated
migrated:
	alembic upgrade head

.PHONY: unmigrated
unmigrated:
	alembic downgrade -1
