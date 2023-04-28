import datetime
import json
import os.path
from enum import Enum
from typing import Type

import numpy as np

from root import ROOT_DIR
from src.lib.Bcolors import Bcolors as Colors
from src.lib.DataLimits import DataLimits, CarriersData
from src.lib.Keys import \
    KeysTrapsheet as K,\
    KeysTrapfile as KO
from src.lib.Utils import Utils


get_val = Utils.get_val


class ParserAirbossData:
    def __init__(self, dump_data: bool = False):
        self.__raw_data = dict
        self.__data = dict
        self.__oth_data = dict
        self.__airframe_index = int
        self.__limits_aoa = dict
        self.__limits_lu = dict
        self.__limits_lue = dict
        self.__limits_gs = dict
        self.__limits_gse = dict
        self.__carrier_data = dict
        self.__dump_name = str
        self.dump_data = dump_data

    @property
    def data(self) -> Type[dict]:
        return self.__data

    @property
    def oth_data(self) -> Type[dict]:
        return self.__oth_data

    @property
    def raw_data(self) -> Type[dict]:
        return self.__raw_data

    @property
    def carrier_data(self) -> Type[dict]:
        return self.__carrier_data

    @property
    def airframe_index(self) -> Type[int]:
        return self.__airframe_index

    @property
    def limits_aoa(self) -> Type[dict]:
        return self.__limits_aoa

    @property
    def limits_lu(self) -> Type[dict]:
        return self.__limits_lu

    @property
    def limits_lue(self) -> Type[dict]:
        return self.__limits_lue

    @property
    def limits_gs(self) -> Type[dict]:
        return self.__limits_gs

    @property
    def limits_gse(self) -> Type[dict]:
        return self.__limits_gse

    def init_data(self, result: dict, filename: str or None = None):
        now = datetime.datetime.now().strftime("%Y_%m_%d_%I_%M")
        if filename:
            self.__dump_name = filename
        else:
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

        self.__raw_data = {
            K.X: result[KO.TRAPSHEET.value][K.X.value],
            K.Z: result[KO.TRAPSHEET.value][K.Z.value],
            K.AOA: result[KO.TRAPSHEET.value][K.AOA.value],
            K.ALT: result[KO.TRAPSHEET.value][K.ALT.value],
            K.VY: result[KO.TRAPSHEET.value][K.VY.value],
            K.ROLL: result[KO.TRAPSHEET.value][K.ROLL.value],
            K.LUE: result[KO.TRAPSHEET.value][K.LUE.value],
            K.GSE: result[KO.TRAPSHEET.value][K.GSE.value],
        }
        self.__data = {
            K.X: -np.array(self.__raw_data[K.X]),
            K.Z: np.array(self.__raw_data[K.Z]),
            K.AOA: np.array(self.__raw_data[K.AOA]),
            K.ALT: np.array(self.__raw_data[K.ALT]),
            K.VY: np.array(self.__raw_data[K.VY]),
            K.ROLL: np.array(self.__raw_data[K.ROLL]),
            K.LUE: -np.array(self.__raw_data[K.LUE]),
            K.GSE: np.array(self.__raw_data[K.GSE]),
        }
        self.__oth_data = {
            KO.AIRFRAME: get_val(result, KO.AIRFRAME.value),
            KO.TGROOVE: get_val(result, KO.TGROOVE.value, precision=1),

            KO.NAME: get_val(result, KO.NAME.value),
            KO.GRADE: get_val(result, KO.GRADE.value),
            KO.POINTS: get_val(result, KO.POINTS.value),
            KO.DETAILS: get_val(result, KO.DETAILS.value),
            KO.CASE: get_val(result, KO.CASE.value),
            KO.WIRE: get_val(result, KO.WIRE.value),

            KO.CARRIERTYPE: get_val(result, KO.CARRIERTYPE.value),
            KO.CARRIERNAME: get_val(result, KO.CARRIERNAME.value),
            KO.LANDINGDIST: get_val(result, KO.LANDINGDIST.value, -86),
            KO.WIND: get_val(result, KO.WIND.value, precision=1),
            KO.MITIME: get_val(result, KO.MITIME.value),
            KO.MIDATE: get_val(result, KO.MIDATE.value),
            KO.THEATRE: get_val(result, KO.THEATRE.value)
        }
        self.__carrier_data = CarriersData.carriers_data(CarriersData.carrier_context(self.__oth_data[KO.CARRIERTYPE]))
        self.__airframe_index = DataLimits.airframe_context(self.__oth_data[KO.AIRFRAME])
        self.__limits_aoa = DataLimits.data_limits_aoa(self.__airframe_index)
        self.__limits_lu = DataLimits.data_limits_lu()
        self.__limits_gs = DataLimits.data_limits_gs(self.__airframe_index)
        self.__limits_gse = DataLimits.data_limits_gse(self.__airframe_index)
        self.__oth_data[KO.CARRIERDATA] = self.__carrier_data

    def dump_data_to_json(self):
        def convert_enum_to_str(input_dict: Type[dict]) -> dict:
            result_dict = {}
            for k, v in input_dict.items():
                if isinstance(k, Enum):
                    k_new = k.value
                else:
                    k_new = k
                if isinstance(v, Enum):
                    v_new = v.value
                elif isinstance(v, dict):
                    v_new = convert_enum_to_str(v)
                else:
                    v_new = v
                result_dict[k_new] = v_new
            return result_dict

        raw_data = convert_enum_to_str(self.raw_data)
        oth_data = convert_enum_to_str(self.oth_data)
        oth_data[KO.TRAPSHEET.value] = raw_data

        with open(self.__dump_name, "w") as oth_data_dump:
            oth_data_dump.write(json.dumps(oth_data, indent=4))


class DownwindStripper:
    @staticmethod
    def downwind_stripper(x: np.array) -> int:
        downwind_index = int
        for i in range(len(x)):
            # astern
            if x[i] > 0:
                # closing range
                if x[i] < x[i - 1]:
                    break
                # farthest astern
                else:
                    downwind_index = i
        return downwind_index
