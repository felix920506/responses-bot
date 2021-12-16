# import libraries

from types import resolve_bases
import discord
import json
from discord.ext import commands
import datetime
from random import randint


# define time function

def clock():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# read credentials file

with open('settings.json','r',encoding="utf-8") as settings_file:
    settings = json.loads(settings_file.read())
    token = settings.get('token')
    owner = settings.get('owner')
    prefix = settings.get('prefix')
    ignore_bot = bool(settings.get('ignore_bot'))

    print(clock() + ' settings loaded successfully')


#read responses from file

with open('responses.json',encoding="utf-8") as res_file:
    responses = json.loads(res_file.read())

    print(clock() + ' responses loaded successfully')


# bot setup

bot = commands.Bot(command_prefix=prefix,description='custom responses bot by felix920506')

@bot.event
async def on_ready():
    print(clock() + ' connected to Discord')


# reload command

@bot.command(brief='reloads responses from file, bot owner only')
async def reload(ctx):
    if ctx.author.id == int(owner):
        print(clock() + ' reload command issued, reloading responses from file')

        with open('responses.json',encoding="utf-8") as res_file:
            global responses
            responses = json.loads(res_file.read())

            # Success Message
            print(clock() + ' responses reloaded successfully')
            await ctx.send('responses reloaded successfully')

    else:
        await ctx.send('you are not the owner')
        print(clock() + f' user {ctx.author} issued "{ctx.message.content}" command but didn\'t have privileges')


# add response command

@bot.command(aliases=['acr','addcustreact'],brief='adds a custom response, server admin only')
@commands.has_guild_permissions(administrator=True)
async def addresponse(ctx,trigger,response):
    global responses
    trigger = trigger.lower()
    if trigger in responses:
        if response in responses[trigger]:
            await ctx.send(f'response "{response}" for trigger "{trigger}" already exists, not adding anything')
            print(clock() + f' response "{response}" for trigger "{trigger}" already exists, not adding anything')

        else:
            responses[trigger].append(response)

            print(clock() + f' response "{response}" to "{trigger}" added')
            await ctx.send(f'new response added:\nTrigger: {trigger}\nResponse: {response}')
            

    else:
        responses[trigger] = [response]

        print(clock() + f' response "{response}" to "{trigger}" added')
        await ctx.send(f'new response added:\nTrigger: {trigger}\nResponse: {response}')
    
    with open('responses.json','w',encoding="utf-8",) as res_file: 
        res_file.write(json.dumps(responses,sort_keys=True, indent=4, ensure_ascii=False))
    
    print(clock() + f' changes have been saved')
    await ctx.send(f'changes have been saved')


# delete response command

@bot.command(aliases=['dcr','delcustreact'],brief='deletes response, server admin only')
@commands.has_guild_permissions(administrator=True)
async def deleteresponse(ctx,trigger,index=-1):
    global responses
    index = int(index)
    trigger = trigger.lower()
    # print(responses)

    old_response = 'something'

    if index == -1:
        del responses[trigger]

        print(clock() + f' all responses to "{trigger}" have been deleted')
        await ctx.send(f'all responses to "{trigger}" have been deleted')
    
    else:    
        old_response = responses[trigger][index]
        del responses[trigger][index]

        print(clock() + f' response "{old_response}" to "{trigger}"" with index of {index} has been deleted.')
        await ctx.send(f'response "{old_response}" with Trigger: {trigger} and index of {index} has been deleted.')

        if index != -1 and len(responses[trigger]) < 1:
            del responses[trigger]

            print(clock() + ' last item was removed from list, deleting empty list')
            ctx.send('last item was removed from list, deleting empty list')

    with open('responses.json','w',encoding="utf-8") as res_file:
        res_file.write(json.dumps(responses,sort_keys=True, indent=4, ensure_ascii=False))


    print(clock() + f' Changes have been saved.')
    await ctx.send(f'Changes have been saved.')
    print(clock() + f' CAUTION! INDEXES OF OTHER MESSAGES MAY HAVE BEEN CHANGED, PLEASE CONFIRM WITH "listresponses" COMMAND OR CHECK "responses.json" FILE BEFORE PROCEEDING.')
    await ctx.send(f'CAUTION! INDEXES OF OTHER MESSAGES MAY HAVE BEEN CHANGED, PLEASE CONFIRM WITH `listresponses` COMMAND BEFORE PROCEEDING.')


# edit response command

@bot.command(aliases=['ecr','editcustreact'],brief='edits response, server admin only')
@commands.has_guild_permissions(administrator=True)
async def editresponse(ctx,trigger,index,response):
    trigger = trigger.lower()
    global responses
    index = int(index)
    old_response = responses[trigger][index]
    responses[trigger][index] = response

    print(clock() + f' response with index of {index} to "{trigger}" has been changed from "{old_response}" to "{response}"')
    await ctx.send(f'response with index of {index} to "{trigger}" has been changed from "{old_response}" to "{response}"')

    with open('responses.json','w',encoding="utf-8") as res_file: 
        res_file.write(json.dumps(responses,sort_keys=True, indent=4, ensure_ascii=False))

    print(clock() + ' changes have been saved')
    await ctx.send('changes have been saved')


# list response trigger command

@bot.command(aliases=['lcr','lts'],brief='list all triggers, server admin only')
@commands.has_guild_permissions(administrator=True)
async def listtriggers(ctx):
    await ctx.send('\n'.join(map(str,responses.keys())))


# list responses by trigger command

@bot.command(aliases=['lrs'],brief='list responses of given trigger, server admin only')
@commands.has_guild_permissions(administrator=True)
async def listreponses(ctx,trigger):
    await ctx.send('\n'.join(map(str,responses[trigger])))


# main function

@bot.event
async def on_message(message):
    if message.content.lower() in responses.keys() and message.author.id != bot.user.id:
        
        print(clock() + f' "{message.content}" detected in message from {message.author} in {message.channel} on server {message.guild}')

        if message.author.bot == False or ignore_bot == False:

            replies = responses.get(message.content.lower())
            reply = replies[randint(1,len(replies))-1]

            await message.channel.send(reply)
            print(clock() + f' replied with "{reply}"')

        else:
            print(clock() + f' message was sent by a bot, ignoring message')


    await bot.process_commands(message)

bot.run(token)