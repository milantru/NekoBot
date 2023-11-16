# This code is based on the following example:
# https://discordpy.readthedocs.io/en/stable/quickstart.html#a-minimal-bot

import os

import discord

import requests
import json

from replit import db

from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


def update_manga_list(manga_name):
  if "mangas" in db.keys():
    mangas = db["mangas"]
    mangas.append(manga_name)
    db["mangas"] = mangas
  else:
    db["mangas"] = [manga_name]


def get_mangas():
  if "mangas" in db.keys():
    mangas = db["mangas"]
    return mangas
  else:
    return []


def delete_from_manga_list(index):
  mangas = db["mangas"]
  if 0 <= index < len(mangas):
    del mangas[index]
    db["mangas"] = mangas


@client.event
async def on_ready():
  print('I, {0.user}, am HERE!'.format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content
  channel = message.channel

  if msg.startswith('$hello'):
    await channel.send('Hello!')

  if msg.startswith('$quote'):
    try:
      res = requests.get('https://animechan.xyz/api/random')
    except Exception:
      await channel.send("Oh no! A wild error has occurred! \
          It seems there is some problem with the anime quotes API :/")
      return

    response = json.loads(res.text)

    await channel.send(
        f'"{response["quote"]}"\n-{response["character"]} from {response["anime"]}'
    )

  if msg.startswith('$add '):
    manga_name = msg.split(' ', 1)[1]
    update_manga_list(manga_name)
    await channel.send(f'Added {manga_name} to the list!')

  if msg.startswith('$list'):
    mangas = get_mangas()
    if len(mangas) > 0:
      tmp = list(zip(range(len(mangas)), mangas, strict=True))
      mangas_numbered_list_str = ''
      for i, manga_name in tmp:
        mangas_numbered_list_str += f'{i + 1}. {manga_name}\n'
      await channel.send('Mangas:\n' + mangas_numbered_list_str)
    else:
      await channel.send('Mangas:\nThere are no mangas! :0')

  if msg.startswith('$del '):
    idx = int(msg.split(' ', 1)[1])
    delete_from_manga_list(idx)
    await channel.send(f'Deleted {idx} from the list!')


keep_alive()
token = os.getenv("TOKEN") or ""
client.run(token)
"""
try:
  token = os.getenv("TOKEN") or ""
  if token == "":
    raise Exception("Please add your token to the Secrets pane.")
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
"""
