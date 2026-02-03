# Karaoke Party

Self hosted Karaoke Web app

Features

- [x] Song Queue
- [ ] Turn Manager (Move Songs on Queue)
- [x] Remote Add to Queue, from mobile WebApp
- [ ] In app Karaoke Video Selection (Currently you need to paste the youtube video link)
- [x] Main web app to show lyrics
- [x] Allow for Queue Visualization through Mobile Web App (And Turns)
- [x] Allow user to join songs already in Queue
- [x] Automated install scripts

## Usage

---
Follow the guide or use the ```windowsRun.ps1``` for windows or ```linuxRun.sh``` for Linux

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
