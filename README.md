# WIMU10

Design proposal ![Polish flag](https://raw.githubusercontent.com/stevenrskelton/flag-icon/master/png/16/country-4x3/pl.png): [DESIGN_PROPOSAL.md](DESIGN_PROPOSAL.md)

## Prerequisites

- `make`
- `bash` (or `git-bash`)

## Development commands

- testing: `make test`,
- checking code style: `make check`,
- formatting code and fixing code style issues: `make format`,
- generating documentation: `make docs`

### Advanced commands

- `make upgrade` - forcibly reinstalls all the dependencies from [requirements.txt](requirements.txt),
- `make freeze` - updates [requirements.txt](requirements.txt) based on the current `pip` state,
- `make ensure_venv` - creates a virtual environment for Python if it does not exists, installs dependencies from [requirements.txt](requirements.txt); this job runs each time any other `make` command is executed, as a prerequisite
