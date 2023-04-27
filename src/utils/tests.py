"""
Test cases.
"""

from random import randint
from src.plotters.funkman_plot.FunkmanPlot import Plot
from src.utils.utils import read_trap_csv


def get_result_strafe():
    nfired = randint(1, 500)
    nhit = randint(0, nfired)
    nfired = 5
    nhit = 5

    # Result.
    resultStrave = {
        "command": "moose_strafe_result",
        "player": "funkyfranky",
        "name": "My Target",
        "clock": "9:45:01",
        "midate": "2022-04-01",
        "roundsFired": nfired,
        "roundsHit": nhit,
        "roundsQuality": "Some Quality",
        "strafeAccuracy": nhit / nfired * 100,
        "rangename": "My Range",
        "airframe": "F/A-18C_hornet",
        "invalid": "false",
        "theatre": "Caucasus",
    }

    return resultStrave


def get_result_bomb():
    # Result.
    result = {
        "command": "moose_bomb_result",
        "name": "Target Name",
        "distance": randint(5, 300),
        "radial": randint(1, 360),
        "weapon": "Mk 82",
        "quality": "Ineffective",
        "player": "funkyfranky",
        "clock": "8:02",
        "airframe": "F/A-18C_hornet",
        "rangename": "My Range Name",
        "attackHdg": randint(1, 360),
        "attackVel": randint(250, 400),
        "attackAlt": randint(6000, 12000),
        "theatre": "Caucasus",
    }

    return result


def get_result_trap(trapfile: str or dict, csv: bool = False) -> dict:
    # Read trapsheet from disk for testing.
    if csv:
        data_csv = read_trap_csv(trapfile)
        trapsheet = data_csv["trapsheet"]
        trapfile = data_csv["info"]
    else:
        trapsheet = trapfile["trapsheet"]

    # Debug info.
    # print(trapsheet)
    # print(trapfile)

    # grade
    try:
        if csv:
            grade = trapsheet["Grade"][-1]
        else:
            grade = trapfile["grade"]
    except:
        grade = "N/A"
    # details
    try:
        if csv:
            details = trapsheet["Details"][-1]
            details.strip()
            if details.strip() == "":
                details = "Unicorn"
        else:
            details = trapfile["details"]
    except:
        details = "N/A"
    # points
    try:
        if csv:
            points = trapsheet["Points"][-1]
        else:
            points = trapfile["points"]
    except:
        points = 0
    # case
    case = trapfile["case"]

    # Result.
    result = {
        "command": "moose_lso_grade",
        "server_name": trapfile["server_name"],
        "name": trapfile["name"],
        "trapsheet": trapsheet,
        "airframe": trapfile["airframe"],
        "mitime": trapfile["mitime"],
        "midate": trapfile["midate"],
        "wind": trapfile["wind"],
        "carriertype": trapfile["carriertype"],
        "carriername": trapfile["carriername"],
        "carrierrwy": trapfile["carrierrwy"],
        "landingdist": trapfile["landingdist"],
        "theatre": trapfile["theatre"],
        "Tgroove": trapfile["Tgroove"],
        "case": trapfile["case"],
        "grade": trapfile["grade"],
        "finalscore": trapfile["points"],
        "points": trapfile["points"],
        "details": details or "(LUL)X (F)IM  LOLULIC LOLULAR"
    }
    if trapfile["wire"]:
        result["wire"] = trapfile["wire"]
    return result


def test_strafe(funkplot: Plot):
    # Debug info.
    print("Testing StrafeRun funkman_plot")

    # Get result.
    resultStrafe = get_result_strafe()

    # Create figuire.
    fig, ax = funkplot.PlotStrafeRun(resultStrafe)

    return fig, ax


def test_bomb(funkplot: Plot):
    # Debug info.
    print("Testing BombRun funkman_plot")

    # Get result.
    resultBomb = get_result_bomb()

    # Create figure.
    fig, ax = funkplot.PlotBombRun(resultBomb)

    return fig, ax


def test_trap(funkplot: Plot, trapfile: str):
    # Debug info.
    print(f"Testing TrapSheet funkman_plot from {trapfile}")

    # Get result.
    result = get_result_trap(trapfile)

    # Create figure.
    fig, axs = funkplot.PlotTrapSheet(result)

    return fig, axs
