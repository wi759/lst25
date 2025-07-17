import pytest
from decimal import Decimal
from tax_calculator import TaxCalculator2025
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)


class TestTaxCalculator2025:
    """Umfassende Tests für die Lohnsteuerberechnung 2025"""

    def test_basic_calculation_steuerklasse_1(self):
        """Test für Steuerklasse I, alleinstehend, keine Kinder"""
        calculator = TaxCalculator2025(
            RE4=Decimal(350000),  # 3500€ in Cent
            STKL=1,
            LZZ=2,  # Monat
            ZKF=Decimal(0),
            R=0,
            KVZ=Decimal("1.7"),
        )
        result = calculator.calculate()

        # Grundlegende Validierungen
        assert result["LSTLZZ"] >= 0, "Lohnsteuer darf nicht negativ sein"
        assert result["SOLZLZZ"] >= 0, "Solidaritätszuschlag darf nicht negativ sein"
        assert result["BK"] == 0, "Keine Kirchensteuer bei R=0"

        # Plausibilitätsprüfung: Lohnsteuer sollte zwischen 15-25% liegen
        tax_rate = float(result["LSTLZZ"]) / 350000 * 100
        assert 10 <= tax_rate <= 30, (
            f"Steuersatz {tax_rate:.1f}% erscheint unrealistisch"
        )

    def test_steuerklasse_3_married(self):
        """Test für Steuerklasse III, verheiratet"""
        calculator = TaxCalculator2025(
            RE4=Decimal(450000),  # 4500€ in Cent
            STKL=3,
            LZZ=2,
            ZKF=Decimal(0),
            R=1,  # Kirchensteuer
            KVZ=Decimal("1.7"),
        )
        result = calculator.calculate()

        assert result["LSTLZZ"] >= 0
        assert result["BK"] > 0, "Kirchensteuer sollte bei R=1 > 0 sein"

        # Steuerklasse III sollte günstiger sein als Steuerklasse I
        calculator_stkl1 = TaxCalculator2025(
            RE4=Decimal(450000), STKL=1, LZZ=2, ZKF=Decimal(0), R=1, KVZ=Decimal("1.7")
        )
        result_stkl1 = calculator_stkl1.calculate()

        assert result["LSTLZZ"] < result_stkl1["LSTLZZ"], (
            "Steuerklasse III sollte günstiger sein als I"
        )

    def test_kinderfreibetrag_effect(self):
        """Test für Auswirkung von Kinderfreibeträgen"""
        # Ohne Kinder
        calc_no_kids = TaxCalculator2025(
            RE4=Decimal(400000), STKL=1, LZZ=2, ZKF=Decimal(0), R=0
        )
        result_no_kids = calc_no_kids.calculate()

        # Mit 1 Kind
        calc_with_kid = TaxCalculator2025(
            RE4=Decimal(400000), STKL=1, LZZ=2, ZKF=Decimal(1), R=0
        )
        result_with_kid = calc_with_kid.calculate()

        assert result_with_kid["LSTLZZ"] <= result_no_kids["LSTLZZ"], (
            "Kinderfreibetrag sollte Steuer reduzieren"
        )

    def test_lzz_consistency(self):
        """Test für Konsistenz zwischen verschiedenen Lohnzahlungszeiträumen"""
        base_params = {
            "RE4": Decimal(350000),  # 3500€ monatlich
            "STKL": 1,
            "ZKF": Decimal(0),
            "R": 0,
            "KVZ": Decimal("1.7"),
        }

        # Monatlich
        calc_monthly = TaxCalculator2025(LZZ=2, **base_params)
        result_monthly = calc_monthly.calculate()

        # Jährlich (3500 * 12 = 42000)
        calc_yearly = TaxCalculator2025(
            LZZ=1,
            RE4=Decimal(4200000),  # 42000€ jährlich in Cent
            **{k: v for k, v in base_params.items() if k != "RE4"},
        )
        result_yearly = calc_yearly.calculate()

        # Jahressteuer sollte etwa 12x Monatssteuer sein (mit kleinen Abweichungen durch Progression)
        monthly_annual = float(result_monthly["LSTLZZ"]) * 12
        yearly_tax = float(result_yearly["LSTLZZ"])

        # Toleranz von 5% wegen Steuerprogression
        tolerance = 0.05
        assert abs(monthly_annual - yearly_tax) / yearly_tax <= tolerance, (
            f"Inkonsistenz zwischen LZZ: Monatlich*12={monthly_annual:.2f}, Jährlich={yearly_tax:.2f}"
        )

    def test_edge_cases(self):
        """Test für Grenzfälle"""
        # Sehr niedriger Lohn
        calc_low = TaxCalculator2025(
            RE4=Decimal(50000),  # 500€
            STKL=1,
            LZZ=2,
        )
        result_low = calc_low.calculate()
        assert result_low["LSTLZZ"] == 0, (
            "Bei niedrigem Einkommen sollte keine Lohnsteuer anfallen"
        )

        # Sehr hoher Lohn
        calc_high = TaxCalculator2025(
            RE4=Decimal(2000000),  # 20000€
            STKL=1,
            LZZ=2,
        )
        result_high = calc_high.calculate()
        assert result_high["LSTLZZ"] > 0, (
            "Bei hohem Einkommen sollte Lohnsteuer anfallen"
        )

        # Spitzensteuersatz sollte nicht überschritten werden
        tax_rate = float(result_high["LSTLZZ"]) / 2000000 * 100
        assert tax_rate <= 45, (
            f"Steuersatz {tax_rate:.1f}% überschreitet Spitzensteuersatz"
        )


class TestAPIEndpoints:
    """Tests für die FastAPI Endpunkte"""

    def test_calculate_endpoint_success(self):
        """Test für erfolgreiche API-Berechnung"""
        data = {"RE4": 350000, "STKL": 1, "LZZ": 2, "ZKF": 0, "R": 0, "KVZ": 1.7}

        response = client.post("/api/v1/calculate_payroll_tax", json=data)
        assert response.status_code == 200

        result = response.json()
        assert "LSTLZZ" in result
        assert "SOLZLZZ" in result
        assert "BK" in result
        assert isinstance(result["LSTLZZ"], (int, float, str))

    def test_calculate_endpoint_validation(self):
        """Test für Eingabevalidierung"""
        # Fehlende Pflichtfelder
        data = {
            "STKL": 1,
            "LZZ": 2,
            # RE4 fehlt
        }

        response = client.post("/api/v1/calculate_payroll_tax", json=data)
        assert response.status_code == 422  # Validation Error

    def test_calculate_endpoint_invalid_values(self):
        """Test für ungültige Werte"""
        data = {
            "RE4": -1000,  # Negativer Wert
            "STKL": 7,  # Ungültige Steuerklasse
            "LZZ": 5,  # Ungültiger LZZ
        }

        response = client.post("/api/v1/calculate_payroll_tax", json=data)
        # Sollte entweder 422 (Validation Error) oder 500 (Server Error) sein
        assert response.status_code in [422, 500]


class TestReferenceValues:
    """Tests mit bekannten Referenzwerten"""

    def test_reference_calculation_1(self):
        """Referenzberechnung 1: Standardfall"""
        # Diese Werte sollten aus offiziellen Quellen oder vertrauenswürdigen Rechnern stammen
        calculator = TaxCalculator2025(
            RE4=Decimal(300000),  # 3000€
            STKL=1,
            LZZ=2,
            ZKF=Decimal(0),
            R=0,
            KVZ=Decimal("1.7"),
            PKV=0,
            PVS=0,
            PVZ=0,
            KRV=0,
        )
        result = calculator.calculate()

        # TODO: Hier sollten bekannte Referenzwerte eingetragen werden
        # Beispiel: assert abs(float(result['LSTLZZ']) - 45000) < 100  # ±1€ Toleranz

        # Für jetzt: Plausibilitätsprüfung
        assert 20000 <= result["LSTLZZ"] <= 80000, (
            f"Lohnsteuer {result['LSTLZZ'] / 100:.2f}€ außerhalb erwarteter Spanne"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
