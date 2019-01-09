import discord
import asyncio
from discord.ext import commands
import urllib.request
import json
import random
import pymysql
import os

class Marriage:
    def __init__(self, client):
        self.client = client

    def is_owner(self, user):
        if user.id == "164068466129633280" or user.id == "142002197998206976" or user.id == "457516809940107264":
            return True
        else:
            return False

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

    @commands.command(pass_context=True)
    async def marriage(self, ctx, user: discord.Member = None):
        author = ctx.message.author
        server = author.server
        marriage_toggle = self.check_setting(server, "Marriage_Toggle")
        if marriage_toggle == False:
            embed = discord.Embed(
                description="Marriage is currently disabled",
                color=0xFF0000
            )
            
            await self.client.say(embed=embed)
            return

        conn = pymysql.connect(host="sql7.freesqldatabase.com", user="sql7273467", password="ihireg57sU", db="sql7273467")
        c = conn.cursor()
        if user == None:
            sql = "SELECT * FROM `Marriage_Table` WHERE user1 = '{}' OR user2 = '{}'".format(str(author.id), str(author.id))
            c.execute(sql)
            conn.commit()
            data = c.fetchall()
            if len(data) >= 1:
                for d in data:
                    user1 = d[1]
                    user2 = d[2]
                if user1 == str(author.id):
                    married_to = int(user2)
                else:
                    married_to = int(user1)

                embed = discord.Embed(
                    description="You are married to <@{}>".format(married_to),
                    color=0xFF0000
                )
                embed.set_image(url="https://cdn.pixabay.com/photo/2015/12/11/17/28/heart-1088487_960_720.png")
                await self.client.say(embed=embed)

            else:
                if author.id == "164068466129633280":
                    embed = discord.Embed(
                        description="You are married to **Charlotte Izoard**",
                        color=0xFF0000
                    )
                    embed.set_image(url="https://i.imgur.com/G7oJSjE.jpg")
                    await self.client.say(embed=embed)
                    return
                elif author.id == "142002197998206976":
                    embed = discord.Embed(
                        description="You are married to **Yukana Yame**",
                        color=0xFF0000
                    )
                    embed.set_image(url="https://i.imgur.com/MEldWsb.jpg")
                    await self.client.say(embed=embed)
                    return
                embed = discord.Embed(
                    description="You are not married",
                    color=0xFF0000
                )

                await self.client.say(embed=embed)
            conn.close()
        else:
            sql = "SELECT * FROM `Marriage_Table` WHERE user1 = '{}' OR user2 = '{}'".format(str(user.id), str(user.id))
            c.execute(sql)
            conn.commit()
            data = c.fetchall()
            if len(data) >= 1:
                for d in data:
                    user1 = d[1]
                    user2 = d[2]
                if user1 == str(user.id):
                    married_to = int(user2)
                else:
                    married_to = int(user1)
                embed = discord.Embed(
                    description="{} is married to <@{}>".format(user.mention, married_to),
                    color=0xFF0000
                )
                embed.set_image(url="https://cdn.pixabay.com/photo/2015/12/11/17/28/heart-1088487_960_720.png")
                await self.client.say(embed=embed)
            else:
                if user.id == "164068466129633280":
                    embed = discord.Embed(
                        description="You are married to **Charlotte Izoard**",
                        color=0xFF0000
                    )
                    embed.set_image(url="https://i.imgur.com/G7oJSjE.jpg")
                    await self.client.say(embed=embed)
                    return
                elif user.id == "142002197998206976":
                    embed = discord.Embed(
                        description="You are married to **Yukana Yame**",
                        color=0xFF0000
                    )
                    embed.set_image(url="https://i.imgur.com/MEldWsb.jpg")
                    await self.client.say(embed=embed)
                    return

                embed = discord.Embed(
                    description="{} is not married".format(user.mention),
                    color=0xFF0000
                )
                await self.client.say(embed=embed)          

    @commands.command(pass_context=True)
    async def divorce(self, ctx):
        author = ctx.message.author
        server = ctx.message.server
        channel = ctx.message.channel
        marriage_toggle = self.check_setting(server, "Marriage_Toggle")
        if marriage_toggle == False:
            embed = discord.Embed(
                description="Marriage is currently disabled",
                color=0xFF0000
            )
            
            await self.client.say(embed=embed)
            return

        conn = pymysql.connect(host="sql7.freesqldatabase.com", user="sql7273467", password="ihireg57sU", db="sql7273467")
        c = conn.cursor()
        sql = "SELECT * FROM `Marriage_Table` WHERE user1 = '{}' OR user2 = '{}'".format(str(author.id), str(author.id))
        c.execute(sql)
        conn.commit()
        data = c.fetchall()
        if len(data) >= 1:
            embed = discord.Embed(
                description="Are you sure you wish to divorce?",
                color=0xFF0000
            )
            await self.client.say(embed=embed)
            user_response = await self.client.wait_for_message(timeout=40, channel=channel, author=author)
            user_response = user_response.clean_content.lower()
            if user_response == "yes":
                for d in data:
                    roleid = d[4]

                for srv in self.client.servers:
                    for role in list(srv.roles):
                        if str(role.id) == str(roleid):
                            try:
                                await self.client.delete_role(srv, role)
                            except discord.HTTPException:
                                embed = discord.Embed(
                                    description = "Role doesn't exist in {}".format(srv.name),
                                    color = 0xFF0000
                                )

                                await self.client.say(embed=embed)

                sql = "DELETE FROM `Marriage_Table` WHERE user1 = '{}' OR user2 = '{}'".format(str(author.id), str(author.id))
                c.execute(sql)
                conn.commit()
                embed = discord.Embed(
                    description="You broke up, you are now single",
                    color=0xFF0000
                )
                embed.set_image(url="https://upload.wikimedia.org/wikipedia/commons/b/bb/Broken_heart.svg")
                await self.client.say(embed=embed)
            elif user_response == "no":
                embed = discord.Embed(
                    description="Good choice",
                    color=0xFF0000
                )
                await self.client.say(embed=embed)
            else:
                embed = discord.Embed(
                    description="Invalid response",
                    color=0xFF0000
                )
                await self.client.say(embed=embed)
        else:
            embed = discord.Embed(
                description="You are not married",
                color=0xFF0000
            )
            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def forcebreakup(self, ctx, user: discord.Member = None):
        author = ctx.message.author
        if self.is_owner(author):
            if user == None:
                embed = discord.Embed(
                    description="You have not tagged any user",
                    color=0xFF0000
                )
                await self.client.say(embed=embed)
                return
            else:
                #breakup
                conn = pymysql.connect(host="sql7.freesqldatabase.com", user="sql7273467", password="ihireg57sU", db="sql7273467")
                c = conn.cursor()
                sql = "SELECT * FROM `Marriage_Table` WHERE user1 = '{}' OR user2 = '{}'".format(str(user.id), str(user.id))
                c.execute(sql)
                conn.commit()
                data = c.fetchall()
                if len(data) >= 1:
                    sql = "DELETE FROM `Marriage_Table` WHERE user1 = '{}' OR user2 = '{}'".format(str(user.id), str(user.id))
                    c.execute(sql)
                    conn.commit()
                    for d in data:
                        roleid = d[4]
                    for srv in self.client.servers:
                        for role in list(srv.roles):
                            if str(role.id) == str(roleid):
                                try:
                                    await self.client.delete_role(srv, role)
                                except discord.HTTPException:
                                    embed = discord.Embed(
                                        description = "Role doesn't exist in {}".format(srv.name),
                                        color = 0xFF0000
                                    )

                                    await self.client.say(embed=embed)
                    embed = discord.Embed(
                        description="You have successfully forced a break up on {}".format(user.mention),
                        color=0xFF0000
                    )
                    
                    await self.client.say(embed=embed)
                    
                else:
                    embed = discord.Embed(
                        description="This user is not married",
                        color=0xFF0000
                    )
                    
                    await self.client.say(embed=embed)
                conn.close()                
        else:
            embed = discord.Embed(
                description="You don't have permission to use this command",
                color=0xFF0000
            )
            
            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def propose(self, ctx, user: discord.Member = None):
        author = ctx.message.author
        server = ctx.message.server
        channel = ctx.message.channel
        marriage_toggle = self.check_setting(server, "Marriage_Toggle")
        if marriage_toggle == False:
            embed = discord.Embed(
                description="Marriage is currently disabled",
                color=0xFF0000
            )
            
            await self.client.say(embed=embed)
            return

        if user == None:
            embed = discord.Embed(
                description="You have not tagged anyone",
                color=0xFF0000
            )
            await self.client.say(embed=embed)
            return
        elif user == author:
            embed = discord.Embed(
                description="You can't marry yourself",
                color=0xFF0000
            )
            await self.client.say(embed=embed)
            return
        conn = pymysql.connect(host="sql7.freesqldatabase.com", user="sql7273467", password="ihireg57sU", db="sql7273467")
        c = conn.cursor()
        sql = "SELECT * FROM `Marriage_Table` WHERE user1 = '{}' OR user2 = '{}'".format(str(author.id), str(author.id))
        c.execute(sql)
        conn.commit()
        data = c.fetchall()
        if len(data) >= 1:
            embed = discord.Embed(
                description="You are already married",
                color=0xFF0000
            )
            await self.client.say(embed=embed)
            return
        else:
            sql = "SELECT * FROM `Marriage_Table` WHERE user1 = '{}' OR user2 = '{}'".format(str(user.id), str(user.id))
            c.execute(sql)
            conn.commit()
            data = c.fetchall()
            if len(data) >= 1:
                embed = discord.Embed(
                    description="{} is already married".format(user.mention),
                    color=0xFF0000
                )
                await self.client.say(embed=embed)
                return
            embed = discord.Embed(
                title="Marriage",
                description=":heart: {} is proposing to you, will you accept {}? :heart:".format(author.mention, user.mention),
                color=0x330000
            )
            embed.set_image(url=author.avatar_url)
            await self.client.say("{}".format(user.mention))
            await self.client.say(embed=embed)
            user_response = await self.client.wait_for_message(timeout=40, channel=channel, author=user)
            user_response = user_response.clean_content.lower()
            if user_response == "yes":
                try:
                    rolename = "{} X {}".format(author.name, user.name)
                    createdrole = await self.client.create_role(server=server, name=rolename, color=discord.Color.purple())
                    sql = "INSERT INTO `Marriage_Table` (user1, user2, ring, roleid) VALUES ('{}', '{}', '{}', '{}')".format(str(author.id), str(user.id), "default", createdrole.id)
                    c.execute(sql)
                    conn.commit()
                    await self.client.add_roles(author, createdrole)
                    await self.client.add_roles(user, createdrole)
                    embed = discord.Embed(
                        title="Marriage",
                        description=":heart: {} and {} is now married :heart:".format(author.mention, user.mention),
                        color=0x330000
                    )
                    embed.set_image(url="https://cdn.pixabay.com/photo/2015/12/11/17/28/heart-1088487_960_720.png")
                    await self.client.say(embed=embed)
                except discord.Forbidden:
                    embed = discord.Embed(
                        description = "Missing permissions",
                        color = 0xFF0000
                    )

                    await self.client.say(embed=embed)
            elif user_response == "no":
                embed = discord.Embed(
                    description="{} sadly denied your request to marry you :(".format(user.mention),
                    color=0xFF0000
                )
                await self.client.say(embed=embed)
                return
            else:
                embed = discord.Embed(
                    description="Invalid response",
                    color=0xFF0000
                )
                await self.client.say(embed=embed)

        conn.close()

def setup(client):
    client.add_cog(Marriage(client))