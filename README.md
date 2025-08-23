# TemplateBaukasten

Ein interaktiver Prompt-Template-Baukasten, mit dem man Kommunikationsstrukturen, Handlungsanweisungen und Probleme dokumentieren und als Vorlagen für Large Language Models (LLMs) generieren kann.

---

## 🚀 Features

- **Template-Erstellung:** Bausteine mit Ebenen, Aktionen und Prioritäten hinzufügen.
- **Arbeitsfläche:** Alle Bausteine übersichtlich in einer Liste bearbeiten, löschen oder rückgängig machen.
- **Ausgabeformate:** Markdown oder Baumstruktur zur Visualisierung von Kommunikations- und Handlungsstrukturen.
- **Projektverwaltung:** Templates speichern, laden und verwalten.
- **GUI:** Benutzerfreundliche Oberfläche mit [Tkinter](https://docs.python.org/3/library/tkinter.html) und [ttkbootstrap](https://ttkbootstrap.readthedocs.io/).

---

## 🗂 Projektstruktur

TemplateBaukasten/
│
├── main.py # Startpunkt des Programms
├── requirements.txt # Abhängigkeiten
│
├── gui/
│ └── app.py # GUI-Implementierung
│
├── core/
│ ├── generator.py # TemplateGenerator-Klasse
│ └── diagram.py # show_tree-Funktion
│
├── data/
│ ├── library.json # Optional: Template-Bibliothek
│ └── outputs/ # Gespeicherte Templates

yaml
Kopieren
Bearbeiten

---

## 💻 Installation

1. Repository klonen:

```bash
git clone https://github.com/JungmannS/TemplateBaukasten.git
cd TemplateBaukasten
Virtuelle Umgebung erstellen:

bash
Kopieren
Bearbeiten
python -m venv venv
Aktivieren der virtuellen Umgebung:

Windows:

bash
Kopieren
Bearbeiten
venv\Scripts\activate
macOS/Linux:

bash
Kopieren
Bearbeiten
source venv/bin/activate
Abhängigkeiten installieren:

bash
Kopieren
Bearbeiten
pip install -r requirements.txt
🏃 Anwendung starten
bash
Kopieren
Bearbeiten
python main.py
