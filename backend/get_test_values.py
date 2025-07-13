from tax_calculator import TaxCalculator2025
from decimal import Decimal

# Test 1: Basic calculation
test1_data = {
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

# Test 2: STKL3
test2_data = {
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

# Run test 1
calc1 = TaxCalculator2025(**test1_data)
result1 = calc1.calculate()
print("Test 1 Results:")
print(f'LSTLZZ: {result1["LSTLZZ"]}')
print(f'SOLZLZZ: {result1["SOLZLZZ"]}')
print(f'BK: {result1["BK"]}')

# Run test 2
calc2 = TaxCalculator2025(**test2_data)
result2 = calc2.calculate()
print("\nTest 2 Results:")
print(f'LSTLZZ: {result2["LSTLZZ"]}')
print(f'SOLZLZZ: {result2["SOLZLZZ"]}')
print(f'BK: {result2["BK"]}')