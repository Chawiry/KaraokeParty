
# Karaoke Party

Self hosted Karaoke Web app

Features

- [x] Song Queue
- [ ] Turn Manager (based on song Queue)
- [x] Remote Add to Queue, from mobile WebApp
- [ ] Karaoke Video Selection
- [ ] Main web app to show lyrics
- [ ] Allow for Queue Visualization through Mobile Web App
- [ ] Allow user to join songs already in Queue
- [ ] Automated install script

## Usage

---
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
