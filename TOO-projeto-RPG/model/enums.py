from enum import Enum

class ClasseHeroi(Enum):
    GUERREIRO = "Guerreiro"
    MAGO = "Mago"
    ARQUEIRO = "Arqueiro"


class TipoInimigo(Enum):
    ORC = "Orc"
    GOBLIN = 'Goblin'
    DRAGAO = 'Dragão'


class StatusMissao(Enum):
    PENDENTE = "Pendente"
    EM_ANDAMENTO = "Em andamento"
    CONCLUIDA = "Concluída"
