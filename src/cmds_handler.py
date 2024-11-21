import requests
import json
import db

def get_random_anime_quote():
  try:
    res = requests.get('https://animechan.io/api/v1/quotes/random')
    response = json.loads(res.text)["data"]
    quote = f'"{response["content"]}"\n-{response["character"]["name"]} from {response["anime"]["name"]}'
  except Exception:
    quote = None
  
  return quote

async def handle_removing_games_async(msg, channel, cmd_for_deleting_games):
    if len(msg) > len(cmd_for_deleting_games):
      games_nums_tmp = msg.split(' ', 2)[2]
      games_nums = []
      for num in games_nums_tmp.split(","):
        n = num.strip()
        if len(n) > 0 and n.isdigit():
          games_nums.append(n)
      db.delete_from_game_list([int(num) - 1 for num in games_nums]) # -1 because function wants indices
      if len(games_nums) > 1:
        notification_msg = f'Hry s č. {", ".join(games_nums)} boli vymazané zo zoznamu!'
      elif len(games_nums) == 0:
        notification_msg = 'Zdá sa, že nič nebolo vymazané!'
      else:
        notification_msg = f'Hra č. {games_nums[0]} bola vymazaná zo zoznamu!'
      await channel.send(notification_msg)
    else:
      await channel.send('Ak mi neprezradíš číslo hry na vymazanie, tak ju nemôžem vymazať (>_<).')

async def handle_removing_mangas_async(msg, channel, cmd_for_deleting_manga):
    if len(msg) > len(cmd_for_deleting_manga):
      mangas_nums_tmp = msg.split(' ', 2)[2]
      mangas_numbers = []
      for num in mangas_nums_tmp.split(","):
        n = num.strip()
        if len(n) > 0 and n.isdigit():
          mangas_numbers.append(n)
      db.delete_from_manga_list([int(num) - 1 for num in mangas_numbers]) # -1 because function wants indices
      if len(mangas_numbers) > 1:
        notification_msg = f'Mangy s č. {", ".join(mangas_numbers)} boli vymazané zo zoznamu!'
      elif len(mangas_numbers) == 0:
        notification_msg = 'Zdá sa, že nič nebolo vymazané!'
      else:
        notification_msg = f'Manga č. {mangas_numbers[0]} bola vymazaná zo zoznamu!'
      await channel.send(notification_msg)
    else:
      await channel.send('Ak mi neprezradíš číslo mangy na vymazanie, tak ju nemôžem vymazať (>_<).')

async def handle_listing_games_async(channel):
    games = db.get_games()
    if len(games) > 0:
      tmp = list(zip(range(len(games)), games, strict=True)) # list of (i, ith game name) pairs
      games_numbered_list_str = ''
      for i, game_name in tmp:
        games_numbered_list_str += f'{i + 1}. {game_name}\n'
      await channel.send('Máme hry:\n' + games_numbered_list_str)
    else:
      await channel.send("Čože?! :0 Nemáme žiadnu hru! :'(")

async def handle_listing_mangas_async(channel):
    mangas = db.get_mangas()
    if len(mangas) > 0:
      tmp = list(zip(range(len(mangas)), mangas, strict=True)) # list of (i, ith manga name) pairs
      mangas_numbered_list_str = ''
      for i, manga_name in tmp:
        mangas_numbered_list_str += f'{i + 1}. {manga_name}\n'
      await channel.send('Máme mangy:\n' + mangas_numbered_list_str)
    else:
      await channel.send("Čože?! :0 Nemáme žiadnu mangu! :'(")

async def handle_adding_game_async(msg, channel, cmd_for_adding_games):
    if len(msg) > len(cmd_for_adding_games):
      game_names_tmp = msg.split(" ", 2)[2]
      game_names = [name.strip() for name in game_names_tmp.split(",") if len(name.strip()) > 0]
      db.add_games(game_names)
      use_plural = len(game_names) > 1
      await channel.send(
          f'{"Hry" if use_plural else "Hra"} {", ".join(game_names)} {"boli pridané" if use_plural else "bola pridaná"} do zoznamu!'
      )
    else:
      await channel.send('Ak mi neprezradíš názov hry na pridanie, tak ju nemôžem pridať (>_<).')

async def handle_adding_manga_async(msg, channel, cmd_for_adding_manga):
    if len(msg) > len(cmd_for_adding_manga):
      manga_names_tmp = msg.split(" ", 2)[2]
      manga_names = [
          name.strip() for name in manga_names_tmp.split(",")
          if len(name.strip()) > 0
      ]
      db.add_mangas(manga_names)
      use_plural = len(manga_names) > 1
      await channel.send(
          f'{"Mangy" if use_plural else "Manga"} {", ".join(manga_names)} {"boli pridané" if use_plural else "bola pridaná"} do zoznamu!'
      )
    else:
      await channel.send('Ak mi neprezradíš názov mangy na pridanie, tak ju nemôžem pridať (>_<).')

async def handle_quote_async(channel):
    quote = get_random_anime_quote()
    await channel.send(quote or "Oh no! A wild error has appeared! (Prosím, nahláste to.)")

async def handle_help_async(channel):
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

async def handle_greeting_async(channel):
    await channel.send('Ahoj!')
