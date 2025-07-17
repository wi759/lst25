"""
Monitoring und Logging Utilities für die Lohnsteuer API
"""

import logging
import time
from typing import Dict, Any
from collections import defaultdict, deque
from datetime import datetime
import threading


class APIMetrics:
    """Sammelt und verwaltet API-Metriken"""

    def __init__(self):
        self.request_count = 0
        self.error_count = 0
        self.response_times = deque(maxlen=1000)  # Letzte 1000 Requests
        self.error_types = defaultdict(int)
        self.endpoint_stats = defaultdict(
            lambda: {"count": 0, "errors": 0, "avg_time": 0}
        )
        self.hourly_stats = defaultdict(int)
        self.lock = threading.Lock()

    def record_request(
        self,
        endpoint: str,
        response_time: float,
        status_code: int,
        error_type: str = None,
    ):
        """Zeichnet eine API-Anfrage auf"""
        with self.lock:
            self.request_count += 1
            self.response_times.append(response_time)

            # Endpoint-spezifische Statistiken
            self.endpoint_stats[endpoint]["count"] += 1
            current_avg = self.endpoint_stats[endpoint]["avg_time"]
            current_count = self.endpoint_stats[endpoint]["count"]
            self.endpoint_stats[endpoint]["avg_time"] = (
                current_avg * (current_count - 1) + response_time
            ) / current_count

            # Fehlerstatistiken
            if status_code >= 400:
                self.error_count += 1
                self.endpoint_stats[endpoint]["errors"] += 1
                if error_type:
                    self.error_types[error_type] += 1

            # Stündliche Statistiken
            current_hour = datetime.now().strftime("%Y-%m-%d %H:00")
            self.hourly_stats[current_hour] += 1

    def get_stats(self) -> Dict[str, Any]:
        """Gibt aktuelle Statistiken zurück"""
        with self.lock:
            avg_response_time = (
                sum(self.response_times) / len(self.response_times)
                if self.response_times
                else 0
            )
            error_rate = (
                (self.error_count / self.request_count * 100)
                if self.request_count > 0
                else 0
            )

            return {
                "total_requests": self.request_count,
                "total_errors": self.error_count,
                "error_rate_percent": round(error_rate, 2),
                "avg_response_time_ms": round(avg_response_time * 1000, 2),
                "requests_last_hour": self._get_last_hour_requests(),
                "endpoint_stats": dict(self.endpoint_stats),
                "error_types": dict(self.error_types),
                "uptime_hours": self._get_uptime_hours(),
            }

    def _get_last_hour_requests(self) -> int:
        """Gibt die Anzahl der Requests in der letzten Stunde zurück"""
        current_hour = datetime.now().strftime("%Y-%m-%d %H:00")
        return self.hourly_stats.get(current_hour, 0)

    def _get_uptime_hours(self) -> float:
        """Berechnet die Uptime in Stunden (vereinfacht)"""
        # In einer echten Implementierung würde man den Startzeit speichern
        return len(self.hourly_stats)


# Globale Metriken-Instanz
metrics = APIMetrics()


class StructuredLogger:
    """Strukturiertes Logging für bessere Analyse"""

    def __init__(self, name: str):
        self.logger = logging.getLogger(name)

    def log_request(
        self, method: str, path: str, client_ip: str, user_agent: str = None
    ):
        """Loggt eingehende Requests"""
        self.logger.info(
            "Request received",
            extra={
                "event_type": "request",
                "method": method,
                "path": path,
                "client_ip": client_ip,
                "user_agent": user_agent,
                "timestamp": datetime.utcnow().isoformat(),
            },
        )

    def log_calculation(self, input_data: Dict, result: Dict, processing_time: float):
        """Loggt erfolgreiche Berechnungen"""
        self.logger.info(
            "Calculation completed",
            extra={
                "event_type": "calculation",
                "processing_time_ms": round(processing_time * 1000, 2),
                "input_summary": {
                    "RE4": float(input_data.get("RE4", 0)) / 100,  # In Euro
                    "STKL": input_data.get("STKL"),
                    "LZZ": input_data.get("LZZ"),
                    "ZKF": float(input_data.get("ZKF", 0)),
                },
                "result_summary": {
                    "LSTLZZ": float(result.get("LSTLZZ", 0)) / 100,  # In Euro
                    "SOLZLZZ": float(result.get("SOLZLZZ", 0)) / 100,
                    "BK": float(result.get("BK", 0)) / 100,
                },
                "timestamp": datetime.utcnow().isoformat(),
            },
        )

    def log_error(
        self,
        error_type: str,
        error_message: str,
        input_data: Dict = None,
        client_ip: str = None,
    ):
        """Loggt Fehler mit Kontext"""
        self.logger.error(
            f"Error occurred: {error_type}",
            extra={
                "event_type": "error",
                "error_type": error_type,
                "error_message": error_message,
                "client_ip": client_ip,
                "input_data": input_data,
                "timestamp": datetime.utcnow().isoformat(),
            },
        )

    def log_validation_error(
        self, field: str, value: Any, error_message: str, client_ip: str = None
    ):
        """Loggt Validierungsfehler"""
        self.logger.warning(
            f"Validation error for field {field}",
            extra={
                "event_type": "validation_error",
                "field": field,
                "invalid_value": str(value),
                "error_message": error_message,
                "client_ip": client_ip,
                "timestamp": datetime.utcnow().isoformat(),
            },
        )


class SecurityMonitor:
    """Überwacht verdächtige Aktivitäten"""

    def __init__(self):
        self.suspicious_ips = defaultdict(list)
        self.blocked_ips = set()
        self.lock = threading.Lock()

    def check_suspicious_activity(self, client_ip: str, request_data: Dict) -> bool:
        """Prüft auf verdächtige Aktivitäten"""
        with self.lock:
            current_time = time.time()

            # Entferne alte Einträge (älter als 1 Stunde)
            self.suspicious_ips[client_ip] = [
                timestamp
                for timestamp in self.suspicious_ips[client_ip]
                if current_time - timestamp < 3600
            ]

            # Prüfe auf verdächtige Muster
            suspicious = False

            # 1. Zu viele Requests mit ungültigen Daten
            if self._has_invalid_patterns(request_data):
                self.suspicious_ips[client_ip].append(current_time)
                suspicious = True

            # 2. Zu viele verdächtige Requests in kurzer Zeit
            if (
                len(self.suspicious_ips[client_ip]) > 10
            ):  # Mehr als 10 verdächtige Requests pro Stunde
                self.blocked_ips.add(client_ip)
                logging.warning(f"IP {client_ip} blocked due to suspicious activity")
                return True

            return suspicious

    def _has_invalid_patterns(self, request_data: Dict) -> bool:
        """Prüft auf verdächtige Eingabemuster"""
        # Extrem hohe Werte (mögliche Angriffe)
        if request_data.get("RE4", 0) > 50000000:  # > 500.000€
            return True

        # Negative Werte wo sie nicht erlaubt sind
        numeric_fields = ["RE4", "JFREIB", "JHINZU", "JRE4", "SONSTB"]
        for field in numeric_fields:
            if request_data.get(field, 0) < 0:
                return True

        # Ungültige Kombinationen
        if request_data.get("STKL") == 4 and request_data.get("f", 1.0) > 5.0:
            return True

        return False

    def is_blocked(self, client_ip: str) -> bool:
        """Prüft ob eine IP blockiert ist"""
        return client_ip in self.blocked_ips


# Globale Instanzen
security_monitor = SecurityMonitor()
structured_logger = StructuredLogger("lohnsteuer_api")
