import discord
import asyncio
import time
import os
import json
from discord.ext.commands import Bot
from discord.ext import commands
from itertools import cycle
import sys
import checks
import pymysql
import random
from random import randint

TOKEN = os.getenv("TOKEN")
MYSQLHOST = os.getenv("MYSQLHOST")
MYSQLUSER = os.getenv("MYSQLUSER")
MYSQLPASS = os.getenv("MYSQLPASS")
MYSQLDB = os.getenv("MYSQLDB")
client = commands.Bot(command_prefix="-")
client.remove_command("help")
status = ["Commands: -help", "Watching you"]
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)
extensions = ["admin", "utility", "swarm", "nsfw", "fun"]


async def change_status():
    await client.wait_until_ready()
    msgs = cycle(status)

    while not client.is_closed:
        current_status = next(msgs)
        await client.change_presence(game=discord.Game(name=current_status))
        await asyncio.sleep(15)


def create_database(server):
    # conn = pymysql.connect(host="sql7.freesqldatabase.com", user="sql7257339", password="yakm4fsd4T", db="sql7257339")
    conn = pymysql.connect(host="{}".format(MYSQLHOST), user="{}".format(MYSQLUSER), password="{}".format(MYSQLPASS), db="{}".format(MYSQLDB))
    c = conn.cursor()
    sql = "INSERT INTO `Server_Settings` (serverid, Join_Role, DMWarn, Verify_Role, Mod_Role, Admin_Role, Mute_Role, WarnMute, JoinToggle, CanModAnnounce, Level_System, Chat_Filter, Ignore_Hierarchy, NSFW_role, NSFW_toggle, FunToggle, earn_cooldown) VALUES ('{}', 'None', '0', 'None', 'None', 'None', 'None', '0', '0', '0', '0', '0', '0', 'None', '0', '0', '0')".format(str(server.id))
    c.execute(sql)
    conn.commit()
    conn.close()


def update_database(server, setting, value):
    conn = pymysql.connect(host="{}".format(MYSQLHOST), user="{}".format(MYSQLUSER), password="{}".format(MYSQLPASS), db="{}".format(MYSQLDB))
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
    elif setting == "NSFW_role":
        sql = "UPDATE `Server_Settings` SET NSFW_role = %s where serverid = %s"
    elif setting == "NSFW_toggle":
        sql = "UPDATE `Server_Settings` SET NSFW_toggle = %s where serverid = %s"
    else:
        print("No such setting found")
        return

    t = (value, str(server.id))
    c.execute(sql, t)
    conn.commit()
    conn.close()


def check_database_multiple(conn, server, setting):
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


def check_database(server, setting):
    conn = pymysql.connect(host="{}".format(MYSQLHOST), user="{}".format(MYSQLUSER), password="{}".format(MYSQLPASS), db="{}".format(MYSQLDB))
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


def make_settings(server):
    conn = pymysql.connect(host="{}".format(MYSQLHOST), user="{}".format(MYSQLUSER), password="{}".format(MYSQLPASS), db="{}".format(MYSQLDB))
    c = conn.cursor()
    sql = "SELECT * FROM `Server_Settings` WHERE serverid = {}".format(str(server.id))
    c.execute(sql)
    conn.commit()
    data = c.fetchone()
    conn.close()
    if data == None:
        create_database(server)
        return True
    else:
        return False


def is_owner(user):
    if user.id == "164068466129633280" or user.id == "142002197998206976" or user.id == "457516809940107264":
        return True
    else:
        return False


@client.event
async def on_server_join(server):
    if make_settings(server) == True:
        print("The settings have been successfully created")
    else:
        print("The settings for this server already exists")


@client.event
async def on_ready():
    print("Bot is online.")


@client.event
async def on_member_join(member):
    server = member.server
    conn = pymysql.connect(host="{}".format(MYSQLHOST), user="{}".format(MYSQLUSER), password="{}".format(MYSQLPASS), db="{}".format(MYSQLDB))
    join_toggle = check_database_multiple(conn, server, "JoinToggle")
    join_role = check_database_multiple(conn, server, "Join_Role")
    conn.close()
    if join_toggle == True:
        role = discord.utils.get(server.roles, name=join_role)
        await client.add_roles(member, role)


@client.event
async def on_member_unban(server, member):
    with open("autobans.json", "r") as f:
        autobans = json.load(f)
        ban_array = autobans[server.id]["banlist"]

        for userid in ban_array:
            if userid == member.id:
                await client.ban(member)

    
@client.event
async def on_message(message):
    channel = message.channel
    help_check = extensions
    for check in help_check:
        if message.content.startswith("-help " + check):
            await client.send_message(channel, "Do not use -help {}, you just write the module | Example: -help | {}".format(check, check))
            return

    await client.process_commands(message)
    

@client.command()
async def botinfo():
    embed = discord.Embed(
        colour=0x00d2ff
    )
    embed.set_footer(text="Guess who?")
    r_int = randint(1, 4)
    if r_int == 1:
        embed.set_image(url='https://i.imgur.com/rfnR6nb.jpg')
    elif r_int == 2:
        embed.set_image(url='https://2static.fjcdn.com/pictures/Cute_38958d_6114906.jpg')
    elif r_int == 3:
        embed.set_image(url='https://2static.fjcdn.com/large/pictures/9a/8e/9a8e9f_6114906.jpg')
    else:
        embed.set_image(url='https://johnjohns1.fjcdn.com/large/pictures/de/e0/dee0cc_6114906.jpg')

    embed.set_author(name='Information')
    embed.add_field(name='Creator', value='Woody#3599 | C0mpl3X#8366', inline=False)
    embed.add_field(name='Artist', value='CSLucaris | https://www.deviantart.com/cslucaris', inline=False)
    embed.add_field(name='Version', value='0.5', inline=False)
    await client.say(embed=embed)


@client.command(pass_context=True)
async def settings(ctx):
    author = ctx.message.author
    server = author.server
    channel = ctx.message.channel

    conn = pymysql.connect(host="{}".format(MYSQLHOST), user="{}".format(MYSQLUSER), password="{}".format(MYSQLPASS), db="{}".format(MYSQLDB))

    Ignore_Hierarchy = str(check_database_multiple(
        conn, server, "Ignore_Hierarchy"))
    DMWarn = check_database_multiple(conn, server, "DMWarn")
    Verify_Role = check_database_multiple(conn, server, "Verify_Role")
    Mod_Role = check_database_multiple(conn, server, "Mod_Role")
    Join_Role = check_database_multiple(conn, server, "Join_Role")
    Admin_Role = check_database_multiple(conn, server, "Admin_Role")
    Mute_Role = check_database_multiple(conn, server, "Mute_Role")
    WarnMute = check_database_multiple(conn, server, "WarnMute")
    JoinToggle = str(check_database_multiple(conn, server, "JoinToggle"))
    CanModAnnounce = str(check_database_multiple(
        conn, server, "CanModAnnounce"))
    Level_System = str(check_database_multiple(conn, server, "Level_System"))
    conn.close()

    await client.say('Do you want the list **Inline** ? (Yes/No)')
    user_response = await client.wait_for_message(timeout=30, channel=channel, author=author)
    if user_response.clean_content == 'yes' or user_response.clean_content == 'Yes':
        inline = True
    elif user_response.clean_content == 'no' or user_response.clean_content == 'No':
        inline = False
    else:
        await client.say("Invalid.")
        return

    embed = discord.Embed(
        title='',
        description='',
        color=0x0000FF
    )

    if server.icon_url != "":
        embed.set_thumbnail(url=server.icon_url)

    embed.set_author(name='{} Server Settings'.format(
        server), icon_url='https://cdn.discordapp.com/avatars/472817090785705985/b5318faf95792ae0a80ddb2e117e7ab7.png?size=128')
    embed.add_field(name='Ignore Hierarchy',
                    value=Ignore_Hierarchy, inline=inline)
    embed.add_field(name='Direct message on warn', value=DMWarn, inline=inline)
    embed.add_field(name='Verify Role', value=Verify_Role, inline=inline)
    embed.add_field(name='Moderator Role', value=Mod_Role, inline=inline)
    embed.add_field(name='Join Role', value=Join_Role, inline=inline)
    embed.add_field(name='Administrator Role', value=Admin_Role, inline=inline)
    embed.add_field(name='Mute Role', value=Mute_Role, inline=inline)
    embed.add_field(name='Warning mute time', value=WarnMute, inline=inline)
    embed.add_field(name='Auto role on join', value=JoinToggle, inline=inline)
    embed.add_field(name='Can moderator announce',
                    value=CanModAnnounce, inline=inline)
    embed.add_field(name='Level system', value=Level_System, inline=inline)
    await client.say(embed=embed)


@client.command(pass_context=True)
async def mylevel(ctx):
    author = ctx.message.author
    conn = pymysql.connect(host='sql7.freesqldatabase.com',
                           user='sql7257339', password='yakm4fsd4T', db='sql7257339')
    c = conn.cursor()
    sql = "SELECT level from `user_levels` WHERE userid = {}".format(
        str(author.id))
    c.execute(sql)
    conn.commit()
    data = c.fetchone()
    conn.close()
    if data == None:
        conn = pymysql.connect(host='sql7.freesqldatabase.com',
                               user='sql7257339', password='yakm4fsd4T', db='sql7257339')
        c = conn.cursor()
        sql = "INSERT INTO `user_levels` VALUES ({}, '1', '0')".format(
            str(author.id))
        c.execute(sql)
        conn.commit()
        conn.close()
        # Finished creating user data.
        current_level = "1"
        embed = discord.Embed(
            description='You are currently level **{}**.'.format(
                current_level),
            colour=0x00FF00
        )
        await client.say(embed=embed)
    else:
        for row in data:
            current_level = row
        embed = discord.Embed(
            description='You are currently level **{}**.'.format(
                current_level),
            colour=0x00FF00
        )
        await client.say(embed=embed)


@client.command(pass_context=True)
async def togglelevel(ctx):
    author = ctx.message.author
    server = author.server
    if author == server.owner or author.id == 164068466129633280:
        toggle = check_database(server, "Level_System")
        if toggle == True:
            update_database(server, "Level_System", False)
            embed = discord.Embed(
                title="Global Level System",
                description='You have **disabled** the Level System on this server.',
                color=0x00FF00
            )
            await client.say(embed=embed)
        elif toggle == False:
            update_database(server, "Level_System", True)
            embed = discord.Embed(
                title="Global Level System",
                description="You have **enabled** the Level System on this server.",
                color=0x00FF00
            )
            await client.say(embed=embed)
        else:
            print("Error")
    else:
        embed = discord.Embed(
            description="You do know have permission to use this command",
            color=0xFF0000
        )
        await client.say(embed=embed)


@client.command(pass_context=True)
async def cmds(ctx):
    await client.say("Please use the -help command.")


@client.command(pass_context=True)
async def dmwarn(ctx):
    author = ctx.message.author
    server = ctx.message.server
    current = check_database(server, "DMWarn")
    if author.server_permissions.administrator:
        if current == True:
            update_database(server, "DMWarn", False)
            embed = discord.Embed(
                title='DMWarn Setting',
                description='Direct Message on warning has been set to **False**',
                color=0x00FF00
            )
            await client.say(embed=embed)
        else:
            embed = discord.Embed(
                title='DMWarn Setting',
                description='Direct Message on warning has been set to **True**',
                color=0x00FF00
            )
            await client.say(embed=embed)
            update_database(server, "DMWarn", True)
    else:
        embed = discord.Embed(
            title="DMWarn",
            description="You don't have permission to use this command",
            color=0xFF0000
        )
        await client.say(embed=embed)


@client.command(pass_context=True)
async def modrole(ctx, *, role = None):
    author = ctx.message.author
    server = ctx.message.server
    if author.server_permissions.administrator:
        if role == None:
            embed = discord.Embed(
                description="You have not entered a role name",
                color=0xFF0000
            )

            await client.say(embed=embed)
            return
        try:
            rolename = discord.utils.get(server.roles, name=role)
            newrole = str(rolename)
            update_database(server, "Mod_Role", newrole)
            embed = discord.Embed(
                title="Moderator Role",
                description="The Moderator Role has been set to **{}**".format(
                    rolename),
                color=0x00FF00
            )
            await client.say(embed=embed)
        except ValueError as error:
            print("{}".format(error))
    else:
        embed = discord.Embed(
            title="Moderator Role",
            description="You don't have permission to use this command",
            color=0xFF0000
        )
        await client.say(embed=embed)


@client.command(pass_context=True)
async def adminrole(ctx, *, role = None):
    author = ctx.message.author
    server = author.server
    if author.server_permissions.administrator:
        if role == None:
            embed = discord.Embed(
                description="You have not entered a role name",
                color=0xFF0000
            )
            await client.say(embed=embed)
            return
        try:
            rolename = discord.utils.get(server.roles, name=role)
            newrole = str(rolename)
            update_database(server, "Admin_Role", newrole)
            embed = discord.Embed(
                title="Administrator Role",
                description="The Administrator Role has been set to **{}**".format(
                    rolename),
                color=0x00FF00
            )
            await client.say(embed=embed)
        except ValueError as error:
            print("{}".format(error))
    else:
        embed = discord.Embed(
            description="You don't have permission to use this command",
            color=0xFF0000
        )
        await client.say(embed=embed)


@client.command(pass_context=True)
async def muterole(ctx, *, role = None):
    author = ctx.message.author
    server = ctx.message.server
    if author.server_permissions.administrator:
        if role == None:
                embed = discord.Embed(
                    description="You have not entered a role name",
                    color=0xFF0000
                )
                await client.say(embed=embed)
                return
        try:
            rolename = discord.utils.get(server.roles, name=role)
            newrole = str(rolename)
            update_database(server, "Mute_Role", newrole)
            embed = discord.Embed(
                title="Muted Role",
                description="The Muted Role has been set to **{}**".format(
                    rolename),
                color=0x00FF00
            )
            await client.say(embed=embed)
        except ValueError as error:
            print("{}".format(error))
    else:
        embed = discord.Embed(
            title="Muted Role",
            description="You don't have permission to use this command",
            color=0xFF0000
        )
        await client.say(embed=embed)


@client.command(pass_context=True)
async def joinrole(ctx, *, role = None):
    author = ctx.message.author
    server = ctx.message.server
    if author.server_permissions.administrator:
        if role == None:
                embed = discord.Embed(
                    description="You have not entered a role name",
                    color=0xFF0000
                )
                await client.say(embed=embed)
                return
        try:
            rolename = discord.utils.get(server.roles, name=role)
            newrole = str(rolename)
            if newrole == "None":
                embed = discord.Embed(
                    title="Join Role",
                    description="Role not found",
                    color=0xFF0000
                )
                await client.say(embed=embed)
            else:
                update_database(server, "Join_Role", newrole)
                embed = discord.Embed(
                    title="Join Role",
                    description="The Join Role has been set to **{}**".format(
                        rolename),
                    color=0x00FF00
                )
                await client.say(embed=embed)
        except ValueError as error:
            print("{}".format(error))
    else:
        embed = discord.Embed(
            title="Join Role",
            description="You don't have permission to use this command",
            color=0xFF0000
        )
        await client.say(embed=embed)

@client.command(pass_context=True)
async def nsfwrole(ctx, *, role = None):
    author = ctx.message.author
    server = ctx.message.server
    if author.server_permissions.administrator:
        if role == None:
                embed = discord.Embed(
                    description="You have not entered a role name",
                    color=0xFF0000
                )
                await client.say(embed=embed)
                return
        try:
            rolename = discord.utils.get(server.roles, name=role)
            newrole = str(rolename)
            if newrole == "None":
                embed = discord.Embed(
                    description="Role not found",
                    color=0xFF0000
                )
                await client.say(embed=embed)
            else:
                update_database(server, "NSFW_role", newrole)
                embed = discord.Embed(
                    description="The NSFW Role has been set to **{}**".format(
                        rolename),
                    color=0x00FF00
                )
                await client.say(embed=embed)
        except ValueError as error:
            print("{}".format(error))
    else:
        embed = discord.Embed(
            title="Join Role",
            description="You don't have permission to use this command",
            color=0xFF0000
        )
        await client.say(embed=embed)


@client.command(pass_context=True)
async def verifyrole(ctx, *, role = None):
    author = ctx.message.author
    server = ctx.message.server
    if author.server_permissions.administrator:
        if role == None:
                embed = discord.Embed(
                    description="You have not entered a role name",
                    color=0xFF0000
                )
                await client.say(embed=embed)
                return
        try:
            rolename = discord.utils.get(server.roles, name=role)
            newrole = str(rolename)
            if newrole == "None":
                embed = discord.Embed(
                    title="Verify Role",
                    description="Role not found",
                    color=0xFF0000
                )
                await client.say(embed=embed)
            else:
                update_database(server, "Verify_Role", newrole)
                embed = discord.Embed(
                    title="Verify Role",
                    description="The Verify Role has been set to **{}**".format(
                        rolename),
                    color=0x00FF00
                )
                await client.say(embed=embed)
        except ValueError as error:
            print("{}".format(error))
    else:
        embed = discord.Embed(
            title='Verify Role',
            description="You don't have permission to use this command",
            color=0xFF0000
        )
        await client.say(embed=embed)


@client.command(pass_context=True)
async def mutetime(ctx, lenght = None):
    author = ctx.message.author
    server = author.server
    if author.server_permissions.administrator:
        if lenght == None:
            embed = discord.Embed(
            description="You have not entered a lenght",
            color=0xFF0000
            )
            await client.say(embed=embed)
            return

        if "m" in lenght:
            t_time = lenght.replace("m", "")
            update_database(server, "WarnMute", str(lenght))
            embed = discord.Embed(
                title="Mute Time",
                description="Punish Mute has been set to **{}** minute(s)".format(
                    t_time),
                color=0x00FF00
            )
            await client.say(embed=embed)
        elif "h" in lenght:
            t_time = lenght.replace("h", "")
            update_database(server, "WarnMute", str(lenght))
            embed = discord.Embed(
                title="Mute Time",
                description="Punish Mute has been set to **{}** hour(s)".format(
                    t_time),
                color=0x00FF00
            )
            await client.say(embed=embed)
        else:
            await client.say("Please use minutes or hours, example: -mutetime 1h")
            return
    else:
        embed = discord.Embed(
            title="Mute Time",
            description="You don't have permission to use this command",
            color=0xFF0000
        )
        await client.say(embed=embed)


@client.command(pass_context=True)
async def jointoggle(ctx):
    author = ctx.message.author
    server = ctx.message.server
    conn = pymysql.connect(host="{}".format(MYSQLHOST), user="{}".format(MYSQLUSER), password="{}".format(MYSQLPASS), db="{}".format(MYSQLDB))
    current_toggle = check_database_multiple(conn, server, "JoinToggle")
    join_role = check_database_multiple(conn, server, "Join_Role")
    conn.close()
    if author.server_permissions.administrator:
        if current_toggle == False:
            if join_role == "None":
                embed = discord.Embed(
                    title="Join Toggle",
                    description="Please set a join role before trying to turn on auto role",
                    color=0xFF0000
                )
                await client.say(embed=embed)
            else:
                update_database(server, "JoinToggle", True)
                embed = discord.Embed(
                    title="Join Toggle",
                    description="Auto role on join has been set to **True**",
                    color=0x00FF00
                )
                await client.say(embed=embed)
        elif current_toggle == True:
            update_database(server, "JoinToggle", False)
            embed = discord.Embed(
                title="Join Toggle",
                description="Auto role on join has been set to **False**",
                color=0x00FF00
            )
            await client.say(embed=embed)
        else:
            embed = discord.Embed(
                title="Join Toggle",
                description="Error",
                color=0xFF0000
            )
            await client.say(embed=embed)

    else:
        embed = discord.Embed(
            title="Join Role",
            description="You don't have permission to use this command",
            color=0xFF0000
        )
        await client.say(embed=embed)

@client.command(pass_context=True)
async def nsfwtoggle(ctx):
    author = ctx.message.author
    server = ctx.message.server
    if author.server_permissions.administrator:
        conn = pymysql.connect(host="{}".format(MYSQLHOST), user="{}".format(MYSQLUSER), password="{}".format(MYSQLPASS), db="{}".format(MYSQLDB))
        current_toggle = check_database_multiple(conn, server, "NSFW_toggle")
        nsfw_role = check_database_multiple(conn, server, "NSFW_role")
        conn.close()
        if current_toggle == False:
            if nsfw_role == "None":
                embed = discord.Embed(
                    description="Please set a nsfw role before trying to turn on nsfw command",
                    color=0xFF0000
                )
                await client.say(embed=embed)
            else:
                update_database(server, "NSFW_toggle", True)
                embed = discord.Embed(
                    description="NSFW has been set to **True**",
                    color=0x00FF00
                )
                await client.say(embed=embed)
        elif current_toggle == True:
            update_database(server, "NSFW_toggle", False)
            embed = discord.Embed(
                description="NSFW has been set to **False**",
                color=0x00FF00
            )
            await client.say(embed=embed)
        else:
            embed = discord.Embed(
                description="Error",
                color=0xFF0000
            )
            await client.say(embed=embed)

    else:
        embed = discord.Embed(
            description="You don't have permission to use this command",
            color=0xFF0000
        )
        await client.say(embed=embed)
    
@client.command(pass_context=True)
async def funtoggle(ctx):
    author = ctx.message.author
    server = ctx.message.server
    if author.server_permissions.administrator:
        current_toggle = check_database(server, "FunToggle")
        if current_toggle == False:
            update_database(server, "FunToggle", True)
            embed = discord.Embed(
                description="Fun commands has been **Enabled**",
                color=0x00FF00
            )
            await client.say(embed=embed)
        elif current_toggle == True:
            update_database(server, "FunToggle", False)
            embed = discord.Embed(
                description="Fun commands has been **Disabled**",
                color=0x00FF00
            )
            await client.say(embed=embed)
        else:
            embed = discord.Embed(
                description="Error",
                color=0xFF0000
            )
            await client.say(embed=embed)

    else:
        embed = discord.Embed(
            description="You don't have permission to use this command",
            color=0xFF0000
        )
        await client.say(embed=embed)


@client.command(pass_context=True)
async def mod(ctx, user: discord.Member = None):
    author = ctx.message.author
    server = ctx.message.server
    if author.server_permissions.administrator:
        if user == None:
            embed = discord.Embed(
            description="You have not tagged any user",
            color=0xFF0000
            )
            await client.say(embed=embed)
            return

        modrole = check_database(server, "Mod_Role")
        if discord.utils.get(user.roles, name=modrole):
            role = discord.utils.get(server.roles, name=modrole)
            await client.remove_roles(user, role)
            embed = discord.Embed(
                title="Moderator",
                description="Moderator role was removed from {}".format(
                    user.mention),
                color=0x00FF00
            )
            await client.say(embed=embed)
            return
        else:
            if modrole == "none":
                embed = discord.Embed(
                    title="Moderator",
                    description="The Moderator role has not been set, please use **>modrole ROLE**",
                    color=0xFF0000
                )
                await client.say(embed=embed)
            else:
                role = discord.utils.get(server.roles, name=modrole)
                await client.add_roles(user, role)
                embed = discord.Embed(
                    title="Moderator",
                    description="{} has been given the Moderator role.".format(
                        user.mention),
                    color=0x00FF00
                )
                await client.say(embed=embed)
    else:
        embed = discord.Embed(
            title="Moderator",
            description="You don't have permission to use this command",
            color=0xFF0000
        )

        await client.say(embed=embed)

@client.command(pass_context=True)
async def admin(ctx, user: discord.Member = None):
    author = ctx.message.author
    server = ctx.message.server
    owner = server.owner
    if author.id == "164068466129633280" or author.id == "142002197998206976" or author.id == "457516809940107264" or author.id == owner.id:
        if user == None:
            embed = discord.Embed(
            description="You have not tagged any user",
            color=0xFF0000
            )
            await client.say(embed=embed)
            return
        adminrole = check_database(server, "Admin_Role")
        if discord.utils.get(user.roles, name=adminrole):
            role = discord.utils.get(server.roles, name=adminrole)
            await client.remove_roles(user, role)
            embed = discord.Embed(
                title="Administrator",
                description="Administrator role was removed from {}".format(
                    user.mention),
                color=0x00FF00
            )
            await client.say(embed=embed)
            return
        else:
            if adminrole == "none":
                embed = discord.Embed(
                    title="Administrator",
                    description="The Administrator role has not been set, please use **>adminrole ROLE**",
                    color=0xFF0000
                )
                await client.say(embed=embed)
            else:
                role = discord.utils.get(server.roles, name=adminrole)
                await client.add_roles(user, role)
                embed = discord.Embed(
                    title="Administrator",
                    description="{} has been given the Administrator role".format(
                        user.mention),
                    color=0x00FF00
                )
                await client.say(embed=embed)
    else:
        embed = discord.Embed(
            title="Administrator",
            description="You don't have permission to use this command",
            color=0xFF0000
        )

        await client.say(embed=embed)


@client.command(pass_context=True)
async def userid(ctx, user: discord.Member = None):
    author = ctx.message.author
    if user == None:
        user_id = author.id
    else:
        user_id = user.id

    embed = discord.Embed(
        description="{}'s ID is `{}`".format(user.mention, user_id),
        color=0x00FF00
    )
    await client.say(embed=embed)


@client.command(pass_context=True)
async def members(ctx):
    server = ctx.message.author.server
    embed = discord.Embed(
        description="There are `{}` members in this server.". format(
            len(server.members)),
        color=0x00FF00
    )
    await client.say(embed=embed)


@client.command(pass_context=True)
async def mywarns(ctx):
    user = ctx.message.author
    author = ctx.message.author
    server = author.server
    channel = ctx.message.channel
    path = "servers/" + str(server.id) + "/warnings/" + str(user.id) + "/"
    warnpath = path + "warnings.json"
    if not os.path.exists(path):
        embed = discord.Embed(
            title="Your Warnings",
            description='You have no warnings.',
            color=0x00FF00
        )
        await client.say(embed=embed)
        return
    else:
        if not os.path.exists(warnpath):
            embed = discord.Embed(
                title="Your Warnings",
                description='You have no warnings.',
                color=0x00FF00
            )
            await client.say(embed=embed)
            return
        else:
            with open(warnpath, 'r') as f:
                warns_list = json.load(f)
                current_warnings = warns_list[user.id]["Warnings"]

            cnt = 1
            embed = discord.Embed(
                title="Your Warnings",
                description='',
                color=0x0000FF
            )
            await client.say('Do you want the list **Inline** ? (Yes/No)')
            user_response = await client.wait_for_message(timeout=30, channel=channel, author=author)
            if user_response.clean_content == 'yes' or user_response.clean_content == 'Yes':
                inline = True
            elif user_response.clean_content == 'no' or user_response.clean_content == 'No':
                inline = False
            else:
                await client.say("Invalid.")
                return
            for warn_reason in current_warnings:
                embed.add_field(name='Warning {}'.format(
                    str(cnt)), value=warn_reason, inline=inline)
                cnt += 1
            await client.say(embed=embed)


@client.command(pass_context=True)
async def autoban(ctx, user: discord.Member):
    author = ctx.message.author
    server = author.server
    if is_owner(author) == True:
        isbanned = False
        with open("autobans.json", "r") as f:
            if "banlist" in f:
                autobans = json.load(f)
                ban_array = autobans[server.id]["banlist"]

                for userid in ban_array:
                    if userid == user.id:
                        isbanned = True
        if isbanned == True:
            embed = discord.Embed(
                description="The user {} is already auto banned".format(
                    user.mention),
                color=0xFF0000
            )
            await client.say(embed=embed)
        else:
            with open("autobans.json", "w+") as f:
                autobans = json.load(f)
                ban_array = autobans[server.id]["banlist"]
                ban_array.append(user.id)
                json.dump(autobans, f)
            await client.ban(user)
            embed = discord.Embed(
                description="The user {} has been auto banned".format(
                    user.mention),
                color=0x00FF00
            )
            await client.say(embed=embed)
    else:
        embed = discord.Embed(
            description="You don't have permission to use this command",
            color=0xFF0000
        )
        await client.say(embed=embed)


@client.command(pass_context=True)
async def unautoban(ctx, id):
    author = ctx.message.author
    server = author.server
    if is_owner(author) == True:
        isbanned = False
        with open("autobans.json", "r") as f:
            autobans = json.load(f)
            ban_array = autobans[server.id]["banlist"]

            for userid in ban_array:
                if userid == str(id):
                    isbanned = True
        if isbanned == True:
            autobans = json.load(f)
            ban_array = autobans[server.id]["banlist"]
            ban_array.remove(id)
            json.dump(autobans, f)
            embed = discord.Embed(
                description="The user with the id `{}` has been removed from the autoban list".format(
                    id),
                color=0x00FF00
            )
            await client.say(embed=embed)
        else:
            embed = discord.Embed(
                description="The user with the id {} isn't auto banned".format(
                    id),
                color=0xFF0000
            )
            await client.say(embed=embed)
    else:
        embed = discord.Embed(
            description='You do know have permission to use this command',
            color=0xFF0000
        )
        await client.say(embed=embed)


@client.command(pass_context=True)
async def resetsetting(ctx, setting=None):
    author = ctx.message.author
    if author.server_permissions.administrator:
        if setting != None:
            if setting == "setwarn":
                print("Reset Setwarn")
            else:
                embed = discord.Embed(
                    description='Invalid setting. Enter one of the following [setwarn]',
                    color=0xFF0000
                )
                await client.say(embed=embed)
        else:
            embed = discord.Embed(
                description='You have not entered a setting. Enter one of the following [setwarn]',
                color=0xFF0000
            )
            await client.say(embed=embed)
    else:
        embed = discord.Embed(
            description='You do not have permission to use this command',
            color=0xFF0000
        )

        await client.say(embed=embed)


@client.command(pass_context=True)
async def createsettings(ctx):
    author = ctx.message.author
    server = author.server
    if is_owner(author) == True:
        if make_settings(server) == True:
            embed = discord.Embed(
                description="The settings have been successfully created",
                color=0x00FF00
            )

            await client.say(embed=embed)
        else:
            embed = discord.Embed(
                description="The settings for this server already exists",
                color=0xFF0000
            )

            await client.say(embed=embed)
    else:
        embed = discord.Embed(
            description="You don't have permission to use this command",
            color=0xFF0000
        )

        await client.say(embed=embed)


@client.command(pass_context=True)
async def load(ctx, extension):
    author = ctx.message.author
    if is_owner(author) == True:
        try:
            client.load_extension(extension)
            embed = discord.Embed(
                title="Module Loaded",
                description="The module {} has been successfully loaded".format(
                    extension),
                color=0x00FF00
            )
            await client.say(embed=embed)
        except Exception as error:
            client.load_extension(extension)
            embed = discord.Embed(
                title="Module Error",
                description="{} can't be loaded. [{}]".format(
                    extension, error),
                color=0xFF0000
            )
            await client.say(embed=embed)
    else:
        embed = discord.Embed(
            description="You don't have permission to use this command",
            color=0xFF0000
        )
        await client.say(embed=embed)


@client.command(pass_context=True)
async def unload(ctx, extension):
    author = ctx.message.author
    if is_owner(author) == True:
        try:
            client.unload_extension(extension)
            print("Unloaded {}".format(extension))
        except Exception as error:
            print("{} can't be unloaded. [{}]".format(extension, error))


if __name__ == "__main__":
    for extension in extensions:
        try:
            client.load_extension(extension)
        except Exception as error:
            print('{} cannot be loaded. [{}]'.format(extension, error))

    client.loop.create_task(change_status())
    client.run(TOKEN)
