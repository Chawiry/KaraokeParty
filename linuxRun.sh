#!/bin/bash

python3 -m venv .KPvenv
source ./.KPvenv/bin/activate
pip install -r requirements.txt
flask run --host=$Host
