#fournit à l’utilisateur une recette aléatoire parmi toutes les recettes disponibles ou débloquées.
import random

# // Donne une recette aléatoire (normale ou VIP débloquée)
class RandomRecipe:
    def __init__(self, save_manager):
        self.save_manager = save_manager

    def get_random(self, user_id):

        # // toutes les recettes existantes
        all_recipes = list(self.save_manager.data.get("recipes", {}).keys())

        # // recettes débloquées par l’utilisateur
        unlocked = self.save_manager.get_unlocked(user_id)

        # // fusion sans doublons
        possible = list(set(all_recipes + unlocked))

        if not possible:
            return "Aucune recette disponible."

        # // choisir une recette au hasard
        choice = random.choice(possible)

        text = self.save_manager.data["recipes"].get(choice, "Pas de recette trouvée")

        return f"{choice}\nRecette: {text}"
