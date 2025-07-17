from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, field_validator
from decimal import Decimal, getcontext
from typing import Optional
import os
import logging
import time
from collections import defaultdict
from tax_calculator import TaxCalculator2025
from monitoring import metrics, structured_logger, security_monitor
from export_service import PDFExportService, ExcelExportService, ComparisonExportService
from fastapi.responses import StreamingResponse
from typing import List
import uuid
import io

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Set precision for Decimal calculations
getcontext().prec = 50

# Rate limiting storage
request_counts = defaultdict(list)


class LohnsteuerRequest(BaseModel):
    af: int = Field(
        default=1,
        ge=0,
        le=1,
        description="1, wenn die Anwendung des Faktorverfahrens gewählt wurden (nur in Steuerklasse IV)",
    )
    AJAHR: Optional[int] = Field(
        default=0,
        ge=1900,
        le=2100,
        description="Auf die Vollendung des 64. Lebensjahres folgende Kalenderjahr",
    )
    ALTER1: Optional[int] = Field(
        default=0,
        ge=0,
        le=1,
        description="1, wenn das 64. Lebensjahr zu Beginn des Kalenderjahres vollendet wurde",
    )
    f: float = Field(
        default=1.0,
        ge=0.001,
        le=10.0,
        description="Eingetragener Faktor mit drei Nachkommastellen",
    )
    JFREIB: Optional[Decimal] = Field(
        default=Decimal(0),
        ge=0,
        le=Decimal(10000000),
        description="Jahresfreibetrag in Cent",
    )
    JHINZU: Optional[Decimal] = Field(
        default=Decimal(0),
        ge=0,
        le=Decimal(10000000),
        description="Jahreshinzurechnungsbetrag in Cent",
    )
    JRE4: Optional[Decimal] = Field(
        default=Decimal(0),
        ge=0,
        le=Decimal(100000000),
        description="Voraussichtlicher Jahresarbeitslohn in Cent",
    )
    JRE4ENT: Optional[Decimal] = Field(
        default=Decimal(0),
        ge=0,
        le=Decimal(100000000),
        description="In JRE4 enthaltene Entschädigungen",
    )
    JVBEZ: Optional[Decimal] = Field(
        default=Decimal(0),
        ge=0,
        le=Decimal(100000000),
        description="In JRE4 enthaltene Versorgungsbezuege in Cents",
    )
    KRV: Optional[int] = Field(
        default=0, ge=0, le=1, description="Merker für die Vorsorgepauschale (0 oder 1)"
    )
    KVZ: Optional[Decimal] = Field(
        default=Decimal(0),
        ge=0,
        le=Decimal(10),
        description="Kassenindividueller Zusatzbeitragssatz in Prozent",
    )
    LZZ: int = Field(
        ge=1, le=4, description="Lohnzahlungszeitraum: 1=Jahr, 2=Monat, 3=Woche, 4=Tag"
    )
    LZZFREIB: Optional[Decimal] = Field(
        default=Decimal(0),
        ge=0,
        le=Decimal(10000000),
        description="Freibetrag für den Lohnzahlungszeitraum in Cent",
    )
    LZZHINZU: Optional[Decimal] = Field(
        default=Decimal(0),
        ge=0,
        le=Decimal(10000000),
        description="Hinzurechnungsbetrag für den Lohnzahlungszeitraum in Cent",
    )
    MBV: Optional[Decimal] = Field(
        default=Decimal(0),
        ge=0,
        le=Decimal(10000000),
        description="Nicht zu besteuernde Vorteile bei Vermögensbeteiligungen in Cent",
    )
    PKPV: Optional[Decimal] = Field(
        default=Decimal(0),
        ge=0,
        le=Decimal(200000),
        description="Private Kranken- bzw. Pflegeversicherung Monatsbetrag in Cent",
    )
    PKV: int = Field(
        default=0,
        ge=0,
        le=2,
        description="0=gesetzlich, 1=privat ohne AG-Zuschuss, 2=privat mit AG-Zuschuss",
    )
    PVA: Optional[Decimal] = Field(
        default=Decimal(0),
        ge=0,
        le=Decimal(10),
        description="Beitragsabschläge in der sozialen Pflegeversicherung",
    )
    PVS: Optional[int] = Field(
        default=0,
        ge=0,
        le=1,
        description="1, wenn Besonderheiten in Sachsen zu berücksichtigen sind",
    )
    PVZ: Optional[int] = Field(
        default=0,
        ge=0,
        le=1,
        description="1, wenn Zuschlag zur sozialen Pflegeversicherung zu zahlen ist",
    )
    R: Optional[int] = Field(
        default=0, ge=0, le=2, description="Religionsgemeinschaft des Arbeitnehmers"
    )
    RE4: Decimal = Field(
        ge=0,
        le=Decimal(100000000),
        description="Steuerpflichtiger Arbeitslohn für den Lohnzahlungszeitraum in Cent",
    )
    SONSTB: Optional[Decimal] = Field(
        default=Decimal(0),
        ge=0,
        le=Decimal(100000000),
        description="Sonstige Bezüge in Cent",
    )
    SONSTENT: Optional[Decimal] = Field(
        default=Decimal(0),
        ge=0,
        le=Decimal(100000000),
        description="In SONSTB enthaltene Entschädigungen",
    )
    STERBE: Optional[Decimal] = Field(
        default=Decimal(0),
        ge=0,
        le=Decimal(1000000),
        description="Sterbegeld bei Versorgungsbezuegen",
    )
    STKL: int = Field(ge=1, le=6, description="Steuerklasse: 1-6")
    VBEZ: Optional[Decimal] = Field(
        default=Decimal(0),
        ge=0,
        le=Decimal(100000000),
        description="In RE4 enthaltene Versorgungsbezuege in Cents",
    )
    VBEZM: Optional[Decimal] = Field(
        default=Decimal(0),
        ge=0,
        le=Decimal(10000000),
        description="Vorsorgungsbezug im Januar 2005 oder ersten vollen Monat in Cents",
    )
    VBEZS: Optional[Decimal] = Field(
        default=Decimal(0),
        ge=0,
        le=Decimal(10000000),
        description="Voraussichtliche Sonderzahlungen im Kalenderjahr des Versorgungsbeginns",
    )
    VBS: Optional[Decimal] = Field(
        default=Decimal(0),
        ge=0,
        le=Decimal(100000000),
        description="In SONSTB enthaltene Versorgungsbezuege",
    )
    VJAHR: Optional[int] = Field(
        default=0,
        ge=0,
        le=2100,
        description="Jahr, in dem der Versorgungsbezug erstmalig gewährt wurde",
    )
    ZKF: Optional[Decimal] = Field(
        default=Decimal(0),
        ge=0,
        le=Decimal(20),
        description="Zahl der Freibetraege fuer Kinder",
    )
    ZMVB: Optional[int] = Field(
        default=0,
        ge=0,
        le=12,
        description="Zahl der Monate, fuer die Versorgungsbezuege gezahlt werden",
    )

    @field_validator("RE4")
    @classmethod
    def validate_re4_not_zero(cls, v):
        if v <= 0:
            raise ValueError("RE4 (Arbeitslohn) muss größer als 0 sein")
        return v

    @field_validator("ZKF")
    @classmethod
    def validate_zkf_increment(cls, v):
        # ZKF muss in 0.5er Schritten sein
        if v % Decimal("0.5") != 0:
            raise ValueError(
                "Kinderfreibeträge müssen in 0.5er Schritten angegeben werden"
            )
        return v


class LohnsteuerResponse(BaseModel):
    BK: Decimal
    BKS: Decimal
    LSTLZZ: Decimal
    SOLZLZZ: Decimal
    SOLZS: Decimal
    STS: Decimal
    VKVLZZ: Decimal
    VKVSONST: Decimal
    VFRB: Optional[Decimal] = None
    VFRBS1: Optional[Decimal] = None
    VFRBS2: Optional[Decimal] = None
    WVFRB: Optional[Decimal] = None
    WVFRBO: Optional[Decimal] = None
    WVFRBM: Optional[Decimal] = None


app = FastAPI(
    title="Lohnsteuerrechner 2025 API",
    description="Eine API zur präzisen Berechnung der deutschen Lohnsteuer für das Jahr 2025 gemäß dem offiziellen Programmablaufplan des Bundesministeriums der Finanzen.",
    version="1.1.0",
    contact={
        "name": "Entwickler-Team",
        "url": "https://github.com/your-repo/lohnsteuer-rechner",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    docs_url="/docs",
    redoc_url="/redoc",
)

# Read allowed origins from environment variable, default to "*"
allowed_origins = os.environ.get("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiting configuration
RATE_LIMIT_REQUESTS = int(
    os.environ.get("RATE_LIMIT_REQUESTS", "100")
)  # requests per minute
RATE_LIMIT_WINDOW = int(os.environ.get("RATE_LIMIT_WINDOW", "60"))  # seconds


def check_rate_limit(client_ip: str) -> bool:
    """Check if client has exceeded rate limit"""
    current_time = time.time()

    # Clean old requests
    request_counts[client_ip] = [
        req_time
        for req_time in request_counts[client_ip]
        if current_time - req_time < RATE_LIMIT_WINDOW
    ]

    # Check if limit exceeded
    if len(request_counts[client_ip]) >= RATE_LIMIT_REQUESTS:
        return False

    # Add current request
    request_counts[client_ip].append(current_time)
    return True


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    """Rate limiting middleware"""
    client_ip = request.client.host

    # Skip rate limiting for health checks
    if request.url.path in ["/", "/health"]:
        response = await call_next(request)
        return response

    if not check_rate_limit(client_ip):
        logging.warning(f"Rate limit exceeded for IP: {client_ip}")
        return JSONResponse(
            status_code=429,
            content={
                "detail": "Rate limit exceeded. Zu viele Anfragen in kurzer Zeit.",
                "retry_after": RATE_LIMIT_WINDOW,
            },
        )

    response = await call_next(request)
    return response


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Handle validation errors with user-friendly messages"""
    logging.warning(f"Validation error from {request.client.host}: {exc}")
    return JSONResponse(
        status_code=400,
        content={"detail": f"Eingabefehler: {str(exc)}", "type": "validation_error"},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected errors"""
    logging.error(
        f"Unexpected error from {request.client.host}: {type(exc).__name__} - {exc}"
    )
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Ein unerwarteter Fehler ist aufgetreten. Bitte versuchen Sie es später erneut.",
            "type": "internal_error",
        },
    )


@app.post("/api/v1/calculate_payroll_tax", response_model=LohnsteuerResponse, tags=["Berechnung"], summary="Berechnet die Lohnsteuer für 2025")
async def calculate_payroll_tax(request: LohnsteuerRequest, http_request: Request):
    """
    Dieser Endpunkt ist das Herzstück der API und berechnet die deutsche Lohnsteuer, den Solidaritätszuschlag und die Kirchensteuer für das Jahr 2025.

    - **Eingabewerte**: Alle monetären Werte müssen in Cent angegeben werden.
    - **Genauigkeit**: Die Berechnung erfolgt mit hoher Präzision unter Verwendung von Dezimalzahlen.
    - **Validierung**: Die Eingabedaten werden serverseitig validiert.
    """
    start_time = time.time()
    client_ip = http_request.client.host
    user_agent = http_request.headers.get("user-agent", "Unknown")

    # Security check
    if security_monitor.is_blocked(client_ip):
        structured_logger.log_error(
            "blocked_ip", f"Request from blocked IP: {client_ip}", client_ip=client_ip
        )
        raise HTTPException(status_code=403, detail="Zugriff verweigert")

    # Log incoming request
    structured_logger.log_request(
        "POST", "/api/v1/calculate_payroll_tax", client_ip, user_agent
    )

    # Check for suspicious activity
    request_data = request.model_dump()
    if security_monitor.check_suspicious_activity(client_ip, request_data):
        structured_logger.log_error(
            "suspicious_activity",
            "Suspicious request pattern detected",
            request_data,
            client_ip,
        )

    try:
        # Input sanitization and validation
        sanitized_data = _sanitize_input(request_data)

        # Perform calculation
        calculator = TaxCalculator2025(**sanitized_data)
        result = calculator.calculate()

        # Calculate processing time
        processing_time = time.time() - start_time

        # Log successful calculation
        structured_logger.log_calculation(sanitized_data, result, processing_time)

        # Record metrics
        metrics.record_request("/api/v1/calculate_payroll_tax", processing_time, 200)

        return result

    except ValueError as e:
        processing_time = time.time() - start_time
        structured_logger.log_validation_error(
            "input_validation", str(e), str(e), client_ip
        )
        metrics.record_request(
            "/api/v1/calculate_payroll_tax", processing_time, 400, "validation_error"
        )
        raise HTTPException(status_code=400, detail=f"Eingabefehler: {str(e)}")

    except Exception as e:
        processing_time = time.time() - start_time
        error_type = type(e).__name__
        structured_logger.log_error(error_type, str(e), request_data, client_ip)
        metrics.record_request(
            "/api/v1/calculate_payroll_tax", processing_time, 500, error_type
        )
        raise HTTPException(
            status_code=500,
            detail=f"Ein interner Fehler ist während der Berechnung aufgetreten: {error_type}",
        )


def _sanitize_input(data: dict) -> dict:
    """Sanitizes and validates input data"""
    sanitized = data.copy()

    # Ensure all Decimal fields are properly converted
    decimal_fields = [
        "JFREIB",
        "JHINZU",
        "JRE4",
        "JRE4ENT",
        "JVBEZ",
        "KVZ",
        "LZZFREIB",
        "LZZHINZU",
        "MBV",
        "PKPV",
        "PVA",
        "RE4",
        "SONSTB",
        "SONSTENT",
        "STERBE",
        "VBEZ",
        "VBEZM",
        "VBEZS",
        "VBS",
        "ZKF",
    ]

    for field in decimal_fields:
        if field in sanitized and sanitized[field] is not None:
            try:
                sanitized[field] = Decimal(str(sanitized[field]))
            except (ValueError, TypeError):
                raise ValueError(f"Ungültiger Wert für {field}: {sanitized[field]}")

    # Additional business logic validation
    if sanitized.get("STKL") == 4 and sanitized.get("f", 1.0) == 1.0:
        # Bei Steuerklasse IV ohne Faktor, setze af auf 0
        sanitized["af"] = 0

    return sanitized


@app.get("/")
async def read_root():
    return FileResponse('../frontend/index.html')


@app.get("/health")
def health_check():
    """Health check endpoint for monitoring"""
    try:
        # Test basic calculation to ensure everything works
        test_calc = TaxCalculator2025(
            RE4=Decimal(100000),  # 1000€
            STKL=1,
            LZZ=2,
        )
        test_calc.calculate()

        return {
            "status": "healthy",
            "timestamp": time.time(),
            "version": "1.0.0",
            "calculation_test": "passed",
        }
    except Exception as e:
        logging.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "timestamp": time.time(), "error": str(e)},
        )


@app.get("/api/v1/info")
def api_info():
    """API information endpoint"""
    return {
        "name": "Lohnsteuerrechner 2025 API",
        "version": "1.0.0",
        "description": "Offizielle Lohnsteuerberechnung nach PAP 2025",
        "endpoints": {
            "calculate": "/api/v1/calculate_payroll_tax",
            "health": "/health",
            "docs": "/docs",
            "redoc": "/redoc",
        },
        "rate_limits": {
            "requests_per_minute": RATE_LIMIT_REQUESTS,
            "window_seconds": RATE_LIMIT_WINDOW,
        },
        "supported_years": [2025],
        "last_updated": "2025-01-16",
    }


@app.get("/api/v1/constants")
def get_tax_constants():
    """Get current tax constants for 2025"""
    return {
        "year": 2025,
        "grundfreibetrag": 12096,  # €
        "kinderfreibetrag": 9600,  # € pro Kind
        "solidaritaetszuschlag_freibetrag": 19950,  # €
        "beitragsbemessungsgrenze_rv": 96600,  # €
        "beitragsbemessungsgrenze_kv_pv": 66150,  # €
        "steuerklassen": {
            1: "Ledig, geschieden, verwitwet",
            2: "Alleinerziehend",
            3: "Verheiratet, höheres Einkommen",
            4: "Verheiratet, ähnliches Einkommen",
            5: "Verheiratet, geringeres Einkommen",
            6: "Nebenjob",
        },
        "kirchensteuer_saetze": {
            0: "Keine Kirchensteuer",
            1: "9% (Evangelisch/Katholisch)",
            2: "8% (Andere Religionsgemeinschaften)",
        },
    }


@app.get("/api/v1/metrics")
def get_metrics():
    """Get API metrics and statistics"""
    return {
        "api_metrics": metrics.get_stats(),
        "security_info": {
            "blocked_ips_count": len(security_monitor.blocked_ips),
            "rate_limit_config": {
                "requests_per_minute": RATE_LIMIT_REQUESTS,
                "window_seconds": RATE_LIMIT_WINDOW,
            },
        },
        "system_info": {"timestamp": time.time(), "uptime_check": "healthy"},
    }


# Export Services
pdf_service = PDFExportService()
excel_service = ExcelExportService()
comparison_service = ComparisonExportService()


class ExportRequest(BaseModel):
    input_data: dict
    result: dict
    name: Optional[str] = None


class ComparisonRequest(BaseModel):
    calculations: List[dict]
    format_type: str = Field(default="pdf", pattern="^(pdf|excel)$")


@app.post("/api/v1/export/pdf")
async def export_pdf(request: ExportRequest, http_request: Request):
    """Export calculation result as PDF"""
    try:
        calculation_id = str(uuid.uuid4())[:8]
        pdf_data = pdf_service.generate_calculation_report(
            request.input_data, request.result, calculation_id
        )

        filename = f"lohnsteuer_{calculation_id}.pdf"
        if request.name:
            safe_name = "".join(
                c for c in request.name if c.isalnum() or c in (" ", "-", "_")
            ).rstrip()
            filename = f"lohnsteuer_{safe_name}_{calculation_id}.pdf"

        return StreamingResponse(
            io.BytesIO(pdf_data),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
    except Exception as e:
        logging.error(f"PDF export error: {e}")
        raise HTTPException(status_code=500, detail="Fehler beim PDF-Export")


@app.post("/api/v1/export/excel")
async def export_excel(request: ExportRequest, http_request: Request):
    """Export calculation result as Excel"""
    try:
        calculation_id = str(uuid.uuid4())[:8]
        excel_data = excel_service.generate_calculation_report(
            request.input_data, request.result, calculation_id
        )

        filename = f"lohnsteuer_{calculation_id}.xlsx"
        if request.name:
            safe_name = "".join(
                c for c in request.name if c.isalnum() or c in (" ", "-", "_")
            ).rstrip()
            filename = f"lohnsteuer_{safe_name}_{calculation_id}.xlsx"

        return StreamingResponse(
            io.BytesIO(excel_data),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
    except Exception as e:
        logging.error(f"Excel export error: {e}")
        raise HTTPException(status_code=500, detail="Fehler beim Excel-Export")


@app.post("/api/v1/export/comparison")
async def export_comparison(request: ComparisonRequest, http_request: Request):
    """Export comparison of multiple calculations"""
    try:
        if len(request.calculations) < 2:
            raise HTTPException(
                status_code=400,
                detail="Mindestens 2 Berechnungen für Vergleich erforderlich",
            )

        if len(request.calculations) > 10:
            raise HTTPException(
                status_code=400, detail="Maximal 10 Berechnungen für Vergleich erlaubt"
            )

        comparison_data = comparison_service.generate_comparison_report(
            request.calculations, request.format_type
        )

        if request.format_type.lower() == "pdf":
            media_type = "application/pdf"
            extension = "pdf"
        else:
            media_type = (
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            extension = "xlsx"

        filename = f"lohnsteuer_vergleich_{str(uuid.uuid4())[:8]}.{extension}"

        return StreamingResponse(
            io.BytesIO(comparison_data),
            media_type=media_type,
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
    except Exception as e:
        logging.error(f"Comparison export error: {e}")
        raise HTTPException(status_code=500, detail="Fehler beim Vergleichs-Export")

# Mount frontend
app.mount("/", StaticFiles(directory="../frontend", html=True), name="static")
