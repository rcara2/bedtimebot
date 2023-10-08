# This example requires the 'message_content' privileged intent to function.

import asyncio

import os
import time
import ctypes
import asyncio
import discord
import random

from discord import Member, VoiceChannel
from discord.ext import commands, tasks
from datetime import datetime, timedelta

# Load hidden .env variables
from dotenv import load_dotenv
load_dotenv()


ffmpeg_options = {
    'options': '-vn',
}

# Bed times
bedTime = '04:00'
bedtime_message_sent = False
bed_reset_time = timedelta(hours=1)
bed_last_reset = datetime.now()
# Morning times
morningTime = '07:00'
morningtime_message_sent = False
morning_reset_time = timedelta(hours=1)
morning_last_reset = datetime.now()

# Song folder name
sfxDirectory = 'songs'
bedtimeSong = sfxDirectory + "/song.mp3"

# Gif links (tenor)
gifLink1 = 'https://tenor.com/view/good-night-sweet-dreams-sleep-well-gif-4015556980797084553'
gifLink2 = 'https://tenor.com/view/night-vec50-gif-11520255790124118829'
gifLink3 = 'https://tenor.com/view/good-night-sweet-dreams-moon-night-sky-sparkle-gif-12046229760731247317'
gifLink4 = 'https://tenor.com/view/cant-sleep-gif-11959356397527146816'
gifLink5 = 'https://tenor.com/view/bedtime-story-cat-moon-sleep-bedtime-gif-15162547'
gifLink6 = 'https://tenor.com/view/madison-tweety-tweety-bird-moon-good-night-gif-5706618092637161003'
gifLink7 = 'https://tenor.com/view/good-night2022-night-2022-images-gif-25660176'
gifLink8 = 'https://tenor.com/view/good-night-sleep-tight-cat-reading-bedtime-stories-gif-16391890'
gifLink9 = 'https://tenor.com/view/good-night-rose-flower-sparkle-glitter-gif-6679665730135008078'
gifLinkGoku = 'https://tenor.com/view/goku-go-to-sleep-go-to-bed-super-saiyan-dragon-ball-gif-22557544'
gifLinkBedtime = 'https://tenor.com/view/bed-time-for-me-server-gif-19666702'
gifLinkMorningtime = 'https://tenor.com/view/good-morning-gif-2770330610160702524'

class SimpleCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def randomgif(self, ctx):
        """Sends a random gif"""
        randomGifLink = random.choice([gifLink1, gifLink2, gifLink3, gifLink4, gifLink5, gifLink6, gifLink7, gifLink8, gifLink9])
        await ctx.send(str(randomGifLink))

    @commands.command()
    async def countdown(self, ctx):
        """Send a gif after counting down from 10"""
        for i in range(10,0,-1):
            await ctx.send('Gif Incoming In T-Minus ``' + str(i) + '`` Second(s)...')
            time.sleep(1)
        await ctx.send(str(gifLinkGoku))

    @commands.command()
    async def bedtime(self, ctx):
        """Display the server's current Bedtime"""
        # Format the time in 12-hour clock with am/pm
        formatted_time = datetime.strptime(bedTime, '%H:%M').strftime('%I:%M %p')
        await ctx.send(f'This Server\'s Scheduled Bedtime Is At: `{formatted_time}`')

    @commands.command()
    async def morningtime(self, ctx):
        """Display the server's current Morningtime"""
        # Format the time in 12-hour clock with am/pm
        formatted_time = datetime.strptime(morningTime, '%H:%M').strftime('%I:%M %p')
        await ctx.send(f'This Server\'s Scheduled Morning Time Is At: `{formatted_time}`')

    @commands.command()
    async def songs(self, ctx):
        """Sends a list of all available songs"""
        filenames_message = "Current Songs:\n"

        for filename in os.listdir(os.path.abspath(str(sfxDirectory))):
            filenames_message += f"`{sfxDirectory}/{filename}`\n"

        await ctx.send(filenames_message)

    @commands.command()
    async def invite(self, ctx):
        permInt = str(os.getenv('PERM_INT'))
        appId = str(os.getenv('APP_ID'))
        await ctx.send('https://discord.com/oauth2/authorize/?permissions='+ permInt +'&scope=bot&client_id=' + appId)

    @commands.command()
    async def setbedtime(self, ctx, hour: int, minute: int = 0):
        """Sets the scheduled bedtime for the server (required mod role)"""

        # Check if the user has the mod role
        mod_role_id = int(os.getenv('MOD_ID'))
        mod_role = discord.utils.get(ctx.guild.roles, id=mod_role_id)

        if mod_role in ctx.author.roles:
            # Ensure the provided hour and minute are within valid ranges
            if 0 <= hour <= 23 and 0 <= minute <= 59:
                global bedTime
                bedTime = f'{hour:02d}:{minute:02d}'
                
                # Format the time in 12-hour clock with am/pm
                formatted_time = datetime.strptime(bedTime, '%H:%M').strftime('%I:%M %p')

                await ctx.send(f'Scheduled Bedtime Updated To: `{formatted_time}`')
            else:
                await ctx.send('Invalid Hour Or Minutes Entered.')
        else:
            await ctx.send('You Need Mod Role For This Command.')

    @commands.command()
    async def setmorningtime(self, ctx, hour: int, minute: int = 0):
        """Sets the scheduled morningtime for the server (required mod role)"""

        # Check if the user has the mod role
        mod_role_id = int(os.getenv('MOD_ID'))
        mod_role = discord.utils.get(ctx.guild.roles, id=mod_role_id)

        if mod_role in ctx.author.roles:
            # Ensure the provided hour and minute are within valid ranges
            if 0 <= hour <= 23 and 0 <= minute <= 59:
                global morningTime
                morningTime = f'{hour:02d}:{minute:02d}'
                
                # Format the time in 12-hour clock with am/pm
                formatted_time = datetime.strptime(morningTime, '%H:%M').strftime('%I:%M %p')

                await ctx.send(f'Scheduled Morning Time Updated To: `{formatted_time}`')
            else:
                await ctx.send('Invalid Hour Or Minutes Entered.')
        else:
            await ctx.send('You Need Mod Role For This Command.')

    @commands.command()
    async def unmuteall(self, ctx):
        """Unmute everyone in the server (requires mod role)"""

        # Check if the user has the mod role
        mod_role_id = int(os.getenv('MOD_ID'))
        mod_role = discord.utils.get(ctx.guild.roles, id=mod_role_id)

        if mod_role in ctx.author.roles:
            # Unmute everyone in the server
            for member in ctx.guild.members:
                if isinstance(member, discord.Member) and member.voice and member.voice.mute:
                    await member.edit(mute=False)

            await ctx.send("Unmuted Everyone.")
        else:
            await ctx.send('You Need Mod Role For This Command.')


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command()
    async def play(self, ctx, *, query=None):
        """Plays a file from the local filesystem"""
        message_start = "Chosen song: "

        # If no specific query, play a random song
        if query is None:
            query = self.get_random_song()
            message_start = "Random song: "

        # If query does not exist, send error
        if not os.path.exists(query):
            return await ctx.send("Error: Song Not Found")

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)

        await ctx.send(f'{message_start}{query}')

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.disconnect()

    def get_random_song(self):
        """Gets a random song from the available songs"""
        
        songs_directory = os.path.abspath(str(sfxDirectory))
        songs = [f"{sfxDirectory}/{filename}" for filename in os.listdir(songs_directory)]
        return random.choice(songs)

    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()


# Used in the Bedtime event
async def join_voice_channel_and_mute(guild):
    members_in_voice_channels = [vc for vc in guild.voice_channels if vc.members]
    if members_in_voice_channels:
        target_channel = members_in_voice_channels[0]
    else:
        target_channel = guild.voice_channels[0]

    if target_channel:
        voice_client = await target_channel.connect()
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(bedtimeSong))
        voice_client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)
    

# Check every 5 seconds, and then go on a 1 hour cooldown for each event
@tasks.loop(seconds=5)
async def check_bedtime():
    global bedtime_message_sent, bed_last_reset, morningtime_message_sent, morning_last_reset

    current_time = datetime.now().strftime('%H:%M')
    channel = bot.get_channel(int(os.getenv('TEXT_CHANNEL_ID')))

    # Check if it's time to reset the a flag variable
    if datetime.now() - bed_last_reset >= bed_reset_time:
        bedtime_message_sent = False
        bed_last_reset = datetime.now()

    if datetime.now() - morning_last_reset >= morning_reset_time:
        morningtime_message_sent = False
        morning_last_reset = datetime.now()

    # Begin Bedtime event
    if current_time == bedTime and not bedtime_message_sent:
        await channel.send(f"@ here\n# It's Bedtime!!!!!\n### No More Chatting Until Morning Time!\n*Everyone Has Been Muted.*\n{gifLinkBedtime}")

        # Mute everyone in the server
        for guild_member in channel.guild.members:
            if isinstance(guild_member, Member) and guild_member != channel.guild.me:
                await guild_member.edit(mute=True)
        
        # Continue playing random songs
        await join_voice_channel_and_mute(channel.guild)

        bedtime_message_sent = True  # Update flag variable

    # Begin Morningtime event
    if current_time == morningTime and not morningtime_message_sent:
        await channel.send(f"# Good Morning!\n### It's Time To Rise And Shine!\n*Everyone Has Been Unmuted.*\n{gifLinkMorningtime}")

        # Unmute everyone in the server
        for guild_member in channel.guild.members:
            if isinstance(guild_member, Member) and guild_member.voice and guild_member.voice.mute:
                await guild_member.edit(mute=False)

        morningtime_message_sent = True # Update flag variable


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("b!"),
    description='BedtimeBot',
    intents=intents,
)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    # Start the background task to check bedtime
    check_bedtime.start()

async def main():
    async with bot:
        await bot.add_cog(Music(bot))
        await bot.add_cog(SimpleCommands(bot))
        await bot.start(os.getenv('BOT_TOKEN'))


asyncio.run(main())

# TODO: Make commands to change mod role id, text channel id, and voice channel ids

# Note:
# The bedtime event has a 1 hour cooldown, so if you activate the event, change the bedtime, and then try to activate the event again within an hour, it will not work.
# The morningtime event works the same.
