# Lohnsteuer 2025 - Backend

Dieses Verzeichnis enthält das FastAPI-Backend für die Lohnsteuerberechnungs-Webanwendung 2025.

## Übersicht

Das Backend ist verantwortlich für:

-   Die Bereitstellung einer REST-API zur Berechnung der Lohnsteuer.
-   Die Implementierung der offiziellen Lohnsteuer-Berechnungslogik für 2025.
-   Die Validierung und Verarbeitung von Eingabedaten.
-   Die Bereitstellung von Endpunkten für den Export von Berechnungsergebnissen.

## Installation

1.  **Navigieren Sie in das `backend`-Verzeichnis:**

    ```bash
    cd backend
    ```

2.  **Erstellen Sie eine virtuelle Umgebung:**

    ```bash
    python -m venv venv
    ```

3.  **Aktivieren Sie die virtuelle Umgebung:**

    -   **Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    -   **macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Installieren Sie die erforderlichen Abhängigkeiten:**

    ```bash
    pip install -r requirements.txt
    ```

## Ausführung

### Entwicklungsserver

Um den FastAPI-Entwicklungsserver zu starten, führen Sie den folgenden Befehl aus:

```bash
uvicorn main:app --reload
```

Die API ist dann unter `http://127.0.0.1:8000` verfügbar.

### API-Dokumentation

Die interaktive API-Dokumentation (Swagger UI) finden Sie unter `http://127.0.0.1:8000/docs`.

Eine alternative Dokumentation (ReDoc) finden Sie unter `http://127.0.0.1:8000/redoc`.

## Tests

Um die Tests auszuführen, verwenden Sie `pytest`:

```bash
pytest
```
