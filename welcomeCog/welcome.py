import asyncio
import aiohttp
import discord
import json

from redbot.core import Config, checks, commands
from redbot.core.utils.chat_formatting import box, humanize_list, pagify

url = 'https://raw.githubusercontent.com/Kanium/KanuimCogs/master/welcomeCog/data/embedded_message.json'

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
        message=discord.Embed(title=str(jsonFormat['title']), description=''.join(map(str, jsonFormat['description'])), color=hex(jsonFormat['color']))      
        message.set_thumbnail(url=jsonFormat['thumbnail'])
        for field in jsonFormat['fields']:
            if(field['id']!='links'):
                message.add_field(name=field['name'], value=field['value'], inline=field['inline'])
            else:
                message.add_field(name=field['name'], value=''.join(map(str,field['value'])), inline=field['inline'])

        message.set_footer(text=jsonFormat['footer']['text'], icon_url=jsonFormat['footer']['icon_url'])
        return message

    except:
        message=discord.Embed(title="Kanuim", description='', color=0x3399ff)     
        message.add_field(name="Welcome", value='Welcome To Kanuim !', inline=True) 
        return message

class WelcomeCog(commands.Cog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message = ''

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        try:
            if self.message == '':
                self.message = await fetchMessage()
            message = formatMessage(self.message)
            await member.send(content=None, embed=message)
        except (discord.NotFound, discord.Forbidden):
            print(f'Error Occured! sending a dm to {member.display_name} didnt work !')
