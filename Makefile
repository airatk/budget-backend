.PHONY: linted
linted:
	isort core/ models/ migrations/ app/ tests/

.PHONY: tested
tested:
	pytest ./
