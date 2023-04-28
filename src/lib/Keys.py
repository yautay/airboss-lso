from enum import Enum


class KeysAirframes(Enum):
    F18 = "FA-18C_hornet"
    F14A = "F-14A-135-GR"
    AV8 = "AV-8B"


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


class KeysTrapsheet(Enum):
    X = "X"
    Z = "Z"
    ALT = "Alt"
    AOA = "AoA"
    GSE = "GSE"
    LUE = "LUE"
    VY = "Vy"
    ROLL = "Roll"


class KeysTrapfile(Enum):
    TGROOVE = "Tgroove"
    AIRFRAME = "airframe"
    CARRIERNAME = "carriername"
    CARRIERRWY = "carrierrwy"
    CARRIERTYPE = "carriertype"
    CASE = "case"
    COMMAND = "command"
    DETAILS = "details"
    GRADE = "grade"
    LANDINGDIST = "landingdist"
    MIDATE = "midate"
    MITIME = "mitime"
    NAME = "name"
    POINTS = "points"
    SERVER_NAME = "server_name"
    THEATRE = "theatre"
    TRAPSHEET = "trapsheet"
    WIND = "wind"
    WIRE = "wire"
