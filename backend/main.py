from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from decimal import Decimal, getcontext
from typing import Optional
import os
import logging
from tax_calculator import TaxCalculator2025

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set precision for Decimal calculations
getcontext().prec = 50

class LohnsteuerRequest(BaseModel):
    af: int = Field(default=1, description="1, wenn die Anwendung des Faktorverfahrens gewählt wurden (nur in Steuerklasse IV)")
    AJAHR: Optional[int] = Field(default=None, description="Auf die Vollendung des 64. Lebensjahres folgende Kalenderjahr")
    ALTER1: Optional[int] = Field(default=0, description="1, wenn das 64. Lebensjahr zu Beginn des Kalenderjahres vollendet wurde")
    f: float = Field(default=1.0, description="Eingetragener Faktor mit drei Nachkommastellen")
    JFREIB: Optional[Decimal] = Field(default=Decimal(0), description="Jahresfreibetrag in Cent")
    JHINZU: Optional[Decimal] = Field(default=Decimal(0), description="Jahreshinzurechnungsbetrag in Cent")
    JRE4: Optional[Decimal] = Field(default=Decimal(0), description="Voraussichtlicher Jahresarbeitslohn in Cent")
    JRE4ENT: Optional[Decimal] = Field(default=Decimal(0), description="In JRE4 enthaltene Entschädigungen")
    JVBEZ: Optional[Decimal] = Field(default=Decimal(0), description="In JRE4 enthaltene Versorgungsbezuege in Cents")
    KRV: Optional[int] = Field(default=0, description="Merker für die Vorsorgepauschale (0 oder 1)")
    KVZ: Optional[Decimal] = Field(default=Decimal(0), description="Kassenindividueller Zusatzbeitragssatz in Prozent")
    LZZ: int = Field(description="Lohnzahlungszeitraum: 1=Jahr, 2=Monat, 3=Woche, 4=Tag")
    LZZFREIB: Optional[Decimal] = Field(default=Decimal(0), description="Freibetrag für den Lohnzahlungszeitraum in Cent")
    LZZHINZU: Optional[Decimal] = Field(default=Decimal(0), description="Hinzurechnungsbetrag für den Lohnzahlungszeitraum in Cent")
    MBV: Optional[Decimal] = Field(default=Decimal(0), description="Nicht zu besteuernde Vorteile bei Vermögensbeteiligungen in Cent")
    PKPV: Optional[Decimal] = Field(default=Decimal(0), description="Private Kranken- bzw. Pflegeversicherung Monatsbetrag in Cent")
    PKV: int = Field(default=0, description="0=gesetzlich, 1=privat ohne AG-Zuschuss, 2=privat mit AG-Zuschuss")
    PVA: Optional[Decimal] = Field(default=Decimal(0), description="Beitragsabschläge in der sozialen Pflegeversicherung")
    PVS: Optional[int] = Field(default=0, description="1, wenn Besonderheiten in Sachsen zu berücksichtigen sind")
    PVZ: Optional[int] = Field(default=0, description="1, wenn Zuschlag zur sozialen Pflegeversicherung zu zahlen ist")
    R: Optional[int] = Field(default=0, description="Religionsgemeinschaft des Arbeitnehmers")
    RE4: Decimal = Field(description="Steuerpflichtiger Arbeitslohn für den Lohnzahlungszeitraum in Cent")
    SONSTB: Optional[Decimal] = Field(default=Decimal(0), description="Sonstige Bezüge in Cent")
    SONSTENT: Optional[Decimal] = Field(default=Decimal(0), description="In SONSTB enthaltene Entschädigungen")
    STERBE: Optional[Decimal] = Field(default=Decimal(0), description="Sterbegeld bei Versorgungsbezuegen")
    STKL: int = Field(description="Steuerklasse: 1-6")
    VBEZ: Optional[Decimal] = Field(default=Decimal(0), description="In RE4 enthaltene Versorgungsbezuege in Cents")
    VBEZM: Optional[Decimal] = Field(default=Decimal(0), description="Vorsorgungsbezug im Januar 2005 oder ersten vollen Monat in Cents")
    VBEZS: Optional[Decimal] = Field(default=Decimal(0), description="Voraussichtliche Sonderzahlungen im Kalenderjahr des Versorgungsbeginns")
    VBS: Optional[Decimal] = Field(default=Decimal(0), description="In SONSTB enthaltene Versorgungsbezuege")
    VJAHR: Optional[int] = Field(default=0, description="Jahr, in dem der Versorgungsbezug erstmalig gewährt wurde")
    ZKF: Optional[Decimal] = Field(default=Decimal(0), description="Zahl der Freibetraege fuer Kinder")
    ZMVB: Optional[int] = Field(default=0, description="Zahl der Monate, fuer die Versorgungsbezuege gezahlt werden")

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


app = FastAPI()

# Read allowed origins from environment variable, default to "*"
allowed_origins = os.environ.get("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/v1/calculate_payroll_tax", response_model=LohnsteuerResponse)
def calculate_payroll_tax(request: LohnsteuerRequest):
    """
    Calculates the German payroll tax (Lohnsteuer) for 2025.

    This endpoint implements the official tax calculation algorithm.
    All monetary values are expected in cents.
    """
    logging.info(f"Received request: {request.dict()}")
    try:
        calculator = TaxCalculator2025(**request.dict())
        result = calculator.calculate()
        logging.info(f"Calculation successful, result: {result}")
        return result
    except Exception as e:
        # Log the error for internal debugging
        logging.error(f"Error during calculation: {type(e).__name__} - {e}")
        raise HTTPException(status_code=500, detail=f"Ein interner Fehler ist während der Berechnung aufgetreten: {type(e).__name__} - {e}")

@app.get("/")
def read_root():
    return {"message": "Lohnsteuer 2025 API is running."}
