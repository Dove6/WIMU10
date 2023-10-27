VENV_DIR = ./.venv

SHELL := /bin/bash
ifeq ($(OS),Windows_NT)
	PYTHON := python
else
	PYTHON := python3
endif

ACTIVATE_VENV_FUNC := activate_venv() { \
	if [ "$$(expr substr $$(uname -s) 1 5)" == "Linux" ]; \
	then \
		. $(VENV_DIR)/bin/activate; \
	else \
		. $(VENV_DIR)/Scripts/activate; \
	fi; \
	if [ "$$(expr substr $$(uname -s) 1 5)" == "MINGW" ]; \
	then \
		VIRTUAL_ENV=$$(cygpath "$$VIRTUAL_ENV"); \
		export VIRTUAL_ENV; \
		PATH=$$(cygpath "$$PATH"); \
		export PATH; \
	fi; \
}

ensure_venv:
	@{ \
		set -e -o pipefail ; \
		if [ ! -d $(VENV_DIR) ]; \
		then \
			$(PYTHON) -m venv $(VENV_DIR); \
		fi; \
		eval '$(ACTIVATE_VENV_FUNC)'; \
		activate_venv; \
		$(PYTHON) -m pip install -r requirements.txt; \
		$(PYTHON) -m pip install -e . ;\
	}

upgrade: ensure_venv
	@{ \
		set -e -o pipefail ; \
		eval '$(ACTIVATE_VENV_FUNC)'; \
		activate_venv; \
		$(PYTHON) -m pip install --disable-pip-version-check --upgrade --force-reinstall -r requirements.txt ;\
	}

freeze: ensure_venv
	@{ \
		set -e -o pipefail ; \
		eval '$(ACTIVATE_VENV_FUNC)'; \
		activate_venv; \
		$(PYTHON) -m pip freeze --exclude-editable > requirements.txt ;\
	}

run: ensure_venv
	@{ \
		set -e -o pipefail ; \
		eval '$(ACTIVATE_VENV_FUNC)'; \
		activate_venv; \
		$(PYTHON) main.py ;\
	}

test: ensure_venv
	@{ \
		set -e -o pipefail ; \
		eval '$(ACTIVATE_VENV_FUNC)'; \
		activate_venv; \
		$(PYTHON) -m pytest tests ;\
	}

check: ensure_venv
	@{ \
		set -e -o pipefail ; \
		eval '$(ACTIVATE_VENV_FUNC)'; \
		activate_venv; \
		$(PYTHON) -m ruff check . ;\
	}

format: ensure_venv
	@{ \
		set -e -o pipefail ; \
		eval '$(ACTIVATE_VENV_FUNC)'; \
		activate_venv; \
		$(PYTHON) -m ruff format . ;\
	}

docs: ensure_venv
	@{ \
		set -e -o pipefail ; \
		eval '$(ACTIVATE_VENV_FUNC)'; \
		activate_venv; \
		cd docs; \
		make html; \
		cd ..; \
	}
