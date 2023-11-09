import asyncio
import random
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio


Bot_token = "OTQyMzQ1NjQyNzM3NTMyOTY4.YgjJxQ.cjTVm1yAiTvn2g7C7R_Xykfy0k8"
intents = discord.Intents.default()
songs = ['rickroll.wav', 'meetTheMadrigals.wav', 'scott.wav', 'goat.wav']
count = 0
intents.members = True
client = commands.Bot(command_prefix='?', intents = intents)


#is the bot connect to a voice channel

#check if queue isn't emptu if it isn't play the first item
#queue

def is_connected(ctx):
    voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    return voice_client and voice_client.is_connected()



async def join(ctx):
    global count
    global songs
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        random.shuffle(songs)
        await play(ctx)
    else:
        await ctx.send ("you must be in a voice channel")








#the bot is online
@client.event
async def on_ready():
    print("bot is online")
    print("-------------")


#connect to the user voice channel



#disconnect from a voice channel
@client.command(pass_context = True)
async def leave(ctx):
    global count
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        count = len(songs) + 1
    else:
        ("I am not in a voice channel")

#pause player
@client.command(pass_context = True)
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    if voice.is_playing():
        voice.pause()
        await ctx.send("music paused")
    else:
        await ctx.send("no music is playing at the moment")

#resume player
@client.command(pass_context = True)
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    if voice.is_paused():
        voice.resume()
        await ctx.send("music resumed")
    else:
        await ctx.send("no song is paused at the moment")

#stop player from running

@client.command(pass_context = True)
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
        else:
            await ctx.send("no music is playing at the moment")
    else:
        await ctx.send ("you must be in a voice channel")
        
    


@client.command(pass_context = True)
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






client.run(Bot_token)
