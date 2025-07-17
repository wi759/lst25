import ast
import json
from decimal import Decimal
from pathlib import Path
from tax_calculator import TaxCalculator2025
from pydantic import BaseModel, Field


# Replicate LohnsteuerRequest model here to avoid import issues
class LohnsteuerRequest(BaseModel):
    af: int = Field(1, description="Arbeitslohn-Faktor")
    AJAHR: int = Field(0, description="Anrechnungsjahr")
    ALTER1: int = Field(0, description="Alterseinkünfte-Entlastungsbetrag")
    f: float = Field(1.0, description="Faktor für Lohnsteuerberechnung")
    JFREIB: Decimal = Field(Decimal("0"), description="Jahresfreibetrag")
    JHINZU: Decimal = Field(Decimal("0"), description="Jahreshinzurechnungsbetrag")
    JRE4: Decimal = Field(Decimal("0"), description="Jahres-Bruttoarbeitslohn")
    JRE4ENT: Decimal = Field(
        Decimal("0"), description="Entschädigungen im Jahres-Bruttoarbeitslohn"
    )
    JVBEZ: Decimal = Field(Decimal("0"), description="Jahres-Versorgungsbezüge")
    KRV: int = Field(0, description="Krankenversicherungs-Art")
    KVZ: Decimal = Field(Decimal("0"), description="Krankenversicherungs-Zusatzbeitrag")
    LZZ: int = Field(2, description="Lohnzahlungszeitraum")
    LZZFREIB: Decimal = Field(
        Decimal("0"), description="Lohnzahlungszeitraum-Freibetrag"
    )
    LZZHINZU: Decimal = Field(
        Decimal("0"), description="Lohnzahlungszeitraum-Hinzurechnungsbetrag"
    )
    MBV: Decimal = Field(Decimal("0"), description="Mehrjährige Bezugsvergütung")
    PKPV: Decimal = Field(
        Decimal("0"), description="Private Krankenversicherungs-Beiträge"
    )
    PKV: int = Field(0, description="Private Krankenversicherung")
    PVA: Decimal = Field(Decimal("0"), description="Pflegeversicherungs-Anteil")
    PVS: int = Field(0, description="Pflegeversicherung-Sachsen")
    PVZ: int = Field(0, description="Pflegeversicherung-Zuschlag")
    R: int = Field(0, description="Religionszugehörigkeit")
    RE4: Decimal = Field(Decimal("0"), description="Bruttoarbeitslohn")
    SONSTB: Decimal = Field(Decimal("0"), description="Sonstige Bezüge")
    SONSTENT: Decimal = Field(
        Decimal("0"), description="Entschädigungen in sonstigen Bezügen"
    )
    STERBE: Decimal = Field(Decimal("0"), description="Sterbegeld")
    STKL: int = Field(1, description="Steuerklasse")
    VBEZ: Decimal = Field(Decimal("0"), description="Versorgungsbezüge")
    VBEZM: Decimal = Field(Decimal("0"), description="Versorgungsbezugs-Monatsbetrag")
    VBEZS: Decimal = Field(Decimal("0"), description="Versorgungsbezugs-Sonderzahlung")
    VBS: Decimal = Field(
        Decimal("0"), description="Versorgungsbezugs-Sonderzahlung für mehrere Jahre"
    )
    VJAHR: int = Field(0, description="Versorgungsbeginn-Jahr")
    ZKF: Decimal = Field(Decimal("0"), description="Kinderfreibeträge")
    ZMVB: int = Field(0, description="Anzahl der Monate mit Versorgungsbezug")


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return super(DecimalEncoder, self).default(obj)


def extract_request_data(dict_node):
    """Extracts the request_data dictionary from an AST Dict node."""
    data = {}
    for key_node, value_node in zip(dict_node.keys, dict_node.values):
        key = ast.literal_eval(key_node)

        if (
            isinstance(value_node, ast.Call)
            and getattr(value_node.func, "id", "") == "Decimal"
        ):
            # Handle Decimal('...')
            arg = value_node.args[0]
            val = ast.literal_eval(arg)
            data[key] = Decimal(val)
        else:
            # Handle other literals like strings, numbers
            data[key] = ast.literal_eval(value_node)
    return data


def get_all_test_values():
    """
    Parses test_main.py, extracts test data for each test function,
    runs the tax calculation, and returns a dictionary of results.
    """
    # Correctly locate test_main.py relative to this script
    base_path = Path(__file__).parent
    test_file_path = base_path / "test_main.py"

    with open(test_file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())

    all_results = {}

    for func_def in ast.walk(tree):
        if not isinstance(func_def, ast.FunctionDef) or not func_def.name.startswith(
            "test_"
        ):
            continue

        request_data_dict = None
        for node in func_def.body:
            if (
                isinstance(node, ast.Assign)
                and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name)
                and node.targets[0].id == "request_data"
            ):
                request_data_dict = extract_request_data(node.value)
                break

        if request_data_dict:
            try:
                # Ensure all values from the model are present, providing defaults if not
                request = LohnsteuerRequest(**request_data_dict)
                calculator = TaxCalculator2025(**request.model_dump())
                result = calculator.calculate()
                all_results[func_def.name] = result
            except Exception as e:
                print(f"Could not calculate for {func_def.name}: {e}")

    return all_results


if __name__ == "__main__":
    test_results = get_all_test_values()

    output_file = Path(__file__).parent / "test_results.py"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# This file is auto-generated by get_all_test_values.py\n")
        f.write("from decimal import Decimal\n\n")
        f.write("TEST_RESULTS = {\n")
        for test_name, results in test_results.items():
            f.write(f"    '{test_name}': {{\n")
            for key, value in results.items():
                if isinstance(value, Decimal):
                    f.write(f"        '{key}': Decimal('{value}'),\n")
                else:
                    f.write(f"        '{key}': {repr(value)},\n")
            f.write("    },\n")
        f.write("}\n")

    print(f"Test results saved to {output_file}")
