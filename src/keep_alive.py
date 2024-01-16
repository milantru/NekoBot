from flask import Flask, jsonify
from threading import Thread
from db import get_games, get_mangas

app = Flask('')


@app.route('/')
def home():
  return "Hello. I am alive!"


@app.route('/games')
def api_get_games():
  games = get_games()
  return jsonify(games)


@app.route('/mangas')
def api_get_mangas():
  mangas = get_mangas()
  return jsonify(mangas)


def run():
  app.run(host='0.0.0.0', port=8080)


def keep_alive():
  t = Thread(target=run)
  t.start()
