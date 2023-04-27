import datetime
import json
import os.path
import numpy as np

from root import ROOT_DIR
from src.lib.Bcolors import Bcolors as Colors
from src.lib.DataLimits import DataLimits
from src.precise_plot.modules.Keys import KeysCSV as K


class ParserAirbossData:
    def __init__(self, dump_data: bool = False):
        self.__data = dict
        self.__oth_data = dict
        self.__airframe_index = int
        self.__limits_aoa = dict
        self.__limits_lu = dict
        self.__limits_lue = dict
        self.__limits_gs = dict
        self.__limits_gse = dict
        self.__dump_name = str
        self.dump_data = dump_data

    def init_data(self, result: dict):
        now = datetime.datetime.now().strftime("%Y_%m_%d_%I_%M")
        self.__dump_name = now + "_trap_file.json"
        if self.dump_data:
            try:
                with open(os.path.join(ROOT_DIR, "tests", "dumps", self.__dump_name), "w") as file:
                    file.write(json.dumps(result))
                    print("Plotter Class debug msg\n")
                    print(datetime.datetime.now().isoformat() + "\n")
                    print(json.dumps(result))
                    print("END\n")
            except Exception as e:
                print(f"{Colors.FAIL} e {Colors.ENDC}")

        self.__data = {
            K.x(): -np.array(result["trapsheet"][K.x()]),
            K.z(): np.array(result["trapsheet"][K.z()]),
            K.aoa(): np.array(result["trapsheet"][K.aoa()]),
            K.alt(): np.array(result["trapsheet"][K.alt()]),
            K.vy(): np.array(result["trapsheet"][K.vy()]),
            K.roll(): np.array(result["trapsheet"][K.roll()]),
            K.lue(): -np.array(result["trapsheet"][K.lue()]),
            K.gse(): np.array(result["trapsheet"][K.gse()]),
        }

        def get_val(table: dict, key: str, nil: str or int = "", precision: int or None = None) -> str or int:
            """
            Get table value.
            """
            if key in table:
                value = table[key]
                if value == "false":
                    return False
                elif value == "true":
                    return True
                else:
                    if precision:
                        return str(round(value, precision))
                    else:
                        return value
            else:
                return nil

        self.__oth_data = {
            "actype": get_val(result, "airframe", "Unkown"),
            "Tgroove": get_val(result, "Tgroove", "?", 1),

            "player": get_val(result, "name", "Ghostrider"),
            "grade": get_val(result, "grade", "?"),
            "points": get_val(result, "points", "?"),
            "details": get_val(result, "details"),
            "case": get_val(result, "case", "?"),
            "wire": get_val(result, "wire", "?"),

            "carriertype": get_val(result, "carriertype", "?"),
            "carriername": get_val(result, "carriername", "?"),
            "landingdist": get_val(result, "landingdist", -86),
            "windondeck": get_val(result, "wind", "?", 1),
            "missiontime": get_val(result, "mitime", "?"),
            "missiondate": get_val(result, "midate", "?"),
            "theatre": get_val(result, "theatre", "Unknown Map")
        }

        self.__airframe_index = DataLimits.airframe_context(self.__oth_data["actype"])
        self.__limits_aoa = DataLimits.data_limits_aoa(self.__airframe_index)
        self.__limits_lu = DataLimits.data_limits_lu()
        self.__limits_gs = DataLimits.data_limits_gs(self.__airframe_index)
        self.__limits_gse = DataLimits.data_limits_gse(self.__airframe_index)

    def dump_data_to_json(self):
        with open(os.path.join(ROOT_DIR, "tests", "results", "data", "json", "data_" + self.__dump_name),
                  "w") as data_dump:
            data_dump.write(json.dumps(self.__data, indent=4))
        with open(os.path.join(ROOT_DIR, "tests", "results", "data", "json", "data_oth" + self.__dump_name),
                  "w") as oth_data_dump:
            oth_data_dump.write(json.dumps(self.__oth_data, indent=4))
