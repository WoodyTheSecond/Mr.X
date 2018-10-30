import discord
import asyncio
import time
import os, sys
import pymysql
import json
from discord.ext import commands
from random import randint
cooldown_array = []
economy_array = {}

class Economy:
    def __init__(self, client):
        self.client = client

    def ValidInt(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    def create_database(self, server):
        conn = pymysql.connect(host="sql7.freesqldatabase.com", user="sql7257339", password="yakm4fsd4T", db="sql7257339")
        c = conn.cursor()
        sql = "INSERT INTO `Economy_Settings` (serverid, max_work_amount, min_work_amount, max_slut_amount, min_slut_amount) VALUES ('{}', '200', '100', '1000', '500')".format(str(server.id))
        c.execute(sql)
        conn.commit()
        conn.close()

    def update_setting(self, server, setting, value):
        settingspath = "servers/{}/economy_settings.json".format(server.id)
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
        settingspath = "servers/{}/economy_settings.json".format(server.id)
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

    def make_settings(self, server):
        conn = pymysql.connect(host="sql7.freesqldatabase.com", user="sql7257339", password="yakm4fsd4T", db="sql7257339")
        c = conn.cursor()
        sql = "SELECT * FROM `Economy_Settings` WHERE serverid = {}".format(server.id)
        c.execute(sql)
        conn.commit()
        data = c.fetchone()
        conn.close()
        if data == None:
            self.create_database(server)
            return True
        else:
            return False

    def is_owner(self, user):
        if user.id == "164068466129633280" or user.id == "142002197998206976" or user.id == "457516809940107264":
            return True
        else:
            return False

    @commands.command(pass_context=True)
    async def work(self, ctx):
        author = ctx.message.author
        server = ctx.message.server
        if str(author.id) in cooldown_array:
            embed = discord.Embed(
                description = "Command is on cooldown, please wait",
                color = 0xFF0000
            )

            await self.client.say(embed=embed)
        else:
            #Check And Set Settings
            if not server.id in economy_array:
                self.make_settings(server)
                economy_array[server.id] = {}
                economy_array[server.id]["max_work_amount"] = int(self.check_setting(server, "max_work_amount"))
                economy_array[server.id]["min_work_amount"] = int(self.check_setting(server, "min_work_amount"))
                economy_array[server.id]["max_slut_amount"] = int(self.check_setting(server, "max_slut_amount"))
                economy_array[server.id]["min_slut_amount"] = int(self.check_setting(server, "min_slut_amount"))
            #Actual Work Code
            path = "eco/{}.json".format(author.id)
            if not os.path.exists(path):
                amount_earned = randint(economy_array[server.id]["min_work_amount"], economy_array[server.id]["max_work_amount"])
                with open(path, "w+") as f:
                    json_data = {}
                    json_data[server.id] = {}
                    json_data[server.id]["Money"] = amount_earned
                    json_data[server.id]["Bank"] = 0
                    json.dump(json_data, f)

                embed = discord.Embed(
                    description = "You earned **{:,}**".format(amount_earned),
                    color = 0x00b8ff
                )

                await self.client.say(embed=embed)
            else:
                with open(path, "r") as f:
                    economy = json.load(f)
                    if str(server.id) in economy:
                        print("Found")
                    else:
                        economy[server.id] = {}
                        economy[server.id]["Money"] = 0
                        economy[server.id]["Bank"] = 0
                        with open(path, "w") as f:
                            json.dump(economy, f)

                amount_earned = randint(economy_array[server.id]["min_work_amount"], economy_array[server.id]["max_work_amount"])
                current_money = None
                with open(path, "r") as f:
                    economy = json.load(f)
                    if economy[server.id]["Money"]:
                        current_money = int(economy[server.id]["Money"])
                    else:
                        current_money = 0
                        economy[server.id]["Money"] = 0

                    economy[server.id]["Money"] = current_money + amount_earned
                    with open(path, "w") as f:
                        json.dump(economy, f)
                        
                embed = discord.Embed(
                    description = "You earned **{:,}**".format(amount_earned),
                    color = 0x00b8ff
                )

                await self.client.say(embed=embed)
            cooldown_array.append(str(author.id))
            await asyncio.sleep(5)
            cooldown_array.remove(str(author.id))

    @commands.command(pass_context=True)
    async def bal(self, ctx, user: discord.Member = None):
        author = ctx.message.author
        server = ctx.message.server
        current_money = 0
        current_bank = 0
        if user == None:
            path = "eco/" + str(author.id) + ".json"
            if not os.path.exists(path):
                with open(path, "w+") as f:
                    json_data = {}
                    json_data[server.id] = {}
                    json_data[server.id]["Money"] = 0
                    json_data[server.id]["Bank"] = 0
                    json.dump(json_data, f)

            with open(path, "r") as f:
                if not str(server.id) in f.read():
                    with open(path, "w+") as f:
                        json_data = {}
                        json_data[server.id] = {}
                        json_data[server.id]["Money"] = 0
                        json_data[server.id]["Bank"] = 0
                        json.dump(json_data, f)
                            
            with open(path, "r") as f:
                economy = json.load(f)
                if economy[server.id]["Money"] != None:
                    current_money = int(economy[server.id]["Money"])
                else:
                    economy[server.id]["Money"] = 0
                    with open(path, "w") as f:
                        json.dump(economy, f)

            with open(path, "r") as f:
                economy = json.load(f)
                if economy[server.id]["Bank"] != None:
                    current_bank = int(economy[server.id]["Bank"])
                else:
                    economy[server.id]["Bank"] = 0
                    with open(path, "w") as f:
                        json.dump(economy, f)

            networth_balance = current_money + current_bank
            embed = discord.Embed(
                description = "**Balance Information**",
                color = 0x00FF00
            )
            embed.add_field(name="Money: ", value=":moneybag:{:,}".format(current_money), inline=True)
            embed.add_field(name="Bank: ", value=":moneybag:{:,}".format(current_bank), inline=True)
            embed.add_field(name="Net Worth: ", value=":moneybag:{:,}".format(networth_balance), inline=True)
            await self.client.say(embed=embed)
        else:
            path = "eco/" + str(user.id) + ".json"
            if not os.path.exists(path):
                with open(path, "w+") as f:
                    json_data = {}
                    json_data[server.id] = {}
                    json_data[server.id]["Money"] = 0
                    json_data[server.id]["Bank"] = 0
                    json.dump(json_data, f)

            with open(path, "r") as f:
                if not str(server.id) in f.read():
                    with open(path, "w+") as f:
                        json_data = {}
                        json_data[server.id] = {}
                        json_data[server.id]["Money"] = 0
                        json_data[server.id]["Bank"] = 0
                        json.dump(json_data, f)

            with open(path, "r") as f:
                economy = json.load(f)
                if economy[server.id]["Money"] != None:
                    current_money = int(economy[server.id]["Money"])

            with open(path, "r") as f:
                economy = json.load(f)
                if economy[server.id]["Bank"] != None:
                    current_bank = int(economy[server.id]["Bank"])
            networth_balance = current_money + current_bank
            embed = discord.Embed(
                description = "{} **Balance Information**".format(user.mention),
                color = 0x00FF00
            )
            embed.add_field(name="Money: ", value=":moneybag:{:,}".format(current_money), inline=True)
            embed.add_field(name="Bank: ", value=":moneybag:{:,}".format(current_bank), inline=True)
            embed.add_field(name="Net Worth: ", value=":moneybag:{:,}".format(networth_balance), inline=True)
            await self.client.say(embed=embed)


    @commands.command(pass_context=True)
    async def withdraw(self, ctx, amount = None):
        author = ctx.message.author
        server = ctx.message.server
        current_money = 0
        current_bank = 0
        if amount != None:
            amount = amount.replace(",", "")
            amount = amount.replace(".", "")

        if amount == None:
            embed = discord.Embed(
                description = "You need to write the amount you want to withdraw",
                     color = 0xFF0000
            )
            await self.client.say(embed=embed)
            return

        if amount.lower() == "all":
            path = "eco/" + str(author.id) + ".json"
            if not os.path.exists(path):
                with open(path, "w+") as f:
                    json_data = {}
                    json_data[server.id] = {}
                    json_data[server.id]["Money"] = 0
                    json_data[server.id]["Bank"] = 0
                    json.dump(json_data, f)
                embed = discord.Embed(
                    description = "You don't have anything to withdraw",
                    color = 0xFF0000
                )
                await self.client.say(embed=embed)
                return
            else:
                with open(path, "r") as f:
                    economy = json.load(f)
                    if economy[server.id]["Bank"] != None:
                        current_bank = int(economy[server.id]["Bank"])
                    else:
                        economy[server.id]["Bank"] = 0
                        with open(path, "w") as f:
                            json.dump(economy, f)
                        embed = discord.Embed(
                            description = "You don't have anything to withdraw",
                            color = 0xFF0000
                        )
                        await self.client.say(embed=embed)
                        return

                with open(path, "r") as f:
                    economy = json.load(f)
                    if economy[server.id]["Money"] != None:
                        current_bank = int(economy[server.id]["Money"])
                    else:
                        economy[server.id]["Money"] = 0
                        with open(path, "w") as f:
                            json.dump(economy, f)
            if current_bank == 0:
                embed = discord.Embed(
                    description = "You don't have anything to withdraw",
                    color = 0xFF0000
                )
                await self.client.say(embed=embed)
                return
            elif current_bank > 0:
                new_bal = current_money + current_bank
                with open(path, "r") as f:
                    economy = json.load(f)
                    economy[server.id]["Bank"] = 0
                    economy[server.id]["Money"] = new_bal
                    with open(path, "w") as f:
                        json.dump(economy, f)
                embed = discord.Embed(
                    description = "You have withdrawed **{:,}** from your bank".format(int(current_bank)),
                    color = 0x00FF00
                )
                await self.client.say(embed=embed)
                return
        elif self.ValidInt(amount) == False:
             embed = discord.Embed(
                description = "Please enter a number/all",
                color = 0xFF0000
             )
             await self.client.say(embed=embed)
             return

        elif amount.startswith("-"):
            embed = discord.Embed(
                description = "You cannot deposit a negative number",
                color = 0xFF0000
            )
            await self.client.say(embed=embed)
            return

        else:
            print("There was a number!")
            amount = int(amount)
            path = "eco/{}.json".format(author.id)
            if not os.path.exists(path):
                with open(path, "w+") as f:
                    json_data = {}
                    json_data[server.id] = {}
                    json_data[server.id]["Money"] = 0
                    json_data[server.id]["Bank"] = 0
                    json.dump(json_data, f)
                    embed = discord.Embed(
                        description = "You don't have anything to withdraw",
                        color = 0xFF0000
                    )

                    await self.client.say(embed=embed)
                return
            else:
                with open(path, "r") as f:
                    economy = json.load(f)
                    if economy[server.id] != None:
                        current_money = int(economy[server.id]["Money"])
                    else:
                        economy[server.id]["Money"] = 0
                        with open(path, "w") as f:
                            json.dump(economy, f)

                with open(path, "r") as f:
                    economy = json.load(f)
                    if economy[server.id] != None:
                        current_bank = int(economy[server.id]["Bank"])
                    else:
                        economy[server.id]["Bank"] = 0
                        with open(path, "w") as f:
                            json.dump(economy, f)
                        embed = discord.Embed(
                            description = "You don't have anything to withdraw",
                            color = 0xFF0000
                        )
                        await self.client.say(embed=embed)
                        return

            if current_bank == 0:
                embed = discord.Embed(
                    description = "You don't have anything to withdraw",
                    color = 0xFF0000
                )
                await self.client.say(embed=embed)
                return
            elif current_bank >= amount:
                current_bank -= amount
                with open(path, "r") as f:
                    economy = json.load(f)
                    economy[server.id]["Money"] = current_money + amount
                    economy[server.id]["Bank"] = current_bank
                    with open(path, "w") as f:
                        json.dump(economy, f)

                embed = discord.Embed(
                    description = "You have successfully withdrawn **{:,}** from your bank".format(amount),
                    color = 0x00FF00
                )
                await self.client.say(embed=embed)
            else:
                embed = discord.Embed(
                    description = "You don't have enough money in your bank to withdraw **{:,}**".format(amount),
                    color = 0xFF0000
                )
                await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def give(self, ctx, user: discord.Member = None, amount = None):
        author = ctx.message.author
        server = ctx.message.server
        if amount != None:
            amount = amount.replace(",", "")
            amount = amount.replace(".", "")
            
        if user == None:
            embed = discord.Embed(
                description = "You have not tagged any user",
                color = 0xFF0000
            )
            await self.client.say(embed=embed)
            return
        elif amount == None:
            embed = discord.Embed(
                description = "You need to specify how much you want to give",
                color = 0xFF0000
            )
            await self.client.say(embed=embed)
            return
        elif self.ValidInt(amount) == False:
            embed = discord.Embed(
                description = "Please specify a valid integer",
                color = 0xFF0000
            )
            await self.client.say(embed=embed)
            return

        amount = int(amount)
        if amount <= 0:
            embed = discord.Embed(
                description = "The amount must be higher than 0",
                color = 0xFF0000
            )
            await self.client.say(embed=embed)
            return

        path = "eco/{}.json".format(str(author.id))
        userpath = "eco/{}.json".format(str(user.id))
        economy = None
        user_economy = None
        current_money = None
        user_current_money = None
        if not os.path.exists(path):
            with open(path, "w+") as f:
                json_data = {}
                json_data[server.id] = {}
                json_data[server.id]["Money"] = 0
                json_data[server.id]["Bank"] = 0
                json.dump(json_data, f)

        with open(path, "r") as f:
            if not str(server.id) in f.read():
                with open(path, "w+") as f:
                    json_data = {}
                    json_data[server.id] = {}
                    json_data[server.id]["Money"] = 0
                    json_data[server.id]["Bank"] = 0
                    json.dump(json_data, f)

        if not os.path.exists(userpath):
            with open(userpath, "w+") as f:
                json_data = {}
                json_data[server.id] = {}
                json_data[server.id]["Money"] = 0
                json_data[server.id]["Bank"] = 0
                json.dump(json_data, f)

        with open(userpath, "r") as f:
            if not str(server.id) in f.read():
                with open(userpath, "w+") as f:
                    json_data = {}
                    json_data[server.id] = {}
                    json_data[server.id]["Money"] = 0
                    json_data[server.id]["Bank"] = 0
                    json.dump(json_data, f)

        with open(path, "r") as f:
            economy = json.load(f)
            if economy[server.id]["Money"] != None:
                current_money = int(economy[server.id]["Money"])
            else:
                economy[server.id]["Money"] = 0
                with open(path, "w") as f:
                    json.dump(economy, f)

        with open(userpath, "r") as f:
            user_economy = json.load(f)
            if user_economy[server.id]["Money"] != None:
                user_current_money = int(user_economy[server.id]["Money"])
            else:
                user_economy[server.id]["Money"] = 0
                with open(userpath, "w") as f:
                    json.dump(user_economy, f)

        if current_money < amount:
            embed = discord.Embed(
                description = "You don't have enough money to give **{:,}**".format(amount),
                color = 0xFF0000
            )
            await self.client.say(embed=embed)
            return

        user_economy[server.id]["Money"] = user_current_money + amount
        economy[server.id]["Money"] = current_money - amount
        with open(userpath, "w") as f:
            json.dump(user_economy, f)

        with open(path, "w") as f:
            json.dump(economy, f)

        embed = discord.Embed(
            description = "{} has successfully received **{:,}** money from you".format(user.mention, amount),
            color = 0x00FF00
        )
        await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def dep(self, ctx, amount = None):
        author = ctx.message.author
        server = ctx.message.server
        current_money = 0
        current_bank = 0
        if amount != None:
            amount = amount.replace(",", "")
            amount = amount.replace(".", "")

        if amount == None:
            embed = discord.Embed(
                description = "You need to write the amount you want to deposit",
                color = 0xFF0000
            )

            await self.client.say(embed=embed)
            return
            
        if amount.lower() == "all":
            path = "eco/" + str(author.id) + ".json"
            if not os.path.exists(path):
                with open(path, "w+") as f:
                    json_data = {}
                    json_data[server.id] = {}
                    json_data[server.id]["Money"] = 0
                    json_data[server.id]["Bank"] = 0
                    json.dump(json_data, f)

                embed = discord.Embed(
                    description = "You don't have anything to deposit",
                    color = 0xFF0000
                )

                await self.client.say(embed=embed)
                return
            else:
                with open(path, "r") as f:
                    economy = json.load(f)
                    if economy[server.id]["Money"] != None:
                        current_money = int(economy[server.id]["Money"])
                    else:
                        economy[server.id]["Money"] = 0
                        with open(path, "w") as f:
                            json.dump(economy, f)

                        embed = discord.Embed(
                            description = "You don't have anything to deposit",
                            color = 0xFF0000
                        )

                        await self.client.say(embed=embed)
                        return

                with open(path, "r") as f:
                    economy = json.load(f)
                    if economy[server.id]["Bank"] != None:
                        current_bank = int(economy[server.id]["Bank"])
                    else:
                        economy[server.id]["Bank"] = 0
                        with open(path, "w") as f:
                            json.dump(economy, f)

            if current_money == 0:
                embed = discord.Embed(
                    description = "You don't have anything to deposit",
                    color = 0xFF0000
                )

                await self.client.say(embed=embed)
                return
            elif current_money > 0:
                with open(path, "r") as f:
                    economy = json.load(f)
                    economy[server.id]["Money"] = 0
                    economy[server.id]["Bank"] = current_bank + current_money
                    with open(path, "w") as f:
                        json.dump(economy, f)

                embed = discord.Embed(
                    description = "You have successfully deposited **{:,}** to your bank".format(current_money),
                    color = 0x00FF00
                )

                await self.client.say(embed=embed)
                return
        elif self.ValidInt(amount) == False:
             embed = discord.Embed(
                description = "Please enter a number/all",
                color = 0xFF0000
             )

             await self.client.say(embed=embed)
             return
        elif amount.startswith("-"):
            embed = discord.Embed(
                description = "You cannot deposit a negative number",
                color = 0xFF0000
            )
            await self.client.say(embed=embed)
            return

        else:
            print("There was a number!")
            amount = int(amount)
            path = "eco/" + str(author.id) + ".json"
            if not os.path.exists(path):
                with open(path, "w+") as f:
                    json_data = {}
                    json_data[server.id] = {}
                    json_data[server.id]["Money"] = 0
                    json_data[server.id]["Bank"] = 0
                    json.dump(json_data, f)

                embed = discord.Embed(
                    description = "You don't have anything to deposit",
                    color = 0xFF0000
                )

                await self.client.say(embed=embed)
                return
            else:
                with open(path, "r") as f:
                    economy = json.load(f)
                    if economy[server.id]["Money"] != None:
                        current_money = int(economy[server.id]["Money"])
                    else:
                        economy[server.id]["Money"] = 0
                        with open(path, "w") as f:
                            json.dump(economy, f)

                        embed = discord.Embed(
                            description = "You don't have anything to deposit",
                            color = 0xFF0000
                        )

                        await self.client.say(embed=embed)
                        return

                with open(path, "r") as f:
                    economy = json.load(f)
                    if economy[server.id]["Bank"] != None:
                        current_bank = int(economy[server.id]["Bank"])
                    else:
                        economy[server.id]["Bank"] = 0
                        with open(path, "w") as f:
                            json.dump(economy, f)
            if current_money == 0:
                embed = discord.Embed(
                        description = "You don't have anything to deposit",
                        color = 0xFF0000
                )

                await self.client.say(embed=embed)
                return
            elif current_money >= amount:
                current_money -= amount
                with open(path, "r") as f:
                    economy = json.load(f)
                    economy[server.id]["Money"] = current_money
                    economy[server.id]["Bank"] = current_bank + amount
                    with open(path, "w") as f:
                        json.dump(economy, f)
                embed = discord.Embed(
                    description = "You have successfully deposited **{:,}** to your bank".format(amount),
                    color = 0x00FF00
                )
                await self.client.say(embed=embed)
                return
            else:
                embed = discord.Embed(
                    description = "You don't have **{:,}**".format(amount),
                    color = 0xFF0000
                )

                await self.client.say(embed=embed)
                return
    
    @commands.command(pass_context=True)
    async def setmax(self, ctx, setting = None, amount = None):
        author = ctx.message.author
        server = author.server
        if author.server_permissions.administrator:
            if amount != None:
                amount = amount.replace(",", "")
                amount = amount.replace(".", "")

            if setting == None or amount == None:
                embed = discord.Embed(
                    description = "You need to write a setting and a value",
                    color = 0xFF0000
                )

                await self.client.say(embed=embed)
                return

            if self.ValidInt(amount) == False:
                embed = discord.Embed(
                    description = "Please enter a valid integer",
                    color = 0xFF0000
                )

                await self.client.say(embed=embed)
                return
            elif amount.startswith("-"):
                embed = discord.Embed(
                    description = "You can't set a negative integer",
                    color = 0xFF0000
                )

                await self.client.say(embed=embed)
                return

            setting = setting.lower()
            amount = int(amount)
            if setting == "work":
                min_amount = int(self.check_setting(server, "min_work_amount"))
                if amount < min_amount:
                    embed = discord.Embed(
                        description = "The maximum amount can't be lower than the minimum amount",
                        colour = 0xFF0000
                    )
                    
                    await self.client.say(embed=embed)
                    return

                self.update_setting(server, "max_work_amount", amount)
                if not server.id in economy_array:
                    economy_array[server.id] = {}
                    economy_array[server.id]["max_work_amount"] = amount
                else:
                    economy_array[server.id]["max_work_amount"] = amount

            elif setting == "slut":
                min_amount = int(self.check_setting(server, "min_slut_amount"))
                if amount < min_amount:
                    embed = discord.Embed(
                        description = "The maximum amount can't be lower than the minimum amount",
                        colour = 0xFF0000
                    )
                    
                    await self.client.say(embed=embed)
                    return

                self.update_setting(server, "max_slut_amount", amount)
                if not server.id in economy_array:
                    economy_array[server.id] = {}
                    economy_array[server.id]["max_slut_amount"] = amount
                else:
                    economy_array[server.id]["max_slut_amount"] = amount

            embed = discord.Embed(
                description = "The maximum **{}** amount has been set to **{:,}**".format(setting, amount),
                color = 0x00FF00
            )

            await self.client.say(embed=embed)
        else:
            embed = discord.Embed(
                description = "You don't have permission to use this command",
                colour = 0xFF0000
            )
            
            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def setmin(self, ctx, setting = None, amount = None):
        author = ctx.message.author
        server = author.server
        if author.server_permissions.administrator:
            if amount != None:
                amount = amount.replace(",", "")
                amount = amount.replace(".", "")

            if setting == None or amount == None:
                embed = discord.Embed(
                    description = "You need to write a setting and a value",
                    color = 0xFF0000
                )

                await self.client.say(embed=embed)
                return

            if self.ValidInt(amount) == False:
                embed = discord.Embed(
                    description = "Please enter a valid integer",
                    color = 0xFF0000
                )

                await self.client.say(embed=embed)
                return
            elif amount.startswith("-"):
                embed = discord.Embed(
                    description = "You can't set a negative integer",
                    color = 0xFF0000
                )

                await self.client.say(embed=embed)
                return

            setting = setting.lower()
            amount = int(amount)
            if setting == "work":
                max_amount = int(self.check_setting(server, "max_work_amount"))
                if amount > max_amount:
                    embed = discord.Embed(
                        description = "The minimum amount can't be higher than the maximum amount",
                        colour = 0xFF0000
                    )
                    
                    await self.client.say(embed=embed)
                    return

                self.update_setting(server, "min_work_amount", amount)
                if not server.id in economy_array:
                    economy_array[server.id] = {}
                    economy_array[server.id]["min_work_amount"] = amount
                else:
                    economy_array[server.id]["min_work_amount"] = amount

            elif setting == "slut":
                max_amount = int(self.check_setting(server, "max_slut_amount"))
                if amount > max_amount:
                    embed = discord.Embed(
                        description = "The minimum amount can't be higher than the maximum amount",
                        colour = 0xFF0000
                    )
                    
                    await self.client.say(embed=embed)
                    return

                self.update_setting(server, "min_slut_amount", amount)
                if not server.id in economy_array:
                    economy_array[server.id] = {}
                    economy_array[server.id]["min_slut_amount"] = amount
                else:
                    economy_array[server.id]["min_slut_amount"] = amount

            embed = discord.Embed(
                description = "The minimum **{}** amount has been set to **{:,}**".format(setting, amount),
                color = 0x00FF00
            )

            await self.client.say(embed=embed)
        else:
            embed = discord.Embed(
                description = "You don't have permission to use this command",
                colour = 0xFF0000
            )
            
            await self.client.say(embed=embed)

    @commands.command(pass_context=True)
    async def setmoney(self, ctx, amount = None, user: discord.Member = None):
        author = ctx.message.author
        server = author.server
        if self.is_owner(author) or author == server.owner:
            if amount != None:
                amount = amount.replace(",", "")
                amount = amount.replace(".", "")

            if amount == None:
                embed = discord.Embed(
                    description = "You need to specify an amount",
                    colour = 0xFF0000
                )
                
                await self.client.say(embed=embed)
                return

            if self.ValidInt(amount) == False:
                embed = discord.Embed(
                    description = "Please enter a valid integer",
                    color = 0xFF0000
                )

                await self.client.say(embed=embed)
                return

            amount = int(amount)
            if user == None:
                path = "eco/{}.json".format(str(author.id))
                if not os.path.exists(path):
                    with open(path, "w+") as f:
                        json_data = {}
                        json_data[server.id] = {}
                        json_data[server.id]["Money"] = 0
                        json_data[server.id]["Bank"] = 0
                        json.dump(json_data, f)

                with open(path, "r") as f:
                    if not str(server.id) in f.read():
                        with open(path, "w+") as f:
                            json_data = {}
                            json_data[server.id] = {}
                            json_data[server.id]["Money"] = 0
                            json_data[server.id]["Bank"] = 0
                            json.dump(json_data, f)

                with open(path, "r") as f:
                    economy = json.load(f)
                    economy[server.id]["Money"] = amount
                    with open(path, "w") as f:
                        json.dump(economy, f)

                embed = discord.Embed(
                    description = "Your money has been successfully set to **{:,}**".format(amount),
                    colour = 0x00FF00
                )
                
                await self.client.say(embed=embed)
            else:
                path = "eco/{}.json".format(str(user.id))
                if not os.path.exists(path):
                    with open(path, "w+") as f:
                        json_data = {}
                        json_data[server.id] = {}
                        json_data[server.id]["Money"] = 0
                        json_data[server.id]["Bank"] = 0
                        json.dump(json_data, f)

                with open(path, "r") as f:
                    if not str(server.id) in f.read():
                        with open(path, "w+") as f:
                            json_data = {}
                            json_data[server.id] = {}
                            json_data[server.id]["Money"] = 0
                            json_data[server.id]["Bank"] = 0
                            json.dump(json_data, f)

                with open(path, "r") as f:
                    economy = json.load(f)
                    economy[server.id]["Money"] = amount
                    with open(path, "w") as f:
                        json.dump(economy, f)

                embed = discord.Embed(
                    description = "The user {} money has been successfully set to **{:,}**".format(user.mention, amount),
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
    async def setbank(self, ctx, amount = None, user: discord.Member = None):
        author = ctx.message.author
        server = author.server
        if self.is_owner(author) or author == server.owner:
            if amount != None:
                amount = amount.replace(",", "")
                amount = amount.replace(".", "")
                
            if amount == None:
                embed = discord.Embed(
                    description = "You need to specify an amount",
                    colour = 0xFF0000
                )
                
                await self.client.say(embed=embed)
                return

            if self.ValidInt(amount) == False:
                embed = discord.Embed(
                    description = "Please enter a valid integer",
                    color = 0xFF0000
                )

                await self.client.say(embed=embed)
                return

            amount = int(amount)
            if user == None:
                path = "eco/{}.json".format(str(author.id))
                if not os.path.exists(path):
                    with open(path, "w+") as f:
                        json_data = {}
                        json_data[server.id] = {}
                        json_data[server.id]["Money"] = 0
                        json_data[server.id]["Bank"] = 0
                        json.dump(json_data, f)

                with open(path, "r") as f:
                    if not str(server.id) in f.read():
                        with open(path, "w+") as f:
                            json_data = {}
                            json_data[server.id] = {}
                            json_data[server.id]["Money"] = 0
                            json_data[server.id]["Bank"] = 0
                            json.dump(json_data, f)

                with open(path, "r") as f:
                    economy = json.load(f)
                    economy[server.id]["Bank"] = amount
                    with open(path, "w") as f:
                        json.dump(economy, f)

                embed = discord.Embed(
                    description = "Your bank money has been successfully set to **{:,}**".format(amount),
                    colour = 0x00FF00
                )
                
                await self.client.say(embed=embed)
            else:
                path = "eco/{}.json".format(str(user.id))
                if not os.path.exists(path):
                    with open(path, "w+") as f:
                        json_data = {}
                        json_data[server.id] = {}
                        json_data[server.id]["Money"] = 0
                        json_data[server.id]["Bank"] = 0
                        json.dump(json_data, f)

                with open(path, "r") as f:
                    if not str(server.id) in f.read():
                        with open(path, "w+") as f:
                            json_data = {}
                            json_data[server.id] = {}
                            json_data[server.id]["Money"] = 0
                            json_data[server.id]["Bank"] = 0
                            json.dump(json_data, f)

                with open(path, "r") as f:
                    economy = json.load(f)
                    economy[server.id]["Bank"] = amount
                    with open(path, "w") as f:
                        json.dump(economy, f)

                embed = discord.Embed(
                    description = "The user {} bank money has been successfully set to **{:,}**".format(user.mention, amount),
                    colour = 0x00FF00
                )
                
                await self.client.say(embed=embed)
        else:
            embed = discord.Embed(
                description = "You don't have permission to use this command",
                colour = 0xFF0000
            )
            
            await self.client.say(embed=embed)

def setup(client):
    client.add_cog(Economy(client))
