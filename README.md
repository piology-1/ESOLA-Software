# E-Bike-Solarladestation (ESOLA) - Gruppe 2022-2023

Dieser Branch enthält alle Codeänderungen und Anpassungen an der Software, welche Die Gruppe von 2022-2023 vorgenommen hat.

## Verzeichnisstruktur

- `gui_main.py`: Der Hauptcode für die ESOLA-Steuerung aus dem die Applikation gestartet wird.
- `backend/`: Ein Ordner, der den Backend-Code enthält.
- `qml/`: Ein Ordner, der den Frontend-Code enthält. Frontend mittels PySide2 und qml.
- `dist/`: Ein Ordner für die Installation des Codes auf dem Raspberry Pi.
- `fonts/`: Ein Ordner mit den verwendeten Schriftarten in der GUI.
- `images/`: Ein Ordner mit den verwendeten Bildern in der GUI.
- `locks.json`: In dieser Datei wird gespeichert, welche Türen mit welcher Card UID verschlossen sind.
- `Solartankstelle.pyproject`: Datei für die GUI und die Bearbeitung im Qt Design Studio.
- `Solartankstelle.qml`: Datei für die GUI und die Bearbeitung im Qt Design Studio.
- `Solartankstelle.qmlproject`: Datei für die GUI und die Bearbeitung im Qt Design Studio.

## Installation auf dem Raspberry Pi

### First installation of the new Code with the RFID feature on the Raspberry Pi

1. Den alten Hauptordner der alten Gruppe löschen: `sudo rm -r /opt/`
2. Dieses Repository auf neu dem Raspberry Pi klonen: `git clone https://gitlab.com/ESOLA_user/esola.git`
3. Die Anmeldedaten eingeben:
   Nutzer: ESOLA_user
   Passwort: SolartankstelleFR20
4. In das Projektverzeichnis navigieren: `cd ESOLA`.
5. In den jeweiligen Branch wechseln (standardmäßig ist der main branch aktiv): `git checkout 2022-2023`
6. Die erforderlichen Module auf dem Raspberry pi installieren, falls noch nicht installiert.
7. Den Code installieren und Autostart in die GUI aktivieren: `sudo install -m 644 dist/solartankstelle.service /etc/systemd/system/`
8. Den Raspberry Pi neustarten: `sudo reboot`

### Installieren der benötigten neuen Packages

sudo apt-get install pip

#### Für pyscard:

```bash
solar@solartankstelle:~/esola $ sudo apt install pcscd libpcsclite-dev
Fortfahren: J bzw. enter
solar@solartankstelle:~/esola $ sudo apt install swig
Fortfahren: J bzw. enter
solar@solartankstelle:~/esola $ pip3 install pyscard
```

#### Pandas

```bash
solar@solartankstelle:~/esola $ pip3 install pandas
```

### Update the Code

1. Den aktuellen esola Ordner löschen: `solar@solartankstelle:~ $ sudo rm -r esola/`
1. Dieses Repository erneut auf den Raspberry Pi klonen.
1. In das Projektverzeichnis navigieren: `cd ESOLA`.
1. In den jeweiligen Branch wechseln (standardmäßig ist der main branch aktiv): `git checkout 2022-2023`
1. Die erforderlichen Module auf dem Raspberry pi installieren, falls noch nicht installiert.
1. Den Code installieren und Autostart in die GUI aktivieren: `sudo install -m 644 dist/solartankstelle.service /etc/systemd/system/`
1. Den Raspberry Pi neustarten: `sudo reboot`

## Autoren

- Lenox aka Leon Merk <your.email@example.com>
- Piology aka Pius Großmann <author2@example.com>

## Bekannte Probleme

- Problem 1: Beschreibung des Problems 1.
- Problem 2: Beschreibung des Problems 2.
