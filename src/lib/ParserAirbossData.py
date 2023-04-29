import datetime
import json
import os.path
from enum import Enum
from typing import Type, Any

import numpy as np

from root import ROOT_DIR
from src.lib.Bcolors import Bcolors as Colors
from src.lib.DataLimits import DataLimits, CarriersData
from src.lib.Keys import \
    KeysTrapsheet as K, \
    KeysTrapfile as KO, \
    KeysTrapfile, KeysTrapsheet, KeysCarrierfile, KeysAirframes, KeysAoA, KeysGRV, KeysGS
from src.lib.Utils import Utils


get_val = Utils.get_val


class ParserAirbossData:
    def __init__(self, dump_rcvd_data: bool = False):
        self.dump_name: str or None = None
        self.limits_lue: dict = {}
        self.raw_data: dict = {}
        self.data: dict[KeysTrapsheet, dict | Any] = {}
        self.oth_data: dict[KeysTrapfile, dict | Any] = {}
        self.airframe_index: KeysAirframes or None = None
        self.limits_aoa: dict[KeysAoA, float] = {}
        self.limits_lu: dict[KeysGRV, float] = {}
        self.limits_lue: dict[KeysGRV, float] = {}
        self.limits_gs: dict[KeysGS, float] = {}
        self.limits_gse: dict[KeysGS, float] = {}
        self.carrier_data: dict[KeysCarrierfile, Any] = {}
        self.dump_rcvd_data: bool = dump_rcvd_data

    def init_data(self, result: dict, filename: str or None = None):
        now = datetime.datetime.now().strftime("%Y_%m_%d_%I_%M")
        if filename:
            self.dump_name = filename
        else:
            self.dump_name = now + "_trap_file.json"
        if self.dump_rcvd_data:
            try:
                with open(os.path.join(ROOT_DIR, "tests", "dumps", self.dump_name), "w") as file:
                    file.write(json.dumps(result))
                    print("Plotter Class debug msg\n")
                    print(datetime.datetime.now().isoformat() + "\n")
                    print(json.dumps(result))
                    print("END\n")
            except Exception as e:
                print(f"{Colors.FAIL} e {Colors.ENDC}")

        print(result)
        print(result.keys())

        self.raw_data = {
            K.X: result[KO.TRAPSHEET.value][K.X.value],
            K.Z: result[KO.TRAPSHEET.value][K.Z.value],
            K.AOA: result[KO.TRAPSHEET.value][K.AOA.value],
            K.ALT: result[KO.TRAPSHEET.value][K.ALT.value],
            K.VY: result[KO.TRAPSHEET.value][K.VY.value],
            K.ROLL: result[KO.TRAPSHEET.value][K.ROLL.value],
            K.LUE: result[KO.TRAPSHEET.value][K.LUE.value],
            K.GSE: result[KO.TRAPSHEET.value][K.GSE.value],
        }
        self.data = {
            K.X: -np.array(self.raw_data[K.X]),
            K.Z: np.array(self.raw_data[K.Z]),
            K.AOA: np.array(self.raw_data[K.AOA]),
            K.ALT: np.array(self.raw_data[K.ALT]),
            K.VY: np.array(self.raw_data[K.VY]),
            K.ROLL: np.array(self.raw_data[K.ROLL]),
            K.LUE: -np.array(self.raw_data[K.LUE]),
            K.GSE: np.array(self.raw_data[K.GSE]),
        }
        self.oth_data = {
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
        self.carrier_data = CarriersData.carriers_data(CarriersData.carrier_context(self.oth_data[KO.CARRIERTYPE]))
        self.airframe_index = DataLimits.airframe_context(self.oth_data[KO.AIRFRAME])
        self.limits_aoa = DataLimits.data_limits_aoa(self.airframe_index)
        self.limits_lu = DataLimits.data_limits_lu()
        self.limits_gs = DataLimits.data_limits_gs(self.airframe_index)
        self.limits_gse = DataLimits.data_limits_gse(self.airframe_index)
        self.oth_data[KO.CARRIERDATA] = self.carrier_data

    def dump_data_to_json(self):
        def convert_enum_to_str(input_dict: dict) -> dict:
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

        with open(self.dump_name, "w") as oth_data_dump:
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
