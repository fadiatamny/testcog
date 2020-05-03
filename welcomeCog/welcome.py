import asyncio
import aiohttp
import discord
import json
from datetime import datetime

from redbot.core import Config, checks, commands
from redbot.core.utils.chat_formatting import box, humanize_list, pagify

url = 'https://raw.githubusercontent.com/Kanium/KaniumCogs/master/welcomeCog/data/embedded_message.json'

allowed_guilds = {274657393936302080, 693796372092289024, 508781789737648138}
admin_roles = {'Developer', 'admin', 'Council'}
statsThumbnailUrl = 'https://www.kanium.org/machineroom/logomachine-small.png'

class WelcomeCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.message: str = ''
        self.channel: discord.TextChannel = None
        self.dailyJoinedCount: int = 0
        self.totalJoinedCount: int = 0
        self.dailyLeftCount: int = 0
        self.totalLeftCount: int = 0
        self.totalLogs: int = 0
        self.toggleLogs: bool = True
        self.date = datetime.now()

    @staticmethod
    async def fetchMessage():
        async def fetch():
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    html = await response.text()
                    x = json.loads(str(html))
                    return x
        return await fetch()

    @staticmethod
    def formatMessage(jsonFormat: str):
        try:
            message = discord.Embed(title=str(jsonFormat['title']), description=''.join(
                map(str, jsonFormat['description'])), color=int(jsonFormat['color'], 16))
            message.set_thumbnail(url=jsonFormat['thumbnail'])
            for field in jsonFormat['fields']:
                if(field['id'] != 'links'):
                    message.add_field(
                        name=field['name'], value=field['value'], inline=field['inline'])
                else:
                    message.add_field(name=field['name'], value=''.join(
                        map(str, field['value'])), inline=field['inline'])

            message.set_footer(
                text=jsonFormat['footer']['text'], icon_url=jsonFormat['footer']['icon_url'])
            return message

        except:
            message = discord.Embed(
                title='Kanium', description='', color=0x3399ff)
            message.add_field(
                name='Welcome', value='Welcome To Kanium !', inline=True)
            return message

    def __checkClock(self):
        currdate = self.date - datetime.now()
        if currdate.day >= 0 :
            self.dailyJoinedCount = 0
            self.dailyLeftCount = 0
            self.date = datetime.now()
            

    @commands.command(name='pullmessage', description='pulls the message from github again')
    @commands.has_any_role(*admin_roles)
    async def pullMessage(self, ctx: commands.Context) -> None:
        try:
            await ctx.trigger_typing()
            self.message = await WelcomeCog.fetchMessage()
            await ctx.send('Welcome message updated')
        except:
            print('error occured fetching message')

    @commands.command(name='welcomepreview', case_insensitive=True, description='Shows a preview of the welcome message')
    @commands.has_any_role(*admin_roles)
    async def previewMessage(self, ctx: commands.Context) -> None:
        try:
            await ctx.trigger_typing()
            if ctx.guild.id not in allowed_guilds:
                return
            if self.message == '':
                self.message = await WelcomeCog.fetchMessage()
            message = WelcomeCog.formatMessage(self.message)
            await ctx.send(content=None, embed=message)
        except():
            print(f'Error Occured!')

    @commands.command(name='setchannel', description='Sets the channel to sends log to')
    @commands.has_any_role(*admin_roles)
    async def setChannel(self, ctx: commands.Context, channel: discord.TextChannel) -> None:
        await ctx.trigger_typing()

        if not channel in ctx.guild.channels:
            await ctx.send('Channel doesnt exist in guild')
            return

        if not channel.permissions_for(ctx.guild.me).send_messages:
            await ctx.send('No permissions to talk in that channel.')
            return

        self.channel = channel

        await ctx.send(f'I will now send event notices to {channel.mention}.')

    @commands.command(name='stats', description='Shows current statistics')
    @commands.has_any_role(*admin_roles)
    async def statistics(self, ctx: commands.Context) -> None:
        self.__checkClock()
        await ctx.trigger_typing()

        statsString = '\nDaily Joined = {0}\tDaily Left = {1}\nTotal Joined = {2}\tTotal Left = {3}\n------------------------\nTotal Logs = {4}'.format(
            self.dailyJoinedCount, self.dailyLeftCount, self.totalJoinedCount, self.totalLeftCount, self.totalLogs)

        message = discord.Embed(title='Server Traffic Stats', description='Statistics on server activity\n\n'.join(statsString))
        message.set_thumbnail(url=statsThumbnailUrl)
        await ctx.send(content=None, embed=message)

    @commands.command(name='resetstats', description='Resets statistics')
    @commands.has_any_role(*admin_roles)
    async def resetStatistics(self, ctx: commands.Context) -> None:
        await ctx.trigger_typing()

        self.dailyJoinedCount = 0
        self.dailyLeftCount = 0
        self.totalJoinedCount = 0
        self.totalLeftCount = 0
        self.totalLogs = 0

        await ctx.send('Successfully reset the statistics')

    @commands.command(name='toggleLogs', description='Toggles the logs functionality on or off')
    @commands.has_any_role(*admin_roles)
    async def toggleLogs(self, ctx: commands.Context) -> None:
        await ctx.trigger_typing()
        self.toggleLogs = not self.toggleLogs
        await ctx.send('Logging functionality is `ON`' if self.toggleLogs else 'Logging functionality is `OFF`')

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        try:
            if member.guild.id not in allowed_guilds:
                return
            if self.message == '':
                self.message = await WelcomeCog.fetchMessage()
            message = WelcomeCog.formatMessage(self.message)
            await member.send(content=None, embed=message)
            self.__checkClock()
            if self.channel in member.guild.channels and self.toggleLogs:
                await self.channel.send('>>> {0} has joined the server'.format(member.mention))
            self.totalJoinedCount += 1
            self.dailyJoinedCount += 1
            self.totalLogs += 1
        except (discord.NotFound, discord.Forbidden):
            print(
                f'Error Occured! sending a dm to {member.display_name} didnt work !')

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member) -> None:
        try:
            self.__checkClock()
            if self.channel in member.guild.channels and self.toggleLogs:
                await self.channel.send('>>> {0} has left the server'.format(member.mention))
            self.totalLeftCount += 1
            self.dailyLeftCount += 1
            self.totalLogs += 1
        except (discord.NotFound, discord.Forbidden):
            print(
                f'Error Occured!')

    @commands.Cog.listener()
    async def on_member_ban(self, guild: discord.Guild, member: discord.Member) -> None:
        try:
            self.__checkClock()
            if self.channel in member.guild.channels and self.toggleLogs:
                await self.channel.send('>>> {0} has been banned from the server'.format(member.mention))
            self.totalLogs += 1
        except (discord.NotFound, discord.Forbidden):
            print(
                f'Error Occured!')

    @commands.Cog.listener()
    async def on_member_ban(self, guild: discord.Guild, member: discord.Member) -> None:
        try:
            self.__checkClock()
            if self.channel in member.guild.channels and self.toggleLogs:
                await self.channel.send('>>> {0} has been unbanned from the server'.format(member.mention))
            self.totalLogs += 1
        except (discord.NotFound, discord.Forbidden):
            print(
                f'Error Occured!')
