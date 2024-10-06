#IMPORTING NECESSARY LIBRARIES

import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import json
import requests
import yt_dlp
import aiohttp
import random
import os

#INTENTS

intents = discord.Intents.default()
intents.message_content = True 
intents.members = True
client=commands.Bot(command_prefix='-', intents=intents)

#BASIC COMMANDS

@client.command()
async def hello(ctx):
    await ctx.send("Hello Human!, How are you?")

@client.command()
async def bye(ctx):
    await ctx.send("Goodbye Human!, See you soon")

@client.command()
async def kritika(ctx):
    await ctx.send("Hey Kritika, How are you?")
    await ctx.send(f"<:monkaS:1287150884748525693> <:pepewow:1287152531167772692> <:Pepega:1287150990629404833>")
    
#EVENTS

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Silas's Server"))
    print("Bot is ready, Hoorahh!!")

@client.event
async def on_member_join(member):
    
    message = f"Welcome to the server, {member.display_name}! 🎉\nWe're excited to have you here. Feel free to explore and join the conversation!"

    embed = discord.Embed(
        title="🎉 Welcome to the Community! 🎉", 
        description=message, 
        color=discord.Color.green()
    )

    embed.set_thumbnail(url="https://cdn.pixabay.com/photo/2017/06/16/17/47/emoji-2416045_960_720.png")
    embed.add_field(
        name="Server Guide", 
        value="Check out the rules and channels to get started! 💬",
        inline=False
    )
    embed.add_field(
        name="Need Help?", 
        value="Feel free to ask any questions in the help channel! 🤔", 
        inline=False
    )
    embed.set_footer(
        text="We're happy to have you with us! 😊",
        icon_url="https://cdn.pixabay.com/photo/2020/09/11/14/00/emoji-5560559_960_720.png"
    )
    channel = client.get_channel(1282705212355907647)

    await member.send(embed=embed)
    
    category_url = "https://jokeapi-v2.p.rapidapi.com/categories"
    headers = {
        "x-rapidapi-key": "1c15998fa5msh35433e7aac88e9bp18053djsn11a8624db585",
        "x-rapidapi-host": "jokeapi-v2.p.rapidapi.com"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(category_url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                categories = data['categories']  

                if categories:
                    selected_category = random.choice(categories) 

                    joke_url = f"https://jokeapi-v2.p.rapidapi.com/joke/{selected_category}"
                    async with session.get(joke_url, headers=headers) as joke_response:
                        if joke_response.status == 200:
                            joke_data = await joke_response.json()
                            if joke_data['type'] == 'single':
                                joke = joke_data['joke']
                            else:
                                joke = f"{joke_data['setup']} ... {joke_data['delivery']}"
                            
                            await channel.send(f"Hey {member.mention}, welcome to the server!")
                            await channel.send(f"'{selected_category}': {joke}")
                        else:
                            await channel.send(f"Oops, couldn't fetch a joke. Error: {joke_response.status}")
                else:
                    await channel.send("Could not retrieve any categories.")
            else:
                await channel.send(f"Oops, couldn't fetch categories. Error: {response.status}")
  
@client.event
async def on_member_remove(member):
    channel=client.get_channel(1282705212355907647)
    await channel.send(f"{member.mention} has left the server")

# MUSIC PART COMMANDS FOR BOT

@client.command(pass_context=True)
async def join(ctx):
    if(ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio('Summertime.mp3', executable='C:/Users/hp/Downloads/ffmpeg/bin/ffmpeg.exe')
        player=voice.play(source)
    else:
        await ctx.send("You are not in a voice channel,Join a vc kiddo.")
        
@client.command(pass_context=True)
async def leave(ctx):
    if(ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("Left the voice channel.")
    else:
        await ctx.send("I am not in a voice channel.")

@client.command(pass_context=True)
async def pause(ctx):
    voice=discord.utils.get(client.voice_clients,guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
        await ctx.send("Paused the audio.")
    else:
        await ctx.send("Currently no audio is playing.")
        
@client.command(pass_context=True)
async def resume(ctx):
    voice=discord.utils.get(client.voice_clients,guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
        await ctx.send("Resumed the audio.")
    else:
        await ctx.send("The audio is not paused.")

@client.command(pass_context=True)
async def stop(ctx):
    voice=discord.utils.get(client.voice_clients,guild=ctx.guild)
    voice.stop()
    await ctx.send("Stopped the audio.")
    
"""
@client.command()
async def play(ctx):
    await ctx.guild.voice_client
    source = FFmpegPCMAudio('Summertime.mp3', executable='C:/Users/hp/Downloads/ffmpeg/bin/ffmpeg.exe')
    player=voice.play(source)
"""

import logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("bot.log"),  
                        logging.StreamHandler()           
                    ])

@client.command()
async def play(ctx, url):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        voice_client = await channel.connect()

        logging.info("Connected to voice channel.")

        ydl_opts = {
            'format': 'bestaudio/best',
            'extractaudio': True,
            'quiet': True,
            'nocheckcertificate': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                audio_url = info['formats'][0]['url']
                logging.info(f"Audio URL: {audio_url}")

                voice_client.play(discord.FFmpegPCMAudio(audio_url, options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'),
                                  after=lambda e: logging.error(f'Player error: {e}') if e else None)

                if voice_client.is_playing():
                    logging.info("Audio is playing.")
                else:
                    logging.info("Audio is not playing.")
            except Exception as e:
                await ctx.send(f"Error: {str(e)}")
                logging.error(f"Error occurred: {str(e)}")
    else:
        await ctx.send("You need to be in a voice channel!")
        logging.warning("User not in a voice channel.")

#KICK AND BAN PEOPLE

from discord.ext.commands import has_permissions,MissingPermissions
from discord import Member
import json

@client.command()
@has_permissions(kick_members=True)
async def kick(ctx,member:discord.Member,*,reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"{member.mention} has been kicked from the server.")

@kick.error
async def kick_error(ctx,error):
    if isinstance(error,commands.MissingPermissions):
        await ctx.send("You don't have permission to kick members.")

@client.command()
@has_permissions(ban_members=True)
async def ban(ctx,member:discord.Member,*,reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"{member.mention} has been banned from the server.")

@ban.error
async def ban_error(ctx,error):
    if isinstance(error,commands.MissingPermissions):
        await ctx.send("You don't have permission to ban members.")

@client.command()
@has_permissions(ban_members=True)
async def unban(ctx, *, member_name: str):
    banned_users = await ctx.guild.bans()  
    member_name, member_discriminator = member_name.split('#') 
    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"{user.mention} has been unbanned from the server.")
            return

    await ctx.send(f"Member {member_name}#{member_discriminator} not found in the ban list.")

@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to unban members.")
    elif isinstance(error, ValueError):
        await ctx.send("Please provide a valid member in the format 'Username#1234'.")

#EMBEDS

@client.command()
async def embed(ctx):
    embed = discord.Embed(
        title="Discord", 
        url="https://discord.com", 
        description="This is a description of Discord", 
        color=0x00ff00
    )
    embed.set_author(
        name=ctx.author.display_name, 
        url="https://discord.com/developers/docs/intro", 
        icon_url=ctx.author.avatar.url  # Updated here
    )
    embed.set_thumbnail(url="https://letsenhance.io/static/8f5e523ee6b2479e26ecc91b9c25261e/1015f/MainAfter.jpg")
    await ctx.send(embed=embed)

#BOTS COMMANDS FOR DM

@client.command()
async def message(ctx, user: discord.Member, *, message=None):
    if message is None:
        message = f"Welcome to the server, {user.display_name}! 🎉\nWe're excited to have you here. Feel free to explore and join the conversation!"

    embed = discord.Embed(
        title="🎉 Welcome to the Community! 🎉", 
        description=message, 
        color=discord.Color.green()
    )

    embed.set_thumbnail(url="https://gratisography.com/wp-content/uploads/2024/01/gratisography-cyber-kitty-800x525.jpg")
    embed.add_field(
        name="Server Guide", 
        value="Check out the rules and channels to get started! 💬",
        inline=False
    )
    embed.add_field(
        name="Need Help?", 
        value="Feel free to ask any questions in the help channel! 🤔", 
        inline=False
    )
    embed.set_footer(
        text="We're happy to have you with us! 😊",
        icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQzk92qOx7c5k5fybjVbUkwg6BGW_ptjgID9A&s"
    )

    await user.send(embed=embed)

#ROLES COMMANDS

from discord.utils import get

@client.command()
@commands.has_permissions(manage_roles=True)
async def addRole(ctx, user: discord.Member, *, role: str):
    role = discord.utils.get(ctx.guild.roles, name=role)
    
    if role is None:
        await ctx.send(f"Role '{role}' not found.")
        return
    
    if role in user.roles:
        await ctx.send(f"{user.mention} already has the role {role.name}.")
    else:
        await user.add_roles(role)
        await ctx.send(f"Role '{role.name}' has been added to {user.mention}.")

@addRole.error
async def role_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to add roles.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please provide a valid member and role.")
      
@client.command(pass_context=True)
@commands.has_permissions(manage_roles=True)
async def removeRole(ctx,user:discord.Member,*,role:discord.Role):
    if role in user.roles:
        await user.remove_roles(role)
        await ctx.send(f"{role} removed from {user.mention}")
    else:
        await user.add_roles(role)
        await ctx.send(f"{user.mention} doesn't have the role {role}")

@removeRole.error
async def role_error(ctx,error):
    if isinstance(error,commands.MissingPermissions):
        await ctx.send("You don't have permission to remove roles.")

# DISCORD BOT RUNNING
client.run(DISCORD_TOKEN)
