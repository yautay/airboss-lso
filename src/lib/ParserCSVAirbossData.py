import csv
from datetime import datetime
from typing import Any
import numpy as np
from numpy import ndarray

from src.lib.DataLimits import CarriersData, DataLimits
from src.lib.Utils import Utils
from src.lib.Keys import \
    KeysTrapfile as KTF, \
    KeysTrapsheet as KTS, \
    KeyesCSVTrapfile as KCSV, \
    KeysAirframes, \
    KeysCarriers, KeysTrapsheet, KeysAoA, KeysGRV, KeysGS, KeysCarrierfile

get_val = Utils.get_val


class ParserCSVAirbossData(object):
    def __init__(self):
        self.limits_lue: dict = {}
        self.raw_data: dict = {}
        self.data: dict[KeysTrapsheet, ndarray] = {}
        self.oth_data: dict[KTF, dict | Any] = {}
        self.airframe_index: KeysAirframes or None = None
        self.limits_aoa: dict[KeysAoA, float] = {}
        self.limits_lu: dict[KeysGRV, float] = {}
        self.limits_lue: dict[KeysGRV, float] = {}
        self.limits_gs: dict[KeysGS, float] = {}
        self.limits_gse: dict[KeysGS, float] = {}
        self.carrier_data: dict[KeysCarrierfile, Any] = {}

    def read_csv_trap(self, filepath: str):
        """Read a trap sheet into a dictionary as numpy arrays."""
        print(f"Reading trap sheet from file={filepath}")

        d = {}
        try:
            with open(filepath) as f:
                groove_first_pass = True
                groove_start = None
                groove_end = None
                reader = csv.DictReader(f)
                for k in reader.fieldnames:
                    d[k] = np.array([])
                for row in reader:
                    for k in reader.fieldnames:
                        svalue = row[k]
                        if k == "Details":
                            if svalue.replace(" ", "") != "":
                                if groove_first_pass:
                                    groove_start = row["#Time"]
                                    groove_first_pass = False
                                groove_end = row["#Time"]
                        try:
                            fvalue = float(svalue)
                            if k == "X":
                                # Invert X. The re-inversion is done in plot now.
                                fvalue = -fvalue
                            elif k == "Alt":
                                # Convert altitude from feet to meters. Back conversion is done in plot now.
                                fvalue = fvalue * 0.3048
                            d[k] = np.append(d[k], fvalue)
                        except ValueError:
                            d[k] = np.append(d[k], svalue)  # svalue
            d["Groove"] = float(groove_end) - float(groove_start)
        except Exception as e:
            print(f'CSV READ ERROR! {str(e)}')

        d[KTS.X] = d.pop('X')
        d[KTS.Z] = d.pop('Z')
        d[KTS.ALT] = d.pop('Alt')
        d[KTS.AOA] = d.pop('AoA')
        d[KTS.GSE] = d.pop('GSE')
        d[KTS.LUE] = d.pop('LUE')
        d[KTS.VY] = d.pop('Vy')
        d[KTS.ROLL] = d.pop('Roll')
        d.pop('Rho')
        d.pop('Vtot')
        d.pop('#Time')
        d.pop('Gamma')
        d.pop('Pitch')
        d.pop('Yaw')
        d.pop('Step')
        d[KTF.GRADE] = d['Grade'][-1]
        d[KTF.POINTS] = d['Points'][-1]
        d[KTF.DETAILS] = d['Details'][-1]
        d[KTF.TGROOVE] = d['Groove']
        d.pop('Grade')
        d.pop('Points')
        d.pop('Details')
        # Get some more data fm file title
        filename = filepath.split("\\")[-1]
        # AIRFRAME
        if KCSV.F_18.value in filename:
            d[KTF.AIRFRAME] = KeysAirframes.HORNET
        elif KCSV.F_14A.value in filename:
            d[KTF.AIRFRAME] = KeysAirframes.F14A
        elif KCSV.F_14B.value in filename:
            d[KTF.AIRFRAME] = KeysAirframes.F14B
        elif KCSV.AV8B.value in filename:
            d[KTF.AIRFRAME] = KeysAirframes.AV8B
        # CVN
        if KCSV.CVN_75.value in filename:
            d[KTF.CARRIERTYPE] = KeysCarriers.TRUMAN
        if KCSV.TARAWA.value in filename:
            d[KTF.CARRIERTYPE] = KeysCarriers.TARAWA
        # PLAYER
        d[KTF.NAME] = filename.strip(".csv").split("Trapsheet-")[1].replace(" _ ", "-").split("_")[0]

        self.raw_data = {
            KTS.X: d[KTS.X],
            KTS.Z: d[KTS.Z],
            KTS.AOA: d[KTS.AOA],
            KTS.ALT: d[KTS.ALT],
            KTS.VY: d[KTS.VY],
            KTS.ROLL: d[KTS.ROLL],
            KTS.LUE: d[KTS.LUE],
            KTS.GSE: d[KTS.GSE]
        }
        self.data = {
            KTS.X: -np.array(self.raw_data[KTS.X]),
            KTS.Z: np.array(self.raw_data[KTS.Z]),
            KTS.AOA: np.array(self.raw_data[KTS.AOA]),
            KTS.ALT: np.array(self.raw_data[KTS.ALT]),
            KTS.VY: np.array(self.raw_data[KTS.VY]),
            KTS.ROLL: np.array(self.raw_data[KTS.ROLL]),
            KTS.LUE: -np.array(self.raw_data[KTS.LUE]),
            KTS.GSE: np.array(self.raw_data[KTS.GSE]),
        }
        self.oth_data = {
            KTF.AIRFRAME: d[KTF.AIRFRAME],
            KTF.TGROOVE: d[KTF.TGROOVE],

            KTF.NAME: d[KTF.NAME],
            KTF.GRADE: d[KTF.GRADE],
            KTF.POINTS: d[KTF.POINTS],
            KTF.DETAILS: d[KTF.DETAILS],
            KTF.CASE: None,
            KTF.WIRE: None,

            KTF.CARRIERTYPE: d[KTF.CARRIERTYPE],
            KTF.CARRIERNAME: None,
            KTF.LANDINGDIST: None,
            KTF.WIND: None,
            KTF.MITIME: datetime.now().strftime("%H:%M:%S"),
            KTF.MIDATE: datetime.now().strftime("%Y/%m/%d"),
            KTF.THEATRE: None
        }
        self.carrier_data = CarriersData.carriers_data(
            CarriersData.carrier_context(self.oth_data[KTF.CARRIERTYPE].value))
        self.airframe_index = DataLimits.airframe_context(self.oth_data[KTF.AIRFRAME].value)
        self.limits_aoa = DataLimits.data_limits_aoa(self.airframe_index)
        self.limits_lu = DataLimits.data_limits_lu()
        self.limits_gs = DataLimits.data_limits_gs(self.airframe_index)
        self.limits_gse = DataLimits.data_limits_gse(self.airframe_index)
        self.oth_data[KTF.CARRIERDATA] = self.carrier_data
