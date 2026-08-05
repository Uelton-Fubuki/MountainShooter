# code/enemy.py
from code.entity import Entity
from code.Const import ENTITY_SPEED, WIN_WIDTH  # Ou a velocidade que você definiu

class Enemy(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        self.speed = 2  # Velocidade do inimigo

    def move(self):
        # Move o retângulo para a esquerda
        self.rect.centerx -= ENTITY_SPEED[self.name]
        if self.rect.right <= 0:
            self.rect.left= WIN_WIDTH