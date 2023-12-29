# Neko Bot

Discord bot pre [Neko Anime Bar](http://nekobar.cz/) Discord server.

## Príkazy
Príkazy označené \* môžu využívať iba niektorí užívatelia.
- `!pozdrav` - Bot pozdraví.
- `!citat` - Vypíše náhodný citát z nejakého anime (zdroj citátov je [Animechan API](https://github.com/rocktimsaikia/anime-chan)).
- \*`!pridaj mangu názov_mangy1, názov_mangy2...` - Pridá mangu do zoznamu.
- \*`!pridaj hru názov_hry1, názov_hry2...` - Pridá hru do zoznamu.
- `!mangy` - Vylistuje abecedne zoradený (číslovaný) zoznam s pridanými mangami.
- `!hry` - Vylistuje abecedne zoradený (číslovaný) zoznam s pridanými hrami.
- \*`!zmaz mangu 1, 2, 3...` - Vymaže mangu zo zoznamu (`1, 2, 3...` sú poradové čísla máng).
- \*`!zmaz hru 1, 2, 3...` - Vymaže hru zo zoznamu (`1, 2, 3...` sú poradové čísla hier).

## O tvorbe bota
Toto je môj prvý Discord bot, ktorého som vytvoril podľa [freeCodeCamp tutoriálu](https://youtu.be/SPTfmiYiuok?si=T_CgfdWieJs5VRmg). Bot bol vytvorený za pomoci platformy [Replit](https://replit.com/~) (podobne ako v tutoriáli).

Projekt využíva premenné (environment variables):
- `TOKEN` : `<bot token>` // bot token sa dá získať z Discordu
- `USER_IDS` : `[<user1 id>, <user2 id>, ...]` // Discord id-čká užívateľov, ktorí môžu využívať všetky príkazy
