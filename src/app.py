import configparser
import os.path

from root import ROOT_DIR
from src.bot.Bot import Bot
from src.lib.ConfigApp import ConfigApp
from src.lib.ConfigDiscord import ConfigDiscord
from src.lib.ConfigUDPSocket import ConfigUDPSocket
from src.lib.ParserCSVAirbossData import ParserCSVAirbossData


class App(object):
    def __init__(self):
        self.config_app = ConfigApp()
        self.config_discord = ConfigDiscord()
        self.config_udp_socket = ConfigUDPSocket()
        self.__set_ini()
        self.bot = Bot(self.config_discord)

    def run(self):
        self.bot.start_bot(True)

    def parse_csv_files(self, files: list[str]):
        files_data = []
        for file in files:
            files_data.append(ParserCSVAirbossData.read_csv_trap(str(self.config_app.airboss_csv_folder) + file))
        for e in files_data:
            print(e.data.keys())

    def __set_ini(self):
        path_ini = os.path.join(ROOT_DIR, "App.ini")
        print(f"Reading config file {path_ini}")
        try:
            os.path.exists(path_ini)
            config = configparser.ConfigParser()
            config.read(path_ini)
            try:
                section_app = config["APP"]
                self.config_app.airboss_csv_folder = section_app.get("AIRBOSSCSV", None)
            except:
                print("ERROR: [APP] section missing in ini file!")
            try:
                section_discord = config["DISCORD"]
                self.config_discord.token = section_discord.get("TOKEN", None)
                self.config_discord.channel_id_main = section_discord.getint("CHANNELID_MAIN", None)
                self.config_discord.channel_id_range = section_discord.getint("CHANNELID_RANGE", None)
                self.config_discord.channel_id_airboss = section_discord.getint("CHANNELID_AIRBOSS", None)
                self.config_discord.channel_id_notam = section_discord.getint("CHANNELID_NOTAM", None)
            except:
                print("ERROR: [DISCORD] section missing in ini file!")
            try:
                section_udp_socket = config["UDPSOCKET"]
                self.config_udp_socket.port = section_udp_socket.getint("PORT", 10042)
                self.config_udp_socket.host = section_udp_socket.get("HOST", "127.0.0.1")
            except:
                print("ERROR: [UDPSOCKET] section missing in ini file!")
        except FileNotFoundError:
            print(f"Could not find ini file {path_ini} in {os.getcwd()}!")
            quit()
