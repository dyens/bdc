.PHONY: run flake mypy pytest check deps stop-deps

run:
	-poetry run python main.py

flake:
	-poetry run flake8 || true

mypy:
	-poetry run mypy bdc || true

pytest:
	-poetry run pytest || true

check: flake mypy pytest


pyuic:
	-pyuic5 bdc/design.ui -o bdc/design.py
