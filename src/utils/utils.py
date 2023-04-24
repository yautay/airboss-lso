"""
Utilities
"""

import csv
from datetime import datetime, date
from random import randint
import numpy as np
from src.utils.colors import Colors


def get_val(table, key, nil="", precision=None):
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
            if precision != None:
                return str(round(value, precision))
            else:
                return value
    else:
        return nil


def read_trap_csv(filename: str) -> dict:
    """Read a trap sheet into a dictionary as numpy arrays."""

    print(f"Reading trap sheet from file={filename}")

    d = {}
    try:
        with open(filename) as f:

            # Read csv.
            reader = csv.DictReader(f)

            # Init array.
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

        if "Tarawa" in filename:
            info = {
                "mitime": datetime.now().strftime("%H:%M:%S"),
                "midate": date.today(),
                "airframe": "AV8B",
                "server_name": "FunkManCSV",
                "name": "Buttrider",
                "carrierrwy": 0,
                "wire": None,
                "carriername": "Uss Trawa",
                "carriertype": "LHA",
                "landingdist": -125 + 69,  # sterndist+landingpos
                "wind": 25,
                "Tgroove": randint(10, 20),
                "case": randint(1, 3),
                "grade": "OK",
                "points": 2,
                "theatre": "Switzerland"
            }
        else:
            info = {
                "mitime": datetime.now().strftime("%H:%M:%S"),
                "midate": date.today(),
                "airframe": "FA-18C",
                "server_name": "FunkManCSV",
                "name": "Buttrider",
                "carrierrwy": -9,
                "wire": randint(1,4),
                "carriername": "USS Penis",
                "carriertype": "CVN-75",
                "landingdist": -165 + 79,  # sterndist+wire3
                "wind": 25,
                "Tgroove": randint(10, 20),
                "case": randint(1, 3),
                "grade": "OK",
                "points": 2,
                "theatre": "Switzerland"
            }
        data = {"info": info, "trapsheet": d}
        print(data)
        return data
    except Exception as e:
        print(f"{Colors.FAIL}ERROR! {Colors.FAIL}", f"{Colors.FAIL} {str(e)} {Colors.ENDC}")
