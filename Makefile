--ensure_venv:
	@bash ./scripts/ensure_venv.sh

upgrade: --ensure_venv
	@. .venv/Scripts/activate; python3 -m pip install --disable-pip-version-check --upgrade --force-reinstall -r requirements.txt

freeze: --ensure_venv
	@. .venv/Scripts/activate; python3 -m pip freeze > requirements.txt

run: --ensure_venv
	@. .venv/Scripts/activate; python3 main.py

test: --ensure_venv
	@. .venv/Scripts/activate; python3 -m pytest tests

check: --ensure_venv
	@. .venv/Scripts/activate; ruff check .

format: --ensure_venv
	@. .venv/Scripts/activate; ruff format .
