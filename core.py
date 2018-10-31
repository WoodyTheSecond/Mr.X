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
import atexit
import shutil
from signal import *
from profanity import profanity

TOKEN = os.getenv("TOKEN")
client = commands.Bot(command_prefix="-")
client.remove_command("help")
status = ["Commands: -help", "Watching you"]
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)
extensions = ["admin", "utility", "swarm", "nsfw", "fun", "economy", "marriage", "otaku"]

async def change_status():
    await client.wait_until_ready()
    msgs = cycle(status)

    while not client.is_closed:
        current_status = next(msgs)
        await client.change_presence(game=discord.Game(name=current_status))
        await asyncio.sleep(15)

async def autosave_economy():
    await client.wait_until_ready()

    while not client.is_closed:
        await asyncio.sleep(3600)
        conn = pymysql.connect(host="sql7.freesqldatabase.com", user="sql7257339", password="yakm4fsd4T", db="sql7257339")
        c = conn.cursor()
        for file in os.listdir("eco"):
            filename = os.fsdecode(file)
            if str(filename) != "placeholder":
                user_id = os.fsdecode(file).replace(".json", "")
                filepath = "eco/{}".format(str(filename))
                with open(filepath, "r") as f:
                    economy = json.load(f)
                    for server in economy:
                        current_money = economy[server]["Money"]
                        current_bank = economy[server]["Bank"]
                        sql = "UPDATE `Economy` SET money = '{}', bank = '{}' WHERE userid = '{}' AND serverid = '{}'".format(current_money, current_bank, str(user_id), str(server))
                        c.execute(sql)
                        conn.commit()

        conn.close()
        print("The economy has been saved")

async def autosave_settings():
    await client.wait_until_ready()

    while not client.is_closed:
        await asyncio.sleep(3600)
        conn = pymysql.connect(host="sql7.freesqldatabase.com", user="sql7257339", password="yakm4fsd4T", db="sql7257339")
        c = conn.cursor()
        for server in os.listdir("servers"):
            server_id = os.fsdecode(server)
            if str(server_id) != "placeholder":
                settingspath = "servers/{}/settings.json".format(str(server_id))
                econony_settingspath = "servers/{}/economy_settings.json".format(str(server_id))
                with open(settingspath, "r") as f:
                    settings = json.load(f)
                    for server in settings:
                        join_role = settings["Join_Role"]
                        dmwarn = settings["DMWarn"]
                        verify_role = settings["Verify_Role"]
                        mod_role = settings["Mod_Role"]
                        admin_role = settings["Admin_Role"]
                        mute_role = settings["Mute_Role"]
                        warn_mute = settings["WarnMute"]
                        join_toggle = settings["JoinToggle"]
                        can_mod_announce = settings["CanModAnnounce"]
                        level_system = settings["Level_System"]
                        chat_filter = settings["Chat_Filter"]
                        ignore_hierarchy = settings["Ignore_Hierarchy"]
                        nsfw_role = settings["NSFW_role"]
                        nsfw_toggle = settings["NSFW_toggle"]
                        fun_toggle = settings["FunToggle"]
                        profanity_filter = settings["Profanity_Filter"]
                        customwords_toggle = settings["Custom_Words"]
                        earn_cooldown = settings["earn_cooldown"]
                        marriage_toggle = settings["Marriage_Toggle"]
                        sql = "UPDATE `Server_Settings` SET Join_Role = '{}', DMWarn = '{}', Verify_Role = '{}', Mod_Role = '{}', Admin_Role = '{}', Mute_Role = '{}', WarnMute = '{}', JoinToggle = '{}', CanModAnnounce = '{}', Level_System = '{}', Chat_Filter = '{}', Ignore_Hierarchy = '{}', NSFW_role = '{}', NSFW_toggle = '{}', FunToggle = '{}', Profanity_Filter = '{}', Custom_Words = '{}', earn_cooldown = '{}', Marriage_Toggle = '{}' WHERE serverid = '{}'".format(join_role, dmwarn, verify_role, mod_role, admin_role, mute_role, warn_mute, join_toggle, can_mod_announce, level_system, chat_filter, ignore_hierarchy, nsfw_role, nsfw_toggle, fun_toggle, profanity_filter, customwords_toggle, earn_cooldown, marriage_toggle, str(server_id))
                        c.execute(sql)
                        conn.commit()

            with open(econony_settingspath, "r") as f:
                settings = json.load(f)
                for server in settings:
                    max_work_amount = settings["max_work_amount"]
                    min_work_amount = settings["min_work_amount"]
                    max_slut_amount = settings["max_slut_amount"]
                    min_slut_amount = settings["min_slut_amount"]
                    sql = "UPDATE `Economy_Settings` SET max_work_amount = '{}', min_work_amount = '{}', max_slut_amount = '{}', min_slut_amount = '{}' WHERE serverid = '{}'".format(max_work_amount, min_work_amount, max_slut_amount, min_slut_amount, str(server))
                    c.execute(sql)
                    conn.commit()

        conn.close()
        print("The settings has been saved")

def save_economy(*args):
    conn = pymysql.connect(host="sql7.freesqldatabase.com", user="sql7257339", password="yakm4fsd4T", db="sql7257339")
    c = conn.cursor()
    for file in os.listdir("eco"):
        filename = os.fsdecode(file)
        if str(filename) != "placeholder":
            user_id = os.fsdecode(file).replace(".json", "")
            filepath = "eco/{}".format(str(filename))
            with open(filepath, "r") as f:
                economy = json.load(f)
                for server in economy:
                    current_money = economy[server]["Money"]
                    current_bank = economy[server]["Bank"]
                    sql = "UPDATE `Economy` SET money = '{}', bank = '{}' WHERE userid = '{}' AND serverid = '{}'".format(current_money, current_bank, str(user_id), str(server))
                    c.execute(sql)
                    conn.commit()

    conn.close()
    print("The economy has been saved")

def save_settings(*args):
    conn = pymysql.connect(host="sql7.freesqldatabase.com", user="sql7257339", password="yakm4fsd4T", db="sql7257339")
    c = conn.cursor()
    for server in os.listdir("servers"):
        server_id = os.fsdecode(server)
        if str(server_id) != "placeholder":
            settingspath = "servers/{}/settings.json".format(str(server_id))
            econony_settingspath = "servers/{}/economy_settings.json".format(str(server_id))
            with open(settingspath, "r") as f:
                settings = json.load(f)
                for server in settings:
                    join_role = settings["Join_Role"]
                    dmwarn = settings["DMWarn"]
                    verify_role = settings["Verify_Role"]
                    mod_role = settings["Mod_Role"]
                    admin_role = settings["Admin_Role"]
                    mute_role = settings["Mute_Role"]
                    warn_mute = settings["WarnMute"]
                    join_toggle = settings["JoinToggle"]
                    can_mod_announce = settings["CanModAnnounce"]
                    level_system = settings["Level_System"]
                    chat_filter = settings["Chat_Filter"]
                    ignore_hierarchy = settings["Ignore_Hierarchy"]
                    nsfw_role = settings["NSFW_role"]
                    nsfw_toggle = settings["NSFW_toggle"]
                    fun_toggle = settings["FunToggle"]
                    profanity_filter = settings["Profanity_Filter"]
                    customwords_toggle = settings["Custom_Words"]
                    earn_cooldown = settings["earn_cooldown"]
                    marriage_toggle = settings["Marriage_Toggle"]
                    sql = "UPDATE `Server_Settings` SET Join_Role = '{}', DMWarn = '{}', Verify_Role = '{}', Mod_Role = '{}', Admin_Role = '{}', Mute_Role = '{}', WarnMute = '{}', JoinToggle = '{}', CanModAnnounce = '{}', Level_System = '{}', Chat_Filter = '{}', Ignore_Hierarchy = '{}', NSFW_role = '{}', NSFW_toggle = '{}', FunToggle = '{}', Profanity_Filter = '{}', Custom_Words = '{}', earn_cooldown = '{}', Marriage_Toggle = '{}' WHERE serverid = '{}'".format(join_role, dmwarn, verify_role, mod_role, admin_role, mute_role, warn_mute, join_toggle, can_mod_announce, level_system, chat_filter, ignore_hierarchy, nsfw_role, nsfw_toggle, fun_toggle, profanity_filter, customwords_toggle, earn_cooldown, marriage_toggle, str(server_id))
                    c.execute(sql)
                    conn.commit()

        with open(econony_settingspath, "r") as f:
            settings = json.load(f)
            for server in settings:
                max_work_amount = settings["max_work_amount"]
                min_work_amount = settings["min_work_amount"]
                max_slut_amount = settings["max_slut_amount"]
                min_slut_amount = settings["min_slut_amount"]
                sql = "UPDATE `Economy_Settings` SET max_work_amount = '{}', min_work_amount = '{}', max_slut_amount = '{}', min_slut_amount = '{}' WHERE serverid = '{}'".format(max_work_amount, min_work_amount, max_slut_amount, min_slut_amount, str(server))
                c.execute(sql)
                conn.commit()

    conn.close()
    print("The settings has been saved")
    return True

def save(*args):
    save_economy()
    save_settings()
    sys.exit(0)

def create_database(settingstype, server):
    conn = pymysql.connect(host="sql7.freesqldatabase.com", user="sql7257339", password="yakm4fsd4T", db="sql7257339")
    c = conn.cursor()
    if settingstype == "server":
        sql = "INSERT INTO `Server_Settings` (serverid, Join_Role, DMWarn, Verify_Role, Mod_Role, Admin_Role, Mute_Role, WarnMute, JoinToggle, CanModAnnounce, Level_System, Chat_Filter, Ignore_Hierarchy, NSFW_role, NSFW_toggle, FunToggle, earn_cooldown) VALUES ('{}', 'None', '0', 'None', 'None', 'None', 'None', '0', '0', '0', '0', '0', '0', 'None', '0', '0', '0')".format(str(server.id))
        c.execute(sql)
        conn.commit()
    elif settingstype == "economy":
        sql = "INSERT INTO `Economy_Settings` (serverid, max_work_amount, min_work_amount, max_slut_amount, min_slut_amount) VALUES ('{}', '1000', '500', '1000', '500')".format(str(server.id))
        c.execute(sql)
        conn.commit()

    conn.close()

def update_setting(server, setting, value):
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

def check_setting(server, setting):
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

def make_settings(server):
    conn = pymysql.connect(host="sql7.freesqldatabase.com", user="sql7257339", password="yakm4fsd4T", db="sql7257339")
    c = conn.cursor()
    sql = "SELECT * FROM `Server_Settings` WHERE serverid = {}".format(str(server.id))
    c.execute(sql)
    conn.commit()
    data = c.fetchone()
    if data == None:
        create_database("server", server)

    settingspath = "servers/{}/settings.json".format(server.id)
    if not os.path.exists("servers/{}".format(server.id)):
        os.makedirs("servers/{}".format(server.id))

    if not os.path.exists(settingspath):
        with open(settingspath, "w+") as f:
            json_data = {}
            json_data["Join_Role"] = "None"
            json_data["DMWarn"] = 0
            json_data["Verify_Role"] = "None"
            json_data["Mod_Role"] = "None"
            json_data["Admin_Role"] = "None"
            json_data["Mute_Role"] = "None"
            json_data["WarnMute"] = "0"
            json_data["JoinToggle"] = 0
            json_data["CanModAnnounce"] = 0
            json_data["Level_System"] = 0
            json_data["Chat_Filter"] = 0
            json_data["Ignore_Hierarchy"] = 0
            json_data["NSFW_role"] = "None"
            json_data["NSFW_toggle"] = 0
            json_data["FunToggle"] = 0
            json_data["Profanity_Filter"] = 0
            json_data["Custom_Words"] = 0
            json_data["earn_cooldown"] = ""
            json_data["Marriage_Toggle"] = 0
            json.dump(json_data, f)

    sql = "SELECT * FROM `Economy_Settings` WHERE serverid = {}".format(str(server.id))
    c.execute(sql)
    conn.commit()
    data = c.fetchone()
    if data == None:
        create_database("economy", server)

    economy_settingspath = "servers/{}/economy_settings.json".format(server.id)
    if not os.path.exists("servers/{}".format(server.id)):
        os.makedirs("servers/{}".format(server.id))

    if not os.path.exists(economy_settingspath):
        with open(economy_settingspath, "w+") as f:
            json_data = {}
            json_data["max_work_amount"] = 1000
            json_data["min_work_amount"] = 500
            json_data["max_slut_amount"] = 1000
            json_data["min_slut_amount"] = 500
            json.dump(json_data, f)

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
    for file in os.listdir("eco"):
        file_path = os.path.join("eco", file)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(e)
    
    conn = pymysql.connect(host="sql7.freesqldatabase.com", user="sql7257339", password="yakm4fsd4T", db="sql7257339")
    c = conn.cursor()
    sql = "SELECT * FROM `Server_Settings`"
    c.execute(sql)
    conn.commit()
    data = c.fetchall()
    for d in data:
        serverid = d[1]
        join_role = d[2]
        dmwarn = d[3]
        verify_role = d[4]
        mod_role = d[5]
        admin_role = d[6]
        mute_role = d[7]
        warn_mute = d[8]
        join_toggle = d[9]
        can_mod_announce = d[10]
        level_system = d[11]
        chat_filter = d[12]
        ignore_hierarchy = d[13]
        nsfw_role = d[14]
        nsfw_toggle = d[15]
        fun_toggle = d[16]
        profanity_filter = d[17]
        customwords_toggle = d[18]
        earn_cooldown = d[19]
        marriage_toggle = d[20]
        if not os.path.exists("servers/{}".format(serverid)):
            os.makedirs("servers/{}".format(serverid))

        settingspath = "servers/{}/settings.json".format(str(serverid))
        with open(settingspath, "w+") as f:
            json_data = {}
            json_data["Join_Role"] = join_role
            json_data["DMWarn"] = dmwarn
            json_data["Verify_Role"] = verify_role
            json_data["Mod_Role"] = mod_role
            json_data["Admin_Role"] = admin_role
            json_data["Mute_Role"] = mute_role
            json_data["WarnMute"] = warn_mute
            json_data["JoinToggle"] = join_toggle
            json_data["CanModAnnounce"] = can_mod_announce
            json_data["Level_System"] = level_system
            json_data["Chat_Filter"] = chat_filter
            json_data["Ignore_Hierarchy"] = ignore_hierarchy
            json_data["NSFW_role"] = nsfw_role
            json_data["NSFW_toggle"] = nsfw_toggle
            json_data["FunToggle"] = fun_toggle
            json_data["Profanity_Filter"] = profanity_filter
            json_data["Custom_Words"] = customwords_toggle
            json_data["earn_cooldown"] = earn_cooldown
            json_data["Marriage_Toggle"] = marriage_toggle
            json.dump(json_data, f)
    
    sql = "SELECT * FROM `Economy_Settings`"
    c.execute(sql)
    conn.commit()
    data = c.fetchall()
    for d in data:
        serverid = d[1]
        max_work_amount = d[2]
        min_work_amount = d[3]
        max_slut_amount = d[4]
        min_slut_amount = d[5]
        if not os.path.exists("servers/{}".format(serverid)):
            os.makedirs("servers/{}".format(serverid))

        settingspath = "servers/{}/economy_settings.json".format(str(serverid))
        with open(settingspath, "w+") as f:
            json_data = {}
            json_data["max_work_amount"] = max_work_amount
            json_data["min_work_amount"] = min_work_amount
            json_data["max_slut_amount"] = max_slut_amount
            json_data["min_slut_amount"] = min_slut_amount
            json.dump(json_data, f)

    sql = "SELECT * FROM `Banned_Words`"
    c.execute(sql)
    conn.commit()
    data = c.fetchall()
    for d in data:
        serverid = d[1]
        word = d[2]
        banned_words_path = "servers/{}/banned_words.txt".format(str(serverid))
        if not os.path.exists("servers/{}".format(serverid)):
            os.makedirs("servers/{}".format(serverid))

        if os.path.exists(banned_words_path):
            banned_words = open(banned_words_path, "r").read()
            if not word in banned_words:
                banned_words += "\n{}".format(word)
                with open(banned_words_path, "w") as f:
                    f.write(banned_words)
        else:
            with open(banned_words_path, "w+") as f:
                f.write(word)

    sql = "SELECT * FROM `Economy`"
    c.execute(sql)
    conn.commit()
    data = c.fetchall()
    for d in data:
        serverid = d[1]
        userid = d[2]
        money = d[3]
        bank = d[4]
        path = "eco/" + str(userid) + ".json"
        if not os.path.exists(path):
            with open(path, 'w+') as f:
                json_data = {}
                json_data[serverid] = {}
                json_data[serverid]["Money"] = money
                json_data[serverid]["Bank"] = bank
                json.dump(json_data, f)
        else:
            with open(path, 'r') as f:
                json_data = json.load(f)
                json_data[serverid] = {}
                json_data[serverid]["Money"] = money
                json_data[serverid]["Bank"] = bank
                with open(path, 'w') as f:
                    json.dump(json_data, f)

    sql = "SELECT * FROM `Economy_Settings`"
    c.execute(sql)
    conn.commit()
    data = c.fetchall()
    conn.close()
    for d in data:
        serverid = d[1]
        max_work_amount = d[2]
        min_work_amount = d[3]
        max_slut_amount = d[4]
        min_slut_amount = d[5]
        path = "servers/{}/economy_settings.json".format(serverid)
        if not os.path.exists(path):
            with open(path, 'w+') as f:
                json_data = {}
                json_data["max_work_amount"] = max_work_amount
                json_data["min_work_amount"] = min_work_amount
                json_data["max_slut_amount"] = max_slut_amount
                json_data["min_slut_amount"] = min_slut_amount
                json.dump(json_data, f)
        else:
            with open(path, 'r') as f:
                json_data = json.load(f)
                json_data["max_work_amount"] = max_work_amount
                json_data["min_work_amount"] = min_work_amount
                json_data["max_slut_amount"] = max_slut_amount
                json_data["min_slut_amount"] = min_slut_amount
                with open(path, 'w') as f:
                    json.dump(json_data, f)

@client.event
async def on_member_join(member):
    server = member.server
    join_toggle = check_setting(server, "JoinToggle")
    join_role = check_setting(server, "Join_Role")
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
    await client.wait_until_ready()
    await client.process_commands(message)
    author = message.author
    if author.bot == False:
        channel = message.channel
        server = author.server
        profanityfiltertoggle = check_setting(server, "Profanity_Filter")
        customfiltertoggle = check_setting(server, "Custom_Words")
        bannedwordspath = "servers/{}/banned_words.txt".format(str(server.id))

        if profanityfiltertoggle == True and is_owner(author) == False and author != server.owner:
            if profanity.contains_profanity(message.clean_content) == True:
                 await client.delete_message(message)
                 msg = await client.send_message(channel, "{}, Watch your language!".format(author.mention))
                 await asyncio.sleep(2)
                 await client.delete_message(msg)
            elif customfiltertoggle == True:
                if os.path.exists(bannedwordspath):
                    banned_words = open(bannedwordspath, "r").read().splitlines()
                    deleted = False
                    for word in banned_words:
                        if word in message.clean_content and deleted == False:
                            deleted = True
                            await client.delete_message(message)
                            msg = await client.send_message(channel, "{}, Watch your language!".format(author.mention))
                            await asyncio.sleep(2)
                            await client.delete_message(msg)

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

    Ignore_Hierarchy = str(check_setting(server, "Ignore_Hierarchy"))
    DMWarn = check_setting(server, "DMWarn")
    Verify_Role = check_setting(server, "Verify_Role")
    Mod_Role = check_setting(server, "Mod_Role")
    Join_Role = check_setting(server, "Join_Role")
    Admin_Role = check_setting(server, "Admin_Role")
    Mute_Role = check_setting(server, "Mute_Role")
    NSFW_role = check_setting(server, "NSFW_role")
    WarnMute = check_setting(server, "WarnMute")
    JoinToggle = str(check_setting(server, "JoinToggle"))
    NSFW_toggle = str(check_setting(server, "NSFW_toggle"))
    FunToggle = str(check_setting(server, "FunToggle"))
    Profanity_Filter = str(check_setting(server, "Profanity_Filter"))
    CanModAnnounce = str(check_setting(server, "CanModAnnounce"))
    Level_System = str(check_setting(server, "Level_System"))
    earn_cooldown = str(check_setting(server, "earn_cooldown"))

    await client.say("Do you want the list **Inline** ? (Yes/No)")
    user_response = await client.wait_for_message(timeout=30, channel=channel, author=author)
    user_response = user_response.clean_content.lower()
    if user_response == "yes":
        inline = True
    elif user_response == "no":
        inline = False
    else:
        await client.say("Invalid.")
        return

    embed = discord.Embed(
        color=0x0000FF
    )

    if server.icon_url != "":
        embed.set_thumbnail(url=server.icon_url)

    embed.set_author(name='{} Server Settings'.format(server), icon_url='https://cdn.discordapp.com/avatars/472817090785705985/b5318faf95792ae0a80ddb2e117e7ab7.png?size=128')
    embed.add_field(name='Ignore Hierarchy',value=Ignore_Hierarchy, inline=inline)
    embed.add_field(name='Direct message on warn', value=DMWarn, inline=inline)
    embed.add_field(name='Verify Role', value=Verify_Role, inline=inline)
    embed.add_field(name='Moderator Role', value=Mod_Role, inline=inline)
    embed.add_field(name='Join Role', value=Join_Role, inline=inline)
    embed.add_field(name='Administrator Role', value=Admin_Role, inline=inline)
    embed.add_field(name='Mute Role', value=Mute_Role, inline=inline)
    embed.add_field(name='NSFW Role', value=NSFW_role, inline=inline)
    embed.add_field(name='Warning mute time', value=WarnMute, inline=inline)
    embed.add_field(name='Auto role on join', value=JoinToggle, inline=inline)
    embed.add_field(name='NSFW commands', value=NSFW_toggle, inline=inline)
    embed.add_field(name='Fun commands', value=FunToggle, inline=inline)
    embed.add_field(name='Profanity filter (swear filter)', value=Profanity_Filter, inline=inline)
    embed.add_field(name='Can moderator announce',value=CanModAnnounce, inline=inline)
    embed.add_field(name='Level system', value=Level_System, inline=inline)
    embed.add_field(name='Work cooldown', value=earn_cooldown, inline=inline)
    await client.say(embed=embed)

@client.command(pass_context=True)
async def seconomy(ctx):
    author = ctx.message.author
    if is_owner(author):
        conn = pymysql.connect(host="sql7.freesqldatabase.com", user="sql7257339", password="yakm4fsd4T", db="sql7257339")
        c = conn.cursor()
        for file in os.listdir("eco"):
            filename = os.fsdecode(file)
            if str(filename) != "placeholder":
                user_id = os.fsdecode(file).replace(".json", "")
                filepath = "eco/{}".format(str(filename))
                with open(filepath, "r") as f:
                    economy = json.load(f)
                    for server in economy:
                        current_money = economy[server]["Money"]
                        current_bank = economy[server]["Bank"]
                        sql = "UPDATE `Economy` SET money = '{}', bank = '{}' WHERE userid = '{}' AND serverid = '{}'".format(current_money, current_bank, str(user_id), str(server))
                        c.execute(sql)
                        conn.commit()

        conn.close()

        embed = discord.Embed(
            description = "The economy has been saved",
            color = 0x00FF00
        )

        await client.say(embed=embed)
    else:
        embed = discord.Embed(
            description="You don't have permission to use this command",
            color=0xFF0000
        )

        await client.say(embed=embed)

@client.command(pass_context=True)
async def ssettings(ctx):
    author = ctx.message.author
    if is_owner(author):
        conn = pymysql.connect(host="sql7.freesqldatabase.com", user="sql7257339", password="yakm4fsd4T", db="sql7257339")
        c = conn.cursor()
        for server in os.listdir("servers"):
            server_id = os.fsdecode(server)
            if str(server_id) != "placeholder":
                settingspath = "servers/{}/settings.json".format(str(server_id))
                econony_settingspath = "servers/{}/economy_settings.json".format(str(server_id))
                with open(settingspath, "r") as f:
                    settings = json.load(f)
                    for server in settings:
                        join_role = settings["Join_Role"]
                        dmwarn = settings["DMWarn"]
                        verify_role = settings["Verify_Role"]
                        mod_role = settings["Mod_Role"]
                        admin_role = settings["Admin_Role"]
                        mute_role = settings["Mute_Role"]
                        warn_mute = settings["WarnMute"]
                        join_toggle = settings["JoinToggle"]
                        can_mod_announce = settings["CanModAnnounce"]
                        level_system = settings["Level_System"]
                        chat_filter = settings["Chat_Filter"]
                        ignore_hierarchy = settings["Ignore_Hierarchy"]
                        nsfw_role = settings["NSFW_role"]
                        nsfw_toggle = settings["NSFW_toggle"]
                        fun_toggle = settings["FunToggle"]
                        profanity_filter = settings["Profanity_Filter"]
                        customwords_toggle = settings["Custom_Words"]
                        earn_cooldown = settings["earn_cooldown"]
                        marriage_toggle = settings["Marriage_Toggle"]
                        sql = "UPDATE `Server_Settings` SET Join_Role = '{}', DMWarn = '{}', Verify_Role = '{}', Mod_Role = '{}', Admin_Role = '{}', Mute_Role = '{}', WarnMute = '{}', JoinToggle = '{}', CanModAnnounce = '{}', Level_System = '{}', Chat_Filter = '{}', Ignore_Hierarchy = '{}', NSFW_role = '{}', NSFW_toggle = '{}', FunToggle = '{}', Profanity_Filter = '{}', Custom_Words = '{}', earn_cooldown = '{}', Marriage_Toggle = '{}' WHERE serverid = '{}'".format(join_role, dmwarn, verify_role, mod_role, admin_role, mute_role, warn_mute, join_toggle, can_mod_announce, level_system, chat_filter, ignore_hierarchy, nsfw_role, nsfw_toggle, fun_toggle, profanity_filter, customwords_toggle, earn_cooldown, marriage_toggle, str(server_id))
                        c.execute(sql)
                        conn.commit()

            with open(econony_settingspath, "r") as f:
                settings = json.load(f)
                for server in settings:
                    max_work_amount = settings["max_work_amount"]
                    min_work_amount = settings["min_work_amount"]
                    max_slut_amount = settings["max_slut_amount"]
                    min_slut_amount = settings["min_slut_amount"]
                    sql = "UPDATE `Economy_Settings` SET max_work_amount = '{}', min_work_amount = '{}', max_slut_amount = '{}', min_slut_amount = '{}' WHERE serverid = '{}'".format(max_work_amount, min_work_amount, max_slut_amount, min_slut_amount, str(server))
                    c.execute(sql)
                    conn.commit()

        conn.close()
        embed = discord.Embed(
            description = "The settings has been saved",
            color = 0x00FF00
        )

        await client.say(embed=embed)
    else:
        embed = discord.Embed(
            description="You don't have permission to use this command",
            color=0xFF0000
        )

        await client.say(embed=embed)

@client.command(pass_context=True)
async def mylevel(ctx):
    author = ctx.message.author
    conn = pymysql.connect(host="sql7.freesqldatabase.com", user="sql7257339", password="yakm4fsd4T", db="sql7257339")
    c = conn.cursor()
    sql = "SELECT level from `User_Levels` WHERE userid = {}".format(str(author.id))
    c.execute(sql)
    conn.commit()
    data = c.fetchone()
    conn.close()
    if data == None:
        conn = pymysql.connect(host="sql7.freesqldatabase.com", user="sql7257339", password="yakm4fsd4T", db="sql7257339")
        c = conn.cursor()
        sql = "INSERT INTO `User_Levels` VALUES ({}, '1', '0')".format(str(author.id))
        c.execute(sql)
        conn.commit()
        conn.close()
        # Finished creating user data.
        current_level = "1"
        embed = discord.Embed(
            description='You are currently level **{}**.'.format(current_level),
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
        toggle = check_setting(server, "Level_System")
        if toggle == True:
            update_setting(server, "Level_System", False)
            embed = discord.Embed(
                title="Global Level System",
                description='You have **disabled** the Level System on this server.',
                color=0x00FF00
            )
            await client.say(embed=embed)
        elif toggle == False:
            update_setting(server, "Level_System", True)
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
            description="You don't have permission to use this command",
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
    current = check_setting(server, "DMWarn")
    if author.server_permissions.administrator:
        if current == True:
            update_setting(server, "DMWarn", False)
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
            update_setting(server, "DMWarn", True)
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
            update_setting(server, "Mod_Role", newrole)
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
            update_setting(server, "Admin_Role", newrole)
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
            update_setting(server, "Mute_Role", newrole)
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
                update_setting(server, "Join_Role", newrole)
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
                update_setting(server, "NSFW_role", newrole)
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
                update_setting(server, "Verify_Role", newrole)
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
            update_setting(server, "WarnMute", str(lenght))
            embed = discord.Embed(
                title="Mute Time",
                description="Punish Mute has been set to **{}** minute(s)".format(
                    t_time),
                color=0x00FF00
            )
            await client.say(embed=embed)
        elif "h" in lenght:
            t_time = lenght.replace("h", "")
            update_setting(server, "WarnMute", str(lenght))
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
    current_toggle = check_setting(server, "JoinToggle")
    join_role = check_setting(server, "Join_Role")
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
                update_setting(server, "JoinToggle", True)
                embed = discord.Embed(
                    title="Join Toggle",
                    description="Auto role on join has been set to **True**",
                    color=0x00FF00
                )
                await client.say(embed=embed)
        elif current_toggle == True:
            update_setting(server, "JoinToggle", False)
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
        current_toggle = check_setting(server, "NSFW_toggle")
        nsfw_role = check_setting(server, "NSFW_role")
        if current_toggle == False:
            if nsfw_role == "None":
                embed = discord.Embed(
                    description="Please set a nsfw role before trying to turn on nsfw command",
                    color=0xFF0000
                )
                await client.say(embed=embed)
            else:
                update_setting(server, "NSFW_toggle", True)
                embed = discord.Embed(
                    description="NSFW has been set to **True**",
                    color=0x00FF00
                )
                await client.say(embed=embed)
        elif current_toggle == True:
            update_setting(server, "NSFW_toggle", False)
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
        current_toggle = check_setting(server, "FunToggle")
        if current_toggle == False:
            update_setting(server, "FunToggle", True)
            embed = discord.Embed(
                description="Fun commands has been **Enabled**",
                color=0x00FF00
            )
            await client.say(embed=embed)
        elif current_toggle == True:
            update_setting(server, "FunToggle", False)
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
async def sweartoggle(ctx):
    author = ctx.message.author
    server = ctx.message.server
    if author.server_permissions.administrator:
        current_toggle = check_setting(server, "Profanity_Filter")
        if current_toggle == False:
            update_setting(server, "Profanity_Filter", True)
            embed = discord.Embed(
                description="The swear filter has been **Enabled**",
                color=0x00FF00
            )
            await client.say(embed=embed)
        elif current_toggle == True:
            update_setting(server, "Profanity_Filter", False)
            embed = discord.Embed(
                description="The swear filter has been **Disabled**",
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
async def customwords(ctx):
    author = ctx.message.author
    server = ctx.message.server
    if author.server_permissions.administrator:
        current_toggle = check_setting(server, "Custom_Words")
        if current_toggle == False:
            update_setting(server, "Custom_Words", True)
            embed = discord.Embed(
                description="The custom words filter has been **Enabled**",
                color=0x00FF00
            )
            await client.say(embed=embed)
        elif current_toggle == True:
            update_setting(server, "Custom_Words", False)
            embed = discord.Embed(
                description="The custom words filter has been **Disabled**",
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
async def marrytoggle(ctx):
    author = ctx.message.author
    server = ctx.message.server
    if author.server_permissions.administrator:
        current_toggle = check_setting(server, "Marriage_Toggle")
        if current_toggle == False:
            update_setting(server, "Marriage_Toggle", True)
            embed = discord.Embed(
                description="Marriage has been **Enabled**",
                color=0x00FF00
            )
            await client.say(embed=embed)
        elif current_toggle == True:
            update_setting(server, "Marriage_Toggle", False)
            embed = discord.Embed(
                description="Marriage has been **Disabled**",
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

        modrole = check_setting(server, "Mod_Role")
        if discord.utils.get(user.roles, name=modrole):
            role = discord.utils.get(server.roles, name=modrole)
            try:
                await client.remove_roles(user, role)
                embed = discord.Embed(
                    title="Moderator",
                    description="Moderator role was removed from {}".format(
                        user.mention),
                    color=0x00FF00
                )
                await client.say(embed=embed)
            except discord.Forbidden:
                embed = discord.Embed(
                    description = "Missing permissions",
                    color = 0xFF0000
                )
                await client.say(embed=embed)
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
                try:
                    await client.add_roles(user, role)
                    embed = discord.Embed(
                        title="Moderator",
                        description="{} has been given the Moderator role.".format(
                            user.mention),
                        color=0x00FF00
                    )
                    await client.say(embed=embed)
                except discord.Forbidden:
                    embed = discord.Embed(
                        description = "Missing permissions",
                        color = 0xFF0000
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
        adminrole = check_setting(server, "Admin_Role")
        if discord.utils.get(user.roles, name=adminrole):
            role = discord.utils.get(server.roles, name=adminrole)
            try:
                await client.remove_roles(user, role)
                embed = discord.Embed(
                    title="Administrator",
                    description="Administrator role was removed from {}".format(
                        user.mention),
                    color=0x00FF00
                )
                await client.say(embed=embed)
            except discord.Forbidden:
                embed = discord.Embed(
                    description = "Missing permissions",
                    color = 0xFF0000
                )
                await client.say(embed=embed)
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
                try:
                    await client.add_roles(user, role)
                    embed = discord.Embed(
                        title="Administrator",
                        description="{} has been given the Administrator role".format(
                            user.mention),
                        color=0x00FF00
                    )
                    await client.say(embed=embed)
                except discord.Forbidden:
                    embed = discord.Embed(
                        description = "Missing permissions",
                        color = 0xFF0000
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
        description="There are `{}` members in this server.". format(len(server.members)),
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
                description="The user {} is already auto banned".format(user.mention),
                color=0xFF0000
            )
            await client.say(embed=embed)
        else:
            with open("autobans.json", "w+") as f:
                autobans = json.load(f)
                ban_array = autobans[server.id]["banlist"]
                ban_array.append(user.id)
                json.dump(autobans, f)

            try:
                await client.ban(user)
                embed = discord.Embed(
                    description="The user {} has been auto banned".format(
                        user.mention),
                    color=0x00FF00
                )
                await client.say(embed=embed)
            except discord.Forbidden:
                embed = discord.Embed(
                    description = "Missing permissions",
                    color = 0xFF0000
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
        make_settings(server)
        embed = discord.Embed(
            description="The settings have been successfully created",
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
async def lockchannel(ctx, channel: discord.Channel = None):
    author = ctx.message.author
    server = author.server
    cchannel = ctx.message.channel
    if channel == None:
        channel = ctx.message.channel

    if is_owner(author) or author == server.owner:
        role_list = [role for role in server.roles]
        path = "locked/" + str(channel.id) + ".json"
        if not os.path.exists(path):
            with open(path, "w+") as f:
                json_data = {}
                json_data["Channel_Permissions"] = {}
                for role in role_list:
                    cur_role_perms = channel.overwrites_for(role)
                    json_data["Channel_Permissions"][str(role.id)] = cur_role_perms.send_messages
                    overwrite = discord.PermissionOverwrite()
                    overwrite.send_messages = False
                    try:
                        await client.edit_channel_permissions(channel, role, overwrite)
                    except discord.Forbidden:
                        embed = discord.Embed(
                            description = "Missing permissions",
                            color = 0xFF0000
                        )
                        await client.say(embed=embed)
                json.dump(json_data, f)
            if channel == cchannel:
                embed = discord.Embed(
                    description="The channel has been locked. Use **-unlockchannel** to unlock it",
                    color=0xFF0000
                )

                await client.say(embed=embed)
            else:
                embed = discord.Embed(
                    description="The channel {} has been locked. Use **-unlockchannel** to unlock it".format(channel.mention),
                    color=0xFF0000
                )

                await client.say(embed=embed)
        else:
            embed = discord.Embed(
                description="Channel is already locked use **-unlockchannel** to unlock it",
                color=0xFF0000
            )

            await client.say(embed=embed)
            return
        bot_perms = channel.overwrites_for(server.me)
        bot_perms_edited = False
        if not bot_perms.read_messages:
            bot_perms.read_messages = True
            bot_perms_edited = True
        if not bot_perms.send_messages:
            bot_perms.send_messages = True
            bot_perms_edited = True
        if bot_perms_edited:
            try:
                await client.edit_channel_permissions(channel, server.me, bot_perms)
            except discord.Forbidden:
                embed = discord.Embed(
                    description = "Missing permissions",
                    color = 0xFF0000
                )
                await client.say(embed=embed)
    else:
        embed = discord.Embed(
            description="You don't have permission to use this command",
            color=0xFF0000
        )

        await client.say(embed=embed)

@client.command(pass_context=True)
async def unlockchannel(ctx, channel: discord.Channel = None):
    author = ctx.message.author
    server = author.server
    cchannel = ctx.message.channel
    if channel == None:
        channel = ctx.message.channel

    if is_owner(author) or author == server.owner:
        path = "locked/" + str(channel.id) + ".json"
        if os.path.exists(path):
            with open(path, "r") as f:
                channel_perms = json.load(f)
                role_list = [role for role in server.roles]
                for role in role_list:
                    if str(role.id) in channel_perms["Channel_Permissions"]:
                        overwrite = discord.PermissionOverwrite()
                        overwrite.send_messages = channel_perms["Channel_Permissions"][str(role.id)]
                        try:
                            await client.edit_channel_permissions(channel, role, overwrite)
                        except discord.Forbidden:
                            embed = discord.Embed(
                                description = "Missing permissions",
                                color = 0xFF0000
                            )
                            await client.say(embed=embed)
                    else:
                        overwrite = discord.PermissionOverwrite()
                        overwrite.send_messages = None
                        try:
                            await client.edit_channel_permissions(channel, role, overwrite)
                        except discord.Forbidden:
                            embed = discord.Embed(
                                description = "Missing permissions",
                                color = 0xFF0000
                            )
                            await client.say(embed=embed)
            os.remove(path)
            if channel == cchannel:
                embed = discord.Embed(
                    description="The channel has been unlocked",
                    color=0x00FF00
                )

                await client.say(embed=embed)
            else:
                embed = discord.Embed(
                    description="The channel {} has been unlocked".format(channel.mention),
                    color=0x00FF00
                )

                await client.say(embed=embed)
        else:
            embed = discord.Embed(
                description="The channel isn't locked use **-lockchannel** to lock it",
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
async def kickbots(ctx):
    author = ctx.message.author
    server = author.server
    channel = ctx.message.channel
    if is_owner(author) or author == server.owner:
        embed = discord.Embed(
            description = "Are you sure you wan't to kick all the bots in the server? (yes/no)",
            color = 0x00FF00
        )
        await client.say(embed=embed)
        user_response = await client.wait_for_message(timeout=40, channel=channel, author=author)
        user_response = user_response.clean_content.lower()
        if user_response == "yes":
            for member in list(server.members):
                if member.bot == True and member != server.me:
                    try:
                        await client.kick(member)
                    except discord.Forbidden:
                        print("I can't kick {}".format(str(member)))

            embed = discord.Embed(
                description = "The bots has been kicked",
                color = 0x00FF00
            )
            await client.say(embed=embed)
        else:
            embed = discord.Embed(
                description = "Command cancelled",
                color = 0x00FF00
            )
            await client.say(embed=embed)
    else:
        embed = discord.Embed(
            description="You don't have permission to use this command",
            color=0xFF0000
        )

        await client.say(embed=embed)

@client.command(pass_context=True)
async def banword(ctx, word: str = None):
    author = ctx.message.author
    server = author.server
    if is_owner(author) == True or author == server.owner:
        if word == None:
            embed = discord.Embed(
                description="You need to write a word",
                color=0xFF0000
            )
            
            await client.say(embed=embed)
        else:
            conn = pymysql.connect(host="sql7.freesqldatabase.com", user="sql7257339", password="yakm4fsd4T", db="sql7257339")
            c = conn.cursor()
            sql = "SELECT * FROM `Banned_Words` WHERE serverid = '{}'".format(server.id)
            c.execute(sql)
            conn.commit()
            data = c.fetchall()
            for d in data:
                bannedword = d[2]
                if word == bannedword:
                    embed = discord.Embed(
                        description="The word `{}` is already banned".format(word),
                        color=0xFF0000
                    )
                    
                    await client.say(embed=embed)
                    return

            sql = "INSERT INTO `Banned_Words` (serverid, word) VALUES ('{}', '{}')".format(server.id, word)
            c.execute(sql)
            conn.commit()
            conn.close()
            c_path = "servers/{}/banned_words.txt".format(str(server.id))
            if not os.path.exists("servers/{}".format(server.id)):
                os.makedirs("servers/{}".format(server.id))

            if os.path.exists(c_path):
                data = open(c_path, "r").read()
                data += "\n{}".format(word)
                with open(c_path, "w") as f:
                    f.write(data)
            else:
                with open(c_path, "w+") as f:
                    f.write(word)

            embed = discord.Embed(
                description="The word `{}` has been successfully banned".format(word),
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
async def unbanword(ctx, word: str = None):
    author = ctx.message.author
    server = author.server
    if is_owner(author) == True or author == server.owner:
        if word == None:
            embed = discord.Embed(
                description="You need to write a word",
                color=0xFF0000
            )
            
            await client.say(embed=embed)
        else:
            conn = pymysql.connect(host="sql7.freesqldatabase.com", user="sql7257339", password="yakm4fsd4T", db="sql7257339")
            c = conn.cursor()
            sql = "SELECT * FROM `Banned_Words` WHERE serverid = '{}'".format(server.id)
            c.execute(sql)
            conn.commit()
            data = c.fetchall()
            wordfound = False
            for d in data:
                bannedword = d[2]
                if word == bannedword:
                    wordfound = True

            if wordfound == True:
                sql = "DELETE FROM `Banned_Words` WHERE serverid = '{}' AND word = '{}'".format(server.id, word)
                c.execute(sql)
                conn.commit()
                conn.close()
                c_path = "servers/{}/banned_words.txt".format(str(server.id))
                if not os.path.exists("servers/{}".format(server.id)):
                    os.makedirs("servers/{}".format(server.id))
                    
                if os.path.exists(c_path):
                    data = open(c_path, "r").read().splitlines()
                    banned_words = ""
                    for d in data:
                        if d != word:
                            if banned_words == "":
                                banned_words = d
                            else:
                                banned_words += "\n{}".format(d)

                    with open(c_path, "w") as f:
                        f.write(banned_words)

                embed = discord.Embed(
                    description="The word `{}` has been successfully unbanned".format(word),
                    color=0x00FF00
                )
                
                await client.say(embed=embed)
            else:
                embed = discord.Embed(
                    description="The word `{}` isn't banned".format(word),
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
async def bannedwords(ctx):
    author = ctx.message.author
    server = author.server
    if is_owner(author) == True or author == server.owner:
        c_path = "servers/{}/banned_words.txt".format(str(server.id))
        if os.path.exists(c_path):
            banned_words = open(c_path, "r").read().splitlines()
            words = ""
            num = 1
            for word in banned_words:
                if words == "":
                    words = "{}. {}".format(num, word)
                else:
                    words += "\n{}. {}".format(num, word)

                num += 1

            if words == "":
                embed = discord.Embed(
                    description="There isn't any banned words",
                    color=0xFF0000
                )
                
                await client.say(embed=embed)
                return

            embed = discord.Embed(
                title = "Banned Words",
                description = words,
                color = 0x00FF00
            )

            await client.send_message(author, embed=embed)

            embed = discord.Embed(
                description = "I have sent you the list of banned words",
                color = 0x00FF00
            )

            await client.say(embed=embed)
        else:
            embed = discord.Embed(
                description="There isn't any banned words",
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
            embed = discord.Embed(
                title="Module Unloaded",
                description="The module {} has been successfully unloaded".format(extension),
                color=0x00FF00
            )
            await client.say(embed=embed)
        except Exception as error:
            print("{} can't be unloaded. [{}]".format(extension, error))


if __name__ == "__main__":
    for extension in extensions:
        try:
            client.load_extension(extension)
        except Exception as error:
            print('{} cannot be loaded. [{}]'.format(extension, error))

    client.loop.create_task(change_status())
    client.loop.create_task(autosave_economy())
    client.loop.create_task(autosave_settings())
    for sig in (SIGABRT, SIGILL, SIGINT, SIGSEGV, SIGTERM):
        signal(sig, save)

    client.run("NDcyODE3MDkwNzg1NzA1OTg1.Dj45QA.A3S3wwN0_lxlQbQCgkC44x-uJJg")
