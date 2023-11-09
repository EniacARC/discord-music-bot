import asyncio
import os
import random
import discord
from discord.ext import commands
from discord import guild
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice,create_option
from discord import FFmpegPCMAudio
from discord.utils import get

bot_token = "OTQyMzQ1NjQyNzM3NTMyOTY4.YgjJxQ.cjTVm1yAiTvn2g7C7R_Xykfy0k8"
intents = discord.Intents.default()
songs = ['rickroll.wav', 'goat.wav', 'meetTheMadrigals.wav', 'happyBDay.wav', 'Like A Dino.wav']
count = 0
jailed = []
jail_var = 0
intents.members = True
client = commands.Bot(command_prefix='?', intents = intents)
slash = SlashCommand(client, sync_commands=True)

def is_connected(ctx):
    voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    return voice_client and voice_client.is_connected()
def is_member_connected(guild, member):
    for c in guild.channels:
        channel = get_channel_by_name(guild, c.name)
        for m in channel.members:
            if m == member:
                return True
        return False


async def join(ctx):
    global count
    global songs
    if (ctx.author.voice):
        channel = ctx.author.voice.channel
        voice = await channel.connect()
        random.shuffle(songs)
        await play(ctx)
    else:
        #await ctx.send ("you must be in a voice channel", hidden=True)
        await ctx.send("you must be in a voice channel", hidden=True)

async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    if voice.is_playing():
        voice.pause()
        #await ctx.send("music paused", hidden=True)
        await ctx.send("music paused", hidden=True)
    else:
        #await ctx.send("no music is playing at the moment", hidden=True)
        await ctx.send("no music is playing at the moment", hidden=True)

async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    if voice.is_paused():
        voice.resume()
        await ctx.send("music resumed", hidden=True)
    else:
        await ctx.send("no song is paused at the moment", hidden=True)

async def leave(ctx):
    global count
    if (ctx.voice_client):
        await ctx.voice_client.disconnect()
        count = len(songs) + 1
    else:
        await ctx.send("I am not in a voice channel", hidden=True)
    
async def skip(ctx):
    global count
    if (ctx.author.guild_permissions.administrator):
        if is_connected(ctx):
            voice = ctx.guild.voice_client
            if voice.is_playing():
                if count >= len(songs):
                    await leave(ctx)
                else:
                    sr = FFmpegPCMAudio(songs[count])
                    count = count + 1
                    voice.source = sr
            else:
                await ctx.send("no music is playing at the moment", hidden=True)
        else:
            await ctx.send ("the bot is not in a voice channel", hidden=True)
    else:
        await ctx.send("you need to be an admin to use this command", hidden=True)

async def play(ctx):
    global count
    if is_connected(ctx):
        if count >= len(songs):
            await leave(ctx)
            await ctx.send("I have left the voice channel", hidden=True)
            count = 0
        else:
            voice = ctx.guild.voice_client
            source = FFmpegPCMAudio(songs[count])
            count = count + 1
            player = voice.play(source, after = lambda e: asyncio.run_coroutine_threadsafe(play(ctx), client.loop))
    else:
        await join(ctx)
        if is_connected(ctx):
            await ctx.send("connected to voice channel", hidden=True)


@client.event
async def on_ready():
    print("bot is online")
    print("-------------")
def check_if_channel_exists(guild, name):
    for c in guild.channels:
        if c.name == name:
            return True
    return False

def get_channel_by_name(guild, name):
    channel_id = None
    for c in guild.channels:
        if c.name == name:
            return c
    return None

async def create_channel(ctx):
    guild = ctx.guild

    if check_if_channel_exists(guild, 'jail'):
        print('channel exists')
    else:
        if create_channel:
            try:
                channel = await guild.create_voice_channel('jail')
            except:
                await ctx.send("error creating channel test", hidden=True)

def play_rickroll():
    global voice1
    global channel1
    source = FFmpegPCMAudio('rickroll.wav')
    try:
        player = voice1.play(source, after = lambda x = None: play_rickroll())
    except:
        print('error at play_rickroll')

@slash.slash(
    name="jail",
    description="put a user in a timeout in jail, or set them free I don't care",
    guild_ids = [704300383576653854,819982486322282506],
    options=[
        create_option(
            name="who",
            description="put someone is jail",
            required=True,
            option_type=6
        )
    ]

)
async def jail(ctx:SlashContext, who:SlashContext):
    global jailed
    global jail_var
    if (ctx.author.guild_permissions.administrator):
        for i in range(2):
            guild = ctx.guild
            if who in jailed:
                try:
                    channel = get_channel_by_name(guild, 'jail')
                    jail_var = channel
                    await who.move_to(channel)
                except:
                    pass
            else:
                if check_if_channel_exists(guild, 'jail'):
                    pass
                else:
                    await create_channel(ctx)
                channel = get_channel_by_name(guild, 'jail')
                jail_var = channel
                jailed.append(who)
                global voice1
                global channel1
                channel1 = get_channel_by_name(guild, 'jail')
                voice1 = await channel1.connect()
                await ctx.send(f"{who} get jailed lol")
                try:
                    await who.move_to(channel)
                except:
                    await ctx.send("error")
                play_rickroll()
    else:
        await ctx.send("you need to be an admin to use this command", hidden=True)
    
@slash.slash(
    name="free",
    description="set a jailed person jailed people",
    guild_ids = [704300383576653854,819982486322282506],
    options=[
            create_option(
                name="who",
                description="free someone",
                required=True,
                option_type=6
        )
    ]

)
async def free(ctx:SlashCommand, who:SlashContext):
        global jailed
        global jail_var
        guild = ctx.guild
        if (ctx.author.guild_permissions.administrator):
            if who in jailed:
                member = who
                jailed.remove(member)
                await ctx.send(f"{member} is now free")
                channel = None
                await member.move_to(channel)
            else:
                await ctx.send("user not jailed", hidden=True)
        else:
            await ctx.send("you need to be an admin to use this command", hidden=True)
        
    #for c in guild.channels:
        #if c.name == 'jail':
            #try:
                #member = c.members[0]
            #except:
                #await ctx.send("no one in jail")
                #member = None
            #break
    

@client.event
async def on_voice_state_update(member, before, after):
    global jail_var
    global jailed
    global voice1
    global channel1
    if jail_var is None:
        pass
    elif before.channel is jail_var and after.channel is not None: 
        if member in jailed:
            try:
                await member.move_to(jail_var)
            except:
                print("an error occured")
            if len(jailed) == 0:
                await jail_var.delete()
    #elif before.channel is jail_var and after.channel is None: 
        #if member in jailed:
            #await member.move_to(jail_var)
        #try:        
            #x = jail_var.members[0]
        #except:
            #print("test")
            #await jail_var.delete()
    elif before.channel is None and after.channel is not None:
        if member in jailed:
            try:
                await member.move_to(jail_var)
            except:
                print("an error ocurred")



@slash.slash(
    name="black_list",
    description="gives you a list of all people that were kicked or banned from the server",
    guild_ids = [704300383576653854,819982486322282506],
    options=[
        create_option(
            name="get",
            description="get the list",
            required=True,
            option_type=3,
            choices=[
                create_choice(
                    name = "get",
                    value="get"
                )
            ]
        )
    ]
)
async def black_list(ctx:SlashContext, get:SlashContext):
    if (ctx.author.guild_permissions.administrator):
        filesize = os.path.getsize("Black_list.txt")
        if filesize == 0:
            await ctx.send("empty", hidden=True)
        else:
            with open('Black_list.txt') as f:
                    contents = f.read()
                    await ctx.send(contents, hidden=True)
    else:
        await ctx.send("you need to be an admin to use this command", hidden=True)
@client.event
async def on_member_remove(member):
    m = str(member)
    with open("Black_list.txt", "a") as myfile:
        myfile.write(f"{m}\n")


@client.event
async def on_member_join(member):
    m = str(member)
    with open("Black_list.txt", "r") as fp:
        lines = fp.readlines()

    with open("Black_list.txt", "w") as fp:
        for line in lines:
            if line.strip("\n") != m:
                fp.write(line)

@slash.slash(
    name="impersonate",
    description="send messages that looked like another user sent them",
    guild_ids = [704300383576653854,819982486322282506],
    options=[
        create_option(
            name="message",
            description="what's the message?",
            required=True,
            option_type=3
        ),
        create_option(
            name="member",
            description="which member would you like to impersonate as",
            required=True,
            option_type=6
        )
    ]
)
async def impersonate(ctx:SlashContext, member:SlashContext, *, message:SlashContext):
    if (ctx.author.guild_permissions.administrator):
        webhook = await ctx.channel.create_webhook(name=member.name)
        await webhook.send(
            str(message), username=member.name, avatar_url=member.avatar_url)

        webhooks = await ctx.channel.webhooks()
        for webhook in webhooks:
            await webhook.delete()
    else:
        await ctx.send("you need to be an admin to use this command", hidden=True)
@slash.slash(
    name="party",
    description="play, skip, pause, resume and so much more...",
    guild_ids = [704300383576653854,819982486322282506],
    options=[
        create_option(
            name="action",
            description="enter wanted action",
            required=True,
            option_type=3,
            choices=[
                create_choice(
                    name="skip",
                    value="skip",
                ),
                create_choice(
                    name="pause",
                    value="pause",
                ),
                create_choice(
                    name="resume",
                    value="resume",
                ),
                create_choice(
                    name="play",
                    value="play",
                ),
                create_choice(
                    name="leave",
                    value="leave",
                )
            ]
        )
    ]
)
async def party(ctx:SlashContext, action:str):
        if(action == "play"):
            await play(ctx)
        elif(action == "skip"):
            await skip(ctx)
        elif(action == "pause"):
            await pause(ctx)
        elif(action == "resume"):
            await resume(ctx)
        elif(action == "leave"):
            await leave(ctx)
client.run(bot_token)