#!/usr/bin/python
# -*- coding: utf-8 -*-
from code.entity import Entity
from code.Const import ENTITY_SPEED


class PlayerShot(Entity):

    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        # Busca a velocidade no Const.py, se não achar usa 8 como padrão
        self.speed = ENTITY_SPEED.get(self.name, 8)

    def move(self):
        # Move o tiro para a direita
        self.rect.x += self.speed