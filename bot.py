import discord
import random
from discord.ext import commands
import datetime
from discord.utils import get
import requests
from PIL import Image, ImageFont, ImageDraw
import io
import os

PREFIX = '.'

client = commands.Bot(command_prefix = PREFIX)
client.remove_command('help')

# Онлайн бота
@client.event
async def on_ready():
	print("Bot is online")

	await client.change_presence(status = discord.Status.online, activity = discord.Game('.help'))

@client.event
async def on_message(message):
	await client.process_commands(message)
	badwords = ['долбаёб', 'лузер', 'сучара', 'дибил', 'иди на хуй', 'гандон', 'гандониха', 'чмо', 'мразь', 'дура', 'шмара', 'еблан', 'гадзила йобана', 'гадзила ёбана', 'годзила ёбана', 'гадзила ёбаная', 'годзила ёбаная', 'годзила йобаная', 'гадзила йобаная', 'годзила йобана', 'шлюха', 'тьотя шлюха', 'дура без трусов', 'иди нахуй', 'нахуй иди', 'на хуй иди', 'хуйло', 'даун', 'сука', 'днище', 'чмо', 'лох', 'лошара', 'чмошник', 'пидар', 'гандон', 'пизда', 'блядина', 'блядский', 'мудозвон', 'выёбывается', 'доебался', 'ебало', 'заебал', 'объебал', 'тупой', 'уёбище', 'твою мать']
	unwarnusers = ['Cordl1nk#6609', 'Kowak#7454']
	for word in badwords:
		if word in message.content.lower():
			if str(message.author) not in unwarnusers:
				warnFile = open('warns.txt', 'a')
				warnFile.write(str(message.author.mention) + '\n')
				warnFile.close()
				warnFile = open('warns.txt', 'r')
				warnedUsers = []
				for line in warnFile:
					warnedUsers.append(line.strip())
				warnFile.close()
				warns = 0
				for user in warnedUsers:
					if str(message.author.mention) == user:
						warns+=1
				if warns > 4:
					mutedRole = discord.utils.get(message.guild.roles, name="mute")
					await message.author.add_roles(mutedRole)
				channel = client.get_channel(700057004210782308)
				await message.delete()
				await channel.send(f'----------------------------\nЗа человеком {message.author.mention} было замечено нарушение.\nВот его сообщение: \n{message.content}\nНарушение было в канале {message.channel}\nНарушения: {warns}\n')
				await message.channel.send(f'{message.author.mention}, нельзя оскорблять пользователей на нашем сервере, иначе будет мут!')

vk_words = ['привет', 'здаров', 'даров', 'всем привет', 'салам алейкум', 'салам', 'приветик', 'приветики', 'вечер в хату', 'всем привет']

@client.event
async def on_message(message):
	await client.process_commands(message)
	msg = message.content.lower()
	if msg in vk_words:
		emb = discord.Embed(title = 'Кликай сюда чтобы перейти!', description = 'Это страница вк владельца сервера, переходи по ссылке выше для связи с ним!', colour = discord.Color.green(), url = 'https://vk.com/max_1_grozniy')

		emb.set_author(name = client.user.name, icon_url = client.user.avatar_url)
		emb.set_footer(text = message.author.name, icon_url = message.author.avatar_url)
		emb.set_thumbnail(url = 'https://sun1-27.userapi.com/kz43bemMxMrDfrVzTlXctQyc4ZSKCD8Fv-_Sow/ao78Foe_A18.jpg')

		await message.channel.send(embed = emb)

@client.event
async def on_command_error(ctx, error):
	pass

# Hello
@client.command(aliases = ['привет'])
async def hello(ctx):
	author = ctx.message.author
	await ctx.send(f"Привет {author.mention}")
	
# Орёл и решка
@client.command(aliases = ['монета', 'монетка', 'копейка'])
async def eagle(ctx):
    a = random.randint(1, 2)
    if a == 1:
        await ctx.send('Вам выпал орёл')
    else:
        await ctx.send('Вам выпала решка')
	
# VK
@client.command(aliases = ['вк'])
async def ownervk(ctx):
	await ctx.channel.purge(limit =1)
	emb = discord.Embed(title = 'Owner VK', description = 'Это вк владельца сервера', colour = discord.Color.green(), url = 'https://vk.com/max_1_grozniy')

	emb.set_author(name = client.user.name, icon_url = client.user.avatar_url)
	emb.set_footer(text = ctx.author.name, icon_url = ctx.author.avatar_url)
	emb.set_thumbnail(url = 'https://sun1-27.userapi.com/kz43bemMxMrDfrVzTlXctQyc4ZSKCD8Fv-_Sow/ao78Foe_A18.jpg')

	await ctx.send(embed = emb)
	
# Отправка сообщения от имени бота
@client.command(aliases = ['отправить', 'сообщение'])
@commands.has_permissions(administrator= True)
async def say(ctx, channel : discord.TextChannel, *args):
    await ctx.message.delete()
    if not channel:
        await ctx.send('Введите канал, в который вы хотите отправить сообщение')
        return
    if not args:
        await ctx.send('Необходимо ввести текст сообщения')
    text = ''
    for item in args:
        text = text + item + ' '
    await channel.send(text)

# Help
@client.command(aliases = ['помощь', 'команды'], pass_context = True)
async def help(ctx):
	emb = discord.Embed(title = 'Навигация по командам', colour = discord.Color.purple() )

	emb.add_field(name = '{}hello'.format(PREFIX), value = 'Бот вам напишет ``Привет``.')
	emb.add_field(name = '{}warn'.format(PREFIX), value = 'Предупреждает пользователя о нарушении правил (за предупреждение без повода дают бан).')
	emb.add_field(name = '{}mute'.format(PREFIX), value = 'Ограничение на отправку сообщений в чате.')
	emb.add_field(name = '{}kick'.format(PREFIX), value = 'Удаление участника с сервера.')
	emb.add_field(name = '{}ban'.format(PREFIX), value = 'Ограничение доступа к серверу.')
	emb.add_field(name = '{}unban'.format(PREFIX), value = 'Удаление ограничений доступа к серверу.')
	emb.add_field(name = '{}time'.format(PREFIX), value = 'Вы сможете узнать время по МСК.')
	emb.add_field(name = '{}clear'.format(PREFIX), value = 'Очистка чата.')
	emb.add_field(name = '{}ownervk'.format(PREFIX), value = 'ВК владельца дискорд сервера.')
	emb.add_field(name = '{}eagle'.format(PREFIX), value = 'Вы сможете подкинуть монетку.')

	await ctx.send(embed = emb)

# Авто выдача роли
@client.event
async def on_member_join(member):
	channel = client.get_channel(699594346860904538)

	role = discord.utils.get(member.guild.roles, id = 657937863379517440)

	await member.add_roles(role)
	await channel.send(embed = discord.Embed(description = f'Пользователь ``{member.name}``, присоеденился к нам!', color = 0x0c0c0c))

# Time
@client.command(aliases = ['время'], pass_context = True)

async def time(ctx):
	await ctx.channel.purge(limit =1)
	emb = discord.Embed(title = 'Your time', description = 'Вы сможете узнать текущее время по МСК.', colour = discord.Color.orange(), url = 'https://www.timeserver.ru/cities/ru/moscow')

	emb.set_author(name = client.user.name, icon_url = client.user.avatar_url)
	emb.set_footer(text = ctx.author.name, icon_url = ctx.author.avatar_url)
	#emb.set_image(url = 'https://sun9-35.userapi.com/c200724/v200724757/14f24/BL06miOGVd8.png')
	emb.set_thumbnail(url = 'https://sun9-35.userapi.com/c200724/v200724757/14f24/BL06miOGVd8.jpg')

	now_date = datetime.datetime.now()

	emb.add_field(name = 'Time', value = 'Time : {}'.format(now_date))

	await ctx.send(embed = emb)

# Clear message
@client.command(aliases = ['очистить', 'очистка'], pass_context = True)
@commands.has_permissions(administrator = True)
async def clear(ctx, amount : int):
	await ctx.channel.purge(limit = amount)
	
# Warn
@client.command(aliases = ['предупреждение', 'пред'])
@commands.has_any_role(667987928810782742, 661704020330807296, 657937468615557120, 657937316442013696, 661703201145487401)
async def warn(message, member: discord.Member):
	emb = discord.Embed(title = 'Warn', colour = discord.Color.red())
	emb.set_author(name = member.name, icon_url = member.avatar_url)
	emb.add_field(name = 'Warn user', value = 'Warned user : {}'.format(member.mention))
	emb.set_footer(text = 'Предупреждение было от пользователя {}'.format(message.author.name), icon_url = message.author.avatar_url)

	await message.send(embed = emb)

	unwarnusers = ['Cordl1nk#6609', 'Kowak#7454']
	if str(member) not in unwarnusers:
		warnFile = open('warns.txt', 'a')
		warnFile.write(str(member.mention) + '\n')
		warnFile.close()
		warnFile = open('warns.txt', 'r')
		warnedUsers = []
		for line in warnFile:
			warnedUsers.append(line.strip())
		warnFile.close()
		warns = 0
		for user in warnedUsers:
			if str(member.mention) == user:
				warns+=1
		if warns > 3:
			mutedRole = discord.utils.get(message.guild.roles, name="mute")
			await member.add_roles(mutedRole)
		channel = client.get_channel(700057004210782308)
		await channel.send(f'----------------------------\nЗа человеком {member.mention} было замечено нарушение.\nНарушение было в канале {message.channel}\nНарушения: {warns}\n')

# Mute
@client.command(aliases = ['мут'])
@commands.has_permissions(administrator = True)

async def mute(ctx, member: discord.Member):
	emb = discord.Embed(title = 'Mute', colour = discord.Color.gold() )
	await ctx.channel.purge(limit = 1)

	mute_role = discord.utils.get(ctx.message.guild.roles, name = "mute")

	emb.set_author(name = member.name, icon_url = member.avatar_url)
	emb.add_field(name = 'Mute user', value = 'Muted user : {}'.format(member.mention))
	emb.set_footer(text = 'Был замутен администратором {}'.format(ctx.author.name), icon_url = ctx.author.avatar_url)
	emb.set_thumbnail(url = 'https://lh3.googleusercontent.com/proxy/Fn6VwQyWS2oJlLaXtyOGWRCxaLPU_gtyoWTlEPwwp96au-qJtGNPDcYmbIl787xBym1QVwO6b-8K209m')

	await ctx.send(embed = emb)
	await member.add_roles(mute_role)

	#await ctx.send(f'У {member.mention}, ограничение на отправку сообщений, за нарушение прав!')

# Kick
@client.command(aliases = ['кик', 'выгнать'], pass_context = True)
@commands.has_permissions(administrator = True)

async def kick(ctx, member: discord.Member, *, reason = None):
	emb = discord.Embed(title = 'Kick', colour = discord.Color.orange() )
	await ctx.channel.purge(limit = 1)

	await member.kick(reason = reason)

	emb.set_author(name = member.name, icon_url = member.avatar_url)
	emb.add_field(name = 'Kick user', value = 'Kicked user : {}'.format(member.mention))
	emb.set_footer(text = 'Был кикнут администратором {}'.format(ctx.author.name), icon_url = ctx.author.avatar_url)
	emb.set_thumbnail(url = 'https://jasonfrye.com/wp-content/uploads//2018/01/delete_user_1516857056.png')

	await ctx.send(embed = emb)

	#await ctx.send(f'User {member.mention} was kicked by admin.')

# Ban
@client.command(aliases = ['бан'], pass_context = True)
@commands.has_permissions(administrator = True)

async def ban(ctx, member: discord.Member, *, reason = None):
	emb = discord.Embed(title = 'Ban', colour = discord.Color.red())
	await ctx.channel.purge(limit = 1)

	await member.ban(reason = reason)

	emb.set_author(name = member.name, icon_url = member.avatar_url)
	emb.add_field(name = 'User was banned by admin.', value = 'Banned user : {}'.format(member.mention))
	emb.set_footer(text = 'Был забанен администратором {}'.format(ctx.author.name), icon_url = ctx.author.avatar_url)
	emb.set_thumbnail(url = 'https://avatanplus.com/files/resources/original/5c1e8a219f3d7167d74b9374.png')

	await ctx.send(embed = emb)

	#await ctx.send(f'User {member.mention} was banned by admin.')

# Unban
@client.command(aliases = ['разбан', 'разбанить'], pass_context = True)
@commands.has_permissions(administrator = True)
async def unban(ctx, *, member):
	await ctx.channel.purge(limit =1)
	banned_users = await ctx.guild.bans()
	for ban_entry in banned_users:
		user = ban_entry.user
		await ctx.guild.unban(user)
		await ctx.send(f'User {user.mention} was unbanned by admin.')
		return

# Личные сообщения
@client.command()
@commands.has_permissions(administrator = True)
async def send_m(ctx, member: discord.Member):
	await member.send(f'{member.name}, привет от {ctx.author.name}')

# Ошибка команд
@clear.error
async def clear_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(f'{ctx.author.name}, обязательно укажите аргумент!')

	if isinstance(error, commands.MissingPermissions):
		await ctx.send(f'{ctx.author.name}, у вас недостаточно прав!')

@kick.error
async def clear_error(ctx, error):
	if isinstance(error, commands.MissingPermissions):
		await ctx.send(f'{ctx.author.name}, у вас недостаточно прав!')

@ban.error
async def clear_error(ctx, error):
	if isinstance(error, commands.MissingPermissions):
		await ctx.send(f'{ctx.author.name}, у вас недостаточно прав!')

@unban.error
async def clear_error(ctx, error):
	if isinstance(error, commands.MissingPermissions):
		await ctx.send(f'{ctx.author.name}, у вас недостаточно прав!')

@mute.error
async def clear_error(ctx, error):
	if isinstance(error, commands.MissingPermissions):
		await ctx.send(f'{ctx.author.name}, у вас недостаточно прав!')

# Run bot
token = os.environ.get('BOT_TOKEN')

client.run(str(token))
