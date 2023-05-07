import configparser
import os.path

from root import ROOT_DIR
from src.lib.DiscordConfig import DiscordConfig
from src.lib.UDPSocketConfig import UDPSocketConfig


class App(object):
    def __init__(self):
        self.discord_config = DiscordConfig()
        self.udp_socket_config = UDPSocketConfig()
        self.__set_ini()

    def run(self):
        pass

    def got_csv_files(self, files: list[str]):
        pass

    def __set_ini(self):
        path_ini = os.path.join(ROOT_DIR, "App.ini")
        print(f"Reading config file {path_ini}")
        try:
            os.path.exists(path_ini)
            config = configparser.ConfigParser()
            config.read(path_ini)
            try:
                section_discord = config["DISCORD"]
                self.discord_config.token = section_discord.get("TOKEN", None)
                self.discord_config.channel_id_main = section_discord.getint("CHANNELID_MAIN", None)
                self.discord_config.channel_id_range = section_discord.getint("CHANNELID_RANGE", None)
                self.discord_config.channel_id_airboss = section_discord.getint("CHANNELID_AIRBOSS", None)
                self.discord_config.channel_id_notam = section_discord.getint("CHANNELID_NOTAM", None)
            except:
                print("ERROR: [DISCORD] section missing in ini file!")
            try:
                section_udp_socket = config["UDPSOCKET"]
                self.udp_socket_config.port = section_udp_socket.getint("PORT", 10042)
                self.udp_socket_config.host = section_udp_socket.get("HOST", "127.0.0.1")
            except:
                print("ERROR: [UDPSOCKET] section missing in ini file!")
        except FileNotFoundError:
            print(f"Could not find ini file {path_ini} in {os.getcwd()}!")
            quit()
