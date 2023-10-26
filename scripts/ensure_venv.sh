if ! (. .venv/Scripts/activate >/dev/null 2>&1); then
    echo Setting up virtual environment.
    python3 -m venv .venv >/dev/null
    . .venv/Scripts/activate
    python3 -m pip install -r requirements.txt
    python3 -m pip install -e .
    echo "Virtual environment ready."
    echo
fi
