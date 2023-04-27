from src.lib.Keys import \
    KeysAoA as AoA, \
    KeysGRV as GRV, \
    KeysGS as GS, \
    KeysCSV as CSV, \
    KeysAirframes as Frame
from Utils import Utils


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
    def data_limits_aoa(airframe: int) -> dict:
        """Gets airframe context based AoA limits

        Parameters
        ----------
        airframe : int
            Airframe index

        Returns
        -------
        dict
            airframe based AoA limits
        """
        if airframe == 1:  # F18
            return {
                AoA.slo_hi(): 9.8,
                AoA.slo_med(): 9.3,
                AoA.slo_lo(): 8.8,
                AoA.ok(): 8.1,
                AoA.fast_lo(): 7.4,
                AoA.fast_med(): 6.9,
                AoA.fast_hi(): 6.3,
            }
        elif airframe == 2:  # F-14
            return {
                AoA.slo_hi(): Utils.units_to_deg(17),
                AoA.slo_med(): Utils.units_to_deg(16),
                AoA.slo_lo(): Utils.units_to_deg(15.5),
                AoA.ok(): Utils.units_to_deg(15),
                AoA.fast_lo(): Utils.units_to_deg(14.5),
                AoA.fast_med(): Utils.units_to_deg(14),
                AoA.fast_hi(): Utils.units_to_deg(13),
            }
        elif airframe == 9:  # AV-8
            return {
                AoA.slo_hi(): 16,
                AoA.slo_med(): 13.5,
                AoA.slo_lo(): 12.5,
                AoA.ok(): 10,
                AoA.fast_lo(): 9.5,
                AoA.fast_med(): 8,
                AoA.fast_hi(): 7.5,
            }

    @staticmethod
    def data_limits_gs(airframe: int) -> dict:
        """Gets airframe context based GS limits

        Parameters
        ----------
        airframe : int
            Airframe index

        Returns
        -------
        dict
            airframe based GS limits
        """

        if airframe == 9:  # AV-8
            return {
                GS.___hi___(): 5.4,
                GS.__hi__(): 4.9,
                GS.hi(): 4.2,
                GS.gs(): 3.5,
                GS.lo(): 3,
                GS.__lo__(): 2.3,
                GS.___lo___(): 2.0,
            }
        else:
            return {
                GS.___hi___(): 5.0,
                GS.__hi__(): 4.3,
                GS.hi(): 3.9,
                GS.gs(): 3.5,
                GS.lo(): 3.2,
                GS.__lo__(): 2.9,
                GS.___lo___(): 2.6,
            }

    @staticmethod
    def data_limits_gse(airframe: int) -> dict:
        """Gets airframe context based GSE limits

        Parameters
        ----------
        airframe : int
            Airframe index

        Returns
        -------
        dict
            airframe based GSE limits
        """
        if airframe == 9:  # AV-8
            return {
                GS.___hi___(): 1.9,
                GS.__hi__(): 1.4,
                GS.hi(): 0.7,
                GS.gs(): 0,
                GS.lo(): -0.5,
                GS.__lo__(): -1.2,
                GS.___lo___(): -1.5,
            }
        else:
            return {
                GS.___hi___(): 1.5,
                GS.__hi__(): 0.8,
                GS.hi(): 0.4,
                GS.gs(): 0,
                GS.lo(): -0.3,
                GS.__lo__(): -0.6,
                GS.___lo___(): -0.9,
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
            GRV.___lul___(): -3,
            GRV.__lul__(): -1,
            GRV.lul(): -.5,
            GRV.ok(): 0,
            GRV.lur(): .5,
            GRV.__lur__(): 1,
            GRV.___lur___(): 3,
        }
