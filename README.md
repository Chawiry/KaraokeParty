# Karaoke Party

Queued Karaoke from yt that basically runs with just one command on windows and linux (macos should work with the linuxRun, not tested)
Have the main screen show the web site and queue songs through phone with a qr code

Features

- [x] Song Queue
- [ ] Turn Manager (Move Songs on Queue or Delete them)
- [x] Remote Add to Queue, from mobile WebApp
- [x] Automatic Karaoke Video Selection
  - [x] Multiple videos in case of automatic selection not ideal
- [x] Main web app to show lyrics (this would go on a TV or the main screen)
- [x] Allow for Queue Visualization through Mobile Web App (And Turns)
- [x] Allow user to join songs already in Queue (and limited to the number of "mics"; default is 10)
- [x] Automated install scripts

TODOs

- [x] Improve / make UI

## Usage

---
Follow the guide or use this command on windows powershell (for linux you can clone the repo and run the ```linuxRun.sh```)

```pwsh
irm https://raw.githubusercontent.com/Chawiry/KaraokeParty/refs/heads/main/windowsRun.ps1?token=GHSAT0AAAAAADUNJVFE7SC3AO27TP6FHUAY2MRDB6Q | iex
```

Create the venv and activate it

```bash
python3 -m venv .KPvenv
```

Linux ``` . ./.KPvenv/bin/activate ```
Windows ``` . .\.KPvenv\Scripts\activate.ps1 ```

Install requirements

```bash
pip install -r .\requirements.txt
```

Run

```pwsh
flask run --host=$(hostname)
```

```Linux
flask run --host=$HOST
```
