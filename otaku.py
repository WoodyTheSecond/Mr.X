import discord
import asyncio
from discord.ext import commands
import urllib.request
import json
import praw
import random
import pymysql
import os
from random import randint

class Otaku:
    def __init__(self, client):
        self.client = client
        
    def check_setting(self, server, setting):
        settingspath = "servers/{}/settings.json".format(server.id)
        with open(settingspath, "r") as f:
            json_data = json.load(f)
            if json_data[setting] == 1:
                return True
            elif json_data[setting] == 0:
                return False
            else:
                return json_data[setting]
    
    def is_allowed_by_hierarchy(self, server, mod, user):
        setting = self.check_setting(server, "Ignore_Hierarchy")
        toggle = setting
        if toggle == False:
            if mod.top_role.position > user.top_role.position:
                return False
            else:
                return True
        else:
            return True

    def is_mod_or_perms(self, server, mod):
        t_modrole = self.check_setting(server, "Mod_Role")
        if discord.utils.get(mod.roles, name=t_modrole) or mod.server_permissions.administrator or mod.id == "164068466129633280" or mod.id == "142002197998206976" or discord.utils.get(mod.roles, name=t_modrole):
            return True
        else:
            return False

    def is_admin_or_perms(self, server, mod):
        t_adminrole = self.check_setting(server, "Admin_Role")
        if discord.utils.get(mod.roles, name=t_adminrole) or mod.server_permissions.administrator or mod.id == "164068466129633280" or mod.id == "142002197998206976":
            return True
        else:
            return False

    @commands.command(pass_context=True)
    async def shiki(self, ctx):
        server = ctx.message.author.server
        author = ctx.message.author
        fun_toggle = self.check_setting(server, "FunToggle")
        if author.id != "164068466129633280" and author.id != "142002197998206976" and author.id != "457516809940107264":
            if fun_toggle == False:
                embed = discord.Embed(
                    description="The fun commands is currently disabled",
                    color=0xFF0000
                )

                await self.client.say(embed=embed)
                return
        embed = discord.Embed(
            title = "Shiki(TMNS)",
            description = "**The SisCon King**",
            color = 0x00FF00
        )
        embed.add_field(name="Youtube", value="https://www.youtube.com/channel/UC0ETiVE1OVi1vazCOPsFNBQ", inline=False)
        embed.add_field(name="Soundcloud", value="https://soundcloud.com/thetmns", inline=False)
        embed.set_image(url="https://i.imgur.com/Qp1sB7o.jpg")
        await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def hdude(self, ctx):
        server = ctx.message.author.server
        author = ctx.message.author
        fun_toggle = self.check_setting(server, "FunToggle")
        if author.id != "164068466129633280" and author.id != "142002197998206976" and author.id != "457516809940107264":
            if fun_toggle == False:
                embed = discord.Embed(
                    description="The fun commands is currently disabled",
                    color=0xFF0000
                )

                await self.client.say(embed=embed)
                return

        embed = discord.Embed(
            title = "Hentai Dude",
            description = "**Anime Nigga Life**",
            color = 0x00FF00
        )
        embed.add_field(name="Youtube", value="https://www.youtube.com/channel/UCyFmOVm5PjEq0pcxtWVZKEw", inline=False)
        embed.add_field(name="Soundcloud", value="https://soundcloud.com/kore-wa-hentais", inline=False)
        embed.set_image(url="https://i.imgur.com/n3w5u6Y.jpg")
        await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def imotou(self, ctx):
        server = ctx.message.author.server
        author = ctx.message.author
        fun_toggle = self.check_setting(server, "FunToggle")
        if author.id != "164068466129633280" and author.id != "142002197998206976" and author.id != "457516809940107264":
            if fun_toggle == False:
                embed = discord.Embed(
                    description="The fun commands is currently disabled",
                    color=0xFF0000
                )

                await self.client.say(embed=embed)
                return

        reddit = praw.Reddit(
            client_id="G9hlJ0OTkWFNhw",
            client_secret="Ps8h_yI1QbNGR0RUreP93_COsFE",
            password="RE9!bE5fCQy8BWTdNOdw77r!W9KCuJ",
            user_agent="Alice discord bot",
            username="WoodyTheSecond"
        )
        memes_submissions = reddit.subreddit("imouto").hot()
        post_to_pick = random.randint(1, 50)
        for i in range(0, post_to_pick):
            submission = next(x for x in memes_submissions if not x.stickied)

        embed = discord.Embed(
            color=0x00FF00
        )
        embed.set_image(url=submission.url)
        embed.set_footer(text="With love from C0mpl3X")
        await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def oniisong(self, ctx):
        server = ctx.message.author.server
        author = ctx.message.author
        fun_toggle = self.check_setting(server, "FunToggle")
        if author.id != "164068466129633280" and author.id != "142002197998206976" and author.id != "457516809940107264":
            if fun_toggle == False:
                embed = discord.Embed(
                    description="The fun commands is currently disabled",
                    color=0xFF0000
                )

                await self.client.say(embed=embed)
                return
        int = randint(1, 6)
        if int == 1:
            embed = discord.Embed(
                title = "Every Loli's Onii Chan (Prod. Killing Spree)",
                description = "https://www.youtube.com/watch?v=j6phcEtXMSU",
                color = 0x00FF00
            )
            await self.client.say(embed=embed)
        elif int == 2:
            embed = discord.Embed(
                title = "Shiki - Who Are You? Ft. Doll.ia (Official Audio)",
                description = "https://www.youtube.com/watch?v=zgTBB6YpxWA",
                color = 0x00FF00
            )
            await self.client.say(embed=embed)
        elif int == 3:
            embed = discord.Embed(
                title = "Hentai Dude - Shoujo Contract",
                description = "https://www.youtube.com/watch?v=Y4HmUbdFE2M",
                color = 0x00FF00
            )
            await self.client.say(embed=embed)
        elif int == 4:
            embed = discord.Embed(
                title = "Shiki(TMNS) - Deviant (ft. Hentai Dude, prod. Killing Spree)",
                description = "https://www.youtube.com/watch?v=id24KyWkZ58",
                color = 0x00FF00
            )
            await self.client.say(embed=embed)
        elif int == 5:
            embed = discord.Embed(
                title = "Shiki(TMNS) - Senpai [MajorLeagueWobs Remix]",
                description = "https://www.youtube.com/watch?v=jQyqrmoYUdY",
                color = 0x00FF00
            )
            await self.client.say(embed=embed)
        elif int == 6:
            embed = discord.Embed(
                title = "My Kawaii Imouto (Prod. By Killing Spree)",
                description = "https://www.youtube.com/watch?v=I52qgMkcW3k",
                color = 0x00FF00
            )
            embed.set_footer(text="C0mpl3X's Favorite")
            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def loli(self, ctx):
        server = ctx.message.author.server
        author = ctx.message.author
        fun_toggle = self.check_setting(server, "FunToggle")
        if author.id != "164068466129633280" and author.id != "142002197998206976" and author.id != "457516809940107264":
            if fun_toggle == False:
                embed = discord.Embed(
                    description="The fun commands is currently disabled",
                    color=0xFF0000
                )

                await self.client.say(embed=embed)
                return

        reddit = praw.Reddit(
            client_id="G9hlJ0OTkWFNhw",
            client_secret="Ps8h_yI1QbNGR0RUreP93_COsFE",
            password="RE9!bE5fCQy8BWTdNOdw77r!W9KCuJ",
            user_agent="Alice discord bot",
            username="WoodyTheSecond"
        )
        memes_submissions = reddit.subreddit("loliconsunite").hot()
        post_to_pick = random.randint(1, 50)
        for i in range(0, post_to_pick):
            submission = next(x for x in memes_submissions if not x.stickied)

        embed = discord.Embed(
            color=0x00FF00
        )
        embed.set_image(url=submission.url)
        embed.set_footer(text="With love from C0mpl3X, the King of Loli's")
        await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def neko(self, ctx):
        server = ctx.message.author.server
        author = ctx.message.author
        fun_toggle = self.check_setting(server, "FunToggle")
        if author.id != "164068466129633280" and author.id != "142002197998206976" and author.id != "457516809940107264":
            if fun_toggle == False:
                embed = discord.Embed(
                    description="The fun commands is currently disabled",
                    color=0xFF0000
                )

                await self.client.say(embed=embed)
                return

        reddit = praw.Reddit(
            client_id="G9hlJ0OTkWFNhw",
            client_secret="Ps8h_yI1QbNGR0RUreP93_COsFE",
            password="RE9!bE5fCQy8BWTdNOdw77r!W9KCuJ",
            user_agent="Alice discord bot",
            username="WoodyTheSecond"
        )
        memes_submissions = reddit.subreddit("nekogirls").hot()
        post_to_pick = random.randint(1, 50)
        for i in range(0, post_to_pick):
            submission = next(x for x in memes_submissions if not x.stickied)

        embed = discord.Embed(
            color=0x00FF00
        )
        embed.set_image(url=submission.url)
        embed.set_footer(text="With love from C0mpl3X, the King of Loli's")
        await self.client.say(embed=embed)


    @commands.command(pass_context=True)
    async def catgirl(self, ctx):
        server = ctx.message.author.server
        author = ctx.message.author
        fun_toggle = self.check_setting(server, "FunToggle")
        if author.id != "164068466129633280" and author.id != "142002197998206976" and author.id != "457516809940107264":
            if fun_toggle == False:
                embed = discord.Embed(
                    description="The fun commands is currently disabled",
                    color=0xFF0000
                )

                await self.client.say(embed=embed)
                return

        await self.client.say("https://catgirlcare.org/")

    
def setup(client):
    client.add_cog(Otaku(client))