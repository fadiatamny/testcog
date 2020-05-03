import asyncio
import aiohttp
import discord
import json

from redbot.core import Config, checks, commands
from redbot.core.utils.chat_formatting import box, humanize_list, pagify

url = 'https://raw.githubusercontent.com/Kanium/KaniumCogs/master/welcomeCog/data/embedded_message.json'

allowed_guilds = {274657393936302080, 693796372092289024, 508781789737648138}


async def fetchMessage():
    async def fetch():
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                html = await response.text()
                x = json.loads(str(html))
                return x
    return await fetch()


def formatMessage(jsonFormat):
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
        message = discord.Embed(title="Kanium", description='', color=0x3399ff)
        message.add_field(
            name="Welcome", value='Welcome To Kanium !', inline=True)
        return message


class WelcomeCog(commands.Cog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message = ''
        self.channel = None

    @commands.command(name='welcomepreview', case_insensitive=True, description='Shows a preview of the welcome message')
    async def previewMessage(self, ctx):
        try:
            if ctx.guild.id not in allowed_guilds:
                return
            if self.message == '':
                self.message = await fetchMessage()
            message = formatMessage(self.message)
            await ctx.send(content=None, embed=message)
        except():
            print(f'Error Occured!')

    @commands.command(name="channel")
    async def logChannel(self, ctx, channel: discord.TextChannel):

        if not channel in ctx.guild.channels:
            await ctx.send('Channel doesnt exist in guild')
            return

        if not channel.permissions_for(ctx.guild.me).send_messages:
            await ctx.send('No permissions to talk in that channel.')
            return

        self.channel = channel

        await ctx.send(f'I will now send event notices to {channel.mention}.')

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        try:
            if member.guild.id not in allowed_guilds:
                return
            if self.message == '':
                self.message = await fetchMessage()
            message = formatMessage(self.message)
            await member.send(content=None, embed=message)
            if not self.channel in member.guild.channels:
                print('Channel doesnt exist in guild')
                print('User {0} joined'.format(member))
                return
            await self.channel.send('{0} - has joined the server'.format(member))
        except (discord.NotFound, discord.Forbidden):
            print(
                f'Error Occured! sending a dm to {member.display_name} didnt work !')
