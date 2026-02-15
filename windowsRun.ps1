#!/usr/bin/env pwsh

$repo_url = "https://github.com/Chawiry/KaraokeParty.git"
$repo_location = "$HOME/Downloads/KaraokeParty"


if (Test-Path $repo_location) {
    Set-Location $repo_location
    git pull
} else {
    # 3. Clone if it doesn't exist
    git clone $repo_url $repo_location
    Set-Location $repo_location
}

if (-not (Test-Path ".\.KPvenv")) {
    python -m venv .KPvenv
}

python -m venv .KPvenv
.\.KPvenv\Scripts\Activate.ps1
pip install -r requirements.txt
Start-Process "http://$(hostname):5000"
flask run --host=$(hostname)
