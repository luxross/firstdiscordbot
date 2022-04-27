import os
import lightbulb
import hikari
import random
from datetime import datetime
import asyncio
from ossapi import *


api = OssapiV2('CLIENT_ID', 'CLIENT_SECRET')

#imput bot token here
bot = lightbulb.BotApp(
    token='BOT_TOKEN', 
    default_enabled_guilds=(GUILDS)
)

#event that listens for messgaes sent in a server
@bot.listen(hikari.GuildMessageCreateEvent)
async def print_message(event):
    print(event.content)


#event that listens for bot start
@bot.listen(hikari.StartedEvent)
async def bot_started(event):
    print("Bot has started")



#Makes the bot repeat a string
@bot.command
@lightbulb.option('text', 'Text you want to echo', type=str)
@lightbulb.command('repeat', 'Make the bot echo a piece of text')
@lightbulb.implements(lightbulb.SlashCommand)
async def repeat(ctx):
    await ctx.respond(ctx.options.text)

#Command to add two numbers
@bot.command
@lightbulb.option('num2', 'second number', type=int)
@lightbulb.option('num1', 'first number', type=int)
@lightbulb.command('add', 'Ddd two numbers together')
@lightbulb.implements(lightbulb.SlashCommand)
async def add(ctx):
    await ctx.respond(ctx.options.num1 + ctx.options.num2)

#Command to roll a random number without a modifier
@bot.command
@lightbulb.option("upper_limit", 'What you want the maximum roll to be', type=int)
@lightbulb.command('roll', 'Roll a random number')
@lightbulb.implements(lightbulb.SlashCommand)
async def roll(ctx):
    random_integer = random.randint(1, ctx.options.upper_limit)
    await ctx.respond(f"{ctx.member.mention} rolled a {random_integer}", user_mentions=True)
    
#Command to Roll two numbers and store them into a list
@bot.command
@lightbulb.option("upper_limit", 'What you want the maximum roll to be', type=int)
@lightbulb.command('roll_twice', 'Roll two random numbers')
@lightbulb.implements(lightbulb.SlashCommand)
async def roll(ctx):
    rolls = [0,0]
    for i in range(2):
        random_integer = random.randint(1, ctx.options.upper_limit)
        rolls[i-1] = random_integer
    await ctx.respond(f"{ctx.member.mention}'s rolls were {rolls[0]} and {rolls[1]}", user_mentions=True)

#Roll a random number with a modifier
@bot.command
@lightbulb.option('modifier', 'adds or subtracts a number to your roll', type=int, required=True)
@lightbulb.option("upper_limit", 'How high you want your roll', type=int)
@lightbulb.command('rollwithmod', 'Roll a random number with a modifier')
@lightbulb.implements(lightbulb.SlashCommand)
async def roll(ctx):
    random_integer = random.randint(1, ctx.options.upper_limit)
    await ctx.respond(f"{ctx.member.mention} rolled a {random_integer + ctx.options.modifier}({random_integer})",
    user_mentions=True)

#Pings the bot and the latency in ms
@bot.command()
@lightbulb.command("ping", "See the gay little bot's latency.", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx):
    embed=hikari.Embed(title=f"**My gay little ping is *{bot.heartbeat_latency * 1_000:.0f}* ms.**", color=0x6100FF)
    await ctx.respond(embed=embed)

#Shows the version of the bot
@bot.command
@lightbulb.command('version', 'Show the version of the bot')
@lightbulb.implements(lightbulb.SlashCommand)
async def repeat(ctx):
    await ctx.respond("Maid Dress Diluc")

#a little trolling
@bot.command
@lightbulb.option('target', 'the member to troll', hikari.User, required=False)
@lightbulb.command('ip', 'a little trolling')
@lightbulb.implements(lightbulb.SlashCommand)
async def ip(ctx):
    #stores each integer in a variable to help clutter
    str1 = str(random.randint(1, 255))
    str2 = str(random.randint(1, 255))
    str3 = str(random.randint(1, 255))
    str4 = str(random.randint(1, 255))
    await ctx.respond(f"{ctx.options.target.mention}'s ip is {str1}.{str2}.{str3}.{str4}", user_mentions=True)
    
#Get info about a user in the server
@bot.command
@lightbulb.option(
    'target', 'The server member to get information about.', hikari.User, required=False
)
@lightbulb.command(
    'userinfo', 'Get info about a server member'
)


@lightbulb.implements(lightbulb.SlashCommand)
async def userinfo(ctx):
    created_at = int(ctx.options.target.created_at.timestamp())
    joined_at = int(ctx.options.target.joined_at.timestamp())
    
    embed = (
        hikari.Embed(
            title=f"User Info - {ctx.options.target.display_name}",
            description=f"ID: `{ctx.options.target.id}`",
            colour=0xEC0402	,
            timestamp=datetime.now().astimezone(),
        )
        .set_footer(
            text=f"Requested by {ctx.member.display_name}",
            icon=ctx.member.avatar_url or ctx.member.default_avatar_url,
        )
        .set_thumbnail(ctx.options.target.avatar_url or ctx.options.target.default_avatar_url)
        .add_field(
            "Bot?",
            str(ctx.options.target.is_bot),
            inline=True,
        )
        .add_field(
            "Created account on",
            f"<t:{created_at}:d>\n(<t:{created_at}:R>)",
            inline=True,
        )
        .add_field(
            "Joined server on",
            f"<t:{joined_at}:d>\n(<t:{joined_at}:R>)",
            inline=True,
        )
    )

    await ctx.respond(embed)
  

#Grab the weather forecast with a country code and zip code
@bot.command
#@lightbulb.option('country_code', 'The two letter initials of country to pull', type=str)
@lightbulb.option('city', 'What city do you want to pull the weather from?')
@lightbulb.command('weather_forecast', 'Pull a weather forecast for a specified country & zip code.')
@lightbulb.implements(lightbulb.SlashCommand)
async def get_weather(ctx):
    client = python_weather.Client(format=python_weather.IMPERIAL)
    weather = await client.find("ctx.options.city")
    await ctx.respond(weather.current.temperature)


#Shows how gay a user is
@bot.command
@lightbulb.option('target', 'the member to calculate homosexuality for', hikari.User, required=False)
@lightbulb.command('howgay', 'Show how gay the user is')
@lightbulb.implements(lightbulb.SlashCommand)
async def repeat(ctx):
    random_integer = random.randint(0,101)
    embed=hikari.Embed(
        title=f"{ctx.options.target.display_name} is {random_integer}% gay!", 
        color=0xFF0000)
    await ctx.respond(embed=embed)



@bot.command
@lightbulb.option('user_id', 'Use the user id of a profile')
@lightbulb.command('playstyle', 'Find the playstyle of a user')
@lightbulb.implements(lightbulb.SlashCommand)
async def playstyle(ctx):
    await ctx.respond(api.user(ctx.options.user_id).playstyle)

bot.run()
