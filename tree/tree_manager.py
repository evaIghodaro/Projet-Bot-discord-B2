from .node import Node

# // Gère l'arbre de choix (sucré / fruité / etc)
class TreeManager:
    def __init__(self):
        self.root = self.build_tree()   # // racine
        self.positions = {}             # // position de chaque user

    # // crée tout l'arbre
    def build_tree(self):

        # // --- listes de desserts ---
        mousse_light = [
            {"name": "Mousse au chocolat 🍫", "recipe": "Chocolat + crème fouettée, laisser 2h", "points": 2},
            {"name": "Mousse café ☕", "recipe": "Café + crème fouettée, congeler 2h", "points": 2},
            {"name": "Mousse fruitée 🍓", "recipe": "Fruits rouges + crème, laisser 2h", "points": 2}
        ]

        fondant_gourmand = [
            {"name": "Fondant au chocolat 🍫🔥", "recipe": "Chocolat + beurre + sucre, cuisson 10min", "points": 3},
            {"name": "Brownie 🍫", "recipe": "Chocolat + noix, cuisson moelleuse", "points": 3},
            {"name": "Cookie géant 🍪", "recipe": "Pâte à cookie + cuisson 12min", "points": 3}
        ]

        fraisier = [
            {"name": "Fraisier 🍓", "recipe": "Génoise + crème mousseline + fraises", "points": 2},
            {"name": "Clafoutis 🍒", "recipe": "Cerises + pâte à clafoutis, cuisson 30min", "points": 2},
            {"name": "Salade de fruits 🍉🍓", "recipe": "Fruits frais mélangés", "points": 2}
        ]

        sorbet = [
            {"name": "Sorbet citron 🍋", "recipe": "Citron + eau + sucre, congeler", "points": 2},
            {"name": "Sorbet exotique 🥭", "recipe": "Mangue + ananas + sucre, congeler", "points": 2},
            {"name": "Smoothie tropical 🍍🥭", "recipe": "Ananas + mangue + lait ou eau", "points": 2}
        ]

        # // --- noeuds secondaires ---
        sucre = Node("Tu veux léger ou gourmand ?")
        sucre.add_child("léger", Node("", mousse_light))
        sucre.add_child("gourmand", Node("", fondant_gourmand))

        fruit = Node("Frais ou acidulé ?")
        fruit.add_child("frais", Node("", fraisier))
        fruit.add_child("acidulé", Node("", sorbet))

        # // --- racine ---
        root = Node("Salut ! Sucré ou fruité ?")
        root.add_child("sucré", sucre)
        root.add_child("fruité", fruit)

        return root

    # // texte à afficher au user
    def get_current_text(self, user_id):
        return self.positions.get(user_id, self.root).display_text()

    # // avance dans l'arbre
    def answer(self, user_id, user_input):
        norm_key = Node().norm(user_input)
        node = self.positions.get(user_id, self.root)

        # // si le choix existe, on avance
        if norm_key in node.children:
            node = node.children[norm_key]
            self.positions[user_id] = node
            return node

        # // sinon, on reste au même endroit
        return node

    # // reset position du user
    def reset(self, user_id):
        self.positions[user_id] = self.root

    # // recherche d'un terme dans l'arbre
    def speak_about(self, term):
        return self.root.find(term)
