from discord.ext import commands
import discord.utils

def is_owner_check(ctx):
    _id = ctx.message.author.id
    if _id == 142002197998206976 or _id == 164068466129633280:
        return True
    else:
        return False
def is_owner():
    return commands.check(is_owner_check)

def create_settings(servers, serverunit):
    servers[serverunit.id] = {}
    servers[serverunit.id]['Ignore_Hierarchy'] = False
    servers[serverunit.id]['DMWarn'] = True
    servers[serverunit.id]['Verify_Role'] = "none"
    servers[serverunit.id]['Mod_Role'] = "none"
    servers[serverunit.id]['Join_Role'] = "none"
    servers[serverunit.id]['Admin_Role'] = "none"
    servers[serverunit.id]['Mute_Role'] = "none"
    servers[serverunit.id]['WarnMute'] = "1h"
    servers[serverunit.id]['JoinToggle'] = False
    servers[serverunit.id]['CanModAnnounce'] = False
    servers[serverunit.id]['Level_System'] = True
    servers[serverunit.id]['Chat_Filter'] = False

def update_settings(serverunit, setting, set):
    with open('srv_settings.json', 'r') as f:
        servers = json.load(f)
        if not serverunit.id in servers:
            create_settings(servers, serverunit)

    servers[serverunit.id][setting] = set
    with open('srv_settings.json', 'w') as f:
        json.dump(servers, f)

def check_settings(serverunit, setting):
    with open('srv_settings.json', 'r') as f:
        servers = json.load(f)
        setting = servers[serverunit.id][setting]
    return setting
