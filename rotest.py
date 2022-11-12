import hikari, lightbulb
from lightbulb.ext import tasks
import random
import mc
from mc.builtin import validators
import json, os, sys
import asyncio
welcome_randomsg = ['Только посмотрите!', 'Как такое возможно...', 'ахуеть <:ms_sus:1028286941382332478>']
randtime = [15, 13, 8]

#Starting a bot
bot = lightbulb.BotApp(
    token='OTUwNDk2NjA2OTk2NzkxMzY2.Gm4A3K.9oQpJKfs9OMIKB98oSJc15uudDC3CvbsA7L_nk',
    intents=hikari.Intents.ALL,
    prefix="+",
    banner=None,
)
tasks.load(bot)
@bot.listen(lightbulb.events.LightbulbStartedEvent)
async def synccmds(event):
   await bot.sync_application_commands()
   print("Commands Synced.")

@bot.command
@lightbulb.command("profile", "Базовая информация о пользователе")
@lightbulb.implements(lightbulb.SlashCommand)
async def profile_cmd(ctx: lightbulb.Context):
    ctx.respond(hikari.ResponseType.DEFERRED_MESSAGE_CREATE)
    embed = hikari.Embed(title="Информация о участнике.")
    embed.set_thumbnail(ctx.author.avatar_url)
    embed.color='0x2F3136'
    embed.add_field("User Info",
    f"Никнейм: {ctx.author.username}\nАйди: {ctx.author.id}\nДата Регистрации: {ctx.author.created_at}\nIs_Bot? {ctx.author.is_bot}\nСсылка на Аватарку: {ctx.author.avatar_url}")
    await ctx.respond(embed)

@bot.command
@lightbulb.app_command_permissions(dm_enabled = False)
@lightbulb.option('amount', "Кол-во сообщений которое нужно удалить", required=True, type=int)
@lightbulb.add_checks(lightbulb.checks.human_only, lightbulb.checks.has_role_permissions(hikari.Permissions.MANAGE_GUILD))
@lightbulb.command("clear", description="Очищает сообщения в чате.")
@lightbulb.implements(lightbulb.SlashCommand)
async def clean_msg(ctx: lightbulb.Context):
    ctx.respond(hikari.ResponseType.DEFERRED_MESSAGE_CREATE)
    iterator = (
        bot.rest.fetch_messages(ctx.channel_id)
        .filter(lambda message: ...)
        .limit(ctx.options.amount)
    )
    async for messages in iterator.chunk(ctx.options.amount):
      await bot.rest.delete_messages(ctx.channel_id, messages)
      await ctx.respond("Канал теперь чист как новый!", flags=hikari.MessageFlag.EPHEMERAL)
      print(ctx.options.amount)


@clean_msg.set_error_handler
async def clean_hdl(event: lightbulb.CommandErrorEvent):
    if isinstance(event.exception, lightbulb.MissingRequiredPermission):
        event.context.respond(hikari.ResponseType.DEFERRED_MESSAGE_CREATE)
        await event.context.respond("Вы не имеете роли, у которой есть доступ к очистке.", flags=hikari.MessageFlag.EPHEMERAL)
        exception = event.exception.__cause__ or event.exception
        print(exception)
        
@bot.command
@lightbulb.command('check', description="Checks the bots ping, and if bot's alive")
@lightbulb.implements(lightbulb.SlashCommand)
async def check_cmd(ctx: lightbulb):
    ctx.respond(hikari.ResponseType.DEFERRED_MESSAGE_CREATE)
    heartbeat = ctx.bot.heartbeat_latency * 1000
    embed = hikari.Embed(title="Kamii's Moderatium Info")
    embed.add_field("Current status", "Current Status: **online**" + '\n' + f"Ping: {heartbeat:,.2f} ms 🏓" + '\n' + '\n'
    "dev: **[kamii#2700](https://discord.com/users/341210088423292928)**")
    embed.color='#F3F3F3'
    await ctx.respond(embed)

@bot.listen(hikari.MemberCreateEvent)
async def welcome_event(event: hikari.MemberCreateEvent):
    guild = event.get_guild()
    channel = guild.system_channel_id
    embed = hikari.Embed(title= random.choice(welcome_randomsg), description="К нам присоединился новый участник!")
    embed.add_field("User Info",
    f"Ник: {event.member.username}" + '\n' f"Айди: **`{event.member.id}`** " + '\n')
    embed.set_thumbnail(event.member.avatar_url)
    embed.set_footer(f"Наше количество: {guild.member_count}")
    await bot.rest.create_message(channel, embed)
    await event.user.send("Добро пожаловать в глэээк скуат буэ")

@bot.command
@lightbulb.app_command_permissions(dm_enabled = False)
@lightbulb.add_checks(lightbulb.checks.human_only, lightbulb.checks.has_role_permissions(hikari.Permissions.MANAGE_GUILD))
@lightbulb.command("bred", description="Генит бред в чат (пока только букавы и символы)")
@lightbulb.implements(lightbulb.SlashCommand)
async def bred_gen(ctx: lightbulb.Context):
    ctx.respond(hikari.ResponseType.DEFERRED_MESSAGE_CREATE)
    iterator = (
        bot.rest.fetch_messages(ctx.channel_id)
        .filter(lambda message: ...)
        .limit(150)
    )

    async for messages in iterator.chunk(150):
        generator = mc.PhraseGenerator(
        samples=random.choice(messages).content + '\n' + random.choice(messages).content + '\n' + random.choice(messages).content + '\n' + random.choice(messages).content + '\n' + random.choice(messages).content
        )
        phrase = generator.generate_phrase(
        validators=[validators.words_count(minimal=1)]
        )
        await bot.rest.create_message(ctx.channel_id, phrase)
        print(generator.samples)
    print("ok")

@bot.command
@lightbulb.app_command_permissions(dm_enabled = False)
@lightbulb.option('user', "Нарушитель", required=True, type=hikari.Member)
@lightbulb.option("reason", "Reason for the ban", required=False)
@lightbulb.add_checks(lightbulb.checks.human_only, lightbulb.checks.has_role_permissions(hikari.Permissions.BAN_MEMBERS))
@lightbulb.command('ban', description='Банит нарушителя.')
@lightbulb.implements(lightbulb.SlashCommand)
async def banusr(ctx):
        await ctx.respond(hikari.ResponseType.DEFERRED_MESSAGE_CREATE)
        print(f"{ctx.options.user} был забанен на сервере {ctx.guild_id} пользователем {ctx.author.username}")
        embed = hikari.Embed(title= "<:BH_icon:1028520775600320603> Ban Member")
        embed.add_field("User Info",
        f"User: {ctx.options.user.mention}" + '\n' + f"Reason: {ctx.options.reason or 'Причина не указана.'}")
        
        await ctx.app.rest.ban_user(ctx.guild_id, ctx.options.user.id, reason=ctx.options.reason or hikari.UNDEFINED)
        await ctx.respond(embed)

@banusr.set_error_handler
async def banusr_hdl(event: lightbulb.CommandErrorEvent):
    if isinstance(event.exception, lightbulb.MissingRequiredPermission):
        event.context.respond(hikari.ResponseType.DEFERRED_MESSAGE_CREATE)
        await event.context.respond("Вы не имеете роли, у которой есть доступ к этой команде.", flags=hikari.MessageFlag.EPHEMERAL)
        exception = event.exception.__cause__ or event.exception
        print(exception)

@bot.command()
@lightbulb.app_command_permissions(dm_enabled = False)
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.option("reason", 'Причина разбана.', str, required=False,
                  modifier=lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.option("user", "Пользователь (ID)", hikari.Snowflake, required=True)
@lightbulb.command("unban", "Разбанивает участника.", auto_defer=True, pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def unban(ctx: lightbulb.Context, user: hikari.Snowflake, reason: str):
    res = reason or f"'Причина не указана.' - {ctx.author.username}"
    await ctx.respond(f"Разбанен пользователь <@{user}>.")
    await ctx.bot.rest.unban_member(user=user, guild=ctx.get_guild(), reason=res)
    await ctx.edit_last_response(f'Разбанен пользователь <@{user}>!' + '\n' + f'Причина: {res}.')
    print(f"{user} был разбанен пользователем {ctx.author.username} на сервере {ctx.guild_id}")

@unban.set_error_handler
async def unban_hdl(event: lightbulb.CommandErrorEvent):
    if isinstance(event.exception, lightbulb.MissingRequiredPermission):
        event.context.respond(hikari.ResponseType.DEFERRED_MESSAGE_CREATE)
        await event.context.respond("Вы не имеете роли, у которой есть доступ к этой команде.", flags=hikari.MessageFlag.EPHEMERAL)
        exception = event.exception.__cause__ or event.exception
        raise event.exception

if __name__ == '__main__':
     bot.run(
     status=hikari.Status.IDLE,
        activity=hikari.Activity(
            name="10 часов белого шума",
            type=hikari.ActivityType.LISTENING
        )
    )