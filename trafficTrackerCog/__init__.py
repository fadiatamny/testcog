from .trafficTrack import TrafficTrack
from redbot.core.bot import Red

def setup(bot: Red):
    bot.add_cog(TrafficTrack(bot))