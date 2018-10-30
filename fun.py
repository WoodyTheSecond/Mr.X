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

class Fun:
    def __init__(self, client):
        self.client = client

    def check_setting(self, server, setting):
        settingspath = "servers/{}/settings.json".format(server.id)
        if not setting in open(settingspath, "r").read():
            print("No such setting found")
            return None

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
        if discord.utils.get(mod.roles, name=t_modrole) or mod.server_permissions.administrator or mod.id == '164068466129633280' or mod.id == '142002197998206976' or discord.utils.get(mod.roles, name=t_modrole):
            return True
        else:
            return False

    def is_admin_or_perms(self, server, mod):
        t_adminrole = self.check_setting(server, "Admin_Role")
        if discord.utils.get(mod.roles, name=t_adminrole) or mod.server_permissions.administrator or mod.id == '164068466129633280' or mod.id == '142002197998206976':
            return True
        else:
            return False

    @commands.command(pass_context=True)
    async def meme(self, ctx):
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
    async def slap(self, ctx, user: discord.Member = None):
        author = ctx.message.author
        server = author.server
        fun_toggle = self.check_setting(server, "FunToggle")
        if author.id != "164068466129633280" and author.id != "142002197998206976" and author.id != "457516809940107264":
            if fun_toggle == False:
                embed = discord.Embed(
                    description="The fun commands is currently disabled",
                    color=0xFF0000
                )

                await self.client.say(embed=embed)
                return

        ints = randint(1, 2)
        if user == None:
            embed = discord.Embed(
                description="You have not tagged any user",
                color=0xFF0000
            )
            await self.client.say(embed=embed)
            return

        embed = discord.Embed(
            description="{} slaps {}".format(author.mention, user.mention),
            color=0xFF0000
        )
        if ints == 1:
            embed.set_image(url="https://i.imgur.com/srwlZ8s.gif")
        elif ints == 2:
            embed.set_image(url="https://i.imgur.com/UFn8Huh.gif")

        await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def splat(self, ctx, user: discord.Member = None):
        author = ctx.message.author
        server = author.server
        fun_toggle = self.check_setting(server, "FunToggle")
        if author.id != "164068466129633280" and author.id != "142002197998206976" and author.id != "457516809940107264":
            if fun_toggle == False:
                embed = discord.Embed(
                    description="The fun commands is currently disabled",
                    color=0xFF0000
                )

                await self.client.say(embed=embed)
                return

        if user == None:
            embed = discord.Embed(
                description="You have not tagged any user",
                color=0xFF0000
            )
            await self.client.say(embed=embed)
            return
                
        embed = discord.Embed(
            description="{} totally annihilates {} with a simple ***SPLAT***".format(author.mention, user.mention),
            color=0xFF0000
        )
        embed.set_image(url="https://i.imgur.com/GnuQkQZ.gif")

        await self.client.say(embed=embed)
    
def setup(client):
    client.add_cog(Fun(client))
