# Simple CRM – Installations- & Migrationsanleitung (PythonAnywhere / Flask)

**Simple CRM – 5BHWII**

## 1) Plattform-Check
- Zielplattform: PythonAnywhere  
- Sprache/Stack: Python (Flask)  
- Datenbank getestet: SQLite (`crm.db` im Projektordner)  
- Entscheidung & Begründung: SQLite wird genutzt, weil PythonAnywhere Free-Accounts keine externen Datenbanken bereitstellen.

## 2) Voraussetzungen
- Account: PythonAnywhere (kostenlos reicht)  
- Tools: Terminal (Bash), optional GitHub-Zugang, SSH-Key, Browser  
- Projektdateien: GitHub-Repo: https://github.com/pczak3/crm/tree/main/simple_crm  
- Datenbank-Datei: `crm.db` mit Beispiel-Daten (durch Seeder erstellt)  
- Hilfstools (optional): FTP-Client (FileZilla), DB-Tools (DBeaver, DB Browser, Adminer)  

## 3) Schritt-für-Schritt Installation

### 3.1 Projekt herunterladen
1. PythonAnywhere → Consoles → Bash  
2. Tippe:
```bash
cd ~
git clone https://github.com/pczak3/crm.git
ls
```
3. Prüfen: Ordner `crm` erscheint

### 3.2 Virtuelle Umgebung erstellen
```bash
mkvirtualenv simple_crm --python=python3.10
workon simple_crm
pip install -r ~/crm/simple_crm/requirements.txt
```

### 3.3 Datenbank vorbereiten
```bash
cd ~/crm/simple_crm/
python seed.py
```
Prüfen: Datei `crm.db` liegt im Projektordner

### 3.4 Web-App konfigurieren
1. Web → Add a new web app → Manual configuration → Python 3.10  
2. Source code: `/home/<dein_username>/crm/simple_crm/`  
3. Virtualenv: `/home/<dein_username>/.virtualenvs/simple_crm/`  

### 3.5 WSGI-Datei bearbeiten
Pfad: `/var/www/<dein_username>_pythonanywhere_com_wsgi.py`  
```python
import sys
import os

project_home = '/home/<dein_username>/crm/simple_crm'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

from app import create_app
application = create_app()
```

### 3.6 Statische Dateien konfigurieren
- Web → Static files:  
| URL      | Pfad                                         |
|----------|---------------------------------------------|
| /static/ | /home/<dein_username>/crm/simple_crm/app/static/ |

### 3.7 App starten
- Klick Reload → Browser: `https://<dein_username>.pythonanywhere.com/`

## 4) Smoke-Test
1. Startseite öffnen → Menü sichtbar  
2. Kunden-Suche testen  
3. Kunden-Detail öffnen → Umsatz gesamt, Umsatz letztes Jahr, Datumsfilter  
4. Tabellen „Letzte Bestellungen“ & „Letzte Kontakte“ prüfen  

## 5) Datenbank Backup / Restore
**Backup:**
```bash
sqlite3 crm.db ".backup 'crm-backup.sqlite'"
sqlite3 crm.db .dump > crm.sqlite.sql
```

**Restore:**
```bash
sqlite3 crm.db < crm.sqlite.sql
```

## 6) Updates einspielen
```bash
cd ~/crm
git pull
```
→ Reload auf PythonAnywhere

## 7) Beispiel .env
```env
FLASK_ENV=production
SECRET_KEY=change-me
SQLALCHEMY_DATABASE_URI=sqlite:///crm.db
TIMEZONE=Europe/Vienna
```

## 8) Troubleshooting
| Problem                       | Lösung                                      |
|--------------------------------|--------------------------------------------|
| Seite lädt nicht               | Reload klicken                             |
| CSS / JS fehlt                 | Static files Mapping prüfen                |
| Pakete fehlen                  | Virtualenv aktivieren + pip install -r … |
| Änderungen nicht sichtbar      | Reload klicken                             |
| GitHub-Klonen schlägt fehl     | HTTPS oder SSH-Key nutzen                  |
