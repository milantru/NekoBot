import os
import discord

from cmds_handler import *

from keep_alive import keep_alive


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
  print('I, {0.user}, am HERE!'.format(client))

@client.event
async def on_message(message):
  allowed_users_ids = os.getenv("USER_IDS")
  if allowed_users_ids is not None:
    allowed_users_ids = allowed_users_ids.split(",")
  else:
    allowed_users_ids = []
  is_allowed_user = str(message.author.id) in allowed_users_ids

  if message.author == client.user:
    return
  
  msg = message.content
  channel = message.channel

  if msg.startswith('!pozdrav'):
    await handle_greeting_async(channel)

  if msg.startswith('!pomoc'):
    await handle_help_async(channel)

  if msg.startswith('!citat'):
    await handle_quote_async(channel)

  cmd_for_adding_manga = "!pridaj mangu "
  if msg.startswith(cmd_for_adding_manga) and is_allowed_user:
    await handle_adding_manga_async(msg, channel, cmd_for_adding_manga)

  cmd_for_adding_games = "!pridaj hru "
  if msg.startswith(cmd_for_adding_games) and is_allowed_user:
    await handle_adding_game_async(msg, channel, cmd_for_adding_games)

  if msg.startswith('!mangy'):
    await handle_listing_mangas_async(channel)
  
  if msg.startswith('!hry'):
    await handle_listing_games_async(channel)

  cmd_for_deleting_manga = "!zmaz mangu "
  if msg.startswith(cmd_for_deleting_manga) and is_allowed_user:
    await handle_removing_mangas_async(msg, channel, cmd_for_deleting_manga)

  cmd_for_deleting_games = "!zmaz hru "
  if msg.startswith(cmd_for_deleting_games) and is_allowed_user:
    await handle_removing_games_async(msg, channel, cmd_for_deleting_games)


keep_alive()

try:
  token = os.getenv("TOKEN") or ""
  if token == "":
    raise Exception("Please add your token to the Secrets.")
  client.run(token)
except discord.HTTPException as e:
  if e.status == 429:
    print(
        "The Discord servers denied the connection for making too many requests"
    )
    print(
        "Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests"
    )
  else:
    raise e
