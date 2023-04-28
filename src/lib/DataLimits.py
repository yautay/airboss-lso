from src.lib.Keys import \
    KeysAoA as AoA, \
    KeysGRV as GRV, \
    KeysGS as GS
from src.lib.Utils import Utils


class DataLimits:
    """Class contains common limitations"""

    @staticmethod
    def airframe_context(airframe_text: str) -> int:
        """Gets airframe context based on airframe type

        Parameters
        ----------
        airframe_text : str
            Airframe name

        Returns
        -------
        int
            integer airframe index
            1: FA-18C
            2: F-14
            9: AV-8
        """

        if "FA-18C" in airframe_text:
            return 1
        elif "F-14" in airframe_text:
            return 2
        elif "AV-8" in airframe_text:
            return 9

    @staticmethod
    def data_limits_aoa(airframe_index: int) -> dict:
        """Gets airframe context based AoA limits

        Parameters
        ----------
        airframe_index : int
            Airframe index

        Returns
        -------
        dict
            airframe based AoA limits
        """
        if airframe_index == 1:  # F18
            return {
                AoA.SLO_HI: 9.8,
                AoA.SLO_MED: 9.3,
                AoA.SLO_LO: 8.8,
                AoA.OK: 8.1,
                AoA.FAST_LO: 7.4,
                AoA.FAST_MED: 6.9,
                AoA.FAST_HI: 6.3,
            }
        elif airframe_index == 2:  # F-14
            return {
                AoA.SLO_HI: Utils.units_to_deg(17),
                AoA.SLO_MED: Utils.units_to_deg(16),
                AoA.SLO_LO: Utils.units_to_deg(15.5),
                AoA.OK: Utils.units_to_deg(15),
                AoA.FAST_LO: Utils.units_to_deg(14.5),
                AoA.FAST_MED: Utils.units_to_deg(14),
                AoA.FAST_HI: Utils.units_to_deg(13),
            }
        elif airframe_index == 9:  # AV-8
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
        airframe_index : int
            Airframe index

        Returns
        -------
        dict
            airframe based GS limits
        """

        if airframe_index == 9:  # AV-8
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
        airframe_index : int
            Airframe index

        Returns
        -------
        dict
            airframe based GSE limits
        """
        if airframe_index == 9:  # AV-8
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
