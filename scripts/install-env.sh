#!/usr/bin/env bash
[ -d .venv ] && echo "Virtualenv already exists. Skipping." && exit 0
python -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
find .venv -type d -name '*site-packages' -exec sh -c 'echo "$PWD" > {}/my-package.pth' \;

rm -f .env
echo "DYNACONF_ROOT_DIR=$PWD" > .env