# Join-Backend

Beschreibung

Dies ist ein Backend-Projekt basierend auf Django 5.1.4 und dem Django REST Framework 3.15.2. Es dient als API-Backend für das Join-Projekt und ermöglicht eine flexible sowie skalierbare Datenverwaltung.

## 🛠️ Technologie-Stack

- Django 5.1.4
- Django REST Framework 3.15.2
- django-cors-headers 4.6.0
- asgiref 3.8.1
- python-dotenv 1.0.1
- sqlparse 0.5.3
- tzdata 2024.2

---

## Voraussetzungen

Python 3.10 oder höher

Virtual Environment (empfohlen)

---

## Installation

### Repository klonen:

```
git clone https://github.com/AlbinSchmid/Join-Backend.git
cd Join-Backend
```

### Virtuelle Umgebung erstellen:

```
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
```

### Abhängigkeiten installieren:

```
pip install -r requirements.txt
```

.env-Datei erstellen:
Erstelle eine .env-Datei im Projektverzeichnis für Umgebungsvariablen.

### Migrationen durchführen:

```
python manage.py migrate
```

---

## Server starten:

python manage.py runserver

---

## API-Endpunkt

Für den Zugriff auf die API-Endpunkte konsultiere bitte die projektspezifische Dokumentation oder die Umgebungsvariablen-Konfiguration. In der Entwicklungsumgebung kann der Standard-Endpunkt http://localhost:8000/ verwendet werden.
