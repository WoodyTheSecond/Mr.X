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

    def ValidInt(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False
    
    def update_setting(self, server, setting, value):
        settingspath = "servers/{}/settings.json".format(server.id)
        if not setting in open(settingspath, "r").read():
            print("No such setting found")
            return None

        with open(settingspath, "r") as f:
            if value == True:
                value = 1
            elif value == False:
                value = 0

            json_data = json.load(f)
            with open(settingspath, "w") as f:
                json_data[setting] = value
                json.dump(json_data, f)

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

    def is_serverowner(self, server, user):
        if user.id == server.owner.id:
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
            #User Warn Uploaded To Database
            conn = pymysql.connect(host="sql7.freesqldatabase.com", user="sql7257339", password="yakm4fsd4T", db="sql7257339")
            c = conn.cursor()
            sql = "INSERT INTO `Warn_Table` (serverid, userid, reason) VALUES ('{}', '{}', '{}')".format(str(server.id), str(user.id), reason)
            c.execute(sql)
            conn.commit()
            #Fetching All User Warnings
            sql = "SELECT * FROM `Warn_Table` WHERE serverid = '{}' AND userid = '{}'".format(str(server.id), str(user.id))
            c.execute(sql)
            conn.commit()
            data = c.fetchall()
            current_warnings = len(data)
            sql = "SELECT * FROM `Punishment_Table` WHERE serverid = '{}' AND warn_number = '{}'".format(str(server.id), str(current_warnings))
            c.execute(sql)
            conn.commit()
            data = c.fetchall()
            print(int(len(data)))
            if int(len(data)) == 1:
                for d in data:
                    warn_type = d[3]
                if warn_type == "mute":
                    mute_lenght = self.check_setting(server, "WarnMute")
                    if "m" in mute_lenght:
                        t_time = mute_lenght.replace("m", "")
                        time_type = "m"
                        if int(t_time) == 0:
                            time = 0
                        else:
                            time = int(t_time)*60

                    elif "h" in mute_lenght:
                        t_time = mute_lenght.replace("h", "")
                        time_type = "h"
                        if int(t_time) == 0:
                            time = 0
                        else:
                            time = int(t_time)*3600
                    else:
                        time_type = "h"
                        time = 7200
                    get_role = self.check_setting(server, "Mute_Role")
                    mutedrole = discord.utils.get(server.roles, name=get_role)
                    if mutedrole == None:
                        await self.client.say("Tried to mute user for reaching warning threshold, but found no muterole")
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
                    try:
                        await self.client.replace_roles(user, mutedrole)
                    except discord.Forbidden:
                        embed = discord.Embed(
                            description = "Missing permissions",
                            color = 0xFF0000
                        )
                        await self.client.say(embed=embed)
                    if time != 0:
                        if time_type == "m":
                            embed = discord.Embed(
                                description="{} has been muted for **{}** minute(s) for reaching the warning threshold".format(user.mention, t_time),
                                color=0x00FF00
                            )
                            await self.client.say(embed=embed)
                            if self.check_setting(server, "DMWarn") == True:
                                embed = discord.Embed(
                                    description="You have been muted for **{}** minute(s) for reaching the warning threshold in {}".format(t_time, server.name),
                                    color=0x00FF00
                                )
                                await self.client.send_message(user, embed=embed)

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
                            try:
                                await self.client.replace_roles(user, *roles_to_give)
                            except discord.Forbidden:
                                embed = discord.Embed(
                                    description = "Missing permissions",
                                    color = 0xFF0000
                                )
                                await self.client.say(embed=embed)
                            os.remove(path)
                        elif time_type == "h":
                            embed = discord.Embed(
                                description="{} has been muted for **{}** hour(s) for reaching the warning threshold".format(user.mention, t_time),
                                color=0x00FF00
                            )
                            await self.client.say(embed=embed)
                            if self.check_setting(server, "DMWarn") == True:
                                embed = discord.Embed(
                                    description="You have been muted for **{}** hour(s) for reaching the warning threshold in {}".format(t_time, server.name),
                                    color=0x00FF00
                                )
                                await self.client.send_message(user, embed=embed)

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
                            try:
                                await self.client.replace_roles(user, *roles_to_give)
                            except discord.Forbidden:
                                embed = discord.Embed(
                                    description = "Missing permissions",
                                    color = 0xFF0000
                                )
                                await self.client.say(embed=embed)
                            os.remove(path)
                elif warn_type == "kick":
                    try:
                        embed = discord.Embed(
                            description="{} has been kicked for reaching the warning threshold",
                            color=0x00FF00
                        )
                        await self.client.say(embed=embed)
                        if self.check_setting(server, "DMWarn") == True:
                            embed = discord.Embed(
                                description="You have been kicked for reaching the warning threshold in {}".format(server.name),
                                color=0x00FF00
                            )
                            await self.client.send_message(user, embed=embed)

                        await self.client.kick(user)
                    except discord.Forbidden:
                        embed = discord.Embed(
                            description = "Missing permissions",
                            color = 0xFF0000
                        )
                        await self.client.say(embed=embed)
                elif warn_type == "ban":
                    try:
                        embed = discord.Embed(
                            description="{} has been banned for reaching the warning threshold".format(user.mention),
                            color=0x00FF00
                        )
                        await self.client.say(embed=embed)
                        if self.check_setting(server, "DMWarn") == True:
                            embed = discord.Embed(
                                description="You have been banned for reaching the warning threshold in {}".format(server.name),
                                color=0x00FF00
                            )
                            await self.client.send_message(user, embed=embed)

                        await self.client.ban(user)
                    except discord.Forbidden:
                        embed = discord.Embed(
                            description = "Missing permissions",
                            color = 0xFF0000
                        )
                        await self.client.say(embed=embed)
            else:
                if reason == "No Reason Given":
                    embed = discord.Embed(
                        description="{} has been warned".format(user.mention),
                        color=0x00FF00
                    )

                    await self.client.say(embed=embed)
                    
                    if self.check_setting(server, "DMWarn") == True:
                        embed = discord.Embed(
                            description="You have been warned in `{}`".format(server.name),
                            color=0x00FF00
                        )

                        await self.client.send_message(user, embed=embed)
                else:
                    embed = discord.Embed(
                        description="{} has been warned with the reason **{}**".format(user.mention, reason),
                        color=0x00FF00
                    )

                    if self.check_setting(server, "DMWarn") == True:
                        await self.client.say(embed=embed)
                        embed = discord.Embed(
                            description="You have been warned with the reason **{}** in `{}`".format(reason, server.name),
                            color=0x00FF00
                        )

                        await self.client.send_message(user, embed=embed)

                return
            
            print(len(data))
            conn.close()
                                                                                       
        else:
            embed = discord.Embed(
                description="You don't have permission to use this command",
                color=0xFF0000
            )

            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def warns(self, ctx, user: discord.Member = None):
        author = ctx.message.author
        server = author.server

        conn = pymysql.connect(host="sql7.freesqldatabase.com", user="sql7257339", password="yakm4fsd4T", db="sql7257339")
        c = conn.cursor()

        if user == None:
            sql = "SELECT * FROM `Warn_Table` WHERE serverid = '{}' AND userid = '{}'".format(str(server.id), str(author.id))
            c.execute(sql)
            conn.commit()
            data = c.fetchall()
            warnnumber = 1
            postedten = False

            if len(data) == 0:
                embed = discord.Embed(
                    title = "Your warnings",
                    description = "No warnings",
                    color = 0x00FF00
                )

                await self.client.say(embed=embed)
            else:
                embed = discord.Embed(
                    title = "Your warnings",
                    color = 0x00FF00
                )

                for warn in data:
                    if warnnumber == 10:
                        if postedten == False:
                            if len(data) > 10:
                                embed.add_field(name="Warning {}".format(warnnumber), value="{}\n\n**{} more warning(s)**".format(warn[3], len(data) - 10), inline=False)
                            else:
                                embed.add_field(name="Warning {}".format(warnnumber), value="{}".format(warn[3]), inline=False)
                            
                            postedten = True
                    else:
                        embed.add_field(name="Warning {}".format(warnnumber), value="{}".format(warn[3]), inline=False)
                        warnnumber += 1

                await self.client.say(embed=embed)
        else:
            sql = "SELECT * FROM `Warn_Table` WHERE serverid = '{}' AND userid = '{}'".format(str(server.id), str(user.id))
            c.execute(sql)
            conn.commit()
            data = c.fetchall()
            warnnumber = 1

            if len(data) == 0:
                embed = discord.Embed(
                    title = "{} Warnings".format(str(user)),
                    description = "No warnings",
                    color = 0x00FF00
                )

                await self.client.say(embed=embed)
            else:
                embed = discord.Embed(
                    title = "{} Warnings".format(str(user)),
                    color = 0x00FF00
                )

                for warn in data:
                    embed.add_field(name="Warning {}".format(warnnumber), value="{}".format(warn[3]), inline=False)
                    warnnumber += 1

                await self.client.say(embed=embed)

        conn.close()

    @commands.command(pass_context=True)
    async def clearwarns(self, ctx, user: discord.Member = None):
        server = ctx.message.author.server
        author = ctx.message.author
        if self.is_admin_or_perms(server, author):
            if user == None:
                embed = discord.Embed(
                    description="You didn't write any user",
                    color=0xFF0000
                )

                await self.client.say(embed=embed)
                return

            conn = pymysql.connect(host="sql7.freesqldatabase.com", user="sql7257339", password="yakm4fsd4T", db="sql7257339")
            c = conn.cursor()
            sql = "DELETE FROM `Warn_Table` WHERE serverid = '{}' AND userid = '{}'".format(server.id, user.id)
            c.execute(sql)
            conn.commit()
            conn.close()
            embed = discord.Embed(
                description="{} Warnings has been removed".format(user.mention),
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
    async def verify(self, ctx, user: discord.Member = None, *, role_name = None):
        author = ctx.message.author
        server = author.server
        if self.is_admin_or_perms(server, author):
            verifyrole_name = self.check_setting(server, "Verify_Role")
            verifyrole = discord.utils.get(server.roles, name=verifyrole_name)
            if role_name == None:
                if verifyrole != None:
                    try:
                        await self.client.add_roles(user, verifyrole)
                        embed = discord.Embed(
                            description="{} has been verified".format(
                                user.mention),
                            color=0x00FF00
                        )
                        await self.client.say(embed=embed)
                    except discord.Forbidden:
                        embed = discord.Embed(
                            description = "Missing permissions",
                            color = 0xFF0000
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
                    try:
                        await self.client.replace_roles(user, *roles_to_give)
                        embed = discord.Embed(
                            description="{} has been verified and given the role **{}**".format(
                                user.mention, role_name),
                            color=0x00FF00
                        )
                        await self.client.say(embed=embed)
                    except discord.Forbidden:
                        embed = discord.Embed(
                            description = "Missing permissions",
                            color = 0xFF0000
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
    async def setwarn(self, ctx, warn_number = None, punishment = None):
        author = ctx.message.author
        server = author.server
        if self.is_owner(author):
            if self.ValidInt(warn_number) == False:
                embed = discord.Embed(
                    description='Please enter a valid integer',
                    color=0xFF0000
                )
                await self.client.say(embed=embed)  
                return

            elif punishment == None:
                embed = discord.Embed(
                    description='Please enter a punishment',
                    color=0xFF0000
                )
                await self.client.say(embed=embed)  
                return

            elif punishment.lower() != "mute" and punishment.lower() != "ban" and punishment.lower() != "kick":
                embed = discord.Embed(
                    description='Please enter a valid punishment [mute/kick/ban]',
                    color=0xFF0000
                )
                await self.client.say(embed=embed)  
                return

            else:
                conn = pymysql.connect(host="sql7.freesqldatabase.com", user="sql7257339", password="yakm4fsd4T", db="sql7257339")
                c = conn.cursor()
                sql = "SELECT * FROM `Punishment_Table` WHERE serverid = '{}' AND warn_number = '{}'".format(str(server.id), str(warn_number))
                c.execute(sql)
                conn.commit()
                data = c.fetchall()
                if len(data) == 1:
                    sql = "UPDATE `Punishment_Table` SET warn_number = '{}', punishment = '{}' WHERE serverid = '{}' AND warn_number = '{}'".format(warn_number, punishment, server.id, warn_number)
                    c.execute(sql)
                    conn.commit()
                    conn.close()
                    embed = discord.Embed(
                        description='Warning number **{}** will now result in **{}**'.format(str(warn_number), str(punishment)),
                        color=0X00FF00
                    )
                    await self.client.say(embed=embed)  
                    return

                else:
                    sql = "INSERT INTO `Punishment_Table` (serverid, warn_number, punishment) VALUES ('{}', '{}', '{}')".format(str(server.id), str(warn_number), str(punishment).lower())
                    c.execute(sql)
                    conn.commit()
                    conn.close()
                    embed = discord.Embed(
                        description='Warning number **{}** will now result in **{}**'.format(str(warn_number), str(punishment)),
                        color=0X00FF00
                    )
                    await self.client.say(embed=embed)  
                    return
                
        else:
            embed = discord.Embed(
                title='',
                description='You do not have permission to use this command.',
                color=0xFF0000
            )
            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def removewarn(self, ctx, number = None):
        author = ctx.message.author
        server = author.server
        if self.is_owner(author) or self.is_serverowner(server, author):
            if number == None:
                embed = discord.Embed(
                    description="You need to write a warn number",
                    color=0xFF0000
                )
                
                await self.client.say(embed=embed)
                return

            if self.ValidInt(number) == False:
                embed = discord.Embed(
                    description="You need to write a number",
                    color=0xFF0000
                )
                
                await self.client.say(embed=embed)
                return

            conn = pymysql.connect(host="sql7.freesqldatabase.com", user="sql7257339", password="yakm4fsd4T", db="sql7257339")
            c = conn.cursor()
            sql = "DELETE FROM `Punishment_Table` WHERE serverid = '{}' AND warn_number = '{}'".format(server.id, number)
            c.execute(sql)
            conn.commit()
            conn.close()
            embed = discord.Embed(
                description = "You have successfully removed the punishment for warn number **{}**".format(number),
                color = 0x00FF00
            )
            
            await self.client.say(embed=embed)
        else:
            embed = discord.Embed(
                description = "You don't have permission to use this command",
                color = 0xFF0000
            )
            
            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def nickname(self, ctx, user: discord.Member, *, nick = None):
        author = ctx.message.author
        server = author.server
        if self.is_mod_or_perms(server, author):
            try:
                await self.client.change_nickname(user, nick)
                embed = discord.Embed(
                    description="Changed {}'s nickname to **{}**".format(
                        user.mention, nick),
                    color=0x00FF00
                )
                await self.client.say(embed=embed)
            except discord.Forbidden:
                embed = discord.Embed(
                    description = "Missing permissions",
                    color = 0xFF0000
                )
                await self.client.say(embed=embed)
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
            try:
                await self.client.change_nickname(user, None)
                embed = discord.Embed(
                    description="Removed {}'s nickname.".format(user.mention),
                    color=0x00FF00
                )
                await self.client.say(embed=embed)
            except discord.Forbidden:
                embed = discord.Embed(
                    description = "Missing permissions",
                    color = 0xFF0000
                )
                await self.client.say(embed=embed)
        else:
            embed = discord.Embed(
                description="You don't have permission to use this command",
                color=0xFF0000
            )
            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def role(self, ctx, user: discord.Member, *, role = None):
        author = ctx.message.author
        server = ctx.message.channel.server
        if self.is_admin_or_perms(server, author):
            if role == None:
                embed = discord.Embed(
                    description = "You need to write a role name",
                    colour = 0xFF0000
                )
                
                await self.client.say(embed=embed)
                return
                
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
                    try:
                        await self.client.remove_roles(user, found_role)
                        embed = discord.Embed(
                            description = "The role **{}** has been removed from {}".format(str(found_role), user.mention),
                            color = 0x00FF00
                        )
                        await self.client.say(embed=embed)
                    except discord.Forbidden:
                        embed = discord.Embed(
                            description = "Missing permissions",
                            color = 0xFF0000
                        )
                        await self.client.say(embed=embed)
                else:
                    try:
                        await self.client.add_roles(user, found_role)
                        embed = discord.Embed(
                            description = "{} has been given the role **{}**".format(user.mention, str(found_role)),
                            colour = 0x00FF00
                        )
                        await self.client.say(embed=embed)
                    except discord.Forbidden:
                        embed = discord.Embed(
                            description = "Missing permissions",
                            color = 0xFF0000
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

        ModAllowed = self.check_setting(server, "CanModAnnounce")
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
                        embed.set_author(name=author.name, icon_url=author.avatar_url)
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
                        embed.set_author(name=author.name, icon_url=author.avatar_url)
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
                        embed.set_author(name=author.name, icon_url=author.avatar_url)
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
                    description="You can't kick youself",
                    color=0xFF0000
                )
                await self.client.say(embed=embed)
                return

            elif self.is_allowed_by_hierarchy(server, author, user):
                embed = discord.Embed(
                    description="You can't kick somebody higher than youself",
                    color=0xFF0000
                )
                await self.client.say(embed=embed)
                return

            try:
                await self.client.kick(user)
                if reason == None:
                    embed = discord.Embed(
                        color=0x0000FF
                    )
                    embed.add_field(name="User", value=user, inline=False)
                    await self.client.say(embed=embed)
                    await self.client.send_message(user, "You have been kicked from **{}**".format(server))
                else:
                    embed = discord.Embed(
                        color=0x0000FF
                    )
                    embed.add_field(name="User", value=user, inline=False)
                    embed.add_field(name="Reason", value=reason, inline=False)
                    await self.client.say(embed=embed)
                    await self.client.send_message(user, "You have been kicked from **{}** for the reason **{}**".format(server, reason))
            except discord.Forbidden:
                embed = discord.Embed(
                    description="I don't have permissions to kick that user",
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
                    embed.add_field(name="User", value=user, inline=False)
                    await self.client.say(embed=embed)
                    await self.client.send_message(user, "You have been banned from `{}`".format(server))
                else:
                    embed = discord.Embed(
                        title="User Banned",
                        color=0x0000FF
                    )
                    embed.add_field(name="User", value=user, inline=False)
                    embed.add_field(name="Reason", value=reason, inline=False)
                    await self.client.say(embed=embed)
                    await self.client.send_message(user, "You have been banned from `{}` for the reason `{}`".format(server, reason))
            except discord.Forbidden:
                embed = discord.Embed(
                    description="I don't have permissions to ban that user",
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
            get_role = self.check_setting(server, "Mute_Role")
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
            get_role = self.check_setting(server, "Mute_Role")
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
            setting = self.check_setting(server, "Mute_Role")
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
            setting = self.check_setting(server, "Mute_Role")
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
                    try:
                        await self.client.purge_from(channel, limit=int(amount))
                    except discord.HTTPException:
                        embed = discord.Embed(
                            description="You can't delete messages that's older than 14 days",
                            color=0xFF0000
                        )
                        await self.client.say(embed=embed)
                else:
                    def is_user(m):
                        return m.author == user
                    
                    try:
                        await self.client.purge_from(channel, limit=int(amount), check=is_user)
                    except discord.HTTPException:
                        embed = discord.Embed(
                            description="You can't delete messages that's older than 14 days",
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
            try:
                invites = await self.client.invites_from(server)
                for inv in invites:
                    await self.client.delete_invite(inv)

                embed = discord.Embed(
                    description = "All of the invites has been deleted",
                    color = 0x00FF00
                )

                await self.client.say(embed=embed)
            except discord.Forbidden:
                embed = discord.Embed(
                    description = "Missing permissions",
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
            elif user == None:
                embed = discord.Embed(
                    description="You have not selected an user to blacklist",
                    color=0xFF0000
                )
                await self.client.say(embed=embed)
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
                                else:
                                    blacklistcheck[server.id]["NSFW"] = True
                                    with open(path, 'w') as f:
                                        json.dump(blacklistcheck, f)
                                    embed = discord.Embed(
                                        description="User has been blacklisted from **NSFW**",
                                        color=0xFF0000
                                    )
                                    await self.client.say(embed=embed)

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
