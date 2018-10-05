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

    def check_database(self, server, setting):
        conn = pymysql.connect(host="sql7.freesqldatabase.com", user="sql7257339", password="yakm4fsd4T", db="sql7257339")
        c = conn.cursor()
        sql = "SELECT {} from `Economy_Settings` WHERE serverid = {}".format(setting, str(server.id))
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

    def update_database(self, server, setting, value):
        conn = pymysql.connect(host="sql7.freesqldatabase.com", user="sql7257339", password="yakm4fsd4T", db="sql7257339")
        c = conn.cursor()
        if setting == "max_work_amount":
            sql = "UPDATE `Economy_Settings` SET max_work_amount = %s where serverid = %s"
        elif setting == "min_work_amount":
            sql = "UPDATE `Economy_Settings` SET min_work_amount = %s where serverid = %s"
        elif setting == "max_slut_amount":
            sql = "UPDATE `Economy_Settings` SET max_slut_amount = %s where serverid = %s"
        elif setting == "min_slut_amount":
            sql = "UPDATE `Economy_Settings` SET min_slut_amount = %s where serverid = %s"
        else:
            print("No such setting found")
            return
        t = (value, str(server.id))
        c.execute(sql, t)
        conn.commit()
        conn.close()

    def make_settings(self, server):
        conn = pymysql.connect(host="sql7.freesqldatabase.com", user="sql7257339", password="yakm4fsd4T", db="sql7257339")
        c = conn.cursor()
        sql = "SELECT * FROM `Economy_Settings` WHERE serverid = {}".format(str(server.id))
        c.execute(sql)
        conn.commit()
        data = c.fetchone()
        conn.close()
        if data == None:
            self.create_database(server)
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
                economy_array[server.id]["max_work_amount"] = int(self.check_database(server, "max_work_amount"))
                economy_array[server.id]["min_work_amount"] = int(self.check_database(server, "min_work_amount"))
                economy_array[server.id]["max_slut_amount"] = int(self.check_database(server, "max_slut_amount"))
                economy_array[server.id]["min_slut_amount"] = int(self.check_database(server, "min_slut_amount"))
            #Actual Work Code
            path = "eco/" + str(author.id) + ".json"
            if not os.path.exists(path):
                amount_earned = randint(economy_array[server.id]["min_work_amount"], economy_array[server.id]["max_work_amount"])
                with open(path, 'w+') as f:
                    json_data = {}
                    json_data[server.id] = {}
                    json_data[server.id]["Money"] = amount_earned
                    json_data[server.id]["Bank"] = 0
                    json.dump(json_data, f)

                embed = discord.Embed(
                    description = "You earned **{}**".format(amount_earned),
                    color = 0x00b8ff
                )

                await self.client.say(embed=embed)
            else:
                with open(path, 'r') as f:
                    economy = json.load(f)
                    if str(server.id) in economy:
                        print("Found")
                    else:
                        economy[server.id] = {}
                        economy[server.id]["Money"] = 0
                        economy[server.id]["Bank"] = 0
                        with open(path, 'w') as f:
                            json.dump(economy, f)
                amount_earned = randint(economy_array[server.id]["min_work_amount"], economy_array[server.id]["max_work_amount"])
                with open(path, 'r') as f:
                    economy = json.load(f)
                    if economy[server.id]["Money"]:
                        current_money = int(economy[server.id]["Money"])
                    else:
                        current_money = 0
                        economy[server.id]["Money"] = 0
            
                    economy[server.id]["Money"] = current_money + amount_earned
                    with open(path, 'w') as f:
                        json.dump(economy, f)

                embed = discord.Embed(
                    description = "You earned **{}**".format(amount_earned),
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
            else:
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
            embed.add_field(name="Money: ", value=":moneybag:{}".format(str(current_money)), inline=True)
            embed.add_field(name="Bank: ", value=":moneybag:{}".format(str(current_bank)), inline=True)
            embed.add_field(name="Net Worth: ", value=":moneybag:{}".format(str(networth_balance)), inline=True)
            await self.client.say(embed=embed)
        else:
            path = "eco/" + str(user.id) + ".json"
            if not os.path.exists(path):
                print("User has no money")
            else:
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
            embed.add_field(name="Money: ", value=":moneybag:{}".format(str(current_money)), inline=True)
            embed.add_field(name="Bank: ", value=":moneybag:{}".format(str(current_bank)), inline=True)
            embed.add_field(name="Net Worth: ", value=":moneybag:{}".format(str(networth_balance)), inline=True)
            await self.client.say(embed=embed)


    @commands.command(pass_context=True)
    async def withdraw(self, ctx, amount = None):
        author = ctx.message.author
        server = ctx.message.server
        current_money = 0
        current_bank = 0
        if amount == None:
            embed = discord.Embed(
                description = "You have not entered any amount to withdraw",
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
                    description = "You have withdrawed **{}** from your bank".format(str(current_bank)),
                    color = 0x00FF00
                )
                await self.client.say(embed=embed)
                return
        elif self.ValidInt(amount) == False:
             embed = discord.Embed(
                description = "Please enter a number",
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
            elif current_bank >= int(amount):
                current_bank -= int(amount)
                with open(path, "r") as f:
                    economy = json.load(f)
                    economy[server.id]["Money"] = current_money + int(amount)
                    economy[server.id]["Bank"] = current_bank
                    with open(path, "w") as f:
                        json.dump(economy, f)
                embed = discord.Embed(
                    description = "You don't have anything to withdraw",
                    color = 0xFF0000
                )
                await self.client.say(embed=embed)
                return
            else:
                embed = discord.Embed(
                    description = "You don't have anything to withdraw",
                    color = 0xFF0000
                )
                await self.client.say(embed=embed)
                return

    @commands.command(pass_context=True)
    async def give(self, ctx, user: discord.Member = None, amount = None):
        author = ctx.message.author
        server = ctx.message.server
        if user == None:
            embed = discord.Embed(
                description = "You have not tagged any user",
                color = 0xFF0000
            )
            await self.client.say(embed=embed)
            return
        elif amount == None:
            print("lort")
            
            

    @commands.command(pass_context=True)
    async def dep(self, ctx, amount = None):
        author = ctx.message.author
        server = ctx.message.server
        current_money = 0
        current_bank = 0
        if amount == None:
            embed = discord.Embed(
                description = "You don't have anything to deposit",
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
                    description = "You have successfully deposited **{}** to your bank".format(current_money),
                    color = 0x00FF00
                )

                await self.client.say(embed=embed)
                return
        elif self.ValidInt(amount) == False:
             embed = discord.Embed(
                description = "Please enter a number",
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
            elif current_money >= int(amount):
                current_money -= int(amount)
                with open(path, "r") as f:
                    economy = json.load(f)
                    economy[server.id]["Money"] = current_money
                    economy[server.id]["Bank"] = current_bank + int(amount)
                    with open(path, "w") as f:
                        json.dump(economy, f)
                embed = discord.Embed(
                    description = "You have successfully deposited **{}** to your bank".format(str(amount)),
                    color = 0x00FF00
                )
                await self.client.say(embed=embed)
                return
            else:
                embed = discord.Embed(
                    description = "You don't have **{}**".format(str(amount)),
                    color = 0xFF0000
                )

                await self.client.say(embed=embed)
                return
    
    @commands.command(pass_context=True)
    async def setmax(self, ctx, setting = None, amount = None):
        author = ctx.message.author
        server = author.server
        if author.server_permissions.administrator:
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
                min_amount = int(self.check_database(server, "min_work_amount"))
                if amount < min_amount:
                    embed = discord.Embed(
                        description = "The maximum amount can't be lower than the minimum amount",
                        colour = 0xFF0000
                    )
                    
                    await self.client.say(embed=embed)
                    return

                self.update_database(server, "max_work_amount", amount)
                if not server.id in economy_array:
                    economy_array[server.id] = {}
                    economy_array[server.id]["max_work_amount"] = amount
                else:
                    economy_array[server.id]["max_work_amount"] = amount

            elif setting == "slut":
                min_amount = int(self.check_database(server, "min_slut_amount"))
                if amount < min_amount:
                    embed = discord.Embed(
                        description = "The maximum amount can't be lower than the minimum amount",
                        colour = 0xFF0000
                    )
                    
                    await self.client.say(embed=embed)
                    return

                self.update_database(server, "max_slut_amount", amount)
                if not server.id in economy_array:
                    economy_array[server.id] = {}
                    economy_array[server.id]["max_slut_amount"] = amount
                else:
                    economy_array[server.id]["max_slut_amount"] = amount

            embed = discord.Embed(
                description = "The maximum **{}** amount has been set to **{}**".format(setting, amount),
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
                max_amount = int(self.check_database(server, "max_work_amount"))
                if amount > max_amount:
                    embed = discord.Embed(
                        description = "The minimum amount can't be higher than the maximum amount",
                        colour = 0xFF0000
                    )
                    
                    await self.client.say(embed=embed)
                    return

                self.update_database(server, "min_work_amount", amount)
                if not server.id in economy_array:
                    economy_array[server.id] = {}
                    economy_array[server.id]["min_work_amount"] = amount
                else:
                    economy_array[server.id]["min_work_amount"] = amount

            elif setting == "slut":
                max_amount = int(self.check_database(server, "max_slut_amount"))
                if amount > max_amount:
                    embed = discord.Embed(
                        description = "The minimum amount can't be higher than the maximum amount",
                        colour = 0xFF0000
                    )
                    
                    await self.client.say(embed=embed)
                    return

                self.update_database(server, "min_slut_amount", amount)
                if not server.id in economy_array:
                    economy_array[server.id] = {}
                    economy_array[server.id]["min_slut_amount"] = amount
                else:
                    economy_array[server.id]["min_slut_amount"] = amount

            embed = discord.Embed(
                description = "The minimum **{}** amount has been set to **{}**".format(setting, amount),
                color = 0x00FF00
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
