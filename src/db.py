from replit import db


def __update_items(items_name, items):
  if items_name in db.keys():
    db_items = list(db[items_name])
    db_items += items
    db_items.sort()
    db[items_name] = db_items
  else:
    items.sort()
    db[items_name] = items


def update_game_list(anime_names):
  __update_items("games", anime_names)


def update_manga_list(manga_names):
  __update_items("mangas", manga_names)


def __get_items(items_name):
  if items_name in db.keys():
    items = db[items_name]
    return list(items)
  else:
    return []


def get_games():
  return __get_items("games")


def get_mangas():
  return __get_items("mangas")


def __delete_from_items_list(items_name, indices):
  items = db[items_name]
  for idx in sorted(indices, reverse=True):
    if 0 <= idx < len(items):
      del items[idx]
      db[items_name] = items


def delete_from_game_list(indices):
  __delete_from_items_list("games", indices)


def delete_from_manga_list(indices):
  __delete_from_items_list("mangas", indices)
