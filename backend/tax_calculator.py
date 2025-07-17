import logging
from decimal import Decimal, getcontext

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Set precision for Decimal calculations
getcontext().prec = 50


class TaxCalculator2025:
    def __init__(self, **kwargs):
        logging.info("Initializing TaxCalculator2025 with input parameters.")
        # INPUTS
        self.af = int(kwargs.get("af", 1))
        self.AJAHR = int(kwargs.get("AJAHR", 0))
        self.ALTER1 = int(kwargs.get("ALTER1", 0))
        self.f = float(kwargs.get("f", 1.0))
        self.JFREIB = Decimal(kwargs.get("JFREIB", "0"))
        self.JHINZU = Decimal(kwargs.get("JHINZU", "0"))
        self.JRE4 = Decimal(kwargs.get("JRE4", "0"))
        self.JRE4ENT = Decimal(kwargs.get("JRE4ENT", "0"))
        self.JVBEZ = Decimal(kwargs.get("JVBEZ", "0"))
        self.KRV = int(kwargs.get("KRV", 0))
        self.KVZ = Decimal(kwargs.get("KVZ", "0"))
        self.LZZ = int(kwargs.get("LZZ", 2))
        self.LZZFREIB = Decimal(kwargs.get("LZZFREIB", "0"))
        self.LZZHINZU = Decimal(kwargs.get("LZZHINZU", "0"))
        self.MBV = Decimal(kwargs.get("MBV", "0"))
        self.PKPV = Decimal(kwargs.get("PKPV", "0"))
        self.PKV = int(kwargs.get("PKV", 0))
        self.PVA = Decimal(kwargs.get("PVA", "0"))
        self.PVS = int(kwargs.get("PVS", 0))
        self.PVZ = int(kwargs.get("PVZ", 0))
        self.R = int(kwargs.get("R", 0))
        self.RE4 = Decimal(kwargs.get("RE4", "0"))
        self.SONSTB = Decimal(kwargs.get("SONSTB", "0"))
        self.SONSTENT = Decimal(kwargs.get("SONSTENT", "0"))
        self.STERBE = Decimal(kwargs.get("STERBE", "0"))
        self.STKL = int(kwargs.get("STKL", 1))
        self.VBEZ = Decimal(kwargs.get("VBEZ", "0"))
        self.VBEZM = Decimal(kwargs.get("VBEZM", "0"))
        self.VBEZS = Decimal(kwargs.get("VBEZS", "0"))
        self.VBS = Decimal(kwargs.get("VBS", "0"))
        self.VJAHR = int(kwargs.get("VJAHR", 0))
        self.ZKF = Decimal(kwargs.get("ZKF", "0"))
        self.ZMVB = int(kwargs.get("ZMVB", 0))

        # Log major input values for debugging
        logging.info(
            f"RE4: {self.RE4}, STKL: {self.STKL}, LZZ: {self.LZZ}, VBEZ: {self.VBEZ}"
        )

        # OUTPUTS
        self.BK = Decimal(0)
        self.BKS = Decimal(0)
        self.LSTLZZ = Decimal(0)
        self.SOLZLZZ = Decimal(0)
        self.SOLZS = Decimal(0)
        self.STS = Decimal(0)
        self.VKVLZZ = Decimal(0)
        self.VKVSONST = Decimal(0)
        self.VFRB = Decimal(0)
        self.VFRBS1 = Decimal(0)
        self.VFRBS2 = Decimal(0)
        self.WVFRB = Decimal(0)
        self.WVFRBO = Decimal(0)
        self.WVFRBM = Decimal(0)

        # INTERNALS
        self.ALTE = Decimal(0)
        self.ANP = Decimal(0)
        self.ANTEIL1 = Decimal(0)
        self.BMG = Decimal(0)
        self.BBGKVPV = Decimal(0)
        self.BBGRV = Decimal(0)
        self.DIFF = Decimal(0)
        self.EFA = Decimal(0)
        self.FVB = Decimal(0)
        self.FVBSO = Decimal(0)
        self.FVBZ = Decimal(0)
        self.FVBZSO = Decimal(0)
        self.GFB = Decimal(0)
        self.HBALTE = Decimal(0)
        self.HFVB = Decimal(0)
        self.HFVBZ = Decimal(0)
        self.HFVBZSO = Decimal(0)
        self.HOCH = Decimal(0)
        self.J = 0
        self.JBMG = Decimal(0)
        self.JLFREIB = Decimal(0)
        self.JLHINZU = Decimal(0)
        self.JW = Decimal(0)
        self.K = 0
        self.KFB = Decimal(0)
        self.KVSATZAG = Decimal(0)
        self.KVSATZAN = Decimal(0)
        self.KZTAB = 0
        self.LSTJAHR = Decimal(0)
        self.LSTOSO = Decimal(0)
        self.LSTSO = Decimal(0)
        self.MIST = Decimal(0)
        self.PVSATZAG = Decimal(0)
        self.PVSATZAN = Decimal(0)
        self.RVSATZAN = Decimal(0)
        self.RW = Decimal(0)
        self.SAP = Decimal(0)
        self.SOLZFREI = Decimal(0)
        self.SOLZJ = Decimal(0)
        self.SOLZMIN = Decimal(0)
        self.SOLZSBMG = Decimal(0)
        self.SOLZSZVE = Decimal(0)
        self.SOLZVBMG = Decimal(0)
        self.ST = Decimal(0)
        self.ST1 = Decimal(0)
        self.ST2 = Decimal(0)
        self.VBEZB = Decimal(0)
        self.VBEZBSO = Decimal(0)
        self.VERGL = Decimal(0)
        self.VHB = Decimal(0)
        self.VKV = Decimal(0)
        self.VSP = Decimal(0)
        self.VSPN = Decimal(0)
        self.VSP1 = Decimal(0)
        self.VSP2 = Decimal(0)
        self.VSP3 = Decimal(0)
        self.W1STKL5 = Decimal(0)
        self.W2STKL5 = Decimal(0)
        self.W3STKL5 = Decimal(0)
        self.X = Decimal(0)
        self.Y = Decimal(0)
        self.ZRE4 = Decimal(0)
        self.ZRE4J = Decimal(0)
        self.ZRE4VP = Decimal(0)
        self.ZTABFB = Decimal(0)
        self.ZVBEZ = Decimal(0)
        self.ZVBEZJ = Decimal(0)
        self.ZVE = Decimal(0)
        self.ZX = Decimal(0)
        self.ZZX = Decimal(0)

        # CONSTANTS
        self.TAB1 = [
            Decimal(v)
            for v in [
                0,
                0.4,
                0.384,
                0.368,
                0.352,
                0.336,
                0.32,
                0.304,
                0.288,
                0.272,
                0.256,
                0.24,
                0.224,
                0.208,
                0.192,
                0.176,
                0.16,
                0.152,
                0.144,
                0.14,
                0.136,
                0.132,
                0.128,
                0.124,
                0.12,
                0.116,
                0.112,
                0.108,
                0.104,
                0.1,
                0.096,
                0.092,
                0.088,
                0.084,
                0.08,
                0.076,
                0.072,
                0.068,
                0.064,
                0.06,
                0.056,
                0.052,
                0.048,
                0.044,
                0.04,
                0.036,
                0.032,
                0.028,
                0.024,
                0.02,
                0.016,
                0.012,
                0.008,
                0.004,
                0,
            ]
        ]
        self.TAB2 = [
            Decimal(v)
            for v in [
                0,
                3000,
                2880,
                2760,
                2640,
                2520,
                2400,
                2280,
                2160,
                2040,
                1920,
                1800,
                1680,
                1560,
                1440,
                1320,
                1200,
                1140,
                1080,
                1050,
                1020,
                990,
                960,
                930,
                900,
                870,
                840,
                810,
                780,
                750,
                720,
                690,
                660,
                630,
                600,
                570,
                540,
                510,
                480,
                450,
                420,
                390,
                360,
                330,
                300,
                270,
                240,
                210,
                180,
                150,
                120,
                90,
                60,
                30,
                0,
            ]
        ]
        self.TAB3 = [
            Decimal(v)
            for v in [
                0,
                900,
                864,
                828,
                792,
                756,
                720,
                684,
                648,
                612,
                576,
                540,
                504,
                468,
                432,
                396,
                360,
                342,
                324,
                315,
                306,
                297,
                288,
                279,
                270,
                261,
                252,
                243,
                234,
                225,
                216,
                207,
                198,
                189,
                180,
                171,
                162,
                153,
                144,
                135,
                126,
                117,
                108,
                99,
                90,
                81,
                72,
                63,
                54,
                45,
                36,
                27,
                18,
                9,
                0,
            ]
        ]
        self.TAB4 = [
            Decimal(v)
            for v in [
                0,
                0.4,
                0.384,
                0.368,
                0.352,
                0.336,
                0.32,
                0.304,
                0.288,
                0.272,
                0.256,
                0.24,
                0.224,
                0.208,
                0.192,
                0.176,
                0.16,
                0.152,
                0.144,
                0.14,
                0.136,
                0.132,
                0.128,
                0.124,
                0.12,
                0.116,
                0.112,
                0.108,
                0.104,
                0.1,
                0.096,
                0.092,
                0.088,
                0.084,
                0.08,
                0.076,
                0.072,
                0.068,
                0.064,
                0.06,
                0.056,
                0.052,
                0.048,
                0.044,
                0.04,
                0.036,
                0.032,
                0.028,
                0.024,
                0.02,
                0.016,
                0.012,
                0.008,
                0.004,
                0,
            ]
        ]
        self.TAB5 = [
            Decimal(v)
            for v in [
                0,
                1900,
                1824,
                1748,
                1672,
                1596,
                1520,
                1444,
                1368,
                1292,
                1216,
                1140,
                1064,
                988,
                912,
                836,
                760,
                722,
                684,
                665,
                646,
                627,
                608,
                589,
                570,
                551,
                532,
                513,
                494,
                475,
                456,
                437,
                418,
                399,
                380,
                361,
                342,
                323,
                304,
                285,
                266,
                247,
                228,
                209,
                190,
                171,
                152,
                133,
                114,
                95,
                76,
                57,
                38,
                19,
                0,
            ]
        ]
        self.ZAHL1 = Decimal(1)
        self.ZAHL2 = Decimal(2)
        self.ZAHL5 = Decimal(5)
        self.ZAHL7 = Decimal(7)
        self.ZAHL12 = Decimal(12)
        self.ZAHL100 = Decimal(100)
        self.ZAHL360 = Decimal(360)
        self.ZAHL500 = Decimal(500)
        self.ZAHL700 = Decimal(700)
        self.ZAHL1000 = Decimal(1000)
        self.ZAHL10000 = Decimal(10000)

    def calculate(self):
        logging.info("Starting tax calculation.")
        self.MPARA()
        self.MRE4JL()
        self.VBEZBSO = Decimal(0)
        self.MRE4()
        self.MRE4ABZ()
        self.MBERECH()
        self.MSONST()

        results = {
            "BK": self.BK,
            "BKS": self.BKS,
            "LSTLZZ": self.LSTLZZ,
            "SOLZLZZ": self.SOLZLZZ,
            "SOLZS": self.SOLZS,
            "STS": self.STS,
            "VKVLZZ": self.VKVLZZ,
            "VKVSONST": self.VKVSONST,
            "VFRB": self.VFRB,
            "VFRBS1": self.VFRBS1,
            "VFRBS2": self.VFRBS2,
            "WVFRB": self.WVFRB,
            "WVFRBO": self.WVFRBO,
            "WVFRBM": self.WVFRBM,
        }
        logging.info(f"Tax calculation finished. Results: {results}")
        return results

    def MPARA(self):
        logging.info("Running MPARA to set calculation parameters.")
        if self.KRV < 1:
            self.BBGRV = Decimal(96600)
            self.RVSATZAN = Decimal("0.093")
        self.BBGKVPV = Decimal(66150)
        self.KVSATZAN = (self.KVZ / self.ZAHL2 / self.ZAHL100) + Decimal("0.07")
        self.KVSATZAG = Decimal("0.0125") + Decimal("0.07")
        if self.PVS == 1:
            self.PVSATZAN = Decimal("0.023")
            self.PVSATZAG = Decimal("0.013")
        else:
            self.PVSATZAN = Decimal("0.018")
            self.PVSATZAG = Decimal("0.018")
        if self.PVZ == 1:
            self.PVSATZAN = self.PVSATZAN + Decimal("0.006")
        else:
            self.PVSATZAN = self.PVSATZAN - (self.PVA * Decimal("0.0025"))
        self.W1STKL5 = Decimal(13785)
        self.W2STKL5 = Decimal(34240)
        self.W3STKL5 = Decimal(222260)
        self.GFB = Decimal(12096)
        self.SOLZFREI = Decimal(19950)
        logging.info(
            f"MPARA results: BBGRV={self.BBGRV}, KVSATZAN={self.KVSATZAN}, PVSATZAN={self.PVSATZAN}"
        )

    def MRE4JL(self):
        logging.info("Running MRE4JL to calculate yearly income.")
        if self.LZZ == 1:
            self.ZRE4J = (self.RE4 / self.ZAHL100).quantize(
                Decimal("0.01"), rounding="ROUND_DOWN"
            )
            self.ZVBEZJ = (self.VBEZ / self.ZAHL100).quantize(
                Decimal("0.01"), rounding="ROUND_DOWN"
            )
            self.JLFREIB = (self.LZZFREIB / self.ZAHL100).quantize(
                Decimal("0.01"), rounding="ROUND_DOWN"
            )
            self.JLHINZU = (self.LZZHINZU / self.ZAHL100).quantize(
                Decimal("0.01"), rounding="ROUND_DOWN"
            )
        elif self.LZZ == 2:
            self.ZRE4J = (self.RE4 * self.ZAHL12 / self.ZAHL100).quantize(
                Decimal("0.01"), rounding="ROUND_DOWN"
            )
            self.ZVBEZJ = (self.VBEZ * self.ZAHL12 / self.ZAHL100).quantize(
                Decimal("0.01"), rounding="ROUND_DOWN"
            )
            self.JLFREIB = (self.LZZFREIB * self.ZAHL12 / self.ZAHL100).quantize(
                Decimal("0.01"), rounding="ROUND_DOWN"
            )
            self.JLHINZU = (self.LZZHINZU * self.ZAHL12 / self.ZAHL100).quantize(
                Decimal("0.01"), rounding="ROUND_DOWN"
            )
        elif self.LZZ == 3:
            self.ZRE4J = (self.RE4 * self.ZAHL360 / self.ZAHL700).quantize(
                Decimal("0.01"), rounding="ROUND_DOWN"
            )
            self.ZVBEZJ = (self.VBEZ * self.ZAHL360 / self.ZAHL700).quantize(
                Decimal("0.01"), rounding="ROUND_DOWN"
            )
            self.JLFREIB = (self.LZZFREIB * self.ZAHL360 / self.ZAHL700).quantize(
                Decimal("0.01"), rounding="ROUND_DOWN"
            )
            self.JLHINZU = (self.LZZHINZU * self.ZAHL360 / self.ZAHL700).quantize(
                Decimal("0.01"), rounding="ROUND_DOWN"
            )
        else:
            self.ZRE4J = (self.RE4 * self.ZAHL360 / self.ZAHL100).quantize(
                Decimal("0.01"), rounding="ROUND_DOWN"
            )
            self.ZVBEZJ = (self.VBEZ * self.ZAHL360 / self.ZAHL100).quantize(
                Decimal("0.01"), rounding="ROUND_DOWN"
            )
            self.JLFREIB = (self.LZZFREIB * self.ZAHL360 / self.ZAHL100).quantize(
                Decimal("0.01"), rounding="ROUND_DOWN"
            )
            self.JLHINZU = (self.LZZHINZU * self.ZAHL360 / self.ZAHL100).quantize(
                Decimal("0.01"), rounding="ROUND_DOWN"
            )
        if self.af == 0:
            self.f = 1.0
        logging.info(f"MRE4JL results: ZRE4J={self.ZRE4J}, ZVBEZJ={self.ZVBEZJ}")

    def MRE4(self):
        logging.info("Running MRE4 to calculate tax-free allowances.")
        if self.ZVBEZJ == 0:
            self.FVBZ = Decimal(0)
            self.FVB = Decimal(0)
            self.FVBZSO = Decimal(0)
            self.FVBSO = Decimal(0)
        else:
            if self.VJAHR < 2006:
                self.J = 1
            elif self.VJAHR < 2058:
                self.J = self.VJAHR - 2004
            else:
                self.J = 54
            if self.LZZ == 1:
                self.VBEZB = self.VBEZM * Decimal(self.ZMVB) + self.VBEZS
                self.HFVB = (
                    self.TAB2[self.J] / self.ZAHL12 * Decimal(self.ZMVB)
                ).quantize(Decimal("1"), rounding="ROUND_UP")
                self.FVBZ = (
                    self.TAB3[self.J] / self.ZAHL12 * Decimal(self.ZMVB)
                ).quantize(Decimal("1"), rounding="ROUND_UP")
            else:
                self.VBEZB = (self.VBEZM * self.ZAHL12 + self.VBEZS).quantize(
                    Decimal("0.01"), rounding="ROUND_DOWN"
                )
                self.HFVB = self.TAB2[self.J]
                self.FVBZ = self.TAB3[self.J]
            self.FVB = (self.VBEZB * self.TAB1[self.J] / self.ZAHL100).quantize(
                Decimal("0.01"), rounding="ROUND_UP"
            )
            if self.FVB > self.HFVB:
                self.FVB = self.HFVB
            if self.FVB > self.ZVBEZJ:
                self.FVB = self.ZVBEZJ
            self.FVBSO = (
                self.FVB + (self.VBEZBSO * self.TAB1[self.J] / self.ZAHL100)
            ).quantize(Decimal("0.01"), rounding="ROUND_UP")
            if self.FVBSO > self.TAB2[self.J]:
                self.FVBSO = self.TAB2[self.J]
            self.HFVBZSO = (
                (self.VBEZB + self.VBEZBSO) / self.ZAHL100 - self.FVBSO
            ).quantize(Decimal("0.01"), rounding="ROUND_DOWN")
            self.FVBZSO = (self.FVBZ + self.VBEZBSO / self.ZAHL100).quantize(
                Decimal("1"), rounding="ROUND_UP"
            )
            if self.FVBZSO > self.HFVBZSO:
                self.FVBZSO = self.HFVBZSO.quantize(Decimal("1"), rounding="ROUND_UP")
            if self.FVBZSO > self.TAB3[self.J]:
                self.FVBZSO = self.TAB3[self.J]
            self.HFVBZ = (self.VBEZB / self.ZAHL100 - self.FVB).quantize(
                Decimal("0.01"), rounding="ROUND_DOWN"
            )
            if self.FVBZ > self.HFVBZ:
                self.FVBZ = self.HFVBZ.quantize(Decimal("1"), rounding="ROUND_UP")
        self.MRE4ALTE()
        logging.info(
            f"MRE4 results: FVB={self.FVB}, FVBZ={self.FVBZ}, ALTE={self.ALTE}"
        )

    def MRE4ALTE(self):
        if self.ALTER1 == 0:
            self.ALTE = Decimal(0)
        else:
            if self.AJAHR < 2006:
                self.K = 1
            elif self.AJAHR < 2058:
                self.K = self.AJAHR - 2004
            else:
                self.K = 54
            self.BMG = self.ZRE4J - self.ZVBEZJ
            self.ALTE = (self.BMG * self.TAB4[self.K]).quantize(
                Decimal("1"), rounding="ROUND_UP"
            )
            self.HBALTE = self.TAB5[self.K]
            if self.ALTE > self.HBALTE:
                self.ALTE = self.HBALTE

    def MRE4ABZ(self):
        logging.info("Running MRE4ABZ to adjust taxable income.")
        self.ZRE4 = (
            self.ZRE4J - self.FVB - self.ALTE - self.JLFREIB + self.JLHINZU
        ).quantize(Decimal("0.01"), rounding="ROUND_DOWN")
        if self.ZRE4 < 0:
            self.ZRE4 = Decimal(0)
        self.ZRE4VP = self.ZRE4J
        self.ZVBEZ = (self.ZVBEZJ - self.FVB).quantize(
            Decimal("0.01"), rounding="ROUND_DOWN"
        )
        if self.ZVBEZ < 0:
            self.ZVBEZ = Decimal(0)
        logging.info(f"MRE4ABZ results: ZRE4={self.ZRE4}, ZVBEZ={self.ZVBEZ}")

    def MBERECH(self):
        logging.info("Running MBERECH to perform main tax calculation.")
        self.MZTABFB()
        self.VFRB = ((self.ANP + self.FVB + self.FVBZ) * self.ZAHL100).quantize(
            Decimal("1"), rounding="ROUND_DOWN"
        )
        self.MLSTJAHR()
        self.WVFRB = ((self.ZVE - self.GFB) * self.ZAHL100).quantize(
            Decimal("1"), rounding="ROUND_DOWN"
        )
        if self.WVFRB < 0:
            self.WVFRB = Decimal(0)
        self.LSTJAHR = (self.ST * Decimal(self.f)).quantize(
            Decimal("1"), rounding="ROUND_DOWN"
        )
        self.UPLSTLZZ()
        self.UPVKVLZZ()
        if self.ZKF > 0:
            self.ZTABFB = self.ZTABFB + self.KFB
            self.MRE4ABZ()
            self.MLSTJAHR()
            self.JBMG = (self.ST * Decimal(self.f)).quantize(
                Decimal("1"), rounding="ROUND_DOWN"
            )
        else:
            self.JBMG = self.LSTJAHR
        self.MSOLZ()
        logging.info(f"MBERECH results: LSTJAHR={self.LSTJAHR}, JBMG={self.JBMG}")

    def MZTABFB(self):
        self.ANP = Decimal(0)
        if self.ZVBEZ >= 0 and self.ZVBEZ < self.FVBZ:
            self.FVBZ = Decimal(int(self.ZVBEZ))
        if self.STKL < 6:
            if self.ZVBEZ > 0:
                if (self.ZVBEZ - self.FVBZ) < 102:
                    self.ANP = (self.ZVBEZ - self.FVBZ).quantize(
                        Decimal("1"), rounding="ROUND_UP"
                    )
                else:
                    self.ANP = Decimal(102)
        else:
            self.FVBZ = Decimal(0)
            self.FVBZSO = Decimal(0)
        if self.STKL < 6:
            if self.ZRE4 > self.ZVBEZ:
                if (self.ZRE4 - self.ZVBEZ) < 1230:
                    self.ANP = (self.ANP + self.ZRE4 - self.ZVBEZ).quantize(
                        Decimal("1"), rounding="ROUND_UP"
                    )
                else:
                    self.ANP = self.ANP + 1230
        self.KZTAB = 1
        if self.STKL == 1:
            self.SAP = Decimal(36)
            self.KFB = (self.ZKF * Decimal(9600)).quantize(
                Decimal("1"), rounding="ROUND_DOWN"
            )
        elif self.STKL == 2:
            self.EFA = Decimal(4260)
            self.SAP = Decimal(36)
            self.KFB = (self.ZKF * Decimal(9600)).quantize(
                Decimal("1"), rounding="ROUND_DOWN"
            )
        elif self.STKL == 3:
            self.KZTAB = 2
            self.SAP = Decimal(36)
            self.KFB = (self.ZKF * Decimal(9600)).quantize(
                Decimal("1"), rounding="ROUND_DOWN"
            )
        elif self.STKL == 4:
            self.SAP = Decimal(36)
            self.KFB = (self.ZKF * Decimal(4800)).quantize(
                Decimal("1"), rounding="ROUND_DOWN"
            )
        elif self.STKL == 5:
            self.SAP = Decimal(36)
            self.KFB = Decimal(0)
        else:
            self.KFB = Decimal(0)
        self.ZTABFB = (self.EFA + self.ANP + self.SAP + self.FVBZ).quantize(
            Decimal("0.01"), rounding="ROUND_DOWN"
        )

    def MLSTJAHR(self):
        logging.info("Running MLSTJAHR to calculate annual tax.")
        self.UPEVP()
        self.ZVE = self.ZRE4 - self.ZTABFB - self.VSP
        self.UPMLST()
        logging.info(f"MLSTJAHR results: ZVE={self.ZVE}, VSP={self.VSP}, ST={self.ST}")

    def UPVKVLZZ(self):
        self.UPVKV()
        self.JW = self.VKV
        self.UPANTEIL()
        self.VKVLZZ = self.ANTEIL1

    def UPVKV(self):
        if self.PKV > 0:
            if self.VSP2 > self.VSP3:
                self.VKV = self.VSP2 * self.ZAHL100
            else:
                self.VKV = self.VSP3 * self.ZAHL100
        else:
            self.VKV = Decimal(0)

    def UPLSTLZZ(self):
        self.JW = self.LSTJAHR * self.ZAHL100
        self.UPANTEIL()
        self.LSTLZZ = self.ANTEIL1

    def UPMLST(self):
        if self.ZVE < 1:
            self.ZVE = Decimal(0)
            self.X = Decimal(0)
        else:
            self.X = (self.ZVE / Decimal(self.KZTAB)).quantize(
                Decimal("1"), rounding="ROUND_DOWN"
            )
        if self.STKL < 5:
            self.UPTAB25()
        else:
            self.MST5_6()

    def UPEVP(self):
        if self.KRV == 1:
            self.VSP1 = Decimal(0)
        else:
            if self.ZRE4VP > self.BBGRV:
                self.ZRE4VP = self.BBGRV
            self.VSP1 = (self.ZRE4VP * self.RVSATZAN).quantize(
                Decimal("0.01"), rounding="ROUND_DOWN"
            )
        self.VSP2 = (self.ZRE4VP * Decimal("0.12")).quantize(
            Decimal("0.01"), rounding="ROUND_DOWN"
        )
        if self.STKL == 3:
            self.VHB = Decimal(3000)
        else:
            self.VHB = Decimal(1900)
        if self.VSP2 > self.VHB:
            self.VSP2 = self.VHB
        self.VSPN = (self.VSP1 + self.VSP2).quantize(Decimal("1"), rounding="ROUND_UP")
        self.MVSP()
        if self.VSPN > self.VSP:
            self.VSP = self.VSPN.quantize(Decimal("0.01"), rounding="ROUND_DOWN")

    def MVSP(self):
        if self.ZRE4VP > self.BBGKVPV:
            self.ZRE4VP = self.BBGKVPV
        if self.PKV > 0:
            if self.STKL == 6:
                self.VSP3 = Decimal(0)
            else:
                self.VSP3 = self.PKPV * self.ZAHL12 / self.ZAHL100
                if self.PKV == 2:
                    self.VSP3 = (
                        self.VSP3 - (self.ZRE4VP * (self.KVSATZAG + self.PVSATZAG))
                    ).quantize(Decimal("0.01"), rounding="ROUND_DOWN")
        else:
            self.VSP3 = (self.ZRE4VP * (self.KVSATZAN + self.PVSATZAN)).quantize(
                Decimal("0.01"), rounding="ROUND_DOWN"
            )
        self.VSP = (self.VSP3 + self.VSP1).quantize(Decimal("1"), rounding="ROUND_UP")

    def MST5_6(self):
        self.ZZX = self.X
        if self.ZZX > self.W2STKL5:
            self.ZX = self.W2STKL5
            self.UP5_6()
            if self.ZZX > self.W3STKL5:
                self.ST = (
                    self.ST + (self.W3STKL5 - self.W2STKL5) * Decimal("0.42")
                ).quantize(Decimal("1"), rounding="ROUND_DOWN")
                self.ST = (
                    self.ST + (self.ZZX - self.W3STKL5) * Decimal("0.45")
                ).quantize(Decimal("1"), rounding="ROUND_DOWN")
            else:
                self.ST = (
                    self.ST + (self.ZZX - self.W2STKL5) * Decimal("0.42")
                ).quantize(Decimal("1"), rounding="ROUND_DOWN")
        else:
            self.ZX = self.ZZX
            self.UP5_6()
            if self.ZZX > self.W1STKL5:
                self.VERGL = self.ST
                self.ZX = self.W1STKL5
                self.UP5_6()
                self.HOCH = (
                    self.ST + (self.ZZX - self.W1STKL5) * Decimal("0.42")
                ).quantize(Decimal("1"), rounding="ROUND_DOWN")
                if self.HOCH < self.VERGL:
                    self.ST = self.HOCH
                else:
                    self.ST = self.VERGL

    def UP5_6(self):
        self.X = (self.ZX * Decimal("1.25")).quantize(
            Decimal("0.01"), rounding="ROUND_DOWN"
        )
        self.UPTAB25()
        self.ST1 = self.ST
        self.X = (self.ZX * Decimal("0.75")).quantize(
            Decimal("0.01"), rounding="ROUND_DOWN"
        )
        self.UPTAB25()
        self.ST2 = self.ST
        self.DIFF = (self.ST1 - self.ST2) * self.ZAHL2
        self.MIST = (self.ZX * Decimal("0.14")).quantize(
            Decimal("1"), rounding="ROUND_DOWN"
        )
        if self.MIST > self.DIFF:
            self.ST = self.MIST
        else:
            self.ST = self.DIFF

    def MSOLZ(self):
        logging.info("Running MSOLZ to calculate solidarity surcharge.")
        self.SOLZFREI = self.SOLZFREI * Decimal(self.KZTAB)
        if self.JBMG > self.SOLZFREI:
            self.SOLZJ = (self.JBMG * Decimal("5.5") / self.ZAHL100).quantize(
                Decimal("0.01"), rounding="ROUND_DOWN"
            )
            self.SOLZMIN = (
                (self.JBMG - self.SOLZFREI) * Decimal("11.9") / self.ZAHL100
            ).quantize(Decimal("0.01"), rounding="ROUND_DOWN")
            if self.SOLZMIN < self.SOLZJ:
                self.SOLZJ = self.SOLZMIN
            self.JW = self.SOLZJ * self.ZAHL100
            self.JW = self.JW.quantize(Decimal("1"), rounding="ROUND_DOWN")
            self.UPANTEIL()
            self.SOLZLZZ = self.ANTEIL1
        else:
            self.SOLZLZZ = Decimal(0)
        if self.R > 0:
            # Kirchensteuer: 9% für evangelisch/katholisch (R=1), 8% für andere (R=2)
            if self.R == 1:
                kirchensteuer_satz = Decimal("0.09")  # 9%
            else:
                kirchensteuer_satz = Decimal("0.08")  # 8%

            self.JW = (self.JBMG * kirchensteuer_satz * self.ZAHL100).quantize(
                Decimal("1"), rounding="ROUND_DOWN"
            )
            self.UPANTEIL()
            self.BK = self.ANTEIL1
        else:
            self.BK = Decimal(0)
        logging.info(f"MSOLZ results: SOLZLZZ={self.SOLZLZZ}, BK={self.BK}")

    def UPANTEIL(self):
        if self.LZZ == 1:
            self.ANTEIL1 = self.JW
        elif self.LZZ == 2:
            self.ANTEIL1 = (self.JW / self.ZAHL12).quantize(
                Decimal("1"), rounding="ROUND_DOWN"
            )
        elif self.LZZ == 3:
            self.ANTEIL1 = (self.JW * self.ZAHL7 / self.ZAHL360).quantize(
                Decimal("1"), rounding="ROUND_DOWN"
            )
        else:
            self.ANTEIL1 = (self.JW / self.ZAHL360).quantize(
                Decimal("1"), rounding="ROUND_DOWN"
            )

    def MSONST(self):
        self.LZZ = 1
        if self.ZMVB == 0:
            self.ZMVB = 12
        if self.SONSTB == 0 and self.MBV == 0:
            self.VKVSONST = Decimal(0)
            self.LSTSO = Decimal(0)
            self.STS = Decimal(0)
            self.SOLZS = Decimal(0)
            self.BKS = Decimal(0)
        else:
            self.MOSONST()
            self.UPVKV()
            self.VKVSONST = self.VKV
            self.ZRE4J = ((self.JRE4 + self.SONSTB) / self.ZAHL100).quantize(
                Decimal("0.01"), rounding="ROUND_DOWN"
            )
            self.ZVBEZJ = ((self.JVBEZ + self.VBS) / self.ZAHL100).quantize(
                Decimal("0.01"), rounding="ROUND_DOWN"
            )
            self.VBEZBSO = self.STERBE
            self.MRE4SONST()
            self.MLSTJAHR()
            self.WVFRBM = ((self.ZVE - self.GFB) * self.ZAHL100).quantize(
                Decimal("0.01"), rounding="ROUND_DOWN"
            )
            if self.WVFRBM < 0:
                self.WVFRBM = Decimal(0)
            self.UPVKV()
            self.VKVSONST = self.VKV - self.VKVSONST
            self.LSTSO = self.ST * self.ZAHL100
            self.STS = (
                (self.LSTSO - self.LSTOSO) * Decimal(self.f) / self.ZAHL100
            ).quantize(Decimal("1"), rounding="ROUND_DOWN") * self.ZAHL100
            self.STSMIN()

    def STSMIN(self):
        if self.STS < 0:
            if self.MBV > 0:
                self.LSTLZZ += self.STS
                if self.LSTLZZ < 0:
                    self.LSTLZZ = Decimal(0)
                self.SOLZLZZ += (self.STS * Decimal("5.5") / self.ZAHL100).quantize(
                    Decimal("1"), rounding="ROUND_DOWN"
                )
                if self.SOLZLZZ < 0:
                    self.SOLZLZZ = Decimal(0)
                self.BK += self.STS
                if self.BK < 0:
                    self.BK = Decimal(0)
            self.STS = Decimal(0)
            self.SOLZS = Decimal(0)
        else:
            self.MSOLZSTS()
        if self.R > 0:
            # Kirchensteuer für sonstige Bezüge: 9% für evangelisch/katholisch (R=1), 8% für andere (R=2)
            if self.R == 1:
                kirchensteuer_satz = Decimal("0.09")  # 9%
            else:
                kirchensteuer_satz = Decimal("0.08")  # 8%

            self.BKS = (self.STS * kirchensteuer_satz).quantize(
                Decimal("1"), rounding="ROUND_DOWN"
            )
        else:
            self.BKS = Decimal(0)

    def MSOLZSTS(self):
        if self.ZKF > 0:
            self.SOLZSZVE = self.ZVE - self.KFB
        else:
            self.SOLZSZVE = self.ZVE
        if self.SOLZSZVE < 1:
            self.SOLZSZVE = Decimal(0)
            self.X = Decimal(0)
        else:
            self.X = (self.SOLZSZVE / Decimal(self.KZTAB)).quantize(
                Decimal("1"), rounding="ROUND_DOWN"
            )
        if self.STKL < 5:
            self.UPTAB25()
        else:
            self.MST5_6()
        self.SOLZSBMG = (self.ST * Decimal(self.f)).quantize(
            Decimal("1"), rounding="ROUND_DOWN"
        )
        if self.SOLZSBMG > self.SOLZFREI:
            self.SOLZS = (self.STS * Decimal("5.5") / self.ZAHL100).quantize(
                Decimal("1"), rounding="ROUND_DOWN"
            )
        else:
            self.SOLZS = Decimal(0)

    def MOSONST(self):
        self.ZRE4J = (self.JRE4 / self.ZAHL100).quantize(
            Decimal("0.01"), rounding="ROUND_DOWN"
        )
        self.ZVBEZJ = (self.JVBEZ / self.ZAHL100).quantize(
            Decimal("0.01"), rounding="ROUND_DOWN"
        )
        self.JLFREIB = (self.JFREIB / self.ZAHL100).quantize(
            Decimal("0.01"), rounding="ROUND_DOWN"
        )
        self.JLHINZU = (self.JHINZU / self.ZAHL100).quantize(
            Decimal("0.01"), rounding="ROUND_DOWN"
        )
        self.MRE4()
        self.MRE4ABZ()
        self.ZRE4VP = self.ZRE4VP - (self.JRE4ENT / self.ZAHL100)
        self.MZTABFB()
        self.VFRBS1 = ((self.ANP + self.FVB + self.FVBZ) * self.ZAHL100).quantize(
            Decimal("0.01"), rounding="ROUND_DOWN"
        )
        self.MLSTJAHR()
        self.WVFRBO = ((self.ZVE - self.GFB) * self.ZAHL100).quantize(
            Decimal("0.01"), rounding="ROUND_DOWN"
        )
        if self.WVFRBO < 0:
            self.WVFRBO = Decimal(0)
        self.LSTOSO = self.ST * self.ZAHL100

    def MRE4SONST(self):
        self.MRE4()
        self.FVB = self.FVBSO
        self.MRE4ABZ()
        self.ZRE4VP = (
            self.ZRE4VP
            + (self.MBV / self.ZAHL100)
            - (self.JRE4ENT / self.ZAHL100)
            - (self.SONSTENT / self.ZAHL100)
        )
        self.FVBZ = self.FVBZSO
        self.MZTABFB()
        self.VFRBS2 = ((self.ANP + self.FVB + self.FVBZ) * self.ZAHL100) - self.VFRBS1

    def UPTAB25(self):
        if self.X < self.GFB + 1:
            self.ST = Decimal(0)
        elif self.X < 17444:
            self.Y = (self.X - self.GFB).scaleb(-4)
            self.RW = self.Y * Decimal("932.30")
            self.RW = self.RW + Decimal(1400)
            self.ST = (self.RW * self.Y).quantize(Decimal("1"), rounding="ROUND_DOWN")
        elif self.X < 68481:
            self.Y = (self.X - Decimal(17443)).scaleb(-4)
            self.RW = self.Y * Decimal("176.64")
            self.RW = self.RW + Decimal(2397)
            self.RW = self.RW * self.Y
            self.ST = (self.RW + Decimal("1015.13")).quantize(
                Decimal("1"), rounding="ROUND_DOWN"
            )
        elif self.X < 277826:
            self.ST = (self.X * Decimal("0.42") - Decimal("10911.92")).quantize(
                Decimal("1"), rounding="ROUND_DOWN"
            )
        else:
            self.ST = (self.X * Decimal("0.45") - Decimal("19246.67")).quantize(
                Decimal("1"), rounding="ROUND_DOWN"
            )
        self.ST = self.ST * Decimal(self.KZTAB)
