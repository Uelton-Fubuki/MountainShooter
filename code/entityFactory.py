from code.Const import WIN_WIDTH
from code.background import Background


class EntityFactory:

    @staticmethod
    def get_entity(entity_name: str, position=(0, 0)):
        match entity_name:
            case 'Level1Bg':
                list_bg = []
                for i in range(7):
                    # Cria a primeira imagem na posição inicial (0,0)
                    list_bg.append(Background(f'Level1Bg{i}', position))
                    # Cria a segunda imagem espelhada à direita para o efeito de rolagem
                    list_bg.append(Background(f'Level1Bg{i}', (WIN_WIDTH, position[1])))
                return list_bg
            case _:
                return []