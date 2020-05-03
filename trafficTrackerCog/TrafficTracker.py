import discord
from datetime import datetime

from redbot.core import Config, commands

allowed_guilds = {274657393936302080, 693796372092289024, 508781789737648138}
admin_roles = {'Developer', 'admin', 'Council'}
statsThumbnailUrl = 'https://www.kanium.org/machineroom/logomachine-small.png'

class TrafficTracker(commands.Cog):

    def __init__(self, bot):
        self.channel: discord.TextChannel = None
        self.dailyJoinedCount: int = 0
        self.totalJoinedCount: int = 0
        self.dailyLeftCount: int = 0
        self.totalLeftCount: int = 0
        self.totalLogs: int = 0
        self.toggleLogs: bool = True
        self.date = datetime.now()

    def __checkClock(self):
        currdate = self.date - datetime.now()
        if currdate.days >= 0 :
            self.dailyJoinedCount = 0
            self.dailyLeftCount = 0
            self.date = datetime.now()

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
        message = discord.Embed(title='Server Traffic Stats', description='Statistics on server activity\n\n')
        message.set_thumbnail(url=statsThumbnailUrl)
        message.add_field(name='Daily Joined', value=self.dailyJoinedCount, inline='True')
        message.add_field(name='Daily Left', value='{0}\n'.format(self.dailyLeftCount), inline='True')
        message.add_field(name='Total Traffic', value=self.totalLogs, inline='False')
        message.add_field(name='Total Joined', value=self.totalJoinedCount, inline='True')
        message.add_field(name='Total Left', value=self.totalLeftCount, inline='True')
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
                await self.channel.send('>>> {0} has been unbanned from the server'.format(member.mention))
            self.totalLogs += 1
        except (discord.NotFound, discord.Forbidden):
            print(
                f'Error Occured!')
