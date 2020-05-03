# WelcomeCog
This is the Kanium community/guild welcome cog. it sends a DM to any new user that joins the Kanium discord with a [message](./data/embedded_message.json), which has been templated in a json format. 
Furthermore, this cog allows the ability to monitor discord activity and log it into a specific channel using the specific commands.

# How to use:
In order to use our cog you would need to install it onto your instance of [RedBot](https://github.com/Cog-Creators/Red-DiscordBot).


## Requirments:
- Instance of [RedBot](https://github.com/Cog-Creators/Red-DiscordBot)
- Downloader cog has to be loaded. to load:
    `[Prefix]load downloader`

## How to install & load:
1. `[PREFIX]repo add [RepoName] https://github.com/Kanium/KaniumCogs [ActiveBranch  (EX: Master)] `
2. `[PREFIX]cog install [RepoName] welcomeCog`
3. `[PREFIX]load welcomeCog`

### To update the Cog:
- `[PREFIX]cog uninstall welcomeCog`
- `[PREFIX]repo update [RepoName]`
- `[PREFIX]cog install [RepoName] welcomeCog`
- `[PREFIX]load welcomeCog`

### Commands
- `[PREFIX]welcomepreview` - sends in the chat a preview of the template message
- `[PREFIX]pullmessage` - allows you to pull the latest version of your message without restarting the bot

### To modify the sent message:
If you would like to modify the message to your liking, you can either :
- fork the bot. change the [message](./data/embedded_message.json) and [welcome.py](./welcome.py) line 9 to your repo.
- fork the bot. update the [welcome.py](./welcome.py) line 9 to be directed to your message.json file that you like without having it hosted on github with your repo.
