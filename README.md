# Mini Échecs

<img src="https://github.com/simonpotel/mini_echecs/blob/f56c4ca841b182559315f62d5da6c6a11919299f/assets/logo.jpg" width="200" height="200">

---

## Auteurs
https://github.com/P1x3l11

https://github.com/simonpotel

## Énnoncé

```
L'usage de la librairie graphique Tkinter est obligatoire, tout autre choix ne sera pas pris en compte.

Une approche orientée objet est obligatoire et le principe d'encapsulation devra être scrupuleusement respecté. Dans le cas contraire le projet sera directement recalé.

Vous implémenterez au minimum deux classes :

Une classe "joueur" avec (au moins) pour attributs les coordonnées de sa reine sur un plateau ainsi que son nombre de pièces restantes.
Une classe "jeu" avec plusieurs attributs à déterminer dont l'un d'eux sera une liste à deux dimensions modélisant le plateau de jeu.
Le design de l'application est libre (on pourra par exemple choisir les couleurs, les formes des pièces, etc.) mais votre programme devra au moins comporter les fonctionnalités suivantes :

Choix de la dimension du plateau via un menu, le nombre de lignes et de colonnes devant être pair et compris entre 6 et 12.
Affichage du plateau (quadrillage et pièces) et du joueur dont c'est le tour.
À chaque tour de jeu, sélection à la souris par le joueur dont c'est le tour de la pièce qu'il souhaite déplacer (conformément aux règles du jeu, i.e. il ne pourra pas sélectionner une pièce de l'adversaire ou l'une de ses pièces ne pouvant se déplacer). On visualisera cette sélection en entourant par exemple la pièce en question par un cercle (voir captures d'écran de la première partie du sujet).
À chaque tour de jeu, sélection à la souris par le joueur dont c'est le tour de la position finale de la pièce qu'il a précédemment sélectionnée (conformément aux règles du jeu).
Déplacements des pions et captures éventuelles.
Gestion des tours de jeu et de l'alternance des joueurs.
Condition de victoire.
Gestion de la fin de partie (affichage du résultat, proposition d'une nouvelle partie, etc.).
On prendra soin de découpler au maximum les méthodes algorithmiques, i.e. celles qui interagissent avec la structure de données modélisant le plateau, des méthodes graphiques qui elles s'occupent de l'affichage et de la gestion des événements.
```

## Bonus

```
Prévisualisation des coups jouables.
Sauvegarde d'une partie dans un fichier texte, et reprise de celle-ci ultérieurement.
Animations visuelles et/ou sonores lors du déplacement des pions et des captures.
Mode de jeu individuel contre l'ordinateur, celui-ci jouant de façon aléatoire (ou intelligemment).
```

