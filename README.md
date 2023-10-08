# Bedtime Bot
A discord bot that enforces a server-wide bedtime in many silly ways.

# Installation
- For voice chat commands to work, install ffmpeg
- For Windows, use `winget install -e --id Gyan.FFmpeg`
- For Ubuntu, install `ffmpeg`

# Configuration
1. Make a file named `.env` (This will be hidden to everyone but you)
2. Paste the code block below into the file
3. Replace everything in quotes (keep the quotes) with your bot's information
4. Replace `MOD_ID` with your server's Mod/Admin role id
5. Replace `TEXT_CHANNEL_ID` with your server's main text channel's id
6. Replace `VC_CHANNEL_ID` with your server's main voice channel's id

```
BOT_TOKEN="YourTokenHere"
PERM_INT="YourPermIntHere"
PUBLIC_KEY="YourKeyHere"
APP_ID="YourAppIdHere"
MOD_ID='YourModRoleIdHere'
CHANNEL_ID='YourBotChannelIdHere'
```

# Running the bot
Type `python3 main.py` to start the bot on your machine
Press `CTRL+C` to shut off the bot

# Use
All commands require the prefix `b!`
Set a server-wide "Bedtime" using `setbedtime <hour> <minutes>`
Set a server-wide "Morning time" using `setmorningtime <hour> <minutes>` (This is when the Bedtime event ends)
For example, type `setbedtime 22 30` to set the Bedtime to `10:30 PM`

When it is Bedtime, the bot will send a message notifying everyone currently online, then server-mute everyone currently in a vc until the Morning Time is reached. (Use `setmorningtime` to configure)
Additionally, the bot will join the voice channel and begin playing some soothing lullabies.

Any user can play/stop/change the songs, but nobody can unmute themselves until Morning time.
This is to encourage the members that are staying up too late to go get some rest.

*"Sleep is the golden chain that ties health and our bodies together."*
*- google.com*