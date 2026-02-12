#!/usr/bin/env pwsh

python -m venv .KPvenv
.\.KPvenv\Scripts\Activate.ps1
pip install -r requirements.txt
Start-Process "http://$(hostname):5000"
flask run --host=$(hostname)

