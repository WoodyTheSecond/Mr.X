import discord
import asyncio
from discord.ext import commands
import urllib.request
import json
import praw
import random
import pymysql

class NSFW:
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

    def check_database(self, server, setting):
        conn = pymysql.connect(host="sql7.freesqldatabase.com",
                               user="sql7257339", password="yakm4fsd4T", db="sql7257339")
        c = conn.cursor()
        sql = "SELECT {} from `Server_Settings` WHERE serverid = {}".format(
            setting, str(server.id))
        c.execute(sql)
        conn.commit()
        data = c.fetchone()
        conn.close()
        for row in data:
            if row == 1:
                return True
            elif row == 0:
                return False
            else:
                return row

    @commands.command(pass_context=True)
    async def pgif(self, ctx):
        server = ctx.message.author.server
        nsfw_toggle = self.check_database(server, "NSFW_toggle")
        if nsfw_toggle == False:
            embed = discord.Embed(
                description="The NSFW commands is currently disabled",
                color=0xFF0000
            )

            await self.client.say(embed=embed)
            return

        if await self.is_nsfw(ctx.message.channel):
            # reddit = praw.Reddit(
            #     client_id="G9hlJ0OTkWFNhw",
            #     client_secret="Ps8h_yI1QbNGR0RUreP93_COsFE",
            #     password="RE9!bE5fCQy8BWTdNOdw77r!W9KCuJ",
            #     user_agent="Alice discord bot",
            #     username="WoodyTheSecond"
            # )
            # submissions = reddit.subreddit("porninfifteenseconds").hot()
            # post_to_pick = random.randint(1, 10)
            # for i in range(0, post_to_pick):
            #     submission = next(x for x in submissions if not x.stickied)

            # embed = discord.Embed(
            #     color=0x800080
            # )
            # embed.set_image(url=submission.url)
            # await self.client.say(embed=embed)
            req = urllib.request.Request("https://nekobot.xyz/api/image?type=pgif", headers={"User-Agent": "Mozilla/5.0"})
            fp = urllib.request.urlopen(req)
            mybytes = fp.read()
            message = mybytes.decode("utf8")
            fp.close()
            res = json.loads(message)
            embed = discord.Embed(
                color=0x800080
            )
            embed.set_image(url=res["message"])

            await self.client.say(embed=embed)
        else:
            embed = discord.Embed(
                description="This is not an NSFW channel",
                color=0xFF0000
            )

            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def fourk(self, ctx):
        server = ctx.message.author.server
        nsfw_toggle = self.check_database(server, "NSFW_toggle")
        if nsfw_toggle == False:
            embed = discord.Embed(
                description="The NSFW commands is currently disabled",
                color=0xFF0000
            )

            await self.client.say(embed=embed)
            return

        if await self.is_nsfw(ctx.message.channel):
            req = urllib.request.Request("https://nekobot.xyz/api/image?type=4k", headers={"User-Agent": "Mozilla/5.0"})
            fp = urllib.request.urlopen(req)
            mybytes = fp.read()
            message = mybytes.decode("utf8")
            fp.close()
            res = json.loads(message)
            embed = discord.Embed(
                color=0x800080
            )
            embed.set_image(url=res["message"])

            await self.client.say(embed=embed)
        else:
            embed = discord.Embed(
                description="This is not an NSFW channel",
                color=0xFF0000
            )

            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def gonewild(self, ctx):
        server = ctx.message.author.server
        nsfw_toggle = self.check_database(server, "NSFW_toggle")
        if nsfw_toggle == False:
            embed = discord.Embed(
                description="The NSFW commands is currently disabled",
                color=0xFF0000
            )

            await self.client.say(embed=embed)
            return

        if await self.is_nsfw(ctx.message.channel):
            req = urllib.request.Request("https://nekobot.xyz/api/image?type=gonewild", headers={"User-Agent": "Mozilla/5.0"})
            fp = urllib.request.urlopen(req)
            mybytes = fp.read()
            message = mybytes.decode("utf8")
            fp.close()
            res = json.loads(message)
            embed = discord.Embed(
                color=0x800080
            )
            embed.set_image(url=res["message"])

            await self.client.say(embed=embed)
        else:
            embed = discord.Embed(
                description="This is not an NSFW channel",
                color=0xFF0000
            )

            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def pussy(self, ctx):
        server = ctx.message.author.server
        nsfw_toggle = self.check_database(server, "NSFW_toggle")
        if nsfw_toggle == False:
            embed = discord.Embed(
                description="The NSFW commands is currently disabled",
                color=0xFF0000
            )

            await self.client.say(embed=embed)
            return

        if await self.is_nsfw(ctx.message.channel):
            req = urllib.request.Request("https://nekobot.xyz/api/image?type=pussy", headers={"User-Agent": "Mozilla/5.0"})
            fp = urllib.request.urlopen(req)
            mybytes = fp.read()
            message = mybytes.decode("utf8")
            fp.close()
            res = json.loads(message)
            embed = discord.Embed(
                color=0x800080
            )
            embed.set_image(url=res["message"])

            await self.client.say(embed=embed)
        else:
            embed = discord.Embed(
                description="This is not an NSFW channel",
                color=0xFF0000
            )

            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def hentai(self, ctx):
        server = ctx.message.author.server
        nsfw_toggle = self.check_database(server, "NSFW_toggle")
        if nsfw_toggle == False:
            embed = discord.Embed(
                description="The NSFW commands is currently disabled",
                color=0xFF0000
            )

            await self.client.say(embed=embed)
            return

        if await self.is_nsfw(ctx.message.channel):
            req = urllib.request.Request("https://nekobot.xyz/api/image?type=hentai", headers={"User-Agent": "Mozilla/5.0"})
            fp = urllib.request.urlopen(req)
            mybytes = fp.read()
            message = mybytes.decode("utf8")
            fp.close()
            res = json.loads(message)
            embed = discord.Embed(
                color=0x800080
            )
            embed.set_image(url=res["message"])

            await self.client.say(embed=embed)
        else:
            embed = discord.Embed(
                description="This is not an NSFW channel",
                color=0xFF0000
            )

            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def lewdneko(self, ctx):
        server = ctx.message.author.server
        nsfw_toggle = self.check_database(server, "NSFW_toggle")
        if nsfw_toggle == False:
            embed = discord.Embed(
                description="The NSFW commands is currently disabled",
                color=0xFF0000
            )

            await self.client.say(embed=embed)
            return

        if await self.is_nsfw(ctx.message.channel):
            req = urllib.request.Request("https://nekobot.xyz/api/image?type=lewdneko", headers={"User-Agent": "Mozilla/5.0"})
            fp = urllib.request.urlopen(req)
            mybytes = fp.read()
            message = mybytes.decode("utf8")
            fp.close()
            res = json.loads(message)
            embed = discord.Embed(
                color=0x800080
            )
            embed.set_image(url=res["message"])

            await self.client.say(embed=embed)
        else:
            embed = discord.Embed(
                description="This is not an NSFW channel",
                color=0xFF0000
            )

            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def hanal(self, ctx):
        server = ctx.message.author.server
        nsfw_toggle = self.check_database(server, "NSFW_toggle")
        if nsfw_toggle == False:
            embed = discord.Embed(
                description="The NSFW commands is currently disabled",
                color=0xFF0000
            )

            await self.client.say(embed=embed)
            return

        if await self.is_nsfw(ctx.message.channel):
            req = urllib.request.Request("https://nekobot.xyz/api/image?type=hentai_anal", headers={"User-Agent": "Mozilla/5.0"})
            fp = urllib.request.urlopen(req)
            mybytes = fp.read()
            message = mybytes.decode("utf8")
            fp.close()
            res = json.loads(message)
            embed = discord.Embed(
                color=0x800080
            )
            embed.set_image(url=res["message"])

            await self.client.say(embed=embed)
        else:
            embed = discord.Embed(
                description="This is not an NSFW channel",
                color=0xFF0000
            )

            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def holo(self, ctx):
        server = ctx.message.author.server
        nsfw_toggle = self.check_database(server, "NSFW_toggle")
        if nsfw_toggle == False:
            embed = discord.Embed(
                description="The NSFW commands is currently disabled",
                color=0xFF0000
            )

            await self.client.say(embed=embed)
            return

        if await self.is_nsfw(ctx.message.channel):
            req = urllib.request.Request("https://nekos.life/api/v2/img/hololewd", headers={"User-Agent": "Mozilla/5.0"})
            fp = urllib.request.urlopen(req)
            mybytes = fp.read()
            message = mybytes.decode("utf8")
            fp.close()
            res = json.loads(message)
            embed = discord.Embed(
                color=0x800080
            )
            embed.set_image(url=res["url"])

            await self.client.say(embed=embed)
        else:
            embed = discord.Embed(
                description="This is not an NSFW channel",
                color=0xFF0000
            )

            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def gasm(self, ctx):
        server = ctx.message.author.server
        nsfw_toggle = self.check_database(server, "NSFW_toggle")
        if nsfw_toggle == False:
            embed = discord.Embed(
                description="The NSFW commands is currently disabled",
                color=0xFF0000
            )

            await self.client.say(embed=embed)
            return

        if await self.is_nsfw(ctx.message.channel):
            req = urllib.request.Request("https://nekos.life/api/v2/img/gasm", headers={"User-Agent": "Mozilla/5.0"})
            fp = urllib.request.urlopen(req)
            mybytes = fp.read()
            message = mybytes.decode("utf8")
            fp.close()
            res = json.loads(message)
            embed = discord.Embed(
                color=0x800080
            )
            embed.set_image(url=res["url"])

            await self.client.say(embed=embed)
        else:
            embed = discord.Embed(
                description="This is not an NSFW channel",
                color=0xFF0000
            )

            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def lewdkitsune(self, ctx):
        server = ctx.message.author.server
        nsfw_toggle = self.check_database(server, "NSFW_toggle")
        if nsfw_toggle == False:
            embed = discord.Embed(
                description="The NSFW commands is currently disabled",
                color=0xFF0000
            )

            await self.client.say(embed=embed)
            return

        if await self.is_nsfw(ctx.message.channel):
            req = urllib.request.Request("https://nekobot.xyz/api/image?type=lewdkitsune", headers={"User-Agent": "Mozilla/5.0"})
            fp = urllib.request.urlopen(req)
            mybytes = fp.read()
            message = mybytes.decode("utf8")
            fp.close()
            res = json.loads(message)
            embed = discord.Embed(
                color=0x800080
            )
            embed.set_image(url=res["message"])

            await self.client.say(embed=embed)
        else:
            embed = discord.Embed(
                description="This is not an NSFW channel",
                color=0xFF0000
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
    #             color=0x800080
    #         )
    #         embed.set_image(url=res["url"])

    #         await self.client.say(embed=embed)
    #     else:
    #         embed = discord.Embed(
    #             description="This is not an NSFW channel",
    #             color=0xFF0000
    #         )

    #         await self.client.say(embed=embed)

def setup(client):
    client.add_cog(NSFW(client))
