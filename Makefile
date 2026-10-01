.PHONY: install app test lint dataset evaluate check

install:
	python -m pip install -e ".[dev]"

app:
	streamlit run app.py

test:
	pytest

lint:
	ruff check .

dataset:
	python scripts/generate_dataset.py
	python scripts/validate_dataset.py

evaluate:
	python scripts/evaluate.py --output artifacts/evaluation-local.json

check: lint test dataset evaluate

