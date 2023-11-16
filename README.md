# Neko Bot

Discord bot pre [Neko Anime Bar](http://nekobar.cz/) Discord server.

## Príkazy (POZOR, pravdepodobne sa ešte bude meniť tvar príkazov)
Príkazy označené \* môžu využívať iba niektorí užívatelia.
- `!pozdrav` - Bot pozdraví.
- `!citat` - Vypíše náhodný citát z nejakého anime (zdroj citátov je [Animechan API](https://github.com/rocktimsaikia/anime-chan)).
- \*`!pridaj <názov mangy>` - Pridá mangu do zoznamu.
- `!mangy` - Vylistuje abecedne zoradený (číslovaný) zoznam s pridanými mangami.
- \*`!zmaz <poradové číslo mangy>` - Vymaže mangu zo zoznamu.

## O tvorbe bota
Toto je môj prvý Discord bot, ktorého som vytvoril podľa [freeCodeCamp tutoriálu](https://youtu.be/SPTfmiYiuok?si=T_CgfdWieJs5VRmg). Bot bol vytvorený za pomoci platformy [Replit](https://replit.com/~) (podobne ako v tutoriáli).

Projekt využíva premenné (environment variables):
- `TOKEN` : `<bot token>` // bot token sa dá získať z Discordu
- `USER_IDS` : `[<user1 id>, <user2 id>, ...]` // Discord id-čká užívateľov, ktorí môžu využívať všetky príkazy
