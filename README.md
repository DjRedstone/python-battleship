# 🚢 Python Battleship
***

Ce projet 100% Python vous permet de jouer au mythique [jeu de la bataille navale](https://fr.wikipedia.org/wiki/Bataille_navale_(jeu)) en faisant affronter ce que vous voulez (utilisateur ou robot). Le jeu tourne avec une interface en ASCII en E/S (entrée/sortie).

## Jouer normalement

Pour jouer normalement, il vous suffit de télécharger le code source du projet et d'exécuter le programme `main.py`. Une partie va débuter contre un robot.

## Modifier les joueurs

Vous pouvez facilement modifier les joueurs qui se disputent. Par exemple, vous pouvez faire affronter deux robots de difficulté différente l'un contre l'autre :

```py
from game import Game
from players import Bot

# Création d'un robot appelé "bot 1" dont la difficulté est de 0
bot1 = Bot("bot 1", 0)
# Création d'un robot appelé "bot 2" dont la difficulté est de 1
bot2 = Bot("bot 2", 1)

# Creation de la partie avec les deux robots
game = Game(bot1, bot2)
game.start()
```

ou encore jouer à deux sur le même écran :

```py
from game import Game
from players import Player

# Création d'un joueur appelé "alice"
player1 = Player("alice")
# Création d'un joueur appelé "bob"
player2 = Player("bob")

# Creation de la partie avec les deux joueurs
game = Game(player1, player2)
game.start()
```

## Analiser les données des jeux

La fonction `start` de `Game` retourne les résultats de la partie à la fin de celle-ci. Elles sont disponibles sous forme d'un `dict` tel que :

```py
game_results = game.start()
print(game_results)
# {
#     "nb_rounds": nb_rounds,
#     "player1_rounds": player1_rounds,
#     "player2_rounds": player2_rounds,
#     "winner": winner
# }
```

## Développer un robot / une IA

Il est tout à faire possible de créer un robot ou une IA pour jouer au jeu de manière automatisée. Pour ce faire, il vous suffit simplement de modifier le code fourni dans `main.py`.

Pour créer un joueur automatique, il faudra fournir à la class `Game` de `game.py` un objet remplissant les conditions suivantes :
- L'objet vient d'une classe comportant au moins :
  - Un nom (`str`)
  - Une fonction `ask_ship` qui, grâce à une liste de bateaux dispobiles par identifiant (`list[int]`), retourne un `tuple[int, bool, int, int]` d'informations permettant de placer un bateau. (Réspectivement : l'identifiant du bateau, l'orientation du bateau [`False`: Horizontal / `True`: Vertical], les coordonnées x et y du début du bateau)
  - Une fonction `ask_code` sans arguments qui retourne un code valable à tirer sur un grille (un `str` sous la forme `<lettre><nombre>` *Exemples : `B4`, `E10`*)

D'autres fonctions sont également possible d'ajouter :
- Une fonction `update_data` permettant de mettre à jour les informations de jeu avec deux paramètres :
  - Une `list[list[str]]` correspondant à une grille de caractères (la grille de tirs du joueur)
  - Une `list[Ship]` correspondant aux bateaux encore vivant
- Une fonction `update_last_res` permettant de mettre à jour les informations du dernier tir avec deux paramètres :
  - Un code (`str`) correspondant au code cible
  - Un `str` correspondant au résultat du tir. Cette variable peut avoir plusieurs formes :
    - `"hit"`: Le tir a touché un bateau
    - `"hit-<n>-sink"` : Le tir a touché un bateau et a fait coulé n bateaux
    - `"miss"` : Le tir a loupé un bateau

> Notes : Ces deux dernières fonctions ne retournent rien

## Dépendances

- Python 3