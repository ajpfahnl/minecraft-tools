#!/usr/bin/env python3

from globals import *
from minecraft_server import MinecraftServerAdmin as MCSA
from client import SudoMinecraftClient

def main():
    mcsa = MCSA()
    client = SudoMinecraftClient(mcsa)
    client.run(TOKEN_SUDO_MINECRAFT)

if __name__ == "__main__":
    main()
