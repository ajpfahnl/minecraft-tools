#!/usr/bin/env python3

from globals import *
from minecraft_server import MinecraftServerAdmin as MCSA
from client import SudoMinecraftClient
import logging

def main():
    # initiate minecraft server class
    mcsa = MCSA()

    # initiate logging
    discord_logger = logging.getLogger('discord')
    discord_logger.setLevel(logging.DEBUG)
    discord_handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    discord_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    discord_logger.addHandler(discord_handler)

    # initiate and run client    
    client = SudoMinecraftClient(mcsa)
    client.run(TOKEN_SUDO_MINECRAFT)

if __name__ == "__main__":
    main()
