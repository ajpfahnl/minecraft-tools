import subprocess
import asyncio
import requests
import shlex
import json
import socket
from globals import *

class MinecraftServerAdmin():
    run_cmd_default = "/usr/libexec/java_home -v 16 --exec java -Xms4G -Xmx8G -jar server.jar nogui"

    def __init__(self):
        self.is_async = True # legacy
        self.server_process = None
        self.ipl = self.get_localIP() # local ip
        self.ipg = self.get_publicIP() # public ip

    # run server
    def start_minecraft_server_old(self):
        cmd = shlex.split(self.run_cmd_default)
        
        p = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            cwd=SERVER_DIRECTORY,
            )
        self.server_process = p
        return p
    
    async def start_minecraft_server(self):
        cmd = shlex.split(self.run_cmd_default)
        
        p = await asyncio.create_subprocess_exec(
            *cmd,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
            text=False, # required
            cwd=SERVER_DIRECTORY,
            )
        self.server_process = p
        return p

    # Server properties functions
    def get_server_properties(self):
        server_properties_path = os.path.join(SERVER_DIRECTORY, "server.properties")
        with open(server_properties_path, 'r') as f:
            properties = {}
            for line in f:
                if line.startswith("#"):
                    continue
                else:
                    p, v = line.strip().split('=')
                    properties[p] = v
        return properties

    def format_server_properties(self, properties):
        string = []
        for p, v in properties.items():
            string.append(f"**{p}**: {v}")
        return "\n".join(string)

    # Whitelist functions
    def get_whitelist(self):
        whitelist_path = os.path.join(SERVER_DIRECTORY, "whitelist.json")
        with open(whitelist_path, 'r') as f:
            json_data = json.loads(f)
        return json_data

    # IP functions
    def get_publicIP(self):
        response = requests.get("http://checkip.amazonaws.com")
        self.ipg = response.text.strip()
        return self.ipg

    def get_localIP(self):
        self.ipl = socket.gethostbyname_ex(socket.gethostname())
        return self.ipl[2][-1]