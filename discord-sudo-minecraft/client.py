import asyncio
import discord
from globals import *
from minecraft_server import MinecraftServerAdmin as MCSA

class SudoMinecraftClient(discord.Client):
    options = {
        # unique key: primary command followed by alternates, meaning
        "help": (["$help", "$h"], "Displays this help message."),
        "ipg": (["$ip"], "Sends the current public IP of the Minecraft server."),
        "ipl": (["$ipl"], "Sends the current local IP of the Minecraft server."),
        "sp": (["$server properties", "$sp"], "Lists the current server properties."),
        "run": (["$run", "$r"], "Run the Minecraft server."),
        "stop": (["$stop"], "Stop the Minecraft server."),
        "msg": (["$message", "$msg", "$m"], "Message the server. Format: `$m <message>`"),
    }
    
    def __init__(self, mcsa: MCSA):
        super().__init__()
        self.FIRST_LOGIN = False        
        self.mcsa = mcsa
        self.default_channel = None

    def set_default_channel(self):
        for channel in self.get_all_channels():
            if channel.name == COMMUNICATION_CHANNEL:
                self.default_channel = channel
                break
        else:
            raise RuntimeError(f"Channel `{COMMUNICATION_CHANNEL}` does not exist")

    def format_options(self, options):
        string = ["__**Help**__", "Source code can be found at <https://github.com/ajpfahnl/minecraft-tools/tree/main/discord-sudo-minecraft>"]
        for l, help_str in options.values():
            cmd_str = "` | `".join(l)
            cmd_str = "".join(["`", cmd_str, "`"])
            string.append(f"**Command**: {cmd_str}:\n\t{help_str}")
        return "\n".join(string)

    async def send_server_logs(self, channel):
        while True:
            line = await self.mcsa.server_process.stdout.readline()
            if self.mcsa.server_process.stdout.at_eof():
                return
            line = line.decode()
            await channel.send(line.rstrip())

    def check_server_running(self):
        running = True
        if self.mcsa.server_process is None:
            running = False
        elif self.mcsa.server_process.returncode is not None:
            running = False
        return running

    async def on_ready(self):
        if self.FIRST_LOGIN == True:
            return
        self.FIRST_LOGIN = True
        self.set_default_channel()
        print(f"Logged in as {self.user}")
        await self.default_channel.send(
            "**I'm logged in!**\n" \
            "Minecraft server is ready to run.\n" \
            "Type `$help` for a list of commands."
            )

    async def on_message(self, message):
        if message.author == self.user:
            return

        msg = message.content.strip().lower()

        '''
        help
        '''
        if msg in self.options["help"][0]:
            opt_string = self.format_options(self.options)
            await message.channel.send(opt_string)

        '''
        ip
        '''
        if msg in self.options["ipg"][0]:
            ip = self.mcsa.get_publicIP()
            await message.channel.send(ip)
        
        if msg in self.options["ipl"][0]:
            ip = self.mcsa.get_localIP()
            await message.channel.send(ip)

        '''
        server properties
        '''
        if msg in self.options["sp"][0]:
            properties = self.mcsa.get_server_properties()
            prop_str = self.mcsa.format_server_properties(properties)
            await message.channel.send(prop_str)

        '''
        run Minecraft
        '''
        if msg in self.options["run"][0]:
            print("[ATTEMPT] Server start")
            p = await self.mcsa.start_minecraft_server()
            print("[COMPLETE] Server start")
            task_print = asyncio.create_task(self.send_server_logs(message.channel))
            print("[INFO] Print task started")
            await task_print
            await p.wait()
        
        '''
        stop Minecraft server
        '''
        if msg in self.options["stop"][0]:
            print("[ATTEMPT] Stop server")
            p = self.mcsa.server_process
            if not self.check_server_running():
                print("[ERROR] No server instance running")
                await message.channel.send("No server instance running.")
                return
            try: 
                p.terminate()
            except ProcessLookupError:
                print("[ERROR] Attempted to stop process already stopped")
            await p.wait()
            print("[COMPLETE] Stop server")
            await message.channel.send("Server stopped.")
        
        '''
        send message to Minecraft server
        '''
        msg_list = message.content.strip().split()
        if msg_list[0] in self.options["msg"][0]:
            p = self.mcsa.server_process
            if not self.check_server_running():
                print("[ERROR] No server instance running")
                await message.channel.send("No server instance running.")
                return
            client_to_server_msg = " ".join(msg_list[1:])
            print(f"[ATTEMPT] Send message to server by user {message.author}:\n\t>{client_to_server_msg}")
            client_to_server_msg = client_to_server_msg + "\n"
            p.stdin.write(client_to_server_msg.encode())
            await p.stdin.drain()
            print(f"[COMPLETE] Send message to server")
