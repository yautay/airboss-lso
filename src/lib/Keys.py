from enum import Enum


class KeysAirframes:
    @staticmethod
    def type():
        return "type"

    @staticmethod
    def f18():
        return "F/A-18C"

    @staticmethod
    def f14():
        return "F-14"

    @staticmethod
    def av8():
        return "AV-8B"


class KeysAoA(Enum):
    SLO_HI = "aoa___slo___limit"
    SLO_MED = "aoa__slo__limit"
    SLO_LO = "aoa_slo_limit"
    OK = "aoa_ok"
    FAST_LO = "aoa_fst_limit"
    FAST_MED = "aoa__fst__limit"
    FAST_HI = "aoa___fst___limit"


class KeysGS(Enum):
    ___HI___ = "gs___hi___limit"
    __HI__ = "gs__hi__limit"
    HI = "gs_hi_limit"
    GS = "gs_ok"
    LO = "gs_lo_limit"
    __LO__ = "gs__lo__limit"
    ___LO___ = "gs___lo___limit"


class KeysGRV(Enum):
    ___LUL___ = "grv___lul___limit"
    __LUL__ = "grv__lul__limit"
    LUL = "grv_lul_limit"
    OK = "grv_ok"
    LUR = "grv_lur_limit"
    __LUR__ = "grv__lur__limit"
    ___LUR___ = "grv___lur___limit"


class KeysCSV:
    @staticmethod
    def time():
        return "Time"

    @staticmethod
    def rho():
        return "Rho"

    @staticmethod
    def x():
        return "X"

    @staticmethod
    def z():
        return "Z"

    @staticmethod
    def alt():
        return "Alt"

    @staticmethod
    def aoa():
        return "AoA"

    @staticmethod
    def gse():
        return "GSE"

    @staticmethod
    def lue():
        return "LUE"

    @staticmethod
    def vtot():
        return "Vtot"

    @staticmethod
    def vy():
        return "Vy"

    @staticmethod
    def gamma():
        return "Gamma"

    @staticmethod
    def pitch():
        return "Pitch"

    @staticmethod
    def roll():
        return "Roll"

    @staticmethod
    def yaw():
        return "Yaw"

    @staticmethod
    def step():
        return "Step"

    @staticmethod
    def grade():
        return "Grade"

    @staticmethod
    def points():
        return "Points"

    @staticmethod
    def details():
        return "Details"
