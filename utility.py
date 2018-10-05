import discord
import asyncio
import time
import json
import random
from discord.ext.commands import Bot
from discord.ext import commands
from random import randint
import datetime
import pymysql
import os

class Utility:
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

    def is_owner(self, user):
        if user.id == "164068466129633280" or user.id == "142002197998206976" or user.id == "457516809940107264":
            return True
        else:
            return False

    @commands.command(pass_context=True)
    async def avatar(self, ctx, user: discord.Member = None):
        author = ctx.message.author
        self_image = author.avatar_url

        if user == None:
            embed = discord.Embed(
                color=0x00FF00
            )

            embed.set_image(url=self_image)
            embed.set_author(name="Your Avatar")
        else:
            embed = discord.Embed(
                color=0x00FF00
            )

            embed.set_image(url=user.avatar_url)
            embed.set_author(name="{}'s Avatar".format(user))

            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def help(self, ctx):
        author = ctx.message.author
        channel = ctx.message.channel
        await self.client.say("What module do you want help with?")
        embed = discord.Embed(
            color=0x0000FF
        )
        embed.add_field(name="Primary Modules", value="Core, Admin, Utility, Creator", inline=False)
        embed.add_field(name="Secondary Modules",value="Fun, Music, Swarm, Level, Economy, NSFW", inline=False)
        await self.client.say(embed=embed)
        user_response = await self.client.wait_for_message(timeout=40, channel=channel, author=author)
        if user_response.clean_content.lower() == "core":
            self.client.say("Core Module Command List")
            embed = discord.Embed(
                color=0x0000FF
            )
            embed.set_author(name="Core Module")
            embed.add_field(name="dmwarn", value="Enable/Disable Direct Message On Warning", inline=False)
            embed.add_field(name="jointoggle", value="Enable/Disable auto role on join", inline=False)
            embed.add_field(name="joinrole ROLE_NAME",value="Set auto join role", inline=False)
            embed.add_field(name="modrole ROLE_NAME",value="Set moderator role", inline=False)
            embed.add_field(name="adminrole ROLE_NAME",value="Set administrator role", inline=False)
            embed.add_field(name="mod user", value="Gives the user the moderator role", inline=False)
            embed.add_field(name="admin user", value="Gives the user the administrator role", inline=False)
            embed.add_field(name="muterole ROLE_NAME",value="Set mute role", inline=False)
            embed.add_field(name="mutetime 1M/1H", value="Set the mute time for when users reach warning mute", inline=False)
            embed.add_field(name="resetsetting SETTING_NAME",value="Resets the setting to default", inline=False)
            embed.add_field(name="funtoggle", value="Toggles the fun commands", inline=False)
            embed.add_field(name="nsfwrole ROLE_NAME", value="Sets the nsfw role", inline=False)
            embed.add_field(name="nsfwtoggle", value="Toggles the nsfw commands", inline=False)
            embed.add_field(name="botinfo", value="Shows the bot information", inline=False)
            await self.client.say(embed=embed)

        elif user_response.clean_content.lower() == "admin":
            self.client.say("Admin Module Command List")
            embed = discord.Embed(
                color=0x0000FF
            )
            embed.set_author(name="Admin Module")
            embed.add_field(name="kick user",value="Kicks the user", inline=False)
            embed.add_field(name="ban user",value="Bans the user", inline=False)
            embed.add_field(name="banid USER_ID",value="Bans the user with ID", inline=False)
            embed.add_field(name="unban USER_ID",value="Unbans the user with ID", inline=False)
            embed.add_field(name="mute user M/H", value="Mutes the user for the given time", inline=False)
            embed.add_field(name="unmute user",value="Unmutes the user", inline=False)
            embed.add_field(name="clear AMOUNT [user]", value="Clears the amount of messages given, if no amount is given it clears 100", inline=False)
            embed.add_field(name="nickname user NAME",value="Nicknames the user with the given name", inline=False)
            embed.add_field(name="removenick user",value="Removes the users nickname", inline=False)
            embed.add_field(name="clearwarns user",value="Clears the users warnings", inline=False)
            embed.add_field(name="warn user REASON",value="Warns the user with given warning", inline=False)
            embed.add_field(name="warns user",value="Displays the users warnings", inline=False)
            embed.add_field(name="setwarn number punishment(mute/kick/ban)",value="Sets the punishment for the given warn number", inline=False)
            embed.add_field(name="removewarn number",value="Removes the punishment for the given number", inline=False)
            embed.add_field(name="announce #channel MESSAGE",value="Announces the given message in given channel", inline=False)
            embed.add_field(name="role user ROLE_NAME",value="Announces the given message in given channel", inline=False)
            embed.add_field(name="verify user [ROLE_NAME]", value="Gives the user the verify role and if chosen also gives another role", inline=False)
            embed.add_field(name="dinvites", value="Delete all of the invites", inline=False)
            await self.client.say(embed=embed)

        elif user_response.clean_content.lower() == "fun":
            self.client.say("Fun Module Command List")
            embed = discord.Embed(
                color=0x0000FF
            )
            embed.set_author(name="Fun Module")
            embed.add_field(name="meme", value="Posts a random meme from reddit", inline=False)
            embed.add_field(name="loli", value="Posts a random loli image from reddit", inline=False)
            embed.add_field(name="catgirl", value="Posts a link to the catgirl care website", inline=False)
            await self.client.say(embed=embed)

        elif user_response.clean_content.lower() == "nsfw":
            self.client.say("NSFW Module Command List")
            embed = discord.Embed(
                color=0x0000FF
            )
            embed.set_author(name="NSFW Module")
            embed.add_field(name="pgif", value="Posts a gif", inline=False)
            embed.add_field(name="fourk", value="Posts a 4k image", inline=False)
            embed.add_field(name="gonewild", value="Posts a gone wild image", inline=False)
            embed.add_field(name="pussy", value="Posts a pussy image", inline=False)
            embed.add_field(name="hentai", value="Posts a hentai image/gif", inline=False)
            embed.add_field(name="lewdneko", value="Posts a lewd neko NSFW image", inline=False)
            embed.add_field(name="hanal", value="Posts a image/gif with hentai anal", inline=False)
            embed.add_field(name="holo", value="Posts NSFW content of the anime character Holo", inline=False)
            embed.add_field(name="gasm", value="Posts a image with someone having an orgasm", inline=False)
            embed.add_field(name="lewdkitsune", value="Posts neko NSFW content", inline=False)
            embed.add_field(name="furry", value="Posts a random furry image from reddit", inline=False)
            await self.client.say(embed=embed)

        elif user_response.clean_content.lower() == "level":
            self.client.say("Level Module Command List")
            embed = discord.Embed(
                color=0x0000FF
            )
            embed.set_author(name="Level Module")
            embed.add_field(name="mylevel", value="Displays your level", inline=False)
            embed.add_field(name="togglelevel", value="Disables the global level system on this server", inline=False)
            await self.client.say(embed=embed)

        elif user_response.clean_content.lower() == "creator":
            self.client.say("Creator Module Command List")
            embed = discord.Embed(
                color=0x0000FF
            )
            embed.set_author(name="Creator Module")
            embed.add_field(name="whitelist Server_ID",value="Whitelists the server so the bot can join", inline=False)
            embed.add_field(name="gannounce MESSAGE",value="Global announces a message to all servers", inline=False)
            embed.add_field(name="autoban user", value="Bans the user and adds the user to the autoban list", inline=False)
            embed.add_field(name="unautoban id", value="Unbans the id and removed the id from the autoban list", inline=False)
            embed.add_field(name="leave server", value="Leaves the given server", inline=False)
            await self.client.say(embed=embed)

        elif user_response.clean_content.lower() == "music":
            self.client.say("Music Module Command List")
            embed = discord.Embed(
                color=0x0000FF
            )
            embed.set_author(name="Music Module")
            embed.add_field(name="W.I.P", value="This module is still in progress", inline=False)
            await self.client.say(embed=embed)

        elif user_response.clean_content.lower() == "swarm":
            self.client.say("Swarm Module Command List")
            embed = discord.Embed(
                color=0x0000FF
            )
            embed.set_author(name="Swarm Module")
            embed.add_field(name="swarm", value="Shows brood information, or starts the creation process if you have none", inline=False)
            embed.add_field(name="spawneggs AMOUNT",value="Spawns the amount of eggs given if possible.", inline=False)
            embed.add_field(name="collect", value="Sends drones out to collect Organic Biomaterials", inline=False)
            await self.client.say(embed=embed)

        elif user_response.clean_content.lower() == "utility":
            self.client.say("Utility Module Command List")
            embed = discord.Embed(
                color=0x0000FF
            )
            embed.set_author(name="Utility Module")
            embed.add_field(name="help", value="Shows list of modules and command list", inline=False)
            embed.add_field(name="avatar [user]", value="Shows your own avatar or the given users avatar", inline=False)
            embed.add_field(name="mywarns", value="Displays your warnings", inline=False)
            embed.add_field(name="flipcoin", value="Flips a coin and will either land on Heads or Tails", inline=False)
            embed.add_field(name="rolldice", value="Rolls a dice and will land on a number between 1 - 6", inline=False)
            embed.add_field(name="members", value="Shows member count", inline=False)
            embed.add_field(name="userid user",value="Shows the users UserID", inline=False)
            embed.add_field(name="userinfo [user]", value="Shows info for yourself or the given user", inline=False)
            embed.add_field(name="nsfw", value="Gives/removes the nsfw role", inline=False)
            await self.client.say(embed=embed)
        elif user_response.clean_content.lower() == "economy":
            self.client.say("Economy Module Command List")
            embed = discord.Embed(
                color=0x0000FF
            )
            embed.set_author(name="Economy Module")
            embed.add_field(name="work", value="Earn money the legal way", inline=False)
            embed.add_field(name="bal", value="Posts your balance", inline=False)
            embed.add_field(name="withdraw amount", value="Withdraw money from your bank", inline=False)
            embed.add_field(name="dep amount", value="Deposit money into your bank", inline=False)
            embed.add_field(name="give user amount", value="Give money to a user", inline=False)
            embed.add_field(name="setmax setting value", value="Set the settings maximum amount", inline=False)
            embed.add_field(name="setmin setting value", value="Set the settings minimum amount", inline=False)
            await self.client.say(embed=embed)
        else:
            await self.client.say("Invalid Module.")

    @commands.command(pass_context=True)
    async def flipcoin(self, ctx):
        r_int = randint(1, 2)
        if r_int == 1:
            embed = discord.Embed(
                title="Coin Flip",
                description="You flipped a coin and it landed on **Tails**",
                color=0x00FF00
            )
            await self.client.say(embed=embed)
        elif r_int == 2:
            embed = discord.Embed(
                title="Coin Flip",
                description="You flipped a coin and it landed on **Heads**",
                color=0x00FF00
            )
            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def rolldice(self, ctx):
        r_int = randint(1, 6)
        embed = discord.Embed(
            title="Roll Dice",
            description="You throw a dice and it lands on **{}**".format(
                str(r_int)),
            color=0x00FF00
        )
        await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def getservers(self, ctx):
        author = ctx.message.author
        if author.id == "142002197998206976" or author.id == "164068466129633280":
            channel = ctx.message.channel
            embed = discord.Embed(
                title="Servers",
                color=0x00FF00
            )
            await self.client.say("Do you want the list **Inline** ? (Yes/No)")
            user_response = await self.client.wait_for_message(timeout=30, channel=channel, author=author)
            if user_response.clean_content == "yes" or user_response.clean_content == "Yes":
                inline = True
            elif user_response.clean_content == "no" or user_response.clean_content == "No":
                inline = False
            else:
                await self.client.say("Invalid.")
                return

            for srv in self.client.servers:
                embed.add_field(name=srv, value=srv.id, inline=inline)

            await self.client.send_message(author, embed=embed)
        else:
            embed = discord.Embed(
                description="You do not have permission to use this command.",
                color=0xFF0000
            )
            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def leave(self, ctx, *, server = None):
        author = ctx.message.author
        if self.is_owner(author) == True:
            if server == None:
                embed = discord.Embed(
                    description = "You need to write what server you want me to leave",
                    color = 0xFF0000
                )

                await self.client.say(embed=embed)
            else:
                servertoleave = None
                for srv in self.client.servers:
                    if str(srv.name).lower() == str(server).lower() or srv.id == server:
                        servertoleave = srv

                if servertoleave == None:
                    embed = discord.Embed(
                        description = "I couldn't find a server with the name or id **{}**".format(server),
                        color = 0xFF0000
                    )

                    await self.client.say(embed=embed)
                else:
                    await self.client.leave_server(servertoleave)

                    embed = discord.Embed(
                        description = "I have successfully left the server **{}**".format(servertoleave.name),
                        color = 0x00FF00
                    )

                    await self.client.say(embed=embed)
        else:
            embed = discord.Embed(
                description="You don't have permission to use this command",
                color=0xFF0000
            )

            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def invite(self, ctx):
        author = ctx.message.author
        invitelink = "https://discordapp.com/oauth2/authorize?client_id={}&scope=bot".format(self.client.user.id)

        if self.is_owner(author) == True:
            embed = discord.Embed(
                title="Invite link",
                description=invitelink,
                color=0x800080
            )

            await self.client.send_message(author, embed=embed)

            embed = discord.Embed(
                description="I have sent you a direct message with the invite link",
                color=0x00FF00
            )

            await self.client.say(embed=embed)
        else:
            embed = discord.Embed(
                description="You don't have permission to use this command.",
                color=0xFF0000
            )
            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def userinfo(self, ctx, user: discord.Member = None):
        author = ctx.message.author
        if user == None:
            status = None
            rolecount = 0
            roles = None
            joindate = author.joined_at.strftime("%b %e, %Y %-I:%M %p")
            registerdate = author.created_at.strftime("%b %e, %Y %-I:%M %p")
            currentdate = datetime.datetime.now().strftime("%b %e, %Y %-I:%M %p")
            name = str(author.name)
            nickname = str(author.display_name)
            if str(author.status) == "online":
                status = "Online"
            elif str(author.status) == "offline":
                status = "Offline"

            for role in author.roles:
                if role.name != "@everyone":
                    rolecount += 1
                    if roles == None:
                        roles = "{}".format(role.mention)
                    else:
                        roles += " {}".format(role.mention)

            embed = discord.Embed(
                description="{}".format(author.mention),
                color=0x00FF00
            )

            embed.set_author(name="{}".format(str(author)),
                             icon_url=author.avatar_url)
            embed.set_thumbnail(url=author.avatar_url)
            embed.add_field(
                name="Status", value="{}".format(status), inline=True)
            embed.add_field(name="Joined", value="{}".format(
                joindate), inline=True)
            embed.add_field(name="Registered", value="{}".format(
                registerdate), inline=True)
            if nickname == name:
                embed.add_field(name="Nickname", value="None", inline=True)
            else:
                embed.add_field(name="Nickname", value="{}".format(
                    nickname), inline=True)

            embed.add_field(name="Roles [{}]".format(
                rolecount), value="{}".format(roles), inline=False)
            embed.set_footer(text="ID: {} • {}".format(author.id, currentdate))
            await self.client.say(embed=embed)
        else:
            status = None
            if str(user.status) == "online":
                status = "Online"
            elif str(user.status) == "offline":
                status = "Offline"

            rolecount = 0
            roles = None
            joindate = user.joined_at.strftime("%b %e, %Y %-I:%M %p")
            registerdate = user.created_at.strftime("%b %e, %Y %-I:%M %p")
            currentdate = datetime.datetime.now().strftime("%b %e, %Y %-I:%M %p")
            name = str(user.name)
            nickname = str(user.display_name)
            for role in user.roles:
                if role.name != "@everyone":
                    rolecount += 1
                    if roles == None:
                        roles = "{}".format(role.mention)
                    else:
                        roles += " {}".format(role.mention)

            embed = discord.Embed(
                description="{}".format(user.mention),
                color=0x00FF00
            )

            embed.set_author(name="{}".format(str(user)),
                             icon_url=user.avatar_url)
            embed.set_thumbnail(url=user.avatar_url)
            embed.add_field(
                name="Status", value="{}".format(status), inline=True)
            embed.add_field(name="Joined", value="{}".format(
                joindate), inline=True)
            embed.add_field(name="Registered", value="{}".format(
                registerdate), inline=True)
            if nickname == name:
                embed.add_field(name="Nickname", value="None", inline=True)
            else:
                embed.add_field(name="Nickname", value="{}".format(
                    nickname), inline=True)

            embed.add_field(name="Roles [{}]".format(
                rolecount), value="{}".format(roles), inline=False)
            embed.set_footer(text="ID: {} • {}".format(user.id, currentdate))

            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def nsfw(self, ctx):
        author = ctx.message.author
        server = ctx.message.server
        nsfw_toggle = self.check_database(server, "NSFW_toggle")
        nsfw_role = self.check_database(server, "NSFW_role")
        if nsfw_toggle == False:
            embed = discord.Embed(
                description="The NSFW commands is currently disabled",
                color=0xFF0000
            )
            await self.client.say(embed=embed)
            return
        else:
            if discord.utils.get(author.roles, name=nsfw_role):
                role = discord.utils.get(server.roles, name=nsfw_role)
                await self.client.remove_roles(author, role)
                embed = discord.Embed(
                    description="Your NSFW role has been removed",
                    color=0x00FF00
                )
                await self.client.say(embed=embed)
            else:
                role = discord.utils.get(server.roles, name=nsfw_role)
                await self.client.add_roles(author, role)
                embed = discord.Embed(
                    description="You have been given the designated NSFW role",
                    color=0x00FF00
                )
                await self.client.say(embed=embed)


def setup(client):
    client.add_cog(Utility(client))
