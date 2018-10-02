import discord
import asyncio
import time
from discord.ext.commands import Bot
from discord.ext import commands
players = {}
queues = {}
class Economy:
    def __init__(self, client):
        self.client = client

    


def setup(client):
    client.add_cog(Economy(client))
