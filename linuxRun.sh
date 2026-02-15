#!/bin/bash

python3 -m venv .KPvenv
source ./.KPvenv/bin/activate
pip install -r requirements.txt
open "http://$Host:5000"
flask run --host=$Host
