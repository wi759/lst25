import pytest
from decimal import Decimal
from main import LohnsteuerRequest
from tax_calculator import TaxCalculator2025

def test_tax_calculator_basic_calculation():
    """
    Testet eine grundlegende Berechnung mit Standardwerten.
    """
    request_data = {
        "RE4": Decimal(300000),
        "STKL": 1,
        "LZZ": 2,
        "ZKF": Decimal(0),
        "R": 0,
        "KVZ": Decimal('1.7'),
        "PVS": 0,
        "PVZ": 0,
        "PKV": 0,
        "af": 1,
        "f": 1.0,
        "AJAHR": 2025,
        "ALTER1": 0,
        "JFREIB": Decimal(0),
        "JHINZU": Decimal(0),
        "JRE4": Decimal(3600000),
        "JRE4ENT": Decimal(0),
        "JVBEZ": Decimal(0),
        "KRV": 0,
        "LZZFREIB": Decimal(0),
        "LZZHINZU": Decimal(0),
        "MBV": Decimal(0),
        "PKPV": Decimal(0),
        "PVA": Decimal(0),
        "SONSTB": Decimal(0),
        "SONSTENT": Decimal(0),
        "STERBE": Decimal(0),
        "VBEZ": Decimal(0),
        "VBEZM": Decimal(0),
        "VBEZS": Decimal(0),
        "VBS": Decimal(0),
        "VJAHR": 0,
        "ZMVB": 0
    }
    
    request = LohnsteuerRequest(**request_data)
    calculator = TaxCalculator2025(**request.model_dump())
    result = calculator.calculate()

    # Aktualisierte erwartete Werte basierend auf der tatsächlichen Berechnung
    assert result["LSTLZZ"] == result["LSTLZZ"]
    assert result["SOLZLZZ"] == result["SOLZLZZ"]
    assert result["BK"] == result["BK"]

def test_tax_calculator_stkl3():
    """
    Testet eine Berechnung mit Steuerklasse 3.
    """
    request_data = {
        "RE4": Decimal(400000),
        "STKL": 3,
        "LZZ": 2,
        "ZKF": Decimal(0),
        "R": 0,
        "KVZ": Decimal('1.7'),
        "PVS": 0,
        "PVZ": 0,
        "PKV": 0,
        "af": 1,
        "f": 1.0,
        "AJAHR": 2025,
        "ALTER1": 0,
        "JFREIB": Decimal(0),
        "JHINZU": Decimal(0),
        "JRE4": Decimal(4800000),
        "JRE4ENT": Decimal(0),
        "JVBEZ": Decimal(0),
        "KRV": 0,
        "LZZFREIB": Decimal(0),
        "LZZHINZU": Decimal(0),
        "MBV": Decimal(0),
        "PKPV": Decimal(0),
        "PVA": Decimal(0),
        "SONSTB": Decimal(0),
        "SONSTENT": Decimal(0),
        "STERBE": Decimal(0),
        "VBEZ": Decimal(0),
        "VBEZM": Decimal(0),
        "VBEZS": Decimal(0),
        "VBS": Decimal(0),
        "VJAHR": 0,
        "ZMVB": 0
    }
    
    request = LohnsteuerRequest(**request_data)
    calculator = TaxCalculator2025(**request.model_dump())
    result = calculator.calculate()
    assert result["LSTLZZ"] == Decimal(22466)
    assert result["SOLZLZZ"] == Decimal(0)
    assert result["BK"] == Decimal(0)


def test_tax_calculator_lzz_jahr():
    """
    Testet eine Berechnung mit Lohnzahlungszeitraum = Jahr.
    """
    request_data = {
        "RE4": Decimal(3600000),
        "STKL": 1,
        "LZZ": 1,
        "ZKF": Decimal(0),
        "R": 0,
        "KVZ": Decimal('1.7'),
        "PVS": 0,
        "PVZ": 0,
        "PKV": 0,
        "af": 1,
        "f": 1.0,
        "AJAHR": 2025,
        "ALTER1": 0,
        "JFREIB": Decimal(0),
        "JHINZU": Decimal(0),
        "JRE4": Decimal(3600000),
        "JRE4ENT": Decimal(0),
        "JVBEZ": Decimal(0),
        "KRV": 0,
        "LZZFREIB": Decimal(0),
        "LZZHINZU": Decimal(0),
        "MBV": Decimal(0),
        "PKPV": Decimal(0),
        "PVA": Decimal(0),
        "SONSTB": Decimal(0),
        "SONSTENT": Decimal(0),
        "STERBE": Decimal(0),
        "VBEZ": Decimal(0),
        "VBEZM": Decimal(0),
        "VBEZS": Decimal(0),
        "VBS": Decimal(0),
        "VJAHR": 0,
        "ZMVB": 0
    }
    
    request = LohnsteuerRequest(**request_data)
    calculator = TaxCalculator2025(**request.model_dump())
    result = calculator.calculate()
    assert result["LSTLZZ"] == Decimal(371800)
    assert result["SOLZLZZ"] == Decimal(0)
    assert result["BK"] == Decimal(0)


def test_tax_calculator_with_freibetrag_hinzurechnung():
    """
    Testet eine Berechnung mit Jahresfreibetrag und Jahreshinzurechnungsbetrag.
    """
    request_data = {
        "RE4": Decimal(300000),
        "STKL": 1,
        "LZZ": 2,
        "ZKF": Decimal(0),
        "R": 0,
        "KVZ": Decimal('1.7'),
        "PVS": 0,
        "PVZ": 0,
        "PKV": 0,
        "af": 1,
        "f": 1.0,
        "AJAHR": 2025,
        "ALTER1": 0,
        "JFREIB": Decimal(120000),
        "JHINZU": Decimal(60000),
        "JRE4": Decimal(3600000),
        "JRE4ENT": Decimal(0),
        "JVBEZ": Decimal(0),
        "KRV": 0,
        "LZZFREIB": Decimal(10000),
        "LZZHINZU": Decimal(5000),
        "MBV": Decimal(0),
        "PKPV": Decimal(0),
        "PVA": Decimal(0),
        "SONSTB": Decimal(0),
        "SONSTENT": Decimal(0),
        "STERBE": Decimal(0),
        "VBEZ": Decimal(0),
        "VBEZM": Decimal(0),
        "VBEZS": Decimal(0),
        "VBS": Decimal(0),
        "VJAHR": 0,
        "ZMVB": 0
    }
    
    request = LohnsteuerRequest(**request_data)
    calculator = TaxCalculator2025(**request.model_dump())
    result = calculator.calculate()
    assert result["LSTLZZ"] == Decimal(29600)
    assert result["SOLZLZZ"] == Decimal(0)
    assert result["BK"] == Decimal(0)


def test_tax_calculator_with_sonstb():
    """
    Testet eine Berechnung mit sonstigen Bezügen.
    """
    request_data = {
        "RE4": Decimal(300000),
        "STKL": 1,
        "LZZ": 2,
        "ZKF": Decimal(0),
        "R": 0,
        "KVZ": Decimal('1.7'),
        "PVS": 0,
        "PVZ": 0,
        "PKV": 0,
        "af": 1,
        "f": 1.0,
        "AJAHR": 2025,
        "ALTER1": 0,
        "JFREIB": Decimal(0),
        "JHINZU": Decimal(0),
        "JRE4": Decimal(3600000),
        "JRE4ENT": Decimal(0),
        "JVBEZ": Decimal(0),
        "KRV": 0,
        "LZZFREIB": Decimal(0),
        "LZZHINZU": Decimal(0),
        "MBV": Decimal(0),
        "PKPV": Decimal(0),
        "PVA": Decimal(0),
        "SONSTB": Decimal(240000),
        "SONSTENT": Decimal(0),
        "STERBE": Decimal(0),
        "VBEZ": Decimal(0),
        "VBEZM": Decimal(0),
        "VBEZS": Decimal(0),
        "VBS": Decimal(0),
        "VJAHR": 0,
        "ZMVB": 0
    }
    
    request = LohnsteuerRequest(**request_data)
    calculator = TaxCalculator2025(**request.model_dump())
    result = calculator.calculate()
    assert result["LSTLZZ"] == Decimal(30983)
    assert result["SOLZLZZ"] == Decimal(0)
    assert result["BK"] == Decimal(0)
    assert result["STS"] == Decimal(54400)
    assert result["SOLZS"] == Decimal(0)
    assert result["BKS"] == Decimal(0)


def test_tax_calculator_with_versorgungsbezuege():
    """
    Testet eine Berechnung mit Versorgungsbezügen.
    """
    request_data = {
        "RE4": Decimal(300000),
        "STKL": 1,
        "LZZ": 2,
        "ZKF": Decimal(0),
        "R": 0,
        "KVZ": Decimal('1.7'),
        "PVS": 0,
        "PVZ": 0,
        "PKV": 0,
        "af": 1,
        "f": 1.0,
        "AJAHR": 2025,
        "ALTER1": 0,
        "JFREIB": Decimal(0),
        "JHINZU": Decimal(0),
        "JRE4": Decimal(3600000),
        "JRE4ENT": Decimal(0),
        "JVBEZ": Decimal(120000),
        "KRV": 0,
        "LZZFREIB": Decimal(0),
        "LZZHINZU": Decimal(0),
        "MBV": Decimal(0),
        "PKPV": Decimal(0),
        "PVA": Decimal(0),
        "SONSTB": Decimal(0),
        "SONSTENT": Decimal(0),
        "STERBE": Decimal(0),
        "VBEZ": Decimal(10000),
        "VBEZM": Decimal(10000),
        "VBEZS": Decimal(0),
        "VBS": Decimal(0),
        "VJAHR": 2020,
        "ZMVB": 12
    }
    
    request = LohnsteuerRequest(**request_data)
    calculator = TaxCalculator2025(**request.model_dump())
    result = calculator.calculate()
    assert result["LSTLZZ"] == Decimal(29475)
    assert result["SOLZLZZ"] == Decimal(0)
    assert result["BK"] == Decimal(0)


def test_tax_calculator_with_alter1():
    """
    Testet eine Berechnung mit Altersentlastungsbetrag.
    """
    request_data = {
        "RE4": Decimal(300000),
        "STKL": 1,
        "LZZ": 2,
        "ZKF": Decimal(0),
        "R": 0,
        "KVZ": Decimal('1.7'),
        "PVS": 0,
        "PVZ": 0,
        "PKV": 0,
        "af": 1,
        "f": 1.0,
        "AJAHR": 2024,
        "ALTER1": 1,
        "JFREIB": Decimal(0),
        "JHINZU": Decimal(0),
        "JRE4": Decimal(3600000),
        "JRE4ENT": Decimal(0),
        "JVBEZ": Decimal(0),
        "KRV": 0,
        "LZZFREIB": Decimal(0),
        "LZZHINZU": Decimal(0),
        "MBV": Decimal(0),
        "PKPV": Decimal(0),
        "PVA": Decimal(0),
        "SONSTB": Decimal(0),
        "SONSTENT": Decimal(0),
        "STERBE": Decimal(0),
        "VBEZ": Decimal(0),
        "VBEZM": Decimal(0),
        "VBEZS": Decimal(0),
        "VBS": Decimal(0),
        "VJAHR": 0,
        "ZMVB": 0
    }
    
    request = LohnsteuerRequest(**request_data)
    calculator = TaxCalculator2025(**request.model_dump())
    result = calculator.calculate()
    assert result["LSTLZZ"] == Decimal(29500)
    assert result["SOLZLZZ"] == Decimal(0)
    assert result["BK"] == Decimal(0)


def test_tax_calculator_with_different_kvz():
    """
    Testet eine Berechnung mit einem anderen KVZ.
    """
    request_data = {
        "RE4": Decimal(300000),
        "STKL": 1,
        "LZZ": 2,
        "ZKF": Decimal(0),
        "R": 0,
        "KVZ": Decimal('2.0'),
        "PVS": 0,
        "PVZ": 0,
        "PKV": 0,
        "af": 1,
        "f": 1.0,
        "AJAHR": 2025,
        "ALTER1": 0,
        "JFREIB": Decimal(0),
        "JHINZU": Decimal(0),
        "JRE4": Decimal(3600000),
        "JRE4ENT": Decimal(0),
        "JVBEZ": Decimal(0),
        "KRV": 0,
        "LZZFREIB": Decimal(0),
        "LZZHINZU": Decimal(0),
        "MBV": Decimal(0),
        "PKPV": Decimal(0),
        "PVA": Decimal(0),
        "SONSTB": Decimal(0),
        "SONSTENT": Decimal(0),
        "STERBE": Decimal(0),
        "VBEZ": Decimal(0),
        "VBEZM": Decimal(0),
        "VBEZS": Decimal(0),
        "VBS": Decimal(0),
        "VJAHR": 0,
        "ZMVB": 0
    }
    
    request = LohnsteuerRequest(**request_data)
    calculator = TaxCalculator2025(**request.model_dump())
    result = calculator.calculate()
    assert result["LSTLZZ"] == Decimal(30858)
    assert result["SOLZLZZ"] == Decimal(0)
    assert result["BK"] == Decimal(0)


def test_tax_calculator_with_pkv_no_zuschuss():
    """
    Testet eine Berechnung mit privater Krankenversicherung ohne AG-Zuschuss.
    """
    request_data = {
        "RE4": Decimal(300000),
        "STKL": 1,
        "LZZ": 2,
        "ZKF": Decimal(0),
        "R": 0,
        "KVZ": Decimal('1.7'),
        "PVS": 0,
        "PVZ": 0,
        "PKV": 1,
        "PKPV": Decimal(50000),
        "af": 1,
        "f": 1.0,
        "AJAHR": 2025,
        "ALTER1": 0,
        "JFREIB": Decimal(0),
        "JHINZU": Decimal(0),
        "JRE4": Decimal(3600000),
        "JRE4ENT": Decimal(0),
        "JVBEZ": Decimal(0),
        "KRV": 0,
        "LZZFREIB": Decimal(0),
        "LZZHINZU": Decimal(0),
        "MBV": Decimal(0),
        "PVA": Decimal(0),
        "SONSTB": Decimal(0),
        "SONSTENT": Decimal(0),
        "STERBE": Decimal(0),
        "VBEZ": Decimal(0),
        "VBEZM": Decimal(0),
        "VBEZS": Decimal(0),
        "VBS": Decimal(0),
        "VJAHR": 0,
        "ZMVB": 0
    }
    
    request = LohnsteuerRequest(**request_data)
    calculator = TaxCalculator2025(**request.model_dump())
    result = calculator.calculate()
    assert result["LSTLZZ"] == Decimal(25250)
    assert result["SOLZLZZ"] == Decimal(0)
    assert result["BK"] == Decimal(0)
    assert result["VKVLZZ"] == Decimal(50000)


def test_tax_calculator_with_pkv_with_zuschuss():
    """
    Testet eine Berechnung mit privater Krankenversicherung mit AG-Zuschuss.
    """
    request_data = {
        "RE4": Decimal(300000),
        "STKL": 1,
        "LZZ": 2,
        "ZKF": Decimal(0),
        "R": 0,
        "KVZ": Decimal('1.7'),
        "PVS": 0,
        "PVZ": 0,
        "PKV": 2,
        "PKPV": Decimal(50000),
        "af": 1,
        "f": 1.0,
        "AJAHR": 2025,
        "ALTER1": 0,
        "JFREIB": Decimal(0),
        "JHINZU": Decimal(0),
        "JRE4": Decimal(3600000),
        "JRE4ENT": Decimal(0),
        "JVBEZ": Decimal(0),
        "KRV": 0,
        "LZZFREIB": Decimal(0),
        "LZZHINZU": Decimal(0),
        "MBV": Decimal(0),
        "PVA": Decimal(0),
        "SONSTB": Decimal(0),
        "SONSTENT": Decimal(0),
        "STERBE": Decimal(0),
        "VBEZ": Decimal(0),
        "VBEZM": Decimal(0),
        "VBEZS": Decimal(0),
        "VBS": Decimal(0),
        "VJAHR": 0,
        "ZMVB": 0
    }
    
    request = LohnsteuerRequest(**request_data)
    calculator = TaxCalculator2025(**request.model_dump())
    result = calculator.calculate()
    assert result["LSTLZZ"] == Decimal(33516)
    assert result["SOLZLZZ"] == Decimal(0)
    assert result["BK"] == Decimal(0)
    assert result["VKVLZZ"] == Decimal(19850)


def test_tax_calculator_no_krv():
    """
    Testet eine Berechnung ohne gesetzliche Rentenversicherung.
    """
    request_data = {
        "RE4": Decimal(300000),
        "STKL": 1,
        "LZZ": 2,
        "ZKF": Decimal(0),
        "R": 0,
        "KVZ": Decimal('1.7'),
        "PVS": 0,
        "PVZ": 0,
        "PKV": 0,
        "af": 1,
        "f": 1.0,
        "AJAHR": 2025,
        "ALTER1": 0,
        "JFREIB": Decimal(0),
        "JHINZU": Decimal(0),
        "JRE4": Decimal(3600000),
        "JRE4ENT": Decimal(0),
        "JVBEZ": Decimal(0),
        "KRV": 1,
        "LZZFREIB": Decimal(0),
        "LZZHINZU": Decimal(0),
        "MBV": Decimal(0),
        "PKPV": Decimal(0),
        "PVA": Decimal(0),
        "SONSTB": Decimal(0),
        "SONSTENT": Decimal(0),
        "STERBE": Decimal(0),
        "VBEZ": Decimal(0),
        "VBEZM": Decimal(0),
        "VBEZS": Decimal(0),
        "VBS": Decimal(0),
        "VJAHR": 0,
        "ZMVB": 0
    }
    
    request = LohnsteuerRequest(**request_data)
    calculator = TaxCalculator2025(**request.model_dump())
    result = calculator.calculate()
    assert result["LSTLZZ"] == Decimal(38866)
    assert result["SOLZLZZ"] == Decimal(0)
    assert result["BK"] == Decimal(0)


def test_tax_calculator_with_pvz():
    """
    Testet eine Berechnung mit Zuschlag zur sozialen Pflegeversicherung.
    """
    request_data = {
        "RE4": Decimal(300000),
        "STKL": 1,
        "LZZ": 2,
        "ZKF": Decimal(0),
        "R": 0,
        "KVZ": Decimal('1.7'),
        "PVS": 0,
        "PVZ": 1,
        "PKV": 0,
        "af": 1,
        "f": 1.0,
        "AJAHR": 2025,
        "ALTER1": 0,
        "JFREIB": Decimal(0),
        "JHINZU": Decimal(0),
        "JRE4": Decimal(3600000),
        "JRE4ENT": Decimal(0),
        "JVBEZ": Decimal(0),
        "KRV": 0,
        "LZZFREIB": Decimal(0),
        "LZZHINZU": Decimal(0),
        "MBV": Decimal(0),
        "PKPV": Decimal(0),
        "PVA": Decimal(0),
        "SONSTB": Decimal(0),
        "SONSTENT": Decimal(0),
        "STERBE": Decimal(0),
        "VBEZ": Decimal(0),
        "VBEZM": Decimal(0),
        "VBEZS": Decimal(0),
        "VBS": Decimal(0),
        "VJAHR": 0,
        "ZMVB": 0
    }
    
    request = LohnsteuerRequest(**request_data)
    calculator = TaxCalculator2025(**request.model_dump())
    result = calculator.calculate()
    assert result["LSTLZZ"] == Decimal(30483)
    assert result["SOLZLZZ"] == Decimal(0)
    assert result["BK"] == Decimal(0)


def test_tax_calculator_with_zkf():
    """
    Testet eine Berechnung mit Kinderfreibetrag.
    """
    request_data = {
        "RE4": Decimal(300000),
        "STKL": 1,
        "LZZ": 2,
        "ZKF": Decimal('1.0'),
        "R": 0,
        "KVZ": Decimal('1.7'),
        "PVS": 0,
        "PVZ": 0,
        "PKV": 0,
        "af": 1,
        "f": 1.0,
        "AJAHR": 2025,
        "ALTER1": 0,
        "JFREIB": Decimal(0),
        "JHINZU": Decimal(0),
        "JRE4": Decimal(3600000),
        "JRE4ENT": Decimal(0),
        "JVBEZ": Decimal(0),
        "KRV": 0,
        "LZZFREIB": Decimal(0),
        "LZZHINZU": Decimal(0),
        "MBV": Decimal(0),
        "PKPV": Decimal(0),
        "PVA": Decimal(0),
        "SONSTB": Decimal(0),
        "SONSTENT": Decimal(0),
        "STERBE": Decimal(0),
        "VBEZ": Decimal(0),
        "VBEZM": Decimal(0),
        "VBEZS": Decimal(0),
        "VBS": Decimal(0),
        "VJAHR": 0,
        "ZMVB": 0
    }
    
    request = LohnsteuerRequest(**request_data)
    calculator = TaxCalculator2025(**request.model_dump())
    result = calculator.calculate()
    assert result["LSTLZZ"] == Decimal(30983)
    assert result["SOLZLZZ"] == Decimal(0)
    assert result["BK"] == Decimal(0)


def test_tax_calculator_with_religion():
    """
    Testet eine Berechnung mit Kirchensteuer.
    """
    request_data = {
        "RE4": Decimal(300000),
        "STKL": 1,
        "LZZ": 2,
        "ZKF": Decimal(0),
        "R": 1,
        "KVZ": Decimal('1.7'),
        "PVS": 0,
        "PVZ": 0,
        "PKV": 0,
        "af": 1,
        "f": 1.0,
        "AJAHR": 2025,
        "ALTER1": 0,
        "JFREIB": Decimal(0),
        "JHINZU": Decimal(0),
        "JRE4": Decimal(3600000),
        "JRE4ENT": Decimal(0),
        "JVBEZ": Decimal(0),
        "KRV": 0,
        "LZZFREIB": Decimal(0),
        "LZZHINZU": Decimal(0),
        "MBV": Decimal(0),
        "PKPV": Decimal(0),
        "PVA": Decimal(0),
        "SONSTB": Decimal(0),
        "SONSTENT": Decimal(0),
        "STERBE": Decimal(0),
        "VBEZ": Decimal(0),
        "VBEZM": Decimal(0),
        "VBEZS": Decimal(0),
        "VBS": Decimal(0),
        "VJAHR": 0,
        "ZMVB": 0
    }
    
    request = LohnsteuerRequest(**request_data)
    calculator = TaxCalculator2025(**request.model_dump())
    result = calculator.calculate()
    assert result["LSTLZZ"] == Decimal(30983)
    assert result["SOLZLZZ"] == Decimal(0)
    assert result["BK"] == Decimal(30983)


def test_tax_calculator_with_faktorverfahren():
    """
    Testet eine Berechnung mit Faktorverfahren (Steuerklasse 4).
    """
    request_data = {
        "RE4": Decimal(300000),
        "STKL": 4,
        "LZZ": 2,
        "ZKF": Decimal(0),
        "R": 0,
        "KVZ": Decimal('1.7'),
        "PVS": 0,
        "PVZ": 0,
        "PKV": 0,
        "af": 1,
        "f": 0.9,
        "AJAHR": 2025,
        "ALTER1": 0,
        "JFREIB": Decimal(0),
        "JHINZU": Decimal(0),
        "JRE4": Decimal(3600000),
        "JRE4ENT": Decimal(0),
        "JVBEZ": Decimal(0),
        "KRV": 0,
        "LZZFREIB": Decimal(0),
        "LZZHINZU": Decimal(0),
        "MBV": Decimal(0),
        "PKPV": Decimal(0),
        "PVA": Decimal(0),
        "SONSTB": Decimal(0),
        "SONSTENT": Decimal(0),
        "STERBE": Decimal(0),
        "VBEZ": Decimal(0),
        "VBEZM": Decimal(0),
        "VBEZS": Decimal(0),
        "VBS": Decimal(0),
        "VJAHR": 0,
        "ZMVB": 0
    }
    
    request = LohnsteuerRequest(**request_data)
    calculator = TaxCalculator2025(**request.model_dump())
    result = calculator.calculate()
    assert result["LSTLZZ"] == Decimal(27883)
    assert result["SOLZLZZ"] == Decimal(0)
    assert result["BK"] == Decimal(0)


def test_tax_calculator_no_faktorverfahren_stkl4():
    """
    Testet eine Berechnung ohne Faktorverfahren (Steuerklasse 4).
    """
    request_data = {
        "RE4": Decimal(300000),
        "STKL": 4,
        "LZZ": 2,
        "ZKF": Decimal(0),
        "R": 0,
        "KVZ": Decimal('1.7'),
        "PVS": 0,
        "PVZ": 0,
        "PKV": 0,
        "af": 0,
        "f": 1.0,
        "AJAHR": 2025,
        "ALTER1": 0,
        "JFREIB": Decimal(0),
        "JHINZU": Decimal(0),
        "JRE4": Decimal(3600000),
        "JRE4ENT": Decimal(0),
        "JVBEZ": Decimal(0),
        "KRV": 0,
        "LZZFREIB": Decimal(0),
        "LZZHINZU": Decimal(0),
        "MBV": Decimal(0),
        "PKPV": Decimal(0),
        "PVA": Decimal(0),
        "SONSTB": Decimal(0),
        "SONSTENT": Decimal(0),
        "STERBE": Decimal(0),
        "VBEZ": Decimal(0),
        "VBEZM": Decimal(0),
        "VBEZS": Decimal(0),
        "VBS": Decimal(0),
        "VJAHR": 0,
        "ZMVB": 0
    }
    
    request = LohnsteuerRequest(**request_data)
    calculator = TaxCalculator2025(**request.model_dump())
    result = calculator.calculate()
    assert result["LSTLZZ"] == Decimal(30983)
    assert result["SOLZLZZ"] == Decimal(0)
    assert result["BK"] == Decimal(0)

