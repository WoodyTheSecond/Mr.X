import discord
import asyncio
from discord.ext import commands
import urllib.request
import json
import praw
import random
import pymysql
import os

class Fun:
    def __init__(self, client):
        self.client = client
        
    def check_database(self, server, setting):
        conn = pymysql.connect(host="sql7.freesqldatabase.com", user="sql7257339", password="yakm4fsd4T", db="sql7257339")
        c = conn.cursor()
        sql = "SELECT {} from `Server_Settings` WHERE serverid = {}".format(setting, str(server.id))
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
    
    def is_allowed_by_hierarchy(self, server, mod, user):
        setting = self.check_database(server, "Ignore_Hierarchy")
        toggle = setting
        if toggle == False:
            if mod.top_role.position > user.top_role.position:
                return False
            else:
                return True
        else:
            return True

    def is_mod_or_perms(self, server, mod):
        t_modrole = self.check_database(server, "Mod_Role")
        if discord.utils.get(mod.roles, name=t_modrole) or mod.server_permissions.administrator or mod.id == '164068466129633280' or mod.id == '142002197998206976' or discord.utils.get(mod.roles, name=t_modrole):
            return True
        else:
            return False

    def is_admin_or_perms(self, server, mod):
        t_adminrole = self.check_database(server, "Admin_Role")
        if discord.utils.get(mod.roles, name=t_adminrole) or mod.server_permissions.administrator or mod.id == '164068466129633280' or mod.id == '142002197998206976':
            return True
        else:
            return False

    @commands.command(pass_context=True)
    async def meme(self, ctx):
        server = ctx.message.author.server
        author = ctx.message.author
        fun_toggle = self.check_database(server, "FunToggle")
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
        memes_submissions = reddit.subreddit("memes").hot()
        post_to_pick = random.randint(1, 50)
        for i in range(0, post_to_pick):
            submission = next(x for x in memes_submissions if not x.stickied)

        embed = discord.Embed(
            color=0x00FF00
        )
        embed.set_image(url=submission.url)
        await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def loli(self, ctx):
        server = ctx.message.author.server
        author = ctx.message.author
        fun_toggle = self.check_database(server, "FunToggle")
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
        await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def catgirl(self, ctx):
        server = ctx.message.author.server
        author = ctx.message.author
        fun_toggle = self.check_database(server, "FunToggle")
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
    client.add_cog(Fun(client))
