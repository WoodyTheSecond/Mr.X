import discord
import asyncio
import time
import os, sys
import pymysql
import json
from discord.ext import commands
cooldown_array = []


class Economy:
    def __init__(self, client):
        self.client = client

    def ValidInt(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    @commands.command(pass_context=True)
    async def work(self, ctx):
        author = ctx.message.author
        server = ctx.message.server
        if str(author.id) in cooldown_array:
            embed = discord.Embed(
            title = '',
            description = 'Command is on cooldown, please wait',
            colour = discord.Colour.red()
            )
            await self.client.say(embed=embed)
        else:
            path = "eco/" + str(author.id) + ".json"
            if not os.path.exists(path):
                with open(path, 'w+') as f:
                    json_data = {}
                    json_data[server.id] = {}
                    json_data[server.id]["Money"] = 100
                    json_data[server.id]["Bank"] = 0
                    json.dump(json_data, f)
                await self.client.say("You earned 100")
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

                with open(path, 'r') as f:
                    economy = json.load(f)
                    if economy[server.id]["Money"]:
                        current_money = int(economy[server.id]["Money"])
                    else:
                        current_money = 0
                        economy[server.id]["Money"] = 0

                    economy[server.id]["Money"] = current_money + 100
                    with open(path, 'w') as f:
                        json.dump(economy, f)
                await self.client.say("You earned 100")
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
                with open(path, 'w+') as f:
                    json_data = {}
                    json_data[server.id] = {}
                    json_data[server.id]["Money"] = 0
                    json_data[server.id]["Bank"] = 0
                    json.dump(json_data, f)
            else:
                with open(path, 'r') as f:
                    economy = json.load(f)
                    if economy[server.id]["Money"] != None:
                        current_money = int(economy[server.id]["Money"])
                    else:
                        economy[server.id]["Money"] = 0
                        with open(path, 'w') as f:
                            json.dump(economy, f)

                with open(path, 'r') as f:
                    economy = json.load(f)
                    if economy[server.id]["Bank"] != None:
                        current_bank = int(economy[server.id]["Bank"])
                    else:
                        economy[server.id]["Bank"] = 0
                        with open(path, 'w') as f:
                            json.dump(economy, f)

            networth_balance = current_money + current_bank
            embed = discord.Embed(
            title = 'Economy Information',
            colour = discord.Colour.green()
            )
            embed.add_field(name='Money:', value=str(current_money), inline=True)
            embed.add_field(name='Bank:', value=str(current_bank), inline=True)
            embed.add_field(name='Net Worth:', value=str(networth_balance), inline=True)
            await self.client.say(embed=embed)
        else:
            path = "eco/" + str(user.id) + ".json"
            if not os.path.exists(path):
                print("User has no money")
            else:
                with open(path, 'r') as f:
                    economy = json.load(f)
                    if economy[server.id]["Money"] != None:
                        current_money = int(economy[server.id]["Money"])

                with open(path, 'r') as f:
                    economy = json.load(f)
                    if economy[server.id]["Bank"] != None:
                        current_bank = int(economy[server.id]["Bank"])
            networth_balance = current_money + current_bank
            embed = discord.Embed(
            description = "**{}'s Balance Information**".format(user.mention),
            colour = discord.Colour.green()
            )
            embed.add_field(name='Money:', value=str(current_money), inline=True)
            embed.add_field(name='Bank:', value=str(current_bank), inline=True)
            embed.add_field(name='Net Worth:', value=str(networth_balance), inline=True)
            await self.client.say(embed=embed)


    @commands.command(pass_context=True)
    async def withdraw(self, ctx, amount = None):
        author = ctx.message.author
        server = ctx.message.server
        current_money = 0
        current_bank = 0
        if amount == None:
            embed = discord.Embed(
            title = '',
            description = 'You have not entered any amount to withdraw',
            colour = discord.Colour.red()
            )
            await self.client.say(embed=embed)
            return
        if amount.lower() == "all":
            path = "eco/" + str(author.id) + ".json"
            if not os.path.exists(path):
                with open(path, 'w+') as f:
                    json_data = {}
                    json_data[server.id] = {}
                    json_data[server.id]["Money"] = 0
                    json_data[server.id]["Bank"] = 0
                    json.dump(json_data, f)
                embed = discord.Embed(
                title = '',
                description = 'You do not have anything to withdraw',
                colour = discord.Colour.red()
                )
                await self.client.say(embed=embed)
                return
            else:
                with open(path, 'r') as f:
                    economy = json.load(f)
                    if economy[server.id]["Bank"] != None:
                        current_bank = int(economy[server.id]["Bank"])
                    else:
                        economy[server.id]["Bank"] = 0
                        with open(path, 'w') as f:
                            json.dump(economy, f)
                        embed = discord.Embed(
                        title = '',
                        description = 'You do not have anything to withdraw',
                        colour = discord.Colour.red()
                        )
                        await self.client.say(embed=embed)
                        return

                with open(path, 'r') as f:
                    economy = json.load(f)
                    if economy[server.id]["Money"] != None:
                        current_bank = int(economy[server.id]["Money"])
                    else:
                        economy[server.id]["Money"] = 0
                        with open(path, 'w') as f:
                            json.dump(economy, f)
            if current_bank == 0:
                embed = discord.Embed(
                title = '',
                description = 'You do not have anything to withdraw',
                colour = discord.Colour.red()
                )
                await self.client.say(embed=embed)
                return
            elif current_bank > 0:
                new_bal = current_money + current_bank
                with open(path, 'r') as f:
                    economy = json.load(f)
                    economy[server.id]["Bank"] = 0
                    economy[server.id]["Money"] = new_bal
                    with open(path, 'w') as f:
                        json.dump(economy, f)
                embed = discord.Embed(
                title = '',
                description = 'You have withdrawed **{}** from your bank'.format(str(current_bank)),
                colour = discord.Colour.green()
                )
                await self.client.say(embed=embed)
                return
        elif self.ValidInt(amount) == False:
             embed = discord.Embed(
             title = '',
             description = 'Please enter a number',
             colour = discord.Colour.red()
             )
             await self.client.say(embed=embed)
             return
        elif amount.startswith("-"):
            embed = discord.Embed(
            title = '',
            description = 'You cannot deposit a negative number',
            colour = discord.Colour.red()
            )
            await self.client.say(embed=embed)
            return

        else:
            print("There was a number!")
            path = "eco/" + str(author.id) + ".json"
            if not os.path.exists(path):
                with open(path, 'w+') as f:
                    json_data = {}
                    json_data[server.id] = {}
                    json_data[server.id]["Money"] = 0
                    json_data[server.id]["Bank"] = 0
                    json.dump(json_data, f)
                embed = discord.Embed(
                title = '',
                description = 'You do not have anything to deposit',
                colour = discord.Colour.red()
                )
                await self.client.say(embed=embed)
                return
            else:
                with open(path, 'r') as f:
                    economy = json.load(f)
                    if economy[server.id]["Money"] != None:
                        current_money = int(economy[server.id]["Money"])
                    else:
                        economy[server.id]["Money"] = 0
                        with open(path, 'w') as f:
                            json.dump(economy, f)
                        embed = discord.Embed(
                        title = '',
                        description = 'You do not have anything to deposit',
                        colour = discord.Colour.red()
                        )
                        await self.client.say(embed=embed)
                        return

                with open(path, 'r') as f:
                    economy = json.load(f)
                    if economy[server.id]["Bank"] != None:
                        current_bank = int(economy[server.id]["Bank"])
                    else:
                        economy[server.id]["Bank"] = 0
                        with open(path, 'w') as f:
                            json.dump(economy, f)
            if current_money == 0:
                embed = discord.Embed(
                title = '',
                description = 'You do not have anything to deposit',
                colour = discord.Colour.red()
                )
                await self.client.say(embed=embed)
                return
            elif current_money >= int(amount):
                current_money -= int(amount)
                with open(path, 'r') as f:
                    economy = json.load(f)
                    economy[server.id]["Money"] = current_money
                    economy[server.id]["Bank"] = current_bank + int(amount)
                    with open(path, 'w') as f:
                        json.dump(economy, f)
                embed = discord.Embed(
                title = '',
                description = 'You have desposited **{}** to your bank'.format(str(amount)),
                colour = discord.Colour.green()
                )
                await self.client.say(embed=embed)
                return
            else:
                embed = discord.Embed(
                title = '',
                description = 'You do not have **{}**'.format(str(amount)),
                colour = discord.Colour.red()
                )
                await self.client.say(embed=embed)
                return


    @commands.command(pass_context=True)
    async def dep(self, ctx, amount = None):
        author = ctx.message.author
        server = ctx.message.server
        current_money = 0
        current_bank = 0
        if amount == None:
            embed = discord.Embed(
            title = '',
            description = 'You have not entered any amount to desposit',
            colour = discord.Colour.red()
            )
            await self.client.say(embed=embed)
            return
        if amount.lower() == "all":
            path = "eco/" + str(author.id) + ".json"
            if not os.path.exists(path):
                with open(path, 'w+') as f:
                    json_data = {}
                    json_data[server.id] = {}
                    json_data[server.id]["Money"] = 0
                    json_data[server.id]["Bank"] = 0
                    json.dump(json_data, f)
                embed = discord.Embed(
                title = '',
                description = 'You do not have anything to deposit',
                colour = discord.Colour.red()
                )
                await self.client.say(embed=embed)
                return
            else:
                with open(path, 'r') as f:
                    economy = json.load(f)
                    if economy[server.id]["Money"] != None:
                        current_money = int(economy[server.id]["Money"])
                    else:
                        economy[server.id]["Money"] = 0
                        with open(path, 'w') as f:
                            json.dump(economy, f)
                        embed = discord.Embed(
                        title = '',
                        description = 'You do not have anything to deposit',
                        colour = discord.Colour.red()
                        )
                        await self.client.say(embed=embed)
                        return

                with open(path, 'r') as f:
                    economy = json.load(f)
                    if economy[server.id]["Bank"] != None:
                        current_bank = int(economy[server.id]["Bank"])
                    else:
                        economy[server.id]["Bank"] = 0
                        with open(path, 'w') as f:
                            json.dump(economy, f)
            if current_money == 0:
                embed = discord.Embed(
                title = '',
                description = 'You do not have anything to deposit',
                colour = discord.Colour.red()
                )
                await self.client.say(embed=embed)
                return
            elif current_money > 0:
                with open(path, 'r') as f:
                    economy = json.load(f)
                    economy[server.id]["Money"] = 0
                    economy[server.id]["Bank"] = current_bank + current_money
                    with open(path, 'w') as f:
                        json.dump(economy, f)
                embed = discord.Embed(
                title = '',
                description = 'You have desposited **{}** to your bank'.format(str(current_money)),
                colour = discord.Colour.green()
                )
                await self.client.say(embed=embed)
                return
        elif self.ValidInt(amount) == False:
             embed = discord.Embed(
             title = '',
             description = 'Please enter a number',
             colour = discord.Colour.red()
             )
             await self.client.say(embed=embed)
             return
        elif amount.startswith("-"):
            embed = discord.Embed(
            title = '',
            description = 'You cannot deposit a negative number',
            colour = discord.Colour.red()
            )
            await self.client.say(embed=embed)
            return

        else:
            print("There was a number!")
            path = "eco/" + str(author.id) + ".json"
            if not os.path.exists(path):
                with open(path, 'w+') as f:
                    json_data = {}
                    json_data[server.id] = {}
                    json_data[server.id]["Money"] = 0
                    json_data[server.id]["Bank"] = 0
                    json.dump(json_data, f)
                embed = discord.Embed(
                title = '',
                description = 'You do not have anything to deposit',
                colour = discord.Colour.red()
                )
                await self.client.say(embed=embed)
                return
            else:
                with open(path, 'r') as f:
                    economy = json.load(f)
                    if economy[server.id]["Money"] != None:
                        current_money = int(economy[server.id]["Money"])
                    else:
                        economy[server.id]["Money"] = 0
                        with open(path, 'w') as f:
                            json.dump(economy, f)
                        embed = discord.Embed(
                        title = '',
                        description = 'You do not have anything to deposit',
                        colour = discord.Colour.red()
                        )
                        await self.client.say(embed=embed)
                        return

                with open(path, 'r') as f:
                    economy = json.load(f)
                    if economy[server.id]["Bank"] != None:
                        current_bank = int(economy[server.id]["Bank"])
                    else:
                        economy[server.id]["Bank"] = 0
                        with open(path, 'w') as f:
                            json.dump(economy, f)
            if current_money == 0:
                embed = discord.Embed(
                title = '',
                description = 'You do not have anything to deposit',
                colour = discord.Colour.red()
                )
                await self.client.say(embed=embed)
                return
            elif current_money >= int(amount):
                current_money -= int(amount)
                with open(path, 'r') as f:
                    economy = json.load(f)
                    economy[server.id]["Money"] = current_money
                    economy[server.id]["Bank"] = current_bank + int(amount)
                    with open(path, 'w') as f:
                        json.dump(economy, f)
                embed = discord.Embed(
                title = '',
                description = 'You have desposited **{}** to your bank'.format(str(amount)),
                colour = discord.Colour.green()
                )
                await self.client.say(embed=embed)
                return
            else:
                embed = discord.Embed(
                title = '',
                description = 'You do not have **{}**'.format(str(amount)),
                colour = discord.Colour.red()
                )
                await self.client.say(embed=embed)
                return





def setup(client):
    client.add_cog(Economy(client))
