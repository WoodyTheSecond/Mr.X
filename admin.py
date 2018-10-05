import discord
import asyncio
import time
import os
import sys
import json
from discord.ext.commands import Bot
from discord.ext import commands
import pymysql


class Admin:
    def __init__(self, client):
        self.client = client

    def update_database(self, server, setting, value):
        conn = pymysql.connect(host="sql7.freesqldatabase.com", user="sql7257339", password="yakm4fsd4T", db="sql7257339")
        c = conn.cursor()
        if setting == "Join_Role":
            sql = "UPDATE `Server_Settings` SET Join_Role = %s where serverid = %s"
        elif setting == "DMWarn":
            sql = "UPDATE `Server_Settings` SET DMWarn = %s where serverid = %s"
        elif setting == "Verify_Role":
            sql = "UPDATE `Server_Settings` SET Verify_Role = %s where serverid = %s"
        elif setting == "Mod_Role":
            sql = "UPDATE `Server_Settings` SET Mod_Role = %s where serverid = %s"
        elif setting == "Admin_Role":
            sql = "UPDATE `Server_Settings` SET Admin_Role = %s where serverid = %s"
        elif setting == "Mute_Role":
            sql = "UPDATE `Server_Settings` SET Mute_Role = %s where serverid = %s"
        elif setting == "WarnMute":
            sql = "UPDATE `Server_Settings` SET WarnMute = %s where serverid = %s"
        elif setting == "JoinToggle":
            sql = "UPDATE `Server_Settings` SET JoinToggle = %s where serverid = %s"
        elif setting == "CanModAnnounce":
            sql = "UPDATE `Server_Settings` SET CanModAnnounce = %s where serverid = %s"
        elif setting == "Level_System":
            sql = "UPDATE `Server_Settings` SET Level_System = %s where serverid = %s"
        elif setting == "Chat_Filter":
            sql = "UPDATE `Server_Settings` SET Chat_Filter = %s where serverid = %s"
        elif setting == "Ignore_Hierarchy":
            sql = "UPDATE `Server_Settings` SET Ignore_Hierarchy = %s where serverid = %s"
        elif setting == "FunToggle":
            sql = "UPDATE `Server_Settings` SET FunToggle = %s where serverid = %s"
        else:
            print("No such setting found")
            return
        t = (value, str(server.id))
        c.execute(sql, t)
        conn.commit()
        conn.close()

    def check_database_multiple(self, conn, server, setting):
        c = conn.cursor()
        sql = "SELECT {} from `Server_Settings` WHERE serverid = {}".format(setting, str(server.id))
        c.execute(sql)
        conn.commit()
        data = c.fetchone()
        for row in data:
            if row == 1:
                return True
            elif row == 0:
                return False
            else:
                return row

    def check_database(self, server, setting):
        conn = pymysql.connect(host="sql7.freesqldatabase.com", user="sql7257339", password="yakm4fsd4T", db="sql7257339")
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
    async def warn(self, ctx, user: discord.Member = None, *, reason="No Reason Given"):
        author = ctx.message.author
        server = author.server
        if self.is_mod_or_perms(server, author):
            if user == None:
                embed = discord.Embed(
                description="You have not tagged any user",
                color=0xFF0000
                )
                await self.client.say(embed=embed)
                return
            # Actual Warning Code
            
                                                                                       
        else:
            embed = discord.Embed(
                description="You don't have permission to use this command",
                color=0xFF0000
            )
            await self.client.say(embed=embed)
        

    @commands.command(pass_context=True)
    async def warns(self, ctx, user: discord.Member):
        author = ctx.message.author
        server = author.server
        channel = ctx.message.channel
       

    @commands.command(pass_context=True)
    async def clearwarns(self, ctx, user: discord.Member):
        server = ctx.message.author.server
        author = ctx.message.author
        if self.is_admin_or_perms(server, author):
            path = "servers/" + str(server.id) + \
                "/warnings/" + str(user.id) + "/"
            warnpath = path + "warnings.json"
            os.remove(warnpath)
            embed = discord.Embed(
                description="{} Warnings has been removed".format(
                    user.mention),
                color=0x00FF00
            )
            await self.client.say(embed=embed)
        else:
            embed = discord.Embed(
                description="You don't have permission to use this command",
                color=0xFF0000
            )
            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def verify(self, ctx, user: discord.Member, *, role_name=None):
        author = ctx.message.author
        server = author.server
        if self.is_admin_or_perms(server, author):
            verifyrole_name = self.check_database(server, "Verify_Role")
            verifyrole = discord.utils.get(server.roles, name=verifyrole_name)
            if role_name == None:
                if verifyrole != None:
                    await self.client.add_roles(user, verifyrole)
                    embed = discord.Embed(
                        description="{} has been verified".format(
                            user.mention),
                        color=0x00FF00
                    )
                    await self.client.say(embed=embed)
                else:
                    embed = discord.Embed(
                        description="There is no Verify Role set, please use -verifyrole ROLE_NAME",
                        color=0xFF0000
                    )
                    await self.client.say(embed=embed)
            else:
                extra_role = discord.utils.get(server.roles, name=role_name)
                if extra_role != None:
                    roles_to_give = []
                    roles_to_give.append(verifyrole)
                    roles_to_give.append(extra_role)
                    await self.client.add_roles(user, *roles_to_give)
                    embed = discord.Embed(
                        description="{} has been verified and given the role **{}**".format(
                            user.mention, role_name),
                        color=0x00FF00
                    )
                    await self.client.say(embed=embed)
                else:
                    embed = discord.Embed(
                        description="**{}** role was not found".format(
                            role_name),
                        color=0xFF0000
                    )
                    await self.client.say(embed=embed)

                print("WITH ROLE")

        else:
            embed = discord.Embed(
                description="You don't have permission to use this command",
                color=0xFF0000
            )
            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def setwarn(self, ctx, warn_number, punishment):
        author = ctx.message.author
        server = author.server
        if author == server.owner or author.id == "164068466129633280" or author.id == "142002197998206976":
            if punishment == "mute" or punishment == "Mute":
                t_punish = "Mute"
            elif punishment == "kick" or punishment == "Kick":
                t_punish = "Kick"
            elif punishment == "ban" or punishment == "Ban":
                t_punish = "Ban"
            else:
                self.client.say(
                    "That is not a possible punishment, the possible punishments is [Mute/Kick/Ban]")
                return
            path = "servers/" + str(server.id) + "/warn_punishments/"
            if not os.path.exists(path):
                os.makedirs(path)
            newfile = path + str(warn_number) + ".txt"
            f = open(newfile, "w+")
            f.write(t_punish)
            f.close()
            embed = discord.Embed(
                title='',
                description='The punishment for warn number **{}** has been set to **{}**'.format(
                    str(warn_number), t_punish),
                color=0x00FF00
            )
            await self.client.say(embed=embed)
        else:
            embed = discord.Embed(
                title='',
                description='You do not have permission to use this command.',
                color=0xFF0000
            )
            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def nickname(self, ctx, user: discord.Member, *, nick = None):
        author = ctx.message.author
        server = author.server
        if self.is_mod_or_perms(server, author):
            try:
                if nick == None:
                    embed = discord.Embed(
                        description = "test"
                    )
                await self.client.change_nickname(user, nick)
                embed = discord.Embed(
                    description="Changed {}'s nickname to **{}**".format(
                        user.mention, nick),
                    color=0x00FF00
                )
                await self.client.say(embed=embed)
            except ValueError:
                print("Error")
        else:
            embed = discord.Embed(
                description="You don't have permission to use this command",
                color=0xFF0000
            )
            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def removenick(self, ctx, user: discord.Member):
        author = ctx.message.author
        server = author.server
        if self.is_mod_or_perms(server, author):
            await self.client.change_nickname(user, None)
            embed = discord.Embed(
                description="Removed {}'s nickname.".format(user.mention),
                color=0x00FF00
            )
            await self.client.say(embed=embed)
        else:
            embed = discord.Embed(
                description="You don't have permission to use this command",
                color=0xFF0000
            )
            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def role(self, ctx, user: discord.Member, role):
        author = ctx.message.author
        server = ctx.message.channel.server
        if self.is_admin_or_perms(server, author):
            found_role = discord.utils.get(server.roles, name=role)
            if found_role == None:
                embed = discord.Embed(
                    description = "Role not found",
                    colour = 0xFF0000
                )
                await self.client.say(embed=embed)
            else:
                has_role = False
                user_roles = user.roles
                for role in user_roles:
                    if str(role) == str(found_role):
                        has_role = True
                if has_role == True:
                    await self.client.remove_roles(user, found_role)
                    embed = discord.Embed(
                        description = "The role **{}** has been removed from {}".format(str(found_role), user.mention),
                        color = 0x00FF00
                    )
                    await self.client.say(embed=embed)
                else:
                    await self.client.add_roles(user, found_role)
                    embed = discord.Embed(
                        description = "{} has been given the role **{}**".format(user.mention, str(found_role)),
                        colour = 0x00FF00
                    )
                    await self.client.say(embed=embed)
        else:
            embed = discord.Embed(
                description = "You don't have permission to use this command",
                colour = 0xFF0000
            )
            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def announce(self, ctx, u_channel: discord.Channel, *, message=None):
        author = ctx.message.author
        server = ctx.message.server
        channel = ctx.message.channel
        if message == None:
            await self.client.say("Please type a message")
            return

        ModAllowed = self.check_database(server, "CanModAnnounce")
        if ModAllowed == False:
            if self.is_mod_or_perms(server, author):
                embed = discord.Embed(
                    description="Who do you wish to tag? [everyone / here / None]",
                    color=0xFFA500
                )
                await self.client.send_message(channel, embed=embed)
                user_response = await self.client.wait_for_message(timeout=30, channel=channel, author=author)
                if user_response.clean_content.lower() == "everyone":
                    embed = discord.Embed(
                        description="Do you want your message to be inside an embed? (Yes/No)",
                        color=0xFFA500
                    )
                    await self.client.send_message(channel, embed=embed)
                    user_response2 = await self.client.wait_for_message(timeout=30, channel=channel, author=author)
                    if user_response2.clean_content.lower() == "yes":
                        embed = discord.Embed(
                            description="{}".format(str(message)),
                            color=0xFFA500
                        )
                        embed.set_author(name=author.name,
                                         icon_url=author.avatar_url)
                        await self.client.send_message(u_channel, "@everyone")
                        await self.client.send_message(u_channel, embed=embed)
                    elif user_response2.clean_content.lower() == "no":
                        await self.client.send_message(u_channel, "@everyone")
                        await self.client.send_message(u_channel, str(message))
                    else:
                        await self.client.say("Invalid.")
                        return
                elif user_response.clean_content.lower() == "here":
                    embed = discord.Embed(
                        description="Do you want your message to be inside an embed? (Yes/No)",
                        color=0xFFA500
                    )
                    await self.client.send_message(channel, embed=embed)
                    user_response2 = await self.client.wait_for_message(timeout=30, channel=channel, author=author)
                    if user_response2.clean_content.lower() == "yes":
                        embed = discord.Embed(
                            description="{}".format(str(message)),
                            color=0xFFA500
                        )
                        embed.set_author(name=author.name,
                                         icon_url=author.avatar_url)
                        await self.client.send_message(u_channel, "@here")
                        await self.client.send_message(u_channel, embed=embed)
                    elif user_response2.clean_content.lower() == "no":
                        await self.client.send_message(u_channel, "@here")
                        await self.client.send_message(u_channel, str(message))
                    else:
                        await self.client.say("Invalid.")
                        return
                elif user_response.clean_content.lower() == "none":
                    embed = discord.Embed(
                        description="Do you want your message to be inside an embed? (Yes/No)",
                        color=0xFFA500
                    )
                    await self.client.send_message(channel, embed=embed)
                    user_response2 = await self.client.wait_for_message(timeout=30, channel=channel, author=author)
                    if user_response2.clean_content.lower() == "yes":
                        embed = discord.Embed(
                            description="{}".format(str(message)),
                            color=0xFFA500
                        )
                        embed.set_author(name=author.name,
                                         icon_url=author.avatar_url)
                        await self.client.send_message(u_channel, embed=embed)
                    elif user_response2.clean_content.lower() == "no":
                        await self.client.send_message(u_channel, str(message))
                    else:
                        await self.client.say("Invalid.")
                        return
                else:
                    await self.client.say("Invalid.")
                    return

            else:
                embed = discord.Embed(
                    title="Permission Denied",
                    description="You don't have permission to use this command {}".format(ctx.message.author.mention),
                    color=0xFF0000
                )

                await self.client.send_message(channel, embed=embed)

        elif ModAllowed == True:
            print("no")
        else:
            print("Error")

    @commands.command(pass_context=True)
    async def kick(self, ctx, user: discord.Member, *, reason=None):
        author = ctx.message.author
        server = author.server
        if self.is_admin_or_perms(server, author):
            if author == user:
                embed = discord.Embed(
                    title="Kick",
                    description="You cannot kick youself",
                    color=0xFF0000
                )
                await self.client.say(embed=embed)
                return

            elif self.is_allowed_by_hierarchy(server, author, user):
                embed = discord.Embed(
                    title="Kick",
                    description="You cannot kick somebody higher than youself",
                    color=0xFF0000
                )
                await self.client.say(embed=embed)
                return
            try:
                await self.client.kick(user)
                if reason == None:
                    embed = discord.Embed(
                        title="User Kicked",
                        color=0x0000FF
                    )
                    embed.set_author(name="Mr. X", icon_url="https://cdn.discordapp.com/avatars/472817090785705985/b5318faf95792ae0a80ddb2e117e7ab7.png?size=128")
                    embed.add_field(name="User", value=user, inline=False)
                    await self.client.say(embed=embed)
                    await self.client.send_message(user, "You have been kicked from **{}**".format(server))
                else:
                    embed = discord.Embed(
                        title="User Kicked",
                        color=0x0000FF
                    )
                    embed.set_author(name="Mr. X", icon_url="https://cdn.discordapp.com/avatars/472817090785705985/b5318faf95792ae0a80ddb2e117e7ab7.png?size=128")
                    embed.add_field(name="User", value=user, inline=False)
                    embed.add_field(name="Reason", value=reason, inline=False)
                    await self.client.say(embed=embed)
                    await self.client.send_message(user, "You have been kicked from **{}** for the reason **{}**".format(server, reason))
            except discord.Forbidden:
                embed = discord.Embed(
                    title="Kick",
                    description="I don't have permissions to kick that user",
                    color=0xFF0000
                )
                await self.client.say(embed=embed)
            except Exception as e:
                print(e)
        else:
            embed = discord.Embed(
                description="You don't have permission to use this command",
                color=0xFF0000
            )
            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def ban(self, ctx, user: discord.Member, *, reason=None):
        author = ctx.message.author
        server = ctx.message.server
        if self.is_admin_or_perms(server, author):
            if author == user:
                embed = discord.Embed(
                    description="You can't ban youself",
                    color=0xFF0000
                )
                await self.client.say(embed=embed)
                return

            elif self.is_allowed_by_hierarchy(server, author, user):
                embed = discord.Embed(
                    description="You can't ban somebody higher than youself",
                    color=0xFF0000
                )
                await self.client.say(embed=embed)
                return

            try:
                await self.client.ban(user)
                if reason == None:
                    embed = discord.Embed(
                        title="User Banned",
                        color=0x0000FF
                    )
                    embed.set_author(
                        name="Mr. X", icon_url="https://cdn.discordapp.com/avatars/472817090785705985/b5318faf95792ae0a80ddb2e117e7ab7.png?size=128")
                    embed.add_field(name="User", value=user, inline=False)
                    await self.client.say(embed=embed)
                    await self.client.send_message(user, "You have been banned from `{}`".format(server))
                else:
                    embed = discord.Embed(
                        title="User Banned",
                        color=0x0000FF
                    )
                    embed.set_author(
                        name="Mr. X", icon_url="https://cdn.discordapp.com/avatars/472817090785705985/b5318faf95792ae0a80ddb2e117e7ab7.png?size=128")
                    embed.add_field(name="User", value=user, inline=False)
                    embed.add_field(name="Reason", value=reason, inline=False)
                    await self.client.say(embed=embed)
                    await self.client.send_message(user, "You have been banned from `{}` for the reason `{}`".format(server, reason))
            except discord.Forbidden:
                await self.client.kick(user)
                embed = discord.Embed(
                    description="I don't have permissions to ban that user",
                    color=0xFF0000
                )
                await self.client.say(embed=embed)
            except Exception as e:
                print(e)
        else:
            embed = discord.Embed(
                description="You don't have permission to use this command",
                color=0xFF0000
            )
            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def banid(self, ctx, id):
        is_id = False
        author = ctx.message.author
        server = ctx.message.server
        if self.is_admin_or_perms(server, author):
            try:
                int(id)
                is_id = True
            except ValueError:
                is_id = False

            if is_id:
                if author.server_permissions.ban_members:
                    await self.client.ban(server.get_member(id))
                    embed = discord.Embed(
                        description="The user with the id **{}** has been banned".format(
                            id),
                        color=0x00FF00
                    )
                    await self.client.say(embed=embed)
                else:
                    embed = discord.Embed(
                        description="You do not have the required permissions",
                        color=0x00FF00
                    )
                    await self.client.say(embed=embed)
            else:
                embed = discord.Embed(
                    description="Please enter a userID",
                    color=0xFF0000
                )
                await self.client.say(embed=embed)
        else:
            embed = discord.Embed(
                description="You don't have permission to use this command",
                color=0xFF0000
            )
            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def unban(self, ctx, userID):
        author = ctx.message.author
        server = author.server
        if author.server_permissions.ban:
            self.client.unban(server, userID)

    @commands.command(pass_context=True)
    async def mute(self, ctx, user: discord.Member, lenght="0m"):
        author = ctx.message.author
        server = author.server
        if self.is_mod_or_perms(server, author):
            if "m" in lenght:
                print("He wrote it in minutes")
                t_time = lenght.replace("m", "")
                time_type = "m"
                if int(t_time) == 0:
                    time = 0
                else:
                    time = int(t_time)*60

            elif "h" in lenght:
                t_time = lenght.replace("h", "")
                time_type = "h"
                if int(t_time) == 0:
                    time = 0
                else:
                    time = int(t_time)*3600
            else:
                await self.client.say("Please use minutes or hours, example: -mute @user 20m")
                return
            get_role = self.check_database(server, "Mute_Role")
            mutedrole = discord.utils.get(server.roles, name=get_role)
            if mutedrole == None:
                await self.client.say("No mute role is set, please use >muterole ROLE_NAME")
                return
            userroles = user.roles
            path = "servers/" + str(server.id) + "/muted/"
            if not os.path.exists(path):
                os.makedirs(path)
            mutepath = path + str(user.id) + ".txt"
            f = open(mutepath, "w+")
            for role in userroles:
                if str(role) != "@everyone":
                    usrole = str(role)
                    write = usrole + "\n"
                    f.write(write)
            f.close()
            await self.client.replace_roles(user, mutedrole)
            if time != 0:
                if time_type == "m":
                    embed = discord.Embed(
                    title = "",
                    description = "{} Has been muted for {} minute(s)".format(user.mention, str(t_time)),
                    colour = 0x00FF00
                    )
                    await self.client.say(embed=embed)
                    await asyncio.sleep(time)
                    path = "servers/" + str(server.id) + "/muted/" + str(user.id) + ".txt"
                    with open(path) as fp:
                       line = fp.readline()
                       roles_to_give = []
                       while line:
                           role = discord.utils.get(server.roles, name=line.strip())
                           roles_to_give.append(role)
                           line = fp.readline()
                       fp.close()
                    await self.client.replace_roles(user, *roles_to_give)
                    embed = discord.Embed(
                    title = "",
                    description = "{} Has been unmuted.".format(user.mention),
                    colour = 0x00FF00
                    )
                    await self.client.say(embed=embed)
                    os.remove(path)
                elif time_type == "h":
                    embed = discord.Embed(
                    title = "",
                    description = "{} Has been muted for {} hour(s)".format(user.mention, str(t_time)),
                    colour = 0x00FF00
                    )
                    await self.client.say(embed=embed)
                    await asyncio.sleep(time)
                    path = "servers/" + str(server.id) + "/muted/" + str(user.id) + ".txt"
                    with open(path) as fp:
                       line = fp.readline()
                       roles_to_give = []
                       while line:
                           role = discord.utils.get(server.roles, name=line.strip())
                           roles_to_give.append(role)
                           line = fp.readline()
                       fp.close()
                    await self.client.replace_roles(user, *roles_to_give)
                    embed = discord.Embed(
                    title = "",
                    description = "{} Has been unmuted.".format(user.mention),
                    colour = 0x00FF00
                    )
                    await self.client.say(embed=embed)
                    os.remove(path)

            else:
                embed = discord.Embed(
                title = "",
                description = "{} Has been muted.".format(user.mention),
                colour = 0x00FF00
                )
                await self.client.say(embed=embed)
        else:
            embed = discord.Embed(
            title = "",
            description = "You don't have permission to use this command",
            colour = 0xFF0000
            )
            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def muteid(self, ctx, userID, lenght="0m"):
        author = ctx.message.author
        server = author.server
        if self.is_mod_or_perms(server, author):
            user = server.get_member(userID)
            if "m" in lenght:
                print("He wrote it in minutes")
                t_time = lenght.replace("m", "")
                time_type = "m"
                if int(t_time) == 0:
                    time = 0
                else:
                    time = int(t_time)*60

            elif "h" in lenght:
                t_time = lenght.replace("h", "")
                time_type = "h"
                if int(t_time) == 0:
                    time = 0
                else:
                    time = int(t_time)*3600
            else:
                await self.client.say("Please use minutes or hours, example: -mute userID 20m")
                return
            get_role = self.check_database(server, "Mute_Role")
            mutedrole = discord.utils.get(server.roles, name=get_role)
            if mutedrole == None:
                await self.client.say("No mute role is set, please use >muterole ROLE_NAME")
                return
            userroles = user.roles
            path = "servers/" + str(server.id) + "/muted/"
            if not os.path.exists(path):
                os.makedirs(path)
            mutepath = path + str(user.id) + ".txt"
            f = open(mutepath, "w+")
            for role in userroles:
                if str(role) != "@everyone":
                    usrole = str(role)
                    write = usrole + "\n"
                    f.write(write)
            f.close()
            await self.client.replace_roles(user, mutedrole)
            if time != 0:
                if time_type == "m":
                    embed = discord.Embed(
                        description = "{} Has been muted for {} minute(s)".format(user.mention, str(t_time)),
                        colour = 0x00FF00
                    )
                    await self.client.say(embed=embed)
                    await asyncio.sleep(time)
                    path = "servers/" + str(server.id) + "/muted/" + str(user.id) + ".txt"
                    with open(path) as fp:
                       line = fp.readline()
                       roles_to_give = []
                       while line:
                           role = discord.utils.get(server.roles, name=line.strip())
                           roles_to_give.append(role)
                           line = fp.readline()
                       fp.close()
                    await self.client.replace_roles(user, *roles_to_give)
                    embed = discord.Embed(
                        description = "{} Has been unmuted.".format(user.mention),
                        colour = 0x00FF00
                    )
                    await self.client.say(embed=embed)
                    os.remove(path)
                elif time_type == "h":
                    embed = discord.Embed(
                        description = "{} Has been muted for {} hour(s)".format(user.mention, str(t_time)),
                        colour = 0x00FF00
                    )
                    await self.client.say(embed=embed)
                    await asyncio.sleep(time)
                    path = "servers/" + str(server.id) + "/muted/" + str(user.id) + ".txt"
                    with open(path) as fp:
                       line = fp.readline()
                       roles_to_give = []
                       while line:
                           role = discord.utils.get(server.roles, name=line.strip())
                           roles_to_give.append(role)
                           line = fp.readline()
                       fp.close()
                    await self.client.replace_roles(user, *roles_to_give)
                    embed = discord.Embed(
                        description = "{} Has been unmuted.".format(user.mention),
                        colour = 0x00FF00
                    )
                    await self.client.say(embed=embed)
                    os.remove(path)

            else:
                embed = discord.Embed(
                    description = "{} Has been muted.".format(user.mention),
                    colour = 0x00FF00
                )
                await self.client.say(embed=embed)
        else:
            embed = discord.Embed(
                description = "You don't have permission to use this command",
                colour = 0xFF0000
            )
            
            await self.client.say(embed=embed)
            
    @commands.command(pass_context=True)
    async def unmute(self, ctx, user: discord.Member):
        author = ctx.message.author
        server = author.server
        if self.is_mod_or_perms(server, author):
            setting = self.check_database(server, "Mute_Role")
            mutedrole = discord.utils.get(server.roles, name=setting)
            if mutedrole == None:
                await self.client.say("There is no mute role yet, please use **-muterole ROLE_NAME** to set it.")
                return
            else:
                path = "servers/" + str(server.id) + \
                    "/muted/" + str(user.id) + ".txt"
                if os.path.exists(path):
                    path = "servers/" + str(server.id) + \
                        "/muted/" + str(user.id) + ".txt"
                    with open(path) as fp:
                        line = fp.readline()
                        roles_to_give = []
                        while line:
                            role = discord.utils.get(
                                server.roles, name=line.strip())
                            roles_to_give.append(role)
                            line = fp.readline()
                        fp.close()
                    await self.client.replace_roles(user, *roles_to_give)
                    embed = discord.Embed(
                        description="{} has been unmuted".format(user.mention),
                        color=0x00FF00
                    )
                    await self.client.say(embed=embed)
                    os.remove(path)
                else:
                    print("This user is not muted")
        else:
            embed = discord.Embed(
                description="You don't have permission to use this command",
                color=0xFF0000
            )
            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def unmuteid(self, ctx, userID):
        author = ctx.message.author
        server = author.server
        user = server.get_member(userID)
        if self.is_mod_or_perms(server, author):
            setting = self.check_database(server, "Mute_Role")
            mutedrole = discord.utils.get(server.roles, name=setting)
            if mutedrole == None:
                await self.client.say("There is no mute role yet, please use **-muterole ROLE_NAME** to set it.")
                return
            else:
                path = "servers/" + str(server.id) + \
                    "/muted/" + str(user.id) + ".txt"
                if os.path.exists(path):
                    path = "servers/" + str(server.id) + \
                        "/muted/" + str(user.id) + ".txt"
                    with open(path) as fp:
                        line = fp.readline()
                        roles_to_give = []
                        while line:
                            role = discord.utils.get(
                                server.roles, name=line.strip())
                            roles_to_give.append(role)
                            line = fp.readline()
                        fp.close()
                    await self.client.replace_roles(user, *roles_to_give)
                    embed = discord.Embed(
                        description="{} has been unmuted".format(user.mention),
                        color=0x00FF00
                    )
                    await self.client.say(embed=embed)
                    os.remove(path)
                else:
                    print("This user is not muted")
        else:
            embed = discord.Embed(
                description="You don't have permission to use this command",
                color=0xFF0000
            )
            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def clear(self, ctx, amount=100, user: discord.Member = None):
        author = ctx.message.author
        server = author.server
        if self.is_admin_or_perms(server, author):
            channel = ctx.message.channel
            try:
                if amount < 2:
                    embed = discord.Embed(
                        title="Clear",
                        description="The amount can't be less than 2",
                        color=0xFF0000
                    )
                    await self.client.say(embed=embed)
                elif amount > 100:
                    embed = discord.Embed(
                        title="Clear",
                        description="You can't clear more than 100 messages.",
                        color=0xFF0000
                    )
                    await self.client.say(embed=embed)
                else:
                    if user == None:
                        await self.client.purge_from(channel, limit=int(amount))
                    else:
                        def is_user(m):
                            return m.author == user

                        await self.client.purge_from(channel, limit=int(amount), check=is_user)
            except:
                embed = discord.Embed(
                    title="Clear",
                    description="You can't clear messages that's older then 14 days",
                    color=0xFF0000
                )
                await self.client.say(embed=embed)
        else:
            embed = discord.Embed(
                description="You don't have permission to use this command",
                color=0xFF0000
            )

            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def dinvites(self, ctx):
        author = ctx.message.author
        server = author.server
        if author.server_permissions.administrator:
            invites = await self.client.invites_from(server)
            for inv in invites:
                await self.client.delete_invite(inv)

            embed = discord.Embed(
                description = "All of the invites has been deleted",
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
    async def blacklist(self, ctx, setting = None, user: discord.Member = None):
        author = ctx.message.author
        server = ctx.message.server
        if self.is_admin_or_perms(server, author):
            if setting == None:
                embed = discord.Embed(
                description="You have not entered a setting",
                color=0xFF0000
                )
                await self.client.say(embed=embed)
                return
            elif user == None:
                embed = discord.Embed(
                description="You have not selected an user to blacklist",
                color=0xFF0000
                )
                await self.client.say(embed=embed)
                return
            else:
                if setting.lower() == "nsfw":
                    path = "blacklist/" + str(author.id) + ".json"
                    if not os.path.exists(path):
                        with open(path, 'w+') as f:
                            json_data = {}
                            json_data[server.id] = {}
                            json_data[server.id]["NSFW"] = True
                            json.dump(json_data, f)
                        embed = discord.Embed(
                            description="User has been blacklisted from **NSFW**",
                            color=0xFF0000
                        )
                        await self.client.say(embed=embed)
                        return
                    else:
                        with open(path, 'r') as f:
                            blacklistcheck = json.load(f)
                            if str(server.id) in blacklistcheck:
                                current = blacklistcheck[server.id]["NSFW"]
                                if current == True:
                                    blacklistcheck[server.id]["NSFW"] = False
                                    with open(path, 'w') as f:
                                        json.dump(blacklistcheck, f)
                                    embed = discord.Embed(
                                        description="User has been unblacklisted from **NSFW**",
                                        color=0xFF0000
                                    )
                                    await self.client.say(embed=embed)
                                    return
                                else:
                                    blacklistcheck[server.id]["NSFW"] = True
                                    with open(path, 'w') as f:
                                        json.dump(blacklistcheck, f)
                                    embed = discord.Embed(
                                        description="User has been blacklisted from **NSFW**",
                                        color=0xFF0000
                                    )
                                    await self.client.say(embed=embed)
                                    return

                            else:
                                blacklistcheck[server.id] = {}
                                blacklistcheck[server.id]["NSFW"] = True
                                with open(path, 'w') as f:
                                    json.dump(blacklistcheck, f)
                    
        else:
            embed = discord.Embed(
                description="You don't have permission to use this command",
                color=0xFF0000
            )

            await self.client.say(embed=embed)
            


def setup(client):
    client.add_cog(Admin(client))
