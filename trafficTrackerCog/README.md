# TrafficTrackerCog
This is the Kanium community/guild welcome cog. monitors the server for activity and logs them to a specific channel using the specific commands.

# How to use:
In order to use our cog you would need to install it onto your instance of [RedBot](https://github.com/Cog-Creators/Red-DiscordBot).


## Requirments:
- Instance of [RedBot](https://github.com/Cog-Creators/Red-DiscordBot)
- Downloader cog has to be loaded. to load:
    `[Prefix]load downloader`

## How to install & load:
1. `[PREFIX]repo add [RepoName] https://github.com/Kanium/KaniumCogs [ActiveBranch  (EX: Master)] `
2. `[PREFIX]cog install [RepoName] trafficTrackerCog`
3. `[PREFIX]load trafficTrackerCog`

### To update the Cog:
- `[PREFIX]cog uninstall trafficTrackerCog`
- `[PREFIX]repo update [RepoName]`
- `[PREFIX]cog install [RepoName] trafficTrackerCog`
- `[PREFIX]load trafficTrackerCog`

### Commands
- `[PREFIX]setchannel` - allows you to select a channel in your discord to dump logs to
- `[PREFIX]stats` - prints the statistics that the cog has gathered.
- `[PREFIX]resetstats` - allows for a hard reset of the stats
- `[PREFIX]toggleLogs` - Toggles the logs functionality on or off
