.PHONY: linted
linted:
	isort core/ models/ migrations/ app/ tests/


.PHONY: tested
tested:
	pytest ./ -vv

.PHONY: fails-tested
fails-tested:
	pytest ./ -vv --last-failed


.PHONY: new-migration
new-migration:
	alembic revision --autogenerate -m ${message}

.PHONY: migrated
migrated:
	alembic upgrade head

.PHONY: unmigrated
unmigrated:
	alembic downgrade -1
