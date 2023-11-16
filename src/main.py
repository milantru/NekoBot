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
    mangas = list(db["mangas"])
    mangas.append(manga_name)
    mangas.sort()
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


def get_random_anime_quote():
  try:
    res = requests.get('https://animechan.xyz/api/random')
    response = json.loads(res.text)
    quote = f'"{response["quote"]}"\n-{response["character"]} from {response["anime"]}'
  except Exception:
    quote = None

  return quote


@client.event
async def on_ready():
  print('I, {0.user}, am HERE!'.format(client))


@client.event
async def on_message(message):
  allowed_users_ids = os.getenv("USER_IDS") or []
  is_allowed_user = str(message.author.id) in allowed_users_ids

  if message.author == client.user:
    return

  msg = message.content
  channel = message.channel

  if msg.startswith('!pozdrav'):
    await channel.send('Ahoj!')

  if msg.startswith('!citat'):
    quote = get_random_anime_quote()
    await channel.send(
        quote or "Oh no! A wild error has appeared! (Prosím, nahláste to.)")

  cmd_for_adding_manga = "!pridaj "
  if msg.startswith(cmd_for_adding_manga) and is_allowed_user:
    if len(msg) > len(cmd_for_adding_manga):
      manga_name = msg.split(' ', 1)[1]
      update_manga_list(manga_name)
      await channel.send(f'Manga {manga_name} bolo pridané do zoznamu!')
    else:
      await channel.send(
          'Ak mi neprezradíš názov mangy na pridanie, tak ju nemôžem pridať (>_<).'
      )

  if msg.startswith('!mangy'):
    mangas = get_mangas()
    if len(mangas) > 0:
      tmp = list(zip(range(len(mangas)), mangas, strict=True))
      mangas_numbered_list_str = ''
      for i, manga_name in tmp:
        mangas_numbered_list_str += f'{i + 1}. {manga_name}\n'
      await channel.send('Máme mangy:\n' + mangas_numbered_list_str)
    else:
      await channel.send("Čože?! :0 Nemáme žiadnu mangu! :'(")

  cmd_for_deleting_manga = "!zmaz "
  if msg.startswith(cmd_for_deleting_manga) and is_allowed_user:
    if len(msg) > len(cmd_for_deleting_manga):
      manga_num = int(msg.split(' ', 1)[1])
      idx = manga_num - 1
      delete_from_manga_list(idx)
      await channel.send(f'Manga č.{manga_num} bola vymazaná zo zoznamu!')
    else:
      await channel.send(
          'Ak mi neprezradíš číslo mangy na vymazanie, tak ju nemôžem vymazať (>_<).'
      )


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
