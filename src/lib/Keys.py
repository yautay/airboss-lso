from enum import Enum


class KeysAirframes(Enum):
    AV8B = "AV8BNA",
    HORNET = "FA-18C_hornet",
    A4EC = "A-4E-C",
    F14A = "F-14A-135-GR",
    F14B = "F-14B",
    T45C = "T-45",


class KeysCarriers(Enum):
    ROOSEVELT = "CVN_71",
    LINCOLN = "CVN_72",
    WASHINGTON = "CVN_73",
    TRUMAN = "CVN_75",
    STENNIS = "Stennis",
    FORRESTAL = "Forrestal",
    VINSON = "VINSON",
    HERMES = "HERMES81",
    INVINCIBLE = "hms_invincible",
    TARAWA = "LHA_Tarawa",
    AMERICA = "USS America LHA-6",
    JCARLOS = "L61",
    CANBERRA = "L02",
    KUZNETSOV = "KUZNECOW"


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


class KeysCarrierfile(Enum):
    STERNDIST = "sterndist"
    DECKHEIGHT = "deckheight"
    TOTLENGTH = "totlength"
    TOTWIDTHPORT = "totwidthport"
    TOTWIDTHSTARBOARD = "totwidthstarboard"
    RWYANGLE = "rwyangle"
    RWYLENGTH = "rwylength"
    RWYWIDTH = "rwywidth"
    WIRE_1 = "wire1"
    WIRE_2 = "wire2"
    WIRE_3 = "wire3"
    WIRE_4 = "wire4"
