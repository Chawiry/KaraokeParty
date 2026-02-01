#!/usr/bin/env pwsh

python -m venv .KPvenv
.\.KPvenv\Scripts\Activate.ps1
pip install -r requirements.txt
flask run --host=$(hostname)
