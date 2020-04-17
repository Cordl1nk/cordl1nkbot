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

@client.event
async def on_command_error(ctx, error):
	pass

# Chat filter
#@client.event
#async def on_message(message):
	#await client.process_commands(message)

	#msg = message.content.lower()

	#if msg in bad_words:
		#await message.delete()
		#await message.channel.send(f'{message.author.mention}, нельзя оскорблять пользователей на нашем сервере, иначе будет бан!')

# Hello
@client.command()
async def hello(ctx):
	author = ctx.message.author
	await ctx.send(f"Привет {author.mention}")
	
# Отправка сообщения от имени бота
@client.command()
@commands.has_permissions(administrator= True)
async def say(ctx, channel : discord.TextChannel, *text):
    await ctx.channel.purge(limit=1)
    channel = channel
    text = text[0]
    await channel.send(text)

# Help
@client.command(pass_context = True)
async def help(ctx):
	emb = discord.Embed(title = 'Навигация по командам', colour = discord.Color.purple() )

	emb.add_field(name = '{}hello'.format(PREFIX), value = 'Бот вам напишет ``Привет``.')
	emb.add_field(name = '{}mute'.format(PREFIX), value = 'Ограничение на отправку сообщений в чате.')
	emb.add_field(name = '{}kick'.format(PREFIX), value = 'Удаление участника с сервера.')
	emb.add_field(name = '{}ban'.format(PREFIX), value = 'Ограничение доступа к серверу.')
	emb.add_field(name = '{}unban'.format(PREFIX), value = 'Удаление ограничений доступа к серверу.')
	emb.add_field(name = '{}time'.format(PREFIX), value = 'Вы сможете узнать время по МСК.')
	emb.add_field(name = '{}card/карта'.format(PREFIX), value = 'Вы сможете посмотреть свою карту пользователя.')
	emb.add_field(name = '{}clear'.format(PREFIX), value = 'Очистка чата.')

	await ctx.send(embed = emb)

# Авто выдача роли
@client.event
async def on_member_join(member):
	channel = client.get_channel(699594346860904538)

	role = discord.utils.get(member.guild.roles, id = 657937863379517440)

	await member.add_roles(role)
	await channel.send(embed = discord.Embed(description = f'Пользователь ``{member.name}``, присоеденился к нам!', color = 0x0c0c0c))

# Time
@client.command(pass_context = True)

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
@client.command(pass_context = True)
@commands.has_permissions(administrator = True)
async def clear(ctx, amount : int):
	await ctx.channel.purge(limit = amount)

# Mute
@client.command()
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
@client.command(pass_context = True)
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
@client.command(pass_context = True)
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
@client.command(pass_context = True)
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

# Карточка пользователя
@client.command(aliases = ['card', 'карта']) # .я
async def card_user(ctx):
	await ctx.channel.purge(limit = 1)

	img = Image.new('RGBA', (450, 200), '#232529')
	url = str(ctx.author.avatar_url)[:-10]

	response = requests.get(url, stream = True)
	response = Image.open(io.BytesIO(response.content))
	response = response.convert('RGBA')
	response = response.resize((100, 100), Image.ANTIALIAS)

	img.paste(response, (15, 15, 115, 115))

	idraw = ImageDraw.Draw(img)
	name = ctx.author.name # Kowak
	tag = ctx.author.discriminator # 0000

	headline = ImageFont.truetype('arial.ttf', size = 20)
	undertext = ImageFont.truetype('arial.ttf', size = 12)

	idraw.text((145, 15), f'{name}#{tag}', font = headline) # Kowak#0000
	idraw.text((145, 50), f'ID: {ctx.author.id}', font = undertext)

	img.save('user_card.png')

	await ctx.send(file = discord.File(fp = 'user_card.png'))

# Run bot
token = os.environ.get('BOT_TOKEN')

client.run(str(token))
