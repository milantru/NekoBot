import os

curr_file_path = os.path.dirname(os.path.realpath(__file__))
PATH_TO_DATA_FOLDER = os.path.join(curr_file_path, os.path.normpath("../data"))


def _get_file_path_for(items_name):
  file_path = os.path.join(PATH_TO_DATA_FOLDER, items_name + ".txt")
  return file_path

def _add_items(items_name, items):
  items.sort()
  res = ""
  for item in items:
    res += item.strip() + "\n"
  file = _get_file_path_for(items_name)
  with open(file, "a") as f:
    f.writelines(res)

def _get_items(items_name):
  file = _get_file_path_for(items_name)
  with open(file, "r") as f:
    items = f.readlines()
  return [item.rstrip("\n") for item in items]
  
def _delete_from_items_list(items_name, indices):
  file = _get_file_path_for(items_name)
  items = _get_items(items_name)

  for idx in sorted(indices, reverse=True):
    if 0 <= idx < len(items):
      del items[idx]
  
  items = "\n".join(items)
  file = _get_file_path_for(items_name)
  with open(file, "w") as f:
    f.writelines(items)


def add_games(anime_names):
  _add_items("games", anime_names)

def add_mangas(manga_names):
  _add_items("mangas", manga_names)

def get_games():
  return _get_items("games")

def get_mangas():
  return _get_items("mangas")

def delete_from_game_list(indices):
  _delete_from_items_list("games", indices)

def delete_from_manga_list(indices):
  _delete_from_items_list("mangas", indices)
