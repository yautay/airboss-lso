import socketserver
import json
import os

from src.plot.Plot import Plot
from src.bot.Bot import Bot
from src.precise_plot.modules.Plotter import Plotter


class Handler(socketserver.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """

    def handle(self):
        # Get data.
        data = self.request[0].strip()

        # Debug message.
        print(f"New message from server {self.client_address[0]}")

        # Table data.
        table = json.loads(data)
        print(json.dumps(table, indent=2, sort_keys=True))

        try:
            # Evaluate table data.
            self.server.EvalData(table)
        except Exception as e:
            print(str(e))
            pass


class Socket(socketserver.UDPServer):
    """
    UDP socket server. It inherits "socketserver.UDPServer".
    """

    def __init__(self, Host="127.0.0.1", Port=10042) -> None:

        super().__init__((Host, Port), Handler)

        self.host = Host
        self.port = Port

        # Enable reuse, in case the restart was too fast and the port was still in TIME_WAIT.
        self.allow_reuse_address = True
        self.max_packet_size = 65504

        self.bot = None
        self.plot = None

        self.channel_id_message = None
        self.channel_id_range = None
        self.channel_id_airboss = None
        self.channel_id_notams = None

        print(f"FunkSocket: Host={self.host}:{self.port}")

    def set_bot(self, bot: Bot):
        """Set the FunkBot instance."""
        self.bot = bot

    def set_plot(self, plot: Plot):
        """Set the FunkPlot instance."""
        self.plot = plot

    def set_channel_id_message(self, channel_id: int):
        """Set channel ID for text messages."""
        self.channel_id_message = channel_id

    def set_channel_id_range(self, channel_id: int):
        """Set channel ID for Range figures."""
        self.channel_id_range = channel_id

    def set_channel_id_airboss(self, channel_id: int):
        """Set channel ID for Airboss."""
        self.channel_id_airboss = channel_id

    def set_channel_id_notams(self, channel_id: int):
        """Set channel ID for NOTAMS"""
        self.channel_id_notams = channel_id

    def start(self):
        """Start socket server."""

        # Info message.
        print(f"Starting Socket server {self.host}:{self.port}")

        try:
            self.serve_forever()
        except:
            print("Keyboard Control+C exception detected, quitting.")
            os._exit(0)

    def EvalData(self, table: dict):
        """Evaluate data received from socket. You might want to overwrite this function."""

        key = "command"
        textmessage = "moose_text"
        bombresult = "moose_bomb_result"
        straferesult = "moose_strafe_result"
        lsograde = "moose_lso_grade"
        notam = "custom_notam"

        # Treat different cases.
        if key in table:

            command = table.get(key, "")
            server = table.get("server_name", "unknown")

            # Debug info
            print("Got {command} from server {server}!")

            if command == textmessage:
                print("Got text message!")

                # Extract text.
                text = table.get("text", " ")

                # Send text to Discord.
                self.bot.send_text(text, self.channel_id_message)

            elif command == bombresult:
                print("Got bomb result!")

                # Create bomb run figure.
                fig, ax = self.plot.PlotBombRun(table)

                # Send figure to Discord.
                self.bot.send_fig(fig, self.channel_id_range)

            elif command == straferesult:
                print("Got strafe result!")

                # Create strafe run figure.
                fig, ax = self.plot.PlotStrafeRun(table)

                # Send figure to discord.
                self.bot.send_fig(fig, self.channel_id_range)

            elif command == lsograde:
                print("Got trap sheet!")

                # Send LSO grade.
                self.bot.send_lso_embed(table, self.channel_id_airboss)

                # Create trap sheet figure.
                fig, ax = self.plot.PlotTrapSheet(table)

                # Send figure to Discord.
                self.bot.send_fig(fig, self.channel_id_airboss)
                # PRECISE PLOTER HERE
                x = Plotter(table)
                fig2 = x.plot_case()
                self.bot.send_fig(fig2, self.channel_id_airboss)

            elif command == notam:
                print("Got NOTAM!")

                # Send LSO grade.
                self.bot.send_text(table, self.channel_id_notams)

            else:
                print("WARNING: Unknown command in table: {command}")
        else:
            print("WARNING: not key command in table!")
            print(table)
