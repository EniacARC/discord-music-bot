import asyncio
import random
import discord
from discord.ext import commands
from discord import guild
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice,create_option
from discord import FFmpegPCMAudio


Bot_token = "OTQyMzQ1NjQyNzM3NTMyOTY4.YgjJxQ.cjTVm1yAiTvn2g7C7R_Xykfy0k8"
intents = discord.Intents.all()
songs = ['rickroll.wav', 'meetTheMadrigals.wav', 'rickroll.wav', 'meetTheMadrigals.wav']
count = 0
intents.members = True
client = commands.Bot(command_prefix='!', intents = intents)
slash = SlashCommand(client, sync_commands=True)

def is_connected(ctx):
    voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    return voice_client and voice_client.is_connected()

async def join(ctx):
    global count
    global songs
    if (ctx.author.voice):
        channel = ctx.author.voice.channel
        voice = await channel.connect()
        random.shuffle(songs)
        await play(ctx)
    else:
        await ctx.send ("you must be in a voice channel")

@client.event
async def on_ready():
    print("bot is online")
    print("-------------")
    

async def leave(ctx):
    global count
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
    else:
        ("I am not in a voice channel")

async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    if voice.is_playing():
        voice.pause()
        await ctx.send("music paused")
    else:
        await ctx.send("no music is playing at the moment")

async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    if voice.is_paused():
        voice.resume()
        await ctx.send("music resumed")
    else:
        await ctx.send("no song is paused at the moment")

async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    await ctx.guild.voice_client.disconnect()
    channel = ctx.message.author.voice.channel
    voice = await channel.connect()

async def skip(ctx):
    global count
    if is_connected(ctx):
        voice = ctx.guild.voice_client
        if voice.is_playing():
            if count >= len(songs):
                await leave(ctx)
                await play(ctx)
            else:
                sr = FFmpegPCMAudio(songs[count])
                count = count + 1
                voice.source = sr
                await ctx.send("skipped to the next song")
        else:
            await ctx.send("no music is playing at the moment")
    else:
        await ctx.send ("you must be in a voice channel")

async def play(ctx):
    global count
    if is_connected(ctx):
        if count >= len(songs):
            await ctx.send("I have left the voice channel")
            await leave(ctx)
            count = 0
        else:
            voice = ctx.guild.voice_client
            source = FFmpegPCMAudio(songs[count])
            count = count + 1
            player = voice.play(source, after = lambda e: asyncio.run_coroutine_threadsafe(play(ctx), client.loop))
    else:
        await join(ctx)

@slash.slash(
    name="party",
    description="make the bot play a playlist that will make you want to dance",
    guild_ids = [940918719633293332],
    options=[
        create_option(
            name="action",
            description="choose action",
            required=True,
            option_type=3,
            choices=[
                create_choice(
                    name="skip",
                    value="skip"
                ),
                create_choice(
                    name="play",
                    value="play"
                ),
                create_choice(
                    name="pause",
                    value="pause"
                ),
                create_choice(
                    name="resume",
                    value="resume"
                ),
                create_choice(
                    name="stop",
                    value="stop"
                ),
                create_choice(
                    name="leave",
                    value="leave"
                )
            ]
        )
    ]
)
async def action(ctx:SlashContext, action:str):
    if(action== "play"):
        await play(ctx)
    elif(action == "skip"):
        await skip(ctx)
    elif(action == "pause"):
        await pause(ctx)
    elif(action == "resume"):
        await resume(ctx)
    elif(action == "leave"):
        await leave(ctx)
    elif(action == "stop"):
        await stop(ctx)

client.run(Bot_token)