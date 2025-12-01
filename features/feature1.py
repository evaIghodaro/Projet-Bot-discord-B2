#chaque utilisateur gagne des points lorsqu’il atteint une feuille normale de l’arbre (dessert non VIP), et ces points sont stockés dans le JSON.
# Gère l'attribution et lecture des points
class PointsManager:
    def __init__(self, save_manager):
        self.save_manager = save_manager  # // accès JSON

    # // ajoute points depuis un dessert
    def award_from_node(self, user_id, dessert):
        if not dessert:
            return
        pts = dessert.get("points", 0)
        if pts > 0:
            self.save_manager.add_points(user_id, pts)

    # // points du joueur
    def get_points(self, user_id):
        return self.save_manager.get_points(user_id)

    # // reset des points
    def reset_points(self, user_id):
        self.save_manager.reset_points(user_id)
