init-env:
	pip install . --no-cache-dir

init-dev:
	pip install -e ".[dev]" --no-cache-dir
	pre-commit install

clean-notebooks:
	jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace notebooks/*.ipynb

clean-folders:
	rm -rf .ipynb_checkpoints __pycache__ .pytest_cache */.ipynb_checkpoints */__pycache__ */.pytest_cache

interrogate:
	interrogate -vv --ignore-nested-functions --ignore-module --ignore-init-method --ignore-private --ignore-magic --ignore-property-decorators --fail-under=80 compclasses tests

format:
	black --target-version py38 compclasses tests

sort:
	isort .

test:
	pytest tests -vv

precommit: clean-folders test interrogate sort format clean-folders

doc:
	mkdocs serve

pypi-push:
	python -m pip install twine wheel --no-cache-dir

	python setup.py sdist
	python setup.py bdist_wheel --universal
	twine upload dist/*

interrogate-badge:
	interrogate -vv --ignore-nested-functions --ignore-semiprivate --ignore-private --ignore-magic --ignore-module --ignore-init-method  --generate-badge docs/img/interrogate-shield.svg
