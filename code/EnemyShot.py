# code/EnemyShot.py
from code.entity import Entity

class EnemyShot(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        self.speed = 5  # Exemplo de velocidade do tiro do inimigo

    def move(self):
        # O tiro do inimigo vai para a esquerda
        self.rect.x -= self.speed