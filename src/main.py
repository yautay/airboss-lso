from src.plot.Plot import Plot
from src.precise_plot.modules.Plotter import Plotter
from src.sock.Sock import Socket
from src.bot.Bot import Bot

import os
import configparser
from root import ROOT_DIR


class Main:
    def __init__(self, configFile=os.path.join(ROOT_DIR, "FunkMan.ini")) -> None:
        # Set config file.
        self.configFile = configFile

        # Define parameters used later on.
        self.port = None
        self.host = None
        self.token = None
        self.channel_id_server = None
        self.channel_id_main = None
        self.channel_id_range = None
        self.channel_id_airboss = None
        self.channel_id_notam = None
        self.image_path = None


        # Read config file.
        set_ini(self)

        # Create plot instance.
        self.funkplot = Plot(self.image_path)

        # Create bot instance.
        self.funkbot = Bot(token=self.token, channel_id=self.channel_id_main, image_path=self.image_path)

        # Create funksocket instance.
        self.funk_sock = Socket(Host=self.host, Port=self.port)

        # Set Bot.
        self.funk_sock.set_bot(self.funkbot)

        # Set Plot.
        self.funk_sock.set_plot(self.funkplot)

        # Set message channel ID.
        self.funk_sock.set_channel_id_message(self.channel_id_main)

        # Set channel ID for range data.
        self.funk_sock.set_channel_id_range(self.channel_id_range)

        # Set channel ID for airboss data.
        self.funk_sock.set_channel_id_airboss(self.channel_id_airboss)

        # Set channel ID for notam data.
        self.funk_sock.set_channel_id_notams(self.channel_id_notam)

    def callback(self, Func, *argv, **kwargs):
        """Callback function called at start."""
        print("callback fman")
        print(argv)
        self.funkbot.callback(Func, *argv, **kwargs)

    def start_bot(self):
        """
        Start socket and bot.
        """
        self.funkbot.start_bot(True)
        self.funk_sock.start()


def set_ini(funkman: Main) -> None:
    """
    Reads the config file.
    """

    # Info message.
    print(f"Reading config file {funkman.configFile}")

    # Check if config file exists
    try:
        os.path.exists(funkman.configFile)
    except FileNotFoundError:
        print(f"Could not find ini file {funkman.configFile} in {os.getcwd()}!")
        quit()

    # Config parser.
    config = configparser.ConfigParser()

    # Read config file.
    config.read(funkman.configFile)

    # FUNKBOT
    try:
        section = config["FUNKBOT"]
        funkman.token = section.get("TOKEN", "FROM_OS_ENV")
        funkman.channel_id_main = section.getint("CHANNELID_MAIN", 123456789)
        funkman.channel_id_range = section.getint("CHANNELID_RANGE", funkman.channel_id_main)
        funkman.channel_id_airboss = section.getint("CHANNELID_AIRBOSS", funkman.channel_id_main)
        funkman.channel_id_notam = section.getint("CHANNELID_NOTAM", funkman.channel_id_main)
    except:
        print("ERROR: [FUNKBOT] section missing in ini file!")

    # FUNKSOCK
    try:
        section = config["FUNKSOCK"]
        funkman.port = section.getint("PORT", 10042)
        funkman.host = section.get("HOST", "127.0.0.1")
    except:
        print("ERROR: [FUNKSOCK] section missing in ini file!")

    # FUNKPLOT
    try:
        section = config["FUNKPLOT"]
        funkman.image_path = section.get("IMAGEPATH", os.path.join(ROOT_DIR, "assets"))
    except:
        print("ERROR: [FUNKPLOT] section missing in ini file!")
