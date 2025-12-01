#permet aux utilisateurs de débloquer des recettes VIP en dépensant leurs points et met à jour le JSON.
# Gère l'achat et le déblocage des recettes VIP

class UnlockManager:
    def __init__(self, save_manager):
        self.save_manager = save_manager
        self.vip_recipes = [
            {"name": "Tiramisu light ☁️", "cost": 2},
            {"name": "Fondant intense 🍫🔥", "cost": 3},
            {"name": "Sorbet exotique 🥭", "cost": 2}
        ]  # // liste VIP

    # // renvoie la liste VIP
    def get_vip_list(self):
        return self.vip_recipes

    # // débloque une recette via son numéro
    def unlock_by_number(self, user_id, num):

        # // numéro invalide
        if num < 1 or num > len(self.vip_recipes):
            return "❌ Recette invalide."

        recipe = self.vip_recipes[num - 1]
        user_points = self.save_manager.get_points(user_id)
        unlocked = self.save_manager.get_unlocked(user_id)

        # // déjà débloquée
        if recipe["name"] in unlocked:
            return f"✅ {recipe['name']} déjà débloquée !"

        # // pas assez de points
        if user_points < recipe["cost"]:
            return f"❌ Pas assez de points ({user_points}/{recipe['cost']})."

        # // déblocage + retrait des points
        self.save_manager.add_points(user_id, -recipe["cost"])
        self.save_manager.add_unlocked(user_id, recipe["name"])

        # // texte de recette depuis JSON
        recipe_text = self.save_manager.data.get("recipes", {}).get(
            recipe["name"], "Recette introuvable"
        )

        return (
            f"🎉 {recipe['name']} débloquée !\n"
            f"💸 {recipe['cost']} pts dépensés.\n"
            f"📜 Recette : {recipe_text}"
        )
