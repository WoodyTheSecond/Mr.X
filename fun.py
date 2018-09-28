import discord
import asyncio
from discord.ext import commands
import urllib.request
import json


class Fun:
    def __init__(self, client):
        self.client = client

    async def is_nsfw(self, channel: discord.Channel):
        try:
            _gid = channel.server.id
        except AttributeError:
            return False
        data = await self.client.http.request(discord.http.Route('GET', '/guilds/{guild_id}/channels', guild_id=_gid))
        channeldata = [d for d in data if d['id'] == channel.id][0]
        return channeldata['nsfw']

    @commands.command(pass_context=True)
    async def pgif(self, ctx):
        if await self.is_nsfw(ctx.message.channel):
            req = urllib.request.Request("https://nekobot.xyz/api/image?type=pgif", headers={"User-Agent": "Mozilla/5.0"})
            fp = urllib.request.urlopen(req)
            mybytes = fp.read()
            message = mybytes.decode("utf8")
            fp.close()
            res = json.loads(message)
            embed = discord.Embed(
                color=discord.Color.purple()
            )
            embed.set_image(url=res["message"])

            await self.client.say(embed=embed)
        else:
            embed = discord.Embed(
                description="This is not an NSFW channel",
                color=discord.Color.red()
            )

            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def fourk(self, ctx):
        if await self.is_nsfw(ctx.message.channel):
            req = urllib.request.Request("https://nekobot.xyz/api/image?type=4k", headers={"User-Agent": "Mozilla/5.0"})
            fp = urllib.request.urlopen(req)
            mybytes = fp.read()
            message = mybytes.decode("utf8")
            fp.close()
            res = json.loads(message)
            embed = discord.Embed(
                color=discord.Color.purple()
            )
            embed.set_image(url=res["message"])

            await self.client.say(embed=embed)
        else:
            embed = discord.Embed(
                description="This is not an NSFW channel",
                color=discord.Color.red()
            )

            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def gonewild(self, ctx):
        if await self.is_nsfw(ctx.message.channel):
            req = urllib.request.Request("https://nekobot.xyz/api/image?type=gonewild", headers={"User-Agent": "Mozilla/5.0"})
            fp = urllib.request.urlopen(req)
            mybytes = fp.read()
            message = mybytes.decode("utf8")
            fp.close()
            res = json.loads(message)
            embed = discord.Embed(
                color=discord.Color.purple()
            )
            embed.set_image(url=res["message"])

            await self.client.say(embed=embed)
        else:
            embed = discord.Embed(
                description="This is not an NSFW channel",
                color=discord.Color.red()
            )

            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def pussy(self, ctx):
        if await self.is_nsfw(ctx.message.channel):
            req = urllib.request.Request("https://nekobot.xyz/api/image?type=pussy", headers={"User-Agent": "Mozilla/5.0"})
            fp = urllib.request.urlopen(req)
            mybytes = fp.read()
            message = mybytes.decode("utf8")
            fp.close()
            res = json.loads(message)
            embed = discord.Embed(
                color=discord.Color.purple()
            )
            embed.set_image(url=res["message"])

            await self.client.say(embed=embed)
        else:
            embed = discord.Embed(
                description="This is not an NSFW channel",
                color=discord.Color.red()
            )

            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def hentai(self, ctx):
        if await self.is_nsfw(ctx.message.channel):
            req = urllib.request.Request("https://nekobot.xyz/api/image?type=hentai", headers={"User-Agent": "Mozilla/5.0"})
            fp = urllib.request.urlopen(req)
            mybytes = fp.read()
            message = mybytes.decode("utf8")
            fp.close()
            res = json.loads(message)
            embed = discord.Embed(
                color=discord.Color.purple()
            )
            embed.set_image(url=res["message"])

            await self.client.say(embed=embed)
        else:
            embed = discord.Embed(
                description="This is not an NSFW channel",
                color=discord.Color.red()
            )

            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def lewdneko(self, ctx):
        if await self.is_nsfw(ctx.message.channel):
            req = urllib.request.Request("https://nekobot.xyz/api/image?type=lewdneko", headers={"User-Agent": "Mozilla/5.0"})
            fp = urllib.request.urlopen(req)
            mybytes = fp.read()
            message = mybytes.decode("utf8")
            fp.close()
            res = json.loads(message)
            embed = discord.Embed(
                color=discord.Color.purple()
            )
            embed.set_image(url=res["message"])

            await self.client.say(embed=embed)
        else:
            embed = discord.Embed(
                description="This is not an NSFW channel",
                color=discord.Color.red()
            )

            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def hanal(self, ctx):
        if await self.is_nsfw(ctx.message.channel):
            req = urllib.request.Request("https://nekobot.xyz/api/image?type=hentai_anal", headers={"User-Agent": "Mozilla/5.0"})
            fp = urllib.request.urlopen(req)
            mybytes = fp.read()
            message = mybytes.decode("utf8")
            fp.close()
            res = json.loads(message)
            embed = discord.Embed(
                color=discord.Color.purple()
            )
            embed.set_image(url=res["message"])

            await self.client.say(embed=embed)
        else:
            embed = discord.Embed(
                description="This is not an NSFW channel",
                color=discord.Color.red()
            )

            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def holo(self, ctx):
        if await self.is_nsfw(ctx.message.channel):
            req = urllib.request.Request("https://nekos.life/api/v2/img/hololewd", headers={"User-Agent": "Mozilla/5.0"})
            fp = urllib.request.urlopen(req)
            mybytes = fp.read()
            message = mybytes.decode("utf8")
            fp.close()
            res = json.loads(message)
            embed = discord.Embed(
                color=discord.Color.purple()
            )
            embed.set_image(url=res["url"])

            await self.client.say(embed=embed)
        else:
            embed = discord.Embed(
                description="This is not an NSFW channel",
                color=discord.Color.red()
            )

            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def gasm(self, ctx):
        if await self.is_nsfw(ctx.message.channel):
            req = urllib.request.Request("https://nekos.life/api/v2/img/gasm", headers={"User-Agent": "Mozilla/5.0"})
            fp = urllib.request.urlopen(req)
            mybytes = fp.read()
            message = mybytes.decode("utf8")
            fp.close()
            res = json.loads(message)
            embed = discord.Embed(
                color=discord.Color.purple()
            )
            embed.set_image(url=res["url"])

            await self.client.say(embed=embed)
        else:
            embed = discord.Embed(
                description="This is not an NSFW channel",
                color=discord.Color.red()
            )

            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def lewdkitsune(self, ctx):
        if await self.is_nsfw(ctx.message.channel):
            req = urllib.request.Request("https://nekobot.xyz/api/image?type=lewdkitsune", headers={"User-Agent": "Mozilla/5.0"})
            fp = urllib.request.urlopen(req)
            mybytes = fp.read()
            message = mybytes.decode("utf8")
            fp.close()
            res = json.loads(message)
            embed = discord.Embed(
                color=discord.Color.purple()
            )
            embed.set_image(url=res["message"])

            await self.client.say(embed=embed)
        else:
            embed = discord.Embed(
                description="This is not an NSFW channel",
                color=discord.Color.red()
            )

            await self.client.say(embed=embed)

    # @commands.command(pass_context=True)
    # async def trap(self, ctx):
    #     if await self.is_nsfw(ctx.message.channel):
    #         req = urllib.request.Request("https://api.computerfreaker.cf/v1/trap", headers={"User-Agent": "Mozilla/5.0"})
    #         fp = urllib.request.urlopen(req)
    #         mybytes = fp.read()
    #         message = mybytes.decode("utf8")
    #         fp.close()
    #         res = json.loads(message)
    #         embed = discord.Embed(
    #             color=discord.Color.purple()
    #         )
    #         embed.set_image(url=res["url"])

    #         await self.client.say(embed=embed)
    #     else:
    #         embed = discord.Embed(
    #             description="This is not an NSFW channel",
    #             color=discord.Color.red()
    #         )

    #         await self.client.say(embed=embed)

def setup(client):
    client.add_cog(Fun(client))
