.PHONY: linted
linted:
	isort core/ models/ migrations/ app/ tests/


.PHONY: tested
tested:
	pytest ./ -vv

.PHONY: fails-tested
fails-tested:
	pytest ./ -vv --last-failed
