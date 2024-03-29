import os

import discord

import requests
import json
from db import get_games, get_mangas, update_game_list, update_manga_list, delete_from_game_list, delete_from_manga_list

from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


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

  # !pozdrav
  if msg.startswith('!pozdrav'):
    await channel.send('Ahoj!')

  # !pomoc
  if msg.startswith('!pomoc'):
    await channel.send("""
    Príkazy označené \* môžu využívať iba oprávnení užívatelia.
- `!pozdrav` - Bot pozdraví.
- `!citat` - Vypíše náhodný citát z nejakého anime (zdroj citátov je [Animechan API](https://github.com/rocktimsaikia/anime-chan)).
- \*`!pridaj mangu názov_mangy1, názov_mangy2...` - Pridá mangu do zoznamu.
- \*`!pridaj hru názov_hry1, názov_hry2...` - Pridá hru do zoznamu.
- `!mangy` - Vylistuje abecedne zoradený (číslovaný) zoznam s pridanými mangami.
- `!hry` - Vylistuje abecedne zoradený (číslovaný) zoznam s pridanými hrami.
- \*`!zmaz mangu 1, 2, 3...` - Vymaže mangu zo zoznamu (`1, 2, 3...` sú poradové čísla máng).
- \*`!zmaz hru 1, 2, 3...` - Vymaže hru zo zoznamu (`1, 2, 3...` sú poradové čísla hier).
    """)

  # !citat
  if msg.startswith('!citat'):
    quote = get_random_anime_quote()
    await channel.send(
        quote or "Oh no! A wild error has appeared! (Prosím, nahláste to.)")

  # !pridaj mangu A, B, C...
  cmd_for_adding_manga = "!pridaj mangu "
  if msg.startswith(cmd_for_adding_manga) and is_allowed_user:
    if len(msg) > len(cmd_for_adding_manga):
      manga_names_tmp = msg.split(" ", 2)[2]
      manga_names = [
          name.strip() for name in manga_names_tmp.split(",")
          if len(name.strip()) > 0
      ]
      update_manga_list(manga_names)
      use_plural = len(manga_names) > 1
      await channel.send(
          f'{"Mangy" if use_plural else "Manga"} {", ".join(manga_names)} {"boli pridané" if use_plural else "bola pridaná"} do zoznamu!'
      )
    else:
      await channel.send(
          'Ak mi neprezradíš názov mangy na pridanie, tak ju nemôžem pridať (>_<).'
      )

  # !pridaj hru A, B, C...
  cmd_for_adding_games = "!pridaj hru "
  if msg.startswith(cmd_for_adding_games) and is_allowed_user:
    if len(msg) > len(cmd_for_adding_games):
      game_names_tmp = msg.split(" ", 2)[2]
      game_names = [
          name.strip() for name in game_names_tmp.split(",")
          if len(name.strip()) > 0
      ]
      update_game_list(game_names)
      use_plural = len(game_names) > 1
      await channel.send(
          f'{"Hry" if use_plural else "Hra"} {", ".join(game_names)} {"boli pridané" if use_plural else "bola pridaná"} do zoznamu!'
      )
    else:
      await channel.send(
          'Ak mi neprezradíš názov hry na pridanie, tak ju nemôžem pridať (>_<).'
      )

  # !mangy
  if msg.startswith('!mangy'):
    mangas = get_mangas()
    if len(mangas) > 0:
      tmp = list(zip(range(len(mangas)), mangas,
                     strict=True))  # list of (i, ith manga name) pairs
      mangas_numbered_list_str = ''
      for i, manga_name in tmp:
        mangas_numbered_list_str += f'{i + 1}. {manga_name}\n'
      await channel.send('Máme mangy:\n' + mangas_numbered_list_str)
    else:
      await channel.send("Čože?! :0 Nemáme žiadnu mangu! :'(")

  # !hry
  if msg.startswith('!hry'):
    games = get_games()
    if len(games) > 0:
      tmp = list(zip(range(len(games)), games,
                     strict=True))  # list of (i, ith game name) pairs
      games_numbered_list_str = ''
      for i, game_name in tmp:
        games_numbered_list_str += f'{i + 1}. {game_name}\n'
      await channel.send('Máme hry:\n' + games_numbered_list_str)
    else:
      await channel.send("Čože?! :0 Nemáme žiadnu hru! :'(")

  # !zmaz mangy 1, 2, 3...
  cmd_for_deleting_manga = "!zmaz mangu "
  if msg.startswith(cmd_for_deleting_manga) and is_allowed_user:
    if len(msg) > len(cmd_for_deleting_manga):
      mangas_nums_tmp = msg.split(' ', 2)[2]
      mangas_numbers = []
      for num in mangas_nums_tmp.split(","):
        n = num.strip()
        if len(n) > 0:
          mangas_numbers.append(n)
      delete_from_manga_list([int(num) - 1 for num in mangas_numbers
                              ])  # -1 because function wants indices
      if len(mangas_numbers) > 1:
        notification_msg = f'Mangy s č. {", ".join(mangas_numbers)} boli vymazané zo zoznamu!'
      else:
        notification_msg = f'Manga č. {mangas_numbers[0]} bola vymazaná zo zoznamu!'
      await channel.send(notification_msg)
    else:
      await channel.send(
          'Ak mi neprezradíš číslo mangy na vymazanie, tak ju nemôžem vymazať (>_<).'
      )

  # !zmaz hry 1, 2, 3...
  cmd_for_deleting_games = "!zmaz hru "
  if msg.startswith(cmd_for_deleting_games) and is_allowed_user:
    if len(msg) > len(cmd_for_deleting_games):
      games_nums_tmp = msg.split(' ', 2)[2]
      games_nums = []
      for num in games_nums_tmp.split(","):
        n = num.strip()
        if len(n) > 0:
          games_nums.append(n)
      delete_from_game_list([int(num) - 1 for num in games_nums
                             ])  # -1 because function wants indices
      if len(games_nums) > 1:
        notification_msg = f'Hry s č. {", ".join(games_nums)} boli vymazané zo zoznamu!'
      else:
        notification_msg = f'Hra č. {games_nums[0]} bola vymazaná zo zoznamu!'
      await channel.send(notification_msg)
    else:
      await channel.send(
          'Ak mi neprezradíš číslo hry na vymazanie, tak ju nemôžem vymazať (>_<).'
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
