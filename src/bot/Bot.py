import os.path
import discord
from discord.ext import commands
import threading
import matplotlib.pyplot as plt
import io
from root import ROOT_DIR
from src.precise_plot.modules.Plotter import Plotter
from src.precise_plot.test_data.test_table import test_data
from src.utils.utils import get_val

class Bot(commands.Bot):
    """
    API class wrapper for Discord based on discord.py.
    """

    def __init__(self, token: str, channel_id: int, command_prefix="$", image_path=os.path.join(ROOT_DIR, "assets"),
                 debug_level: int = 0):

        # Intents.
        intents = discord.Intents.all()

        # Init discord.Client superclass.
        super().__init__(command_prefix, intents=intents)

        self.debug_level = debug_level
        # Set config parameters:

        self.token = str(token)
        self.channel_id = int(channel_id)
        self.image_path = image_path

        self.callback_start_func = None
        self.callback_start_argv = None
        self.callback_start_kwarg = None

        self.channel = None

        # Init bot commands.
        self._init_commands()

    def callback(self, Func, *argv, **kwargs):
        """Callback function called at start."""
        self.callback_start_func = Func
        self.callback_start_argv = argv
        self.callback_start_kwarg = kwargs

    async def on_ready(self):
        """
        Event when connected to server.
        """
        # Get channel.
        try:
            self.channel = self.get_channel(self.channel_id)
        except:
            print(f"ERROR: Could not get channel with ID={self.channel_id}")

        # Info that bot is online and ready.

        print('Connected as {0.name} [ID: {0.id}]'.format(self.user))

        # Set message to channel.
        await self.send_message("DCS-Bot reporting for duty!", self.channel_id)

    async def on_disconnect(self):
        """
        Called when the client has disconnected from Discord, or a connection attempt to Discord has failed. This could happen either through the internet being disconnected, 
        explicit calls to close, or Discord terminating the connection one way or the other.
        """
        # Get channel.
        try:
            self.channel = self.get_channel(self.channel_id)
        except:
            print(f"ERROR: Could not get channel with ID={self.channel_id}")

        # Info that bot is online and ready.
        print('Connected as {0.name} [ID: {0.id}]'.format(self.user))

    def start_bot(self, Threaded=False):
        """
        Connect to server using the token.
        """
        if Threaded:
            print("Starting threaded discord bot!")
            discordThread = threading.Thread(target=self.start_bot, args=(False,))
            discordThread.start()
        else:
            print(f"Starting Bot Client with Token {self.token[0:5]}...")
            self.run(self.token)

    async def send_message(self, text: str, channel_id: int):
        """
        Async send text message to channel.
        """
        channel = self.get_channel(channel_id)
        await channel.send(text)

    def send_text(self, text: str, channel_id: int):
        """
        Send text message to channel using loop.create_task().
        """
        channel = self.get_channel(channel_id)
        try:
            self.loop.create_task(channel.send(text))
        except:
            print(f"ERROR: Could not send text! {text}")

    def send_discord_file(self, discord_file: discord.File, channel_id: int, embed: discord.Embed = None):
        """
        Send discord file.
        """
        channel = self.get_channel(channel_id)
        if embed:
            self.loop.create_task(channel.send(file=discord_file, embed=embed))
        else:
            self.loop.create_task(channel.send(file=discord_file))

    def send_io(self, data_stream: io.BytesIO, channel_id: int):
        """
        Send text message to channel using loop.create_task().
        """
        # Rewind stream.
        data_stream.seek(0)

        # Create data stream.
        file = discord.File(data_stream, filename="bot.png", spoiler=False)

        # Send discord file.
        self.send_discord_file(file, channel_id)

    def send_fig(self, fig, channel_id: int):
        """
        Set matplotlib fig object.
        """

        # Create io.
        data_stream = io.BytesIO()

        # Seve figure in data stream.
        fig.savefig(data_stream, format='png')

        # Close figure.
        plt.close(fig)

        # Send data stream.
        self.send_io(data_stream, channel_id)

    def send_lso_embed(self, result, channel_id: int):

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

    def _init_commands(self):
        """Init commands."""

        @self.command(aliases=['testplots'])
        async def TestPlots(ctx: commands.Context):
            self._test_plots(ctx.channel.id)

        @self.command(aliases=['testjtfplot'])
        async def TestJtfPlot(ctx: commands.Context):
            self._test_traps(ctx.channel.id, True)

        @self.command(aliases=['teststrafe'])
        async def TestStrafe(ctx: commands.Context):
            self._test_strafe(ctx.channel.id)

        @self.command(aliases=['testbomb'])
        async def TestBomb(ctx: commands.Context):
            self._test_bomb(ctx.channel.id)

    def _test_traps(self, channel_id, sci_only=False):
        if not sci_only:
            from src.utils.tests import test_trap, get_result_trap
            from src.plot.Plot import Plot

            # Init FunkPlot.
            funkyplot = Plot()

            # Trap sheet files.
            trapfiles = [
                os.path.join(ROOT_DIR, "tests", "Trapsheet-FA-18C_hornet-001.csv"),
                os.path.join(ROOT_DIR, "tests", "Trapsheet-FA-18C_hornet-002.csv"),
                os.path.join(ROOT_DIR, "tests", "SH_unicorn_AIRBOSS-trapsheet-Yoda_FA-18C_hornet-0001.csv"),
                os.path.join(ROOT_DIR, "tests", "Trapsheet-AV8B_Tarawa-001.csv")]

            for trapfile in trapfiles:
                # Get result from trap file.
                result = get_result_trap(trapfile)

                # Test LSO embed.
                self.send_lso_embed(result, channel_id)

                # Test trap.
                f1, a1 = test_trap(funkyplot, trapfile)
                self.send_fig(f1, channel_id)

        plotter = Plotter(test_data)
        fig = plotter.plot_case1(file_name="test")
        self.send_fig(fig, channel_id)

    def _test_strafe(self, channel_id):
        from src.utils.tests import test_strafe
        from src.plot.Plot import Plot

        # Init FunkPlot.
        funkyplot = Plot()

        # Test strafe.
        fig, ax = test_strafe(funkyplot)
        self.send_fig(fig, channel_id)

    def _test_bomb(self, channel_id):
        from src.utils.tests import test_bomb
        from src.plot.Plot import Plot

        # Init FunkPlot.
        funkyplot = Plot()

        # Test strafe.
        fig, ax = test_bomb(funkyplot)
        self.send_fig(fig, channel_id)

    def _test_plots(self, channel_id):

        # Debug info.
        print("Testing Plots...")

        # Test trapsheet.
        self._test_traps(channel_id)

        # Test strafe.
        self._test_strafe(channel_id)

        # Test bomb.
        self._test_bomb(channel_id)
