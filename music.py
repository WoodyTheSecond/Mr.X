import discord
import asyncio
import time
import youtube_dl
from discord.ext.commands import Bot
from discord.ext import commands
players = {}
queues = {}
class Music:
    def __init__(self, client):
        self.client = client

    def check_queue(self, id):
        if queues[id] != []:
            player = queues[id].pop(0)
            players[id] = player
            player.start()

    @commands.command(pass_context=True)
    async def join(self, ctx):
        channel = ctx.message.author.voice.voice_channel
        await self.client.join_voice_channel(channel)

    @commands.command(pass_context=True)
    async def play(self, ctx, url):
        server = ctx.message.server
        voice_client = self.client.voice_client_in(server.id)
        player = await voice_client.create_ytdl_player(url, after=lambda: self.check_queue(server.id))
        players[server.id] = player
        player.start()

    @commands.command(pass_context=True)
    async def leave(self, ctx):
        server = ctx.message.server
        voice_client = self.client.voice_client_in(server.id)
        await voice_client.disconnect()

    @commands.command(pass_context=True)
    async def pause(self, ctx):
        id = ctx.message.server.id
        players[id].pause()

    @commands.command(pass_context=True)
    async def stop(self, ctx):
        id = ctx.message.server.id
        players[id].stop()


    @commands.command(pass_context=True)
    async def resume(self, ctx):
        id = ctx.message.server.id
        players[id].resume()

    @commands.command(pass_context=True)
    async def queue(self, ctx, url):
        server = ctx.message.server
        voice_client = self.client.voice_client_in(server.id)
        player = await voice_client.create_ytdl_player(url)

        if server.id in queues:
            queues[server.id].append(player)
        else:
            queues[server.id] = [player]
        await self.client.say('Video queued.')


def setup(client):
    client.add_cog(Music(client))
