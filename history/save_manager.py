import json
import os

# // Gère le stockage JSON (points, VIP, historique, recettes)
class SaveManager:
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = self.load()

    # // charger fichier JSON
    def load(self):
        if not os.path.exists(self.filepath):
            return {}
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}

    # // sauvegarder fichier JSON
    def save(self):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    # // ----------------------------------
    # // POINTS
    # // ----------------------------------

    def get_points(self, user_id):
        return self.data.get(user_id, {}).get("points", 0)

    def add_points(self, user_id, amount):
        user = self.data.setdefault(user_id, {})
        user["points"] = user.get("points", 0) + amount
        self.save()

    def reset_points(self, user_id):
        self.data.setdefault(user_id, {})["points"] = 0
        self.save()

    # // ----------------------------------
    # // RECETTES VIP DÉBLOQUÉES
    # // ----------------------------------

    def get_unlocked(self, user_id):
        return self.data.get(user_id, {}).get("unlocked", [])

    def add_unlocked(self, user_id, recipe_name):
        user = self.data.setdefault(user_id, {})
        unlocked = user.setdefault("unlocked", [])
        if recipe_name not in unlocked:
            unlocked.append(recipe_name)
            self.save()

    def reset_recipes(self, user_id):
        self.data.setdefault(user_id, {})["unlocked"] = []
        self.save()

    # // ----------------------------------
    # // HISTORIQUE
    # // ----------------------------------

    def get_history(self, user_id):
        return self.data.get(user_id, {}).get("history", [])

    def save_history(self, user_id, history_list):
        user = self.data.setdefault(user_id, {})
        user["history"] = history_list
        self.save()
