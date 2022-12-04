.PHONY: linted
linted:
	isort core/ models/ migrations/ app/
