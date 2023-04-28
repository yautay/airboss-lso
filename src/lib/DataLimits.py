from enum import Enum

from src.lib.Keys import \
    KeysAoA as AoA, \
    KeysGRV as GRV, \
    KeysGS as GS, \
    KeysAirframes as KAIRFRAME, \
    KeysCarriers as KCARRIER, \
    KeysCarrierfile as KCARRIERFILE
from src.lib.Utils import Utils


class DataLimits:
    """Class contains common limitations"""

    @staticmethod
    def airframe_context(airframe_text: str) -> Enum:
        """Gets airframe context based on airframe type

        Parameters
        ----------
        airframe_text : str
            Airframe name

        Returns
        -------
        Enum
            Airframe type
        """
        if KAIRFRAME.HORNET.value[0] in airframe_text:
            return KAIRFRAME.HORNET
        elif KAIRFRAME.F14A.value[0] in airframe_text:
            return KAIRFRAME.F14A
        elif KAIRFRAME.F14B.value[0] in airframe_text:
            return KAIRFRAME.F14B
        elif KAIRFRAME.A4EC.value[0] in airframe_text:
            return KAIRFRAME.A4EC
        elif KAIRFRAME.T45C.value[0] in airframe_text:
            return KAIRFRAME.T45C
        elif KAIRFRAME.AV8B.value[0] in airframe_text:
            return KAIRFRAME.AV8B

    @staticmethod
    def data_limits_aoa(airframe_index: Enum) -> dict:
        """Gets airframe context based AoA limits

        Parameters
        ----------
        airframe_index : Enum
            Airframe type

        Returns
        -------
        dict
            airframe based AoA limits
        """
        if airframe_index == KAIRFRAME.HORNET:
            return {
                AoA.SLO_HI: 9.8,
                AoA.SLO_MED: 9.3,
                AoA.SLO_LO: 8.8,
                AoA.OK: 8.1,
                AoA.FAST_LO: 7.4,
                AoA.FAST_MED: 6.9,
                AoA.FAST_HI: 6.3,
            }
        elif airframe_index == KAIRFRAME.F14A:
            return {
                AoA.SLO_HI: Utils.units_to_deg(17),
                AoA.SLO_MED: Utils.units_to_deg(16),
                AoA.SLO_LO: Utils.units_to_deg(15.5),
                AoA.OK: Utils.units_to_deg(15),
                AoA.FAST_LO: Utils.units_to_deg(14.5),
                AoA.FAST_MED: Utils.units_to_deg(14),
                AoA.FAST_HI: Utils.units_to_deg(13),
            }
        elif airframe_index == KAIRFRAME.F14B:
            return {
                AoA.SLO_HI: Utils.units_to_deg(17),
                AoA.SLO_MED: Utils.units_to_deg(16),
                AoA.SLO_LO: Utils.units_to_deg(15.5),
                AoA.OK: Utils.units_to_deg(15),
                AoA.FAST_LO: Utils.units_to_deg(14.5),
                AoA.FAST_MED: Utils.units_to_deg(14),
                AoA.FAST_HI: Utils.units_to_deg(13),
            }
        elif airframe_index == KAIRFRAME.AV8B:
            return {
                AoA.SLO_HI: 16,
                AoA.SLO_MED: 13.5,
                AoA.SLO_LO: 12.5,
                AoA.OK: 10,
                AoA.FAST_LO: 9.5,
                AoA.FAST_MED: 8,
                AoA.FAST_HI: 7.5,
            }

    @staticmethod
    def data_limits_gs(airframe_index: int) -> dict:
        """Gets airframe context based GS limits

        Parameters
        ----------
        airframe_index : Enum
            Airframe type

        Returns
        -------
        dict
            airframe based GS limits
        """

        if airframe_index == KAIRFRAME.AV8B:
            return {
                GS.___HI___: 5.4,
                GS.__HI__: 4.9,
                GS.HI: 4.2,
                GS.GS: 3.5,
                GS.LO: 3,
                GS.__LO__: 2.3,
                GS.___LO___: 2.0,
            }
        else:
            return {
                GS.___HI___: 5.0,
                GS.__HI__: 4.3,
                GS.HI: 3.9,
                GS.GS: 3.5,
                GS.LO: 3.2,
                GS.__LO__: 2.9,
                GS.___LO___: 2.6,
            }

    @staticmethod
    def data_limits_gse(airframe_index: int) -> dict:
        """Gets airframe context based GSE limits

        Parameters
        ----------
        airframe_index : Enum
            Airframe type

        Returns
        -------
        dict
            airframe based GSE limits
        """
        if airframe_index == KAIRFRAME.AV8B:
            return {
                GS.___HI___: 1.9,
                GS.__HI__: 1.4,
                GS.HI: 0.7,
                GS.GS: 0,
                GS.LO: -0.5,
                GS.__LO__: -1.2,
                GS.___LO___: -1.5,
            }
        else:
            return {
                GS.___HI___: 1.5,
                GS.__HI__: 0.8,
                GS.HI: 0.4,
                GS.GS: 0,
                GS.LO: -0.3,
                GS.__LO__: -0.6,
                GS.___LO___: -0.9,
            }

    @staticmethod
    def data_limits_lu() -> dict:
        """Gets LU limits

        Returns
        -------
        dict
            LU limits
        """

        return {
            GRV.___LUL___: -3,
            GRV.__LUL__: -1,
            GRV.LUL: -.5,
            GRV.OK: 0,
            GRV.LUR: .5,
            GRV.__LUR__: 1,
            GRV.___LUR___: 3,
        }


class CarriersData:
    @staticmethod
    def carrier_context(carrier_text: str) -> Enum:
        if KCARRIER.ROOSEVELT.value[0] in carrier_text:
            return KCARRIER.ROOSEVELT
        elif KCARRIER.LINCOLN.value[0] in carrier_text:
            return KCARRIER.LINCOLN
        elif KCARRIER.WASHINGTON.value[0] in carrier_text:
            return KCARRIER.WASHINGTON
        elif KCARRIER.TRUMAN.value[0] in carrier_text:
            return KCARRIER.TRUMAN
        elif KCARRIER.STENNIS.value[0] in carrier_text:
            return KCARRIER.STENNIS
        elif KCARRIER.FORRESTAL.value[0] in carrier_text:
            return KCARRIER.FORRESTAL
        elif KCARRIER.VINSON.value[0] in carrier_text:
            return KCARRIER.VINSON
        elif KCARRIER.HERMES.value[0] in carrier_text:
            return KCARRIER.HERMES
        elif KCARRIER.INVINCIBLE.value[0] in carrier_text:
            return KCARRIER.INVINCIBLE
        elif KCARRIER.TARAWA.value[0] in carrier_text:
            return KCARRIER.TARAWA
        elif KCARRIER.AMERICA.value[0] in carrier_text:
            return KCARRIER.AMERICA
        elif KCARRIER.JCARLOS.value[0] in carrier_text:
            return KCARRIER.JCARLOS
        elif KCARRIER.CANBERRA.value[0] in carrier_text:
            return KCARRIER.CANBERRA
        elif KCARRIER.KUZNETSOV.value[0] in carrier_text:
            return KCARRIER.KUZNETSOV

    @staticmethod
    def carriers_data(c_type: Enum) -> dict:
        if c_type in [KCARRIER.VINSON, KCARRIER.KUZNETSOV]:
            return {
                KCARRIERFILE.STERNDIST: -153,
                KCARRIERFILE.DECKHEIGHT: 18.30,
                KCARRIERFILE.TOTLENGTH: 310,
                KCARRIERFILE.TOTWIDTHPORT: 40,
                KCARRIERFILE.TOTWIDTHSTARBOARD: 30,
                KCARRIERFILE.RWYANGLE: -9.1359,
                KCARRIERFILE.RWYLENGTH: 225,
                KCARRIERFILE.RWYWIDTH: 20,
                KCARRIERFILE.WIRE_1: 46,
                KCARRIERFILE.WIRE_2: 58,
                KCARRIERFILE.WIRE_3: 70,
                KCARRIERFILE.WIRE_4: 81,
            }
        elif c_type in [KCARRIER.STENNIS, KCARRIER.ROOSEVELT, KCARRIER.LINCOLN, KCARRIER.WASHINGTON, KCARRIER.TRUMAN]:
            return {
                KCARRIERFILE.STERNDIST: -164,
                KCARRIERFILE.DECKHEIGHT: 20.1494,
                KCARRIERFILE.TOTLENGTH: 332.8,
                KCARRIERFILE.TOTWIDTHPORT: 45,
                KCARRIERFILE.TOTWIDTHSTARBOARD: 35,
                KCARRIERFILE.RWYANGLE: -9.1359,
                KCARRIERFILE.RWYLENGTH: 250,
                KCARRIERFILE.RWYWIDTH: 25,
                KCARRIERFILE.WIRE_1: 55,
                KCARRIERFILE.WIRE_2: 67,
                KCARRIERFILE.WIRE_3: 79,
                KCARRIERFILE.WIRE_4: 92,
            }
        elif c_type in [KCARRIER.FORRESTAL]:
            return {
                KCARRIERFILE.STERNDIST: -135.5,
                KCARRIERFILE.DECKHEIGHT: 20,
                KCARRIERFILE.TOTLENGTH: 315,
                KCARRIERFILE.TOTWIDTHPORT: 45,
                KCARRIERFILE.TOTWIDTHSTARBOARD: 35,
                KCARRIERFILE.RWYANGLE: -9.1359,
                KCARRIERFILE.RWYLENGTH: 212,
                KCARRIERFILE.RWYWIDTH: 25,
                KCARRIERFILE.WIRE_1: 44,
                KCARRIERFILE.WIRE_2: 54,
                KCARRIERFILE.WIRE_3: 64,
                KCARRIERFILE.WIRE_4: 74,
            }
        elif c_type in [KCARRIER.HERMES]:
            return {
                KCARRIERFILE.STERNDIST: -105,
                KCARRIERFILE.DECKHEIGHT: 12,
                KCARRIERFILE.TOTLENGTH: 228.19,
                KCARRIERFILE.TOTWIDTHPORT: 20.5,
                KCARRIERFILE.TOTWIDTHSTARBOARD: 24.5,
                KCARRIERFILE.RWYANGLE: 0,
                KCARRIERFILE.RWYLENGTH: 215,
                KCARRIERFILE.RWYWIDTH: 13,
                KCARRIERFILE.WIRE_1: None,
                KCARRIERFILE.WIRE_2: None,
                KCARRIERFILE.WIRE_3: 69,
                KCARRIERFILE.WIRE_4: None,
            }
        elif c_type in [KCARRIER.INVINCIBLE]:
            return {
                KCARRIERFILE.STERNDIST: -105,
                KCARRIERFILE.DECKHEIGHT: 12,
                KCARRIERFILE.TOTLENGTH: 228.19,
                KCARRIERFILE.TOTWIDTHPORT: 20.5,
                KCARRIERFILE.TOTWIDTHSTARBOARD: 24.5,
                KCARRIERFILE.RWYANGLE: 0,
                KCARRIERFILE.RWYLENGTH: 215,
                KCARRIERFILE.RWYWIDTH: 13,
                KCARRIERFILE.WIRE_1: None,
                KCARRIERFILE.WIRE_2: None,
                KCARRIERFILE.WIRE_3: 69,
                KCARRIERFILE.WIRE_4: None,
            }
        elif c_type in [KCARRIER.TARAWA]:
            return {
                KCARRIERFILE.STERNDIST: -125,
                KCARRIERFILE.DECKHEIGHT: 21,
                KCARRIERFILE.TOTLENGTH: 245,
                KCARRIERFILE.TOTWIDTHPORT: 10,
                KCARRIERFILE.TOTWIDTHSTARBOARD: 25,
                KCARRIERFILE.RWYANGLE: 0,
                KCARRIERFILE.RWYLENGTH: 225,
                KCARRIERFILE.RWYWIDTH: 15,
                KCARRIERFILE.WIRE_1: None,
                KCARRIERFILE.WIRE_2: None,
                KCARRIERFILE.WIRE_3: 57,
                KCARRIERFILE.WIRE_4: None,
            }
        elif c_type in [KCARRIER.AMERICA]:
            return {
                KCARRIERFILE.STERNDIST: -125,
                KCARRIERFILE.DECKHEIGHT: 20,
                KCARRIERFILE.TOTLENGTH: 257,
                KCARRIERFILE.TOTWIDTHPORT: 11,
                KCARRIERFILE.TOTWIDTHSTARBOARD: 25,
                KCARRIERFILE.RWYANGLE: 0,
                KCARRIERFILE.RWYLENGTH: 240,
                KCARRIERFILE.RWYWIDTH: 15,
                KCARRIERFILE.WIRE_1: None,
                KCARRIERFILE.WIRE_2: None,
                KCARRIERFILE.WIRE_3: 59,
                KCARRIERFILE.WIRE_4: None,
            }
        elif c_type in [KCARRIER.JCARLOS, KCARRIER.CANBERRA]:
            return {
                KCARRIERFILE.STERNDIST: -125,
                KCARRIERFILE.DECKHEIGHT: 20,
                KCARRIERFILE.TOTLENGTH: 231,
                KCARRIERFILE.TOTWIDTHPORT: 10,
                KCARRIERFILE.TOTWIDTHSTARBOARD: 22,
                KCARRIERFILE.RWYANGLE: 0,
                KCARRIERFILE.RWYLENGTH: 202,
                KCARRIERFILE.RWYWIDTH: 14,
                KCARRIERFILE.WIRE_1: None,
                KCARRIERFILE.WIRE_2: None,
                KCARRIERFILE.WIRE_3: 89,
                KCARRIERFILE.WIRE_4: None,
            }
