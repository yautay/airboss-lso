"""
Test cases.
"""

from random import randint
from src.plot.Plot import Plot
from src.utils.utils import read_trap


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


def get_result_trap(trapfile: str):
    # Read trapsheet from disk for testing.
    trapsheet = read_trap(trapfile)

    # Debug info.
    # print(trapsheet)
    # print(trapsheet.keys())
    try:
        grade = trapsheet.get("Grade")[-1]
    except:
        grade = "N/A"
    try:
        details = trapsheet.get("Details")[-1]
    except:
        details = "N/A"
    try:
        points = trapsheet.get("Points")[-1]
    except:
        points = 0

    details.strip()
    if details.strip() == "":
        details = "Unicorn"

    rwyangle = -9
    wire = randint(1, 4)
    carriername = "USS Stennis"
    carriertype = "CVN-74"
    landingdist = -165 + 79  # sterndist+wire3
    if "Tarawa" in trapfile:
        rwyangle = 0
        wire = None
        carriername = "Tarawa"
        carriertype = "LHA"
        landingdist = -125 + 69  # sterndist+landingpos

    airframe = 'FA-18C_hornet'
    if "AV8B" in trapfile:
        airframe = "AV8BNA"

    # Result.
    result = {
        "command": "moose_lso_grade",
        "name": "Ghostrider",
        "trapsheet": trapsheet,
        "airframe": airframe,
        "mitime": "05:00:01",
        "midate": "2022-04-01",
        "wind": 25.13432432432423,
        "carriertype": carriertype,
        "carriername": carriername,
        "carrierrwy": rwyangle,
        "landingdist": landingdist,
        "theatre": "Kola",
        "Tgroove": randint(10, 20),
        "case": randint(1, 3),
        "grade": grade or "OK",
        "finalscore": points or 2,
        "points": points or 3,
        "details": details or "(LUL)X (F)IM  LOLULIC LOLULAR"
    }
    if wire:
        result["wire"] = wire

    print(result)

    return result


def test_strafe(funkplot: Plot):
    # Debug info.
    print("Testing StrafeRun plot")

    # Get result.
    resultStrafe = get_result_strafe()

    # Create figuire.
    fig, ax = funkplot.PlotStrafeRun(resultStrafe)

    return fig, ax


def test_bomb(funkplot: Plot):
    # Debug info.
    print("Testing BombRun plot")

    # Get result.
    resultBomb = get_result_bomb()

    # Create figure.
    fig, ax = funkplot.PlotBombRun(resultBomb)

    return fig, ax


def test_trap(funkplot: Plot, trapfile: str):
    # Debug info.
    print(f"Testing TrapSheet plot from {trapfile}")

    # Get result.
    result = get_result_trap(trapfile)

    # Create figure.
    fig, axs = funkplot.PlotTrapSheet(result)

    return fig, axs
