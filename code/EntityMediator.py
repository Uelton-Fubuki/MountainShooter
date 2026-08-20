from code.Const import WIN_WIDTH


class EntityMediator:
    @staticmethod
    def __verify_collision_window(ent):
        # Destrói entidades que saem dos limites da tela
        if 'Enemy' in getattr(ent, 'name', '') and ent.rect.right < 0:
            ent.health = 0
            ent.last_dmg = None  # Evita pontuar quando o inimigo apenas sai da tela
        elif 'Player' in getattr(ent, 'name', '') and 'Shot' in getattr(ent, 'name', '') and ent.rect.left >= WIN_WIDTH:
            ent.health = 0
        elif 'Enemy' in getattr(ent, 'name', '') and 'Shot' in getattr(ent, 'name', '') and ent.rect.right <= 0:
            ent.health = 0

    @staticmethod
    def __verify_collision_entity(ent1, ent2):
        valid_interaction = False

        type1 = ent1.__class__.__name__
        type2 = ent2.__class__.__name__
        name1 = getattr(ent1, 'name', '')
        name2 = getattr(ent2, 'name', '')

        # Checa colisão entre objetos do Player (nave/tiro) e objetos do Inimigo (nave/tiro)
        if ('Player' in type1 or 'Player' in name1) and ('Enemy' in type2 or 'Enemy' in name2):
            # Garante que não haja colisão entre tiro vs tiro
            if not ('Shot' in (type1 + name1) and 'Shot' in (type2 + name2)):
                valid_interaction = True

        elif ('Enemy' in type1 or 'Enemy' in name1) and ('Player' in type2 or 'Player' in name2):
            if not ('Shot' in (type1 + name1) and 'Shot' in (type2 + name2)):
                valid_interaction = True

        if valid_interaction:
            # Detecta sobreposição física usando colliderect
            if ent1.rect.colliderect(ent2.rect):
                ent1.health -= ent2.damage
                ent2.health -= ent1.damage
                ent1.last_dmg = getattr(ent2, 'name', '')
                ent2.last_dmg = getattr(ent1, 'name', '')

    @staticmethod
    def __give_score(enemy, entity_list: list):
        enemy_score = getattr(enemy, 'score', 0)
        last_dmg = getattr(enemy, 'last_dmg', None)

        if not last_dmg:
            return

        # Identifica quem causou o dano fatal (seja tiro ou colisão direta com a nave)
        target_player = None
        if 'Player1' in last_dmg:
            target_player = 'Player1'
        elif 'Player2' in last_dmg:
            target_player = 'Player2'

        # Atribui os pontos EXCLUSIVAMENTE ao jogador que destruiu o inimigo
        if target_player:
            for ent in entity_list:
                if getattr(ent, 'name', '') == target_player:
                    ent.score += enemy_score
                    break  # Para a busca imediatamente após pontuar o jogador correto

    @staticmethod
    def verify_collision(entity_list: list):
        for i in range(len(entity_list)):
            entity1 = entity_list[i]
            EntityMediator.__verify_collision_window(entity1)
            for j in range(i + 1, len(entity_list)):
                entity2 = entity_list[j]
                EntityMediator.__verify_collision_entity(entity1, entity2)

    @staticmethod
    def verify_health(entity_list: list):
        for ent in entity_list[:]:
            if ent.health <= 0:
                # Pontua apenas se a entidade destruída for uma nave inimiga
                if 'Enemy' in getattr(ent, 'name', '') and 'Shot' not in getattr(ent, 'name', ''):
                    EntityMediator.__give_score(ent, entity_list)
                entity_list.remove(ent)