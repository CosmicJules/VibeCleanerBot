import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.presences = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

target_channel_id = 519179405533249539
text_target_channel_id = 698674905255772190

badBoys = ['']
goodBoys = ['']
quarantinedBoys = []
gif_url = ''

@bot.event
async def on_ready():
    print('Ready to go!')

@bot.event
async def on_presence_update(before, after):
    game = after.activity
    
    if game is not None and game.name == "Counter-Strike 2" and before.name in badBoys:
        
        print(before.name + ' is playing it')

        print(str(quarantinedBoys))
        target_channel = bot.get_channel(target_channel_id)
        text_target_channel = bot.get_channel(text_target_channel_id)
        
        await text_target_channel.send(f'Quarantining: {after.mention}. No vibes being destroyed today.')
       
        await after.move_to(target_channel)
        
        if game is None or game.name != "Counter-Strike 2" and before.name in badBoys:
            quarantinedBoys.remove(before.name)
            print(str(quarantinedBoys))

@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel and after.channel.id != target_channel_id and member.name in badBoys :
        game = member.activity
        
        if (game is not None and game.name == "Counter-Strike 2") or member.name in quarantinedBoys :
            target_channel = bot.get_channel(target_channel_id)
            await member.move_to(target_channel)

@bot.command()
async def Quarantine(ctx, user: discord.Member):
    await ctx.message.delete()
    if str(ctx.author) in goodBoys:
        print('quarantine that guy')
        if user.name not in quarantinedBoys:
            quarantinedBoys.append(user.name)
            target_channel = ctx.guild.get_channel(target_channel_id)
            await user.move_to(target_channel)
            print(str(quarantinedBoys))
    else:
        text_target_channel = bot.get_channel(text_target_channel_id)
        await text_target_channel.send('Get Drenched, Moron.')
        await text_target_channel.send(gif_url)

@bot.command()
async def Unquarantine(ctx, user: discord.Member):
    await ctx.message.delete()
    if str(ctx.author) in goodBoys:
        quarantinedBoys.remove(user.name)
        print(str(quarantinedBoys))
    else:
        text_target_channel = bot.get_channel(text_target_channel_id)
        await text_target_channel.send('Get Drenched, Moron.')
        await text_target_channel.send(gif_url)

@bot.command()
async def UnquarantineAll(ctx):
    await ctx.message.delete()
    if str(ctx.author) in goodBoys:
        quarantinedBoys = []
        print(str(quarantinedBoys))
    else:
        text_target_channel = bot.get_channel(text_target_channel_id)
        await text_target_channel.send('Get Drenched, Moron.')
        await text_target_channel.send(gif_url)

@bot.command()
async def delete_bot_messages(ctx):
    channel = ctx.channel
    await ctx.message.delete()
    async for message in channel.history(limit=None):
        if message.author.bot and message.author.name == "Vibe Cleaner Bot":
            await message.delete()


bot.run('')