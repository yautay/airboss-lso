def get_result_trap(trapfile: str or dict) -> dict:
    trapsheet = trapfile["trapsheet"]
    # grade
    try:
        grade = trapfile["grade"]
    except:
        grade = "N/A"
    # details
    try:
        details = trapfile["details"]
    except:
        details = "N/A"
    # points
    try:
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
        "details": details
    }
    if trapfile["wire"]:
        result["wire"] = trapfile["wire"]
    return result
