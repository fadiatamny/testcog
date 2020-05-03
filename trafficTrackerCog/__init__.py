from .trafficCog import TrafficCog
from redbot.core.bot import Red

def setup(bot: Red):
    bot.add_cog(TrafficCog(bot))