init-env:
	pip install . --no-cache-dir

init-dev:
	pip install -e ".[dev]" --no-cache-dir

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

precommit: clean-folders interrogate sort format clean-folders
