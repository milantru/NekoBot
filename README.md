# Neko Bot

Discord bot pre [Neko Anime Bar](http://nekobar.cz/) Discord server.

## Príkazy
Príkazy označené \* môžu využívať iba oprávnení užívatelia.
- `!pozdrav` - Bot pozdraví.
- `!citat` - Vypíše náhodný citát z nejakého anime (zdroj citátov je [Animechan API](https://github.com/rocktimsaikia/anime-chan)).
- \*`!pridaj mangu názov_mangy1, názov_mangy2...` - Pridá mangu do zoznamu.
- \*`!pridaj hru názov_hry1, názov_hry2...` - Pridá hru do zoznamu.
- `!mangy` - Vylistuje abecedne zoradený (číslovaný) zoznam s pridanými mangami.
- `!hry` - Vylistuje abecedne zoradený (číslovaný) zoznam s pridanými hrami.
- \*`!zmaz mangu 1, 2, 3...` - Vymaže mangu zo zoznamu (`1, 2, 3...` sú poradové čísla máng).
- \*`!zmaz hru 1, 2, 3...` - Vymaže hru zo zoznamu (`1, 2, 3...` sú poradové čísla hier).

## O tvorbe bota
Toto je môj prvý Discord bot, ktorého som vytvoril podľa [freeCodeCamp tutoriálu](https://youtu.be/SPTfmiYiuok?si=T_CgfdWieJs5VRmg). Bot bol vytvorený za pomoci platformy [Replit](https://replit.com/~) (podobne ako v tutoriáli). | **UPDATE:** Kód bol masívne refaktorovaný a zbavený závislosti na platforme Replit.

Projekt využíva `.env`:
- `TOKEN` : `<bot token>` // bot token sa dá získať z Discordu
- `USER_IDS` : `"<user1 id>, <user2 id>, ..."` // Discord id-čká oprávnených užívateľov, ktorí môžu využívať všetky príkazy

## REST API

Bot poskytuje takisto aj API. Je možné sa dotazovať na aktuálne hry alebo mangy v bare.

Príklad 1 (Python, vypíše stolné hry v bare):

```Python
import requests
import json

res = requests.get('https://0f34ac37-e0e0-4a82-b452-5c2b69293918-00-momoqbv0zn71.janeway.replit.dev/games')
response = json.loads(res.text)

for res in response:
    print(res)
```

Príklad 2 (Python, vypíše mangy v bare):

```Python
import requests
import json

res = requests.get('https://0f34ac37-e0e0-4a82-b452-5c2b69293918-00-momoqbv0zn71.janeway.replit.dev/mangas')
response = json.loads(res.text)

for res in response:
    print(res)
```
