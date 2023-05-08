import time
import discord
from discord.ext import commands
import threading
import matplotlib.pyplot as plt
import io
from src.lib.ConfigDiscord import ConfigDiscord


class Bot(commands.Bot):
    def __init__(self, config: ConfigDiscord, command_prefix="$"):
        intents = discord.Intents.all()
        super().__init__(command_prefix, intents=intents)

        self.token = config.token
        self.channel_id = int(config.channel_id_main)

        self.callback_start_func = None
        self.callback_start_argv = None
        self.callback_start_kwarg = None

        self.channel = None

        # Init bot commands.
        # self._init_commands()

    # def callback(self, Func, *argv, **kwargs):
    #     self.callback_start_func = Func
    #     self.callback_start_argv = argv
    #     self.callback_start_kwarg = kwargs

    async def on_ready(self):
        async def send_message(text: str, channel_id: int):
            """
            Async send text message to channel.
            """
            channel = self.get_channel(channel_id)
            await channel.send(text)
        self.channel = self.get_channel(self.channel_id)
        print('Connected as {0.name} [ID: {0.id}]'.format(self.user))
        await send_message("DCS-Bot reporting!", self.channel_id)

    async def on_disconnect(self):
        reconnect = True
        while reconnect:
            try:
                self.channel = self.get_channel(self.channel_id)
                reconnect = False
                print('RE-Connected as {0.name} [ID: {0.id}]'.format(self.user))
            except:
                print(f"ERROR: Could not get channel with ID={self.channel_id}")
                time.sleep(10)

    def start_bot(self, threaded=False):
        if threaded:
            print("Starting threaded discord bot!")
            DiscordThread = threading.Thread(target=self.start_bot, args=(False,))
            DiscordThread.start()
        else:
            print(f"Starting Bot Client with Token {self.token[0:5]}...")
            self.run(self.token)

    def send_text(self, text: str, channel_id: int):
        channel = self.get_channel(channel_id)
        try:
                self.loop.create_task(channel.send(text))
        except:
            print(f"ERROR: Could not send text! {text}")

    def send_discord_file(self, discord_file: discord.File, channel_id: int, embed: discord.Embed = None):
        channel = self.get_channel(channel_id)
        if embed:
            self.loop.create_task(channel.send(file=discord_file, embed=embed))
        else:
            self.loop.create_task(channel.send(file=discord_file))

    def send_fig(self, fig, channel_id: int):
        def send_io(data_stream: io.BytesIO, channel_id: int):
            data_stream.seek(0)
            file = discord.File(data_stream, filename="bot.png", spoiler=False)
            self.send_discord_file(file, channel_id)

        data_stream = io.BytesIO()
        fig.savefig(data_stream, format='png')
        plt.close(fig)
        send_io(data_stream, channel_id)

    # def _init_commands(self):
    #     """Init commands."""

        # @self.command(aliases=['testplots'])
        # async def TestPlots(ctx: commands.Context):
        #     self._test_plots(ctx.channel.id)
