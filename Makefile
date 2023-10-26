--ensure_venv:
	@bash ./scripts/ensure_venv.sh

upgrade: --ensure_venv
	@. env/Scripts/activate; pip install --disable-pip-version-check --upgrade --force-reinstall -r requirements.txt

freeze: --ensure_venv
	@. env/Scripts/activate; pip freeze > requirements.txt

run: --ensure_venv
	@. env/Scripts/activate; python main.py

test: --ensure_venv
	@. env/Scripts/activate; pytest tests

check: --ensure_venv
	@. env/Scripts/activate; ruff check .

format: --ensure_venv
	@. env/Scripts/activate; ruff format .

