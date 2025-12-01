# Objectif Représenter un nœud de ton arbre Chaque nœud peut être :Une question (avec des enfants)Une feuille/dessert (avec mini-recette et points) 
import unicodedata

# // Un noeud de l'arbre (question ou feuille)
class Node:
    def __init__(self, text="", desserts=None):
        self.text = text                    # // texte affiché
        self.children = {}                  # // choix -> Node
        self.desserts = desserts or []      # // desserts si feuille

    # // normalise (minuscule + unicode + trim)
    def norm(self, s: str):
        return unicodedata.normalize("NFKC", s.lower().strip())

    # // ajoute un enfant
    def add_child(self, key, node):
        self.children[self.norm(key)] = node

    # // vrai si aucune suite possible
    def is_leaf(self):
        return not self.children

    # // texte du noeud
    def display_text(self):
        return self.text

    # // recherche d’un terme dans l’arbre (texte + clés + enfants)
    def find(self, term):
        term = self.norm(term)

        # // cherche dans le texte
        if term in self.norm(self.text):
            return True

        # // cherche dans les clés enfants
        if term in self.children:
            return True

        # // cherche dans chaque sous-noeud
        for child in self.children.values():
            if child.find(term):
                return True

        return False
