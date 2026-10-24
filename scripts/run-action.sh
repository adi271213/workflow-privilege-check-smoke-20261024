#!/usr/bin/env bash
set -euo pipefail
# Dependency setup is separate from analysis and uses the trusted Action directory.
# -I prevents Python importing modules from the analyzed checkout or PYTHONPATH.
action_root="$GITHUB_ACTION_PATH"
venv_dir="$(mktemp -d "$RUNNER_TEMP/workflow-privilege-check.XXXXXX")"
trap 'rm -rf "$venv_dir"' EXIT
python3 -I -m venv "$venv_dir"
"$venv_dir/bin/python" -I -m pip --isolated install --disable-pip-version-check --only-binary=:all: -r "$action_root/requirements.txt"
"$venv_dir/bin/python" -I "$action_root/scripts/action_entry.py"
