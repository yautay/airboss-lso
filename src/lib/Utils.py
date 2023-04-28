from enum import Enum


class Utils:

    @staticmethod
    def mtrs_to_nm(mtrs: float) -> float:
        return mtrs / 1852

    @staticmethod
    def cbl_to_feet(cbls: float) -> float:
        return cbls * 607.61155

    @staticmethod
    def feet_to_cbl(feet: float) -> float:
        return feet / 607.61155

    @staticmethod
    def mtrs_to_cbls(mtrs: float) -> float:
        return mtrs / 185.2

    @staticmethod
    def mtrs_to_feet(mtrs: float) -> float:
        return mtrs * 3.2808399

    @staticmethod
    def nm_to_mtrs(nm: float) -> float:
        return nm * 1852

    @staticmethod
    def nm_to_cbls(nm: float) -> float:
        return nm * 10

    @staticmethod
    def nm_to_feet(nm: float) -> float:
        return nm * 6076.11549

    @staticmethod
    def mile_quarts(quarts: int, mtrs: bool = True, nm: bool = False, cbls: bool = False, feet: bool = False) -> float:
        mile_decimal = quarts / 4
        if mtrs:
            return Utils.nm_to_mtrs(mile_decimal)
        elif nm:
            return mile_decimal
        elif cbls:
            return Utils.nm_to_cbls(mile_decimal)
        elif feet:
            return Utils.nm_to_feet(mile_decimal)

    @staticmethod
    def units_to_deg(units: float, hb_method: bool = True) -> float:
        if hb_method:
            return (0.918 * units) - 3.411
        else:
            return -10 + (50 / 30 * units)

    @staticmethod
    def get_val(table: dict, key: Enum or str, nil: str or int = "N/A", precision: int or None = None) -> bool or int or str:
        if key in table.keys():
            value = table[key]
            if value == "false":
                return False
            elif value == "true":
                return True
            elif isinstance(value, int):
                if precision:
                    return str(round(value, precision))
                else:
                    return str(value)
            else:
                return value
        else:
            return nil
