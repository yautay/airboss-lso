import csv
import numpy as np
from src.lib.Utils import Utils
from src.lib.Keys import KeysTrapfile as KTF, KeysTrapsheet as KTS

get_val = Utils.get_val


class CSVData(object):
    def __init__(self, data: dict):
        self.data = data


class ParserCSVAirbossData:

    @staticmethod
    def read_csv_trap(filepath: str) -> CSVData:
        """Read a trap sheet into a dictionary as numpy arrays."""
        print(f"Reading trap sheet from file={filepath}")

        d = {}
        try:
            with open(filepath) as f:
                reader = csv.DictReader(f)
                for k in reader.fieldnames:
                    d[k] = np.array([])
                for row in reader:
                    for k in reader.fieldnames:
                        svalue = row[k]
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
        d.pop('Grade')
        d.pop('Points')
        d.pop('Details')
        # ToDo Dorobić parsowanie nazwy CSV -> lotniskowiec/typ + name gracza + airframe
        print(d)
        return CSVData(d)


# def get_result_trap(trapfile: str):
#     # Read trapsheet from disk for testing.
#     trapsheet = read_trap(trapfile)
#
#     # Debug info.
#     # print(trapsheet)
#     # print(trapsheet.keys())
#
#
#     rwyangle = -9
#     wire = randint(1, 4)
#     carriername = "USS Stennis"
#     carriertype = "CVN-74"
#     landingdist = -165 + 79  # sterndist+wire3
#     if "Tarawa" in trapfile:
#         rwyangle = 0
#         wire = None
#         carriername = "Tarawa"
#         carriertype = "LHA"
#         landingdist = -125 + 69  # sterndist+landingpos
#
#     airframe = 'FA-18C_hornet'
#     if "AV8B" in trapfile:
#         airframe = "AV8BNA"
#
#     # Result.
#     result = {
#         "command": "moose_lso_grade",
#         "name": "Ghostrider",
#         "trapsheet": trapsheet,
#         "airframe": airframe,
#         "mitime": "05:00:01",
#         "midate": "2022-04-01",
#         "wind": 25.13432432432423,
#         "carriertype": carriertype,
#         "carriername": carriername,
#         "carrierrwy": rwyangle,
#         "landingdist": landingdist,
#         "theatre": "Kola",
#         "Tgroove": randint(10, 20),
#         "case": randint(1, 3),
#         "grade": grade or "OK",
#         "finalscore": points or 2,
#         "points": points or 3,
#         "details": details or "(LUL)X (F)IM  LOLULIC LOLULAR"
#     }
#     if wire:
#         result["wire"] = wire
#
#     print(result)
#
#     return result