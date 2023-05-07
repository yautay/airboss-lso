from src.lib.ParserAirbossData import ParserAirbossData
from src.lib.Utils import Utils

get_val = Utils.get_val


class FunkmanLso:
    def __init__(self, data_object: ParserAirbossData):
        self.__data = data_object.data
        self.__oth_data = data_object.oth_data
        self.__airframe_index = data_object.airframe_index
        self.__limits_aoa = data_object.limits_aoa
        self.__limits_lu = data_object.limits_lu
        self.__limits_lue = data_object.limits_lue
        self.__limits_gs = data_object.limits_gs
        self.__limits_gse = data_object.limits_gse


    # Get date from result.
    actype = get_val(result, "airframe", "Unkown")
    tgroove = get_val(result, "Tgroove", "?", 1)
    player = get_val(result, "name", "Ghostrider")
    grade = get_val(result, "grade", "?")
    points = get_val(result, "points", "?")
    details = get_val(result, "details", "?")
    case = get_val(result, "case", "?")
    wire = get_val(result, "wire", "?")
    carriertype = get_val(result, "carriertype", "?")
    carriername = get_val(result, "carriername", "?")
    windondeck = get_val(result, "wind", "?", 1)
    missiontime = get_val(result, "mitime", "?")
    missiondate = get_val(result, "midate", "?")
    theatre = get_val(result, "theatre", "Unknown Map")
    theta = get_val(result, "carrierrwy", -9)

    # ToDo tutaj podmieniamy obrazki LSO :)

    lso_pic = "LSO.png"
    if abs(theta) < 0.1:
        lso_pic = "LSO_Vstol.png"

    # ToDo tutaj podmieniamy obrazki punktów :)
    color = 0x00ff00
    url_im = "https://i.imgur.com/1bWgcV7.png"
    if type(points) != str:
        if points == 0:
            color = 0x000000  # black
            url_im = "https://i.imgur.com/rZpu9c0.png"
        elif points == 1:
            color = 0xff0000  # red
            url_im = "https://i.imgur.com/LXgD2Op.png"
        elif points == 2:
            color = 0xFFA500  # orange
            url_im = "https://i.imgur.com/EjviMBk.png"
        elif points == 2.5:
            color = 0xB47E59  # brown
            url_im = "https://i.imgur.com/nYWrL4Z.png"
        elif points == 3:
            color = 0xFFFF00  # yellow
            url_im = "https://i.imgur.com/wH0Gjqx.png"
        elif points == 4:
            color = 0x00FF00  # green
            url_im = "https://i.imgur.com/1bWgcV7.png"
        elif points == 5:
            color = 0x0000FF  # blue
            url_im = "https://i.imgur.com/6ecFSqo.png"

    # Create Embed
    embed = discord.Embed(title="LSO Grade",
                          description=f"Result for {player} at carrier {carriername} [{carriertype}]", color=color)

    # Create file.
    fileLSO = discord.File(self.image_path + lso_pic, filename="lso.png")

    # Images.
    embed.set_image(url="attachment://lso.png")
    embed.set_thumbnail(url=url_im)

    # Author.
    embed.set_author(name="FunkMan")

    # Data.
    embed.add_field(name="Grade", value=grade, inline=True)
    embed.add_field(name="Points", value=points, inline=True)
    embed.add_field(name="Details", value=details, inline=True)
    embed.add_field(name="Groove", value=tgroove, inline=True)
    if wire != "?":
        embed.add_field(name="Wire", value=wire, inline=True)
    embed.add_field(name="Case", value=case, inline=True)
    embed.add_field(name="Wind", value=windondeck, inline=True)
    embed.add_field(name="Aircraft", value=actype, inline=True)

    # Footer.
    embed.set_footer(text=f"{theatre}: {missiondate} ({missiontime})")

    # Send to Discord.
    self.send_discord_file(fileLSO, channel_id, embed)