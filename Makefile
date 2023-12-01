.PHONY: ruff
ruff:
	pdm run ruff format src

.PHONY: mypy
mypy:
	MYPYPATH=src pdm run mypy --strict --explicit-package-bases src