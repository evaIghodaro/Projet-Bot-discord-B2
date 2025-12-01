#gère l’historique des commandes des utilisateurs en stockant, récupérant et effaçant les commandes via une liste chaînée faite à la main.
# // Gère l'historique des commandes utilisateur

from history.save_manager import SaveManager

class HistoryManager:
    def __init__(self, save_manager: SaveManager, user_id=None):
        self.save_manager = save_manager
        self.user_id = user_id

        # // liste simple au lieu d'une liste chaînée
        self.history = []

        # // charger historique existant
        if user_id:
            saved = self.save_manager.get_history(user_id)
            if saved:
                self.history = list(saved)

    # // ajouter une commande
    def add(self, command):
        self.history.append(command)
        self.save()

    # // dernière commande
    def get_last(self):
        return self.history[-1] if self.history else None

    # // toutes les commandes
    def get_all(self):
        return self.history

    # // effacer historique
    def clear(self):
        self.history = []
        self.save()

    # // enregistrer dans le JSON
    def save(self):
        if self.user_id:
            self.save_manager.save_history(self.user_id, self.history)
