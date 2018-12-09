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
                title = "Your Avatar",
                color=0x00FF00
            )

            embed.set_image(url=self_image)
        else:
            embed = discord.Embed(
                title = "{}'s Avatar".format(str(user)),
                color=0x00FF00
            )

            embed.set_image(url=user.avatar_url)

            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def setcolor(self, ctx):
        author = ctx.message.author
        server = author.server
        channel = ctx.message.channel
        if author == server.owner or self.is_owner(author):
            embed = discord.Embed(
                description="Enter the name for the color you wish to make",
                color=0x00FF00
            )
            await self.client.say(embed=embed)
            user_response = await self.client.wait_for_message(timeout=40, channel=channel, author=author)
            color_name = user_response.clean_content.lower()
            embed = discord.Embed(
                description="Enter the rolename for your color **{}**".format(color_name),
                color=0x00FF00
            )
            await self.client.say(embed=embed)
            user_response = await self.client.wait_for_message(timeout=40, channel=channel, author=author)
            color_rolename = user_response.clean_content
            rolename = discord.utils.get(server.roles, name=color_rolename)
            newrole = str(rolename)
            if newrole == "None":
                embed = discord.Embed(
                    description="Role not found",
                    color=0xFF0000
                )
                await self.client.say(embed=embed)
                return
            else:
                embed = discord.Embed(
                    description="Color information - Confirm[Yes/No]",
                    color=0x00FF00
                )
                embed.add_field(name="Color name", value="{}".format(color_name))
                embed.add_field(name="Color rolename", value="{}".format(newrole))
                await self.client.say(embed=embed)
                user_response = await self.client.wait_for_message(timeout=40, channel=channel, author=author)
                user_response = user_response.clean_content.lower()
                if user_response == "yes":
                    conn = pymysql.connect(host="sql7.freesqldatabase.com", user="sql7268803", password="lL2exAj7JR", db="sql7268803")
                    c = conn.cursor()
                    sql = "SELECT * FROM `Color_Table` WHERE serverid = '{}' AND color_name = '{}'".format(str(server.id), str(color_name))
                    c.execute(sql)
                    conn.commit()
                    data = c.fetchall()
                    if len(data) >= 1:
                        #Color Already Exists
                        sql = "UPDATE `Color_Table` SET color_name = '{}', color_rolename = '{}' WHERE serverid = '{}' AND color_name = '{}'".format(color_name, newrole, server.id, color_name)
                        c.execute(sql)
                        conn.commit()
                        embed = discord.Embed(
                            description="Color has been made",
                            color=0x00FF00
                        )
                        await self.client.say(embed=embed)
                        conn.close()
                        return
                    else:
                        #Color Does Not Exist
                        sql = "INSERT INTO `Color_Table` (serverid, color_name, color_rolename) VALUES ('{}', '{}', '{}')".format(str(server.id), str(color_name), newrole)
                        c.execute(sql)
                        conn.commit()
                        embed = discord.Embed(
                            description="Color has been made",
                            color=0x00FF00
                        )
                        await self.client.say(embed=embed)
                        conn.close()
                        return
                elif user_response == "no":
                    embed = discord.Embed(
                        description="Exiting",
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
                    return               
        else:
            embed = discord.Embed(
                description="You don't have permission to use this command.",
                color=0xFF0000
            )
            await self.client.say(embed=embed)


    @commands.command(pass_context=True)
    async def help(self, ctx, module: str = None):
        author = ctx.message.author
        channel = ctx.message.channel
        if module == None:
            await self.client.say("What module do you want help with?")
            embed = discord.Embed(
                color = 0x0000FF
            )
            embed.add_field(name="Primary Modules", value="Core, Admin, Utility, Creator", inline=False)
            embed.add_field(name="Secondary Modules",value="Fun, Music, Swarm, Level, Economy, NSFW, Marriage, Otaku", inline=False)
            await self.client.say(embed=embed)
            user_response = await self.client.wait_for_message(timeout=40, channel=channel, author=author)
            user_response = user_response.clean_content.lower()
        else:
            user_response = module.lower()

        if user_response == "core":
            self.client.say("Core Module Command List")
            embed = discord.Embed(
                title = "Core Module",
                color = 0x0000FF
            )
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
            embed.add_field(name="marrytoggle", value="Toggles the marriage commands", inline=False)
            embed.add_field(name="sweartoggle", value="Toggles the profanity filter (swear filter)", inline=False)
            embed.add_field(name="customwords", value="Toggles the custom words filter (banned words filter)", inline=False)
            embed.add_field(name="banword word", value="Bans the word/add the word to the swear filter", inline=False)
            embed.add_field(name="unbanword word", value="Unbans the word/removes the word from the swear filter", inline=False)
            embed.add_field(name="bannedwords", value="Sends you the list of banned words", inline=False)
            embed.add_field(name="lockchannel [channel]", value="Locks the channel", inline=False)
            embed.add_field(name="unlockchannel [channel]", value="Unlocks the channel", inline=False)
            embed.add_field(name="kickbots", value="Kicks all the bots in the server", inline=False)
            embed.add_field(name="botinfo", value="Shows the bot information", inline=False)
            await self.client.say(embed=embed)

        elif user_response == "admin":
            self.client.say("Admin Module Command List")
            embed = discord.Embed(
                title = "Admin Module",
                color = 0x0000FF
            )
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
            embed.add_field(name="role user ROLE_NAME",value="Gives/removes the given role to/from the user", inline=False)
            embed.add_field(name="verify user [ROLE_NAME]", value="Gives the user the verify role and if chosen also gives another role", inline=False)
            embed.add_field(name="dinvites", value="Delete all of the invites", inline=False)
            await self.client.say(embed=embed)

        elif user_response == "fun":
            self.client.say("Fun Module Command List")
            embed = discord.Embed(
                title = "Fun Module",
                color = 0x0000FF
            )
            embed.add_field(name="meme", value="Posts a random meme from reddit", inline=False)
            embed.add_field(name="slap user", value="Slaps the user", inline=False)
            embed.add_field(name="splat user", value="Splat out the user", inline=False)
            await self.client.say(embed=embed)

        elif user_response == "nsfw":
            self.client.say("NSFW Module Command List")
            embed = discord.Embed(
                title = "NSFW Module",
                color = 0x0000FF
            )
            embed.add_field(name="porn [search]", value="Posts a porn image", inline=False)
            embed.add_field(name="porng [search]", value="Posts a porn GIF image", inline=False)
            embed.add_field(name="hentai", value="Posts a hentai image", inline=False)
            embed.add_field(name="lewdneko", value="Posts a lewd neko NSFW image", inline=False)
            embed.add_field(name="holo", value="Posts NSFW content of the anime character Holo", inline=False)
            embed.add_field(name="lewdkitsune", value="Posts neko NSFW content", inline=False)
            embed.add_field(name="rule34 tag", value="Posts a rule34 image", inline=False)
            embed.add_field(name="e621 tag", value="Posts a e621 image", inline=False)
            await self.client.say(embed=embed)

        elif user_response == "level":
            self.client.say("Level Module Command List")
            embed = discord.Embed(
                title = "Level Module",
                color = 0x0000FF
            )
            embed.add_field(name="mylevel", value="Displays your level", inline=False)
            embed.add_field(name="togglelevel", value="Disables the global level system on this server", inline=False)
            await self.client.say(embed=embed)

        elif user_response == "creator":
            self.client.say("Creator Module Command List")
            embed = discord.Embed(
                title = "Creator Module",
                color = 0x0000FF
            )
            embed.add_field(name="whitelist Server_ID",value="Whitelists the server so the bot can join", inline=False)
            embed.add_field(name="gannounce MESSAGE",value="Global announces a message to all servers", inline=False)
            embed.add_field(name="autoban user", value="Bans the user and adds the user to the autoban list", inline=False)
            embed.add_field(name="unautoban id", value="Unbans the id and removed the id from the autoban list", inline=False)
            embed.add_field(name="leave server", value="Leaves the given server", inline=False)
            await self.client.say(embed=embed)

        elif user_response == "music":
            self.client.say("Music Module Command List")
            embed = discord.Embed(
                title = "Music Module",
                color = 0x0000FF
            )
            embed.add_field(name="W.I.P", value="This module is still in progress", inline=False)
            await self.client.say(embed=embed)

        elif user_response == "swarm":
            self.client.say("Swarm Module Command List")
            embed = discord.Embed(
                title = "Swarm Module",
                color = 0x0000FF
            )
            embed.add_field(name="swarm", value="Shows brood information, or starts the creation process if you have none", inline=False)
            embed.add_field(name="spawneggs AMOUNT",value="Spawns the amount of eggs given if possible.", inline=False)
            embed.add_field(name="collect", value="Sends drones out to collect Organic Biomaterials", inline=False)
            await self.client.say(embed=embed)

        elif user_response == "utility":
            self.client.say("Utility Module Command List")
            embed = discord.Embed(
                title = "Utility Module",
                color = 0x0000FF
            )
            embed.add_field(name="help [module]", value="Shows list of modules and command list", inline=False)
            embed.add_field(name="avatar [user]", value="Shows your own avatar or the given users avatar", inline=False)
            embed.add_field(name="mywarns", value="Displays your warnings", inline=False)
            embed.add_field(name="flipcoin", value="Flips a coin and will either land on Heads or Tails", inline=False)
            embed.add_field(name="rolldice", value="Rolls a dice and will land on a number between 1 - 6", inline=False)
            embed.add_field(name="members", value="Shows member count", inline=False)
            embed.add_field(name="userid user",value="Shows the users UserID", inline=False)
            embed.add_field(name="userinfo [user]", value="Shows info for yourself or the given user", inline=False)
            embed.add_field(name="nsfw", value="Gives/removes the nsfw role", inline=False)
            await self.client.say(embed=embed)
        elif user_response == "economy":
            self.client.say("Economy Module Command List")
            embed = discord.Embed(
                title = "Economy Module",
                color = 0x0000FF
            )
            embed.add_field(name="work", value="Earn money the legal way", inline=False)
            embed.add_field(name="bal", value="Posts your balance", inline=False)
            embed.add_field(name="withdraw amount", value="Withdraw money from your bank", inline=False)
            embed.add_field(name="dep amount", value="Deposit money into your bank", inline=False)
            embed.add_field(name="give user amount", value="Give money to a user", inline=False)
            embed.add_field(name="setmoney amount [user]", value="Sets the money for yourself or the given user", inline=False)
            embed.add_field(name="setbank amount [user]", value="Sets the bank money for yourself or the given user", inline=False)
            embed.add_field(name="setmax setting value", value="Set the settings maximum amount", inline=False)
            embed.add_field(name="setmin setting value", value="Set the settings minimum amount", inline=False)
            await self.client.say(embed=embed)
        elif user_response == "marriage":
            self.client.say("Marriage Module Command List")
            embed = discord.Embed(
                title = "Marriage Module",
                color = 0x0000FF
            )
            embed.add_field(name="propose user", value="Propose to the user", inline=False)
            embed.add_field(name="marriage", value="Shows who you are married to", inline=False)
            embed.add_field(name="divorce", value="Breaks up with the on you are married to", inline=False)
            await self.client.say(embed=embed)
        elif user_response == "otaku":
            self.client.say("Otaku Module Command List")
            embed = discord.Embed(
                title = "Otaku Module",
                color = 0x0000FF
            )
            embed.add_field(name="shiki", value="Shows information about the King of Siscon", inline=False)
            embed.add_field(name="hdude", value="Shows information about the rapper Hentai Dude", inline=False)
            embed.add_field(name="imotou", value="Display a random image from reddit with a cute imotou", inline=False)
            embed.add_field(name="oniisong", value="Shows a random song from either hdude or shiki", inline=False)
            embed.add_field(name="loli", value="Display a random image from reddit with a cute loli", inline=False)
            embed.add_field(name="neko", value="Display a random image from reddit with a cute neko", inline=False)
            embed.add_field(name="catgirl", value="Posts a link to the catgirl website", inline=False)
            await self.client.say(embed=embed)
        else:
            embed = discord.Embed(
                description = "The module `{}` doesn't exist".format(module),
                color = 0xFF0000
            )
            await self.client.say(embed=embed)

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
            user_response = user_response.clean_content.lower()
            if user_response == "yes":
                inline = True
            elif user_response == "no":
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
            try:
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
            except discord.HTTPException:
                embed = discord.Embed(
                    description="I can't send any direct messages to {}".format(author.mention),
                    color=0xFF0000
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

            embed.set_author(name="{}".format(str(author)),icon_url=author.avatar_url)
            embed.set_thumbnail(url=author.avatar_url)
            embed.add_field(name="Status", value="{}".format(status), inline=True)
            embed.add_field(name="Joined", value="{}".format(joindate), inline=True)
            embed.add_field(name="Registered", value="{}".format(registerdate), inline=True)
            if nickname == name:
                embed.add_field(name="Nickname", value="None", inline=True)
            else:
                embed.add_field(name="Nickname", value="{}".format(nickname), inline=True)

            embed.add_field(name="Roles [{}]".format(rolecount), value="{}".format(roles), inline=False)
            embed.set_footer(text="ID: {}".format(author.id))
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

            embed.set_author(name="{}".format(str(user)),icon_url=user.avatar_url)
            embed.set_thumbnail(url=user.avatar_url)
            embed.add_field(name="Status", value="{}".format(status), inline=True)
            embed.add_field(name="Joined", value="{}".format(joindate), inline=True)
            embed.add_field(name="Registered", value="{}".format(registerdate), inline=True)
            if nickname == name:
                embed.add_field(name="Nickname", value="None", inline=True)
            else:
                embed.add_field(name="Nickname", value="{}".format(nickname), inline=True)

            embed.add_field(name="Roles [{}]".format(
                rolecount), value="{}".format(roles), inline=False)
            embed.set_footer(text="ID: {} • {}".format(user.id, currentdate))

            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def nsfw(self, ctx):
        author = ctx.message.author
        server = ctx.message.server
        nsfw_toggle = self.check_setting(server, "NSFW_toggle")
        nsfw_role = self.check_setting(server, "NSFW_role")
        if nsfw_toggle == False:
            embed = discord.Embed(
                description="The NSFW commands is currently disabled",
                color=0xFF0000
            )
            await self.client.say(embed=embed)
            return
        else:
            if discord.utils.get(author.roles, name=nsfw_role):
                try:
                    role = discord.utils.get(server.roles, name=nsfw_role)
                    await self.client.remove_roles(author, role)
                    embed = discord.Embed(
                        description="Your NSFW role has been removed",
                        color=0x00FF00
                    )

                    await self.client.say(embed=embed)
                except discord.Forbidden:
                    embed = discord.Embed(
                        description="Missing permissions",
                        color=0xFF0000
                    )

                    await self.client.say(embed=embed)
            else:
                try:
                    role = discord.utils.get(server.roles, name=nsfw_role)
                    await self.client.add_roles(author, role)
                    embed = discord.Embed(
                        description="You've been given the designated NSFW role",
                        color=0x00FF00
                    )

                    await self.client.say(embed=embed)
                except discord.Forbidden:
                    embed = discord.Embed(
                        description="Missing permissions",
                        color=0xFF0000
                    )

                    await self.client.say(embed=embed)

def setup(client):
    client.add_cog(Utility(client))
