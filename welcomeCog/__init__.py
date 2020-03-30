from .welcome import WelcomeCog
from redbot.core.bot import Red

def setup(bot: Red):
    bot.add_cog(WelcomeCog())