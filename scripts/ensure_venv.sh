if ! (. env/Scripts/activate >/dev/null 2>&1); then
    echo Setting up virtual environment.
    py -m venv env >/dev/null
    . env/Scripts/activate
    pip install -r requirements.txt
    pip install -e .
    echo Virtual environment ready.
    echo
fi
