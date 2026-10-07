from model.enums import StatusMissao, TipoInimigo

# Justificativa dos setters:
# - nome, descricao e recompensa NÃO têm setter: são a definição da missão e não
#   fazem sentido mudar no meio do jogo (evita, por exemplo, alterar a recompensa
#   depois de aceita a missão).
# - status TEM setter, pois muda durante o jogo (PENDENTE -> EM_ANDAMENTO ->
#   CONCLUIDA). O setter valida o tipo (precisa ser StatusMissao) e só aceita a
#   próxima etapa da sequência, sem pular nem retroceder.
class Missao:
    # Próximo status permitido para cada status atual
    _PROXIMO = {
        StatusMissao.PENDENTE: StatusMissao.EM_ANDAMENTO,
        StatusMissao.EM_ANDAMENTO: StatusMissao.CONCLUIDA,
        StatusMissao.CONCLUIDA: None,
    }

    def __init__(self, nome, descricao, recompensa):
        if not isinstance(recompensa, int) or recompensa < 0:
            raise ValueError("A recompensa base precisa ser um inteiro maior ou igual a zero")
        self.__nome = nome
        self.__descricao = descricao
        self.__recompensa = recompensa
        self.__status = StatusMissao.PENDENTE

    @property
    def nome(self):
        return self.__nome

    @property
    def descricao(self):
        return self.__descricao

    @property
    def recompensa(self):
        return self.__recompensa

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, novo_status):
        if not isinstance(novo_status, StatusMissao):
            raise TypeError("O status precisa ser um StatusMissao")
        esperado = self._PROXIMO[self.__status]
        if novo_status is not esperado:
            if esperado is None:
                raise ValueError(
                    f"Transição inválida: a missão já está {self.__status.value} "
                    f"e não pode mudar de status")
            raise ValueError(
                f"Transição inválida: de {self.__status.value} só é possível "
                f"ir para {esperado.value}, não para {novo_status.value}")
        self.__status = novo_status

    def iniciar_missao(self):
        if self.status is StatusMissao.PENDENTE:
            self.status = StatusMissao.EM_ANDAMENTO
            return f"A missão {self.nome} começou! O objetivo é {self.descricao}."
        return f"A missão {self.nome} já foi iniciada!!!"

    def calcular_recompensa(self):
        if self.status is not StatusMissao.CONCLUIDA:
            return 0
        return self.recompensa

    def concluir_missao(self, heroi):
        if self.status is StatusMissao.CONCLUIDA:
            raise ValueError(f"A missão {self.nome} já foi concluída; a recompensa não é paga duas vezes")
        # 1º muda o status (a recompensa só é paga após a conclusão)
        self.status = StatusMissao.CONCLUIDA
        # 2º calcula e entrega o XP ao herói
        xp = self.calcular_recompensa()
        heroi.ganhar_experiencia(xp)
        return xp

    def exibir_dados(self):
        msg = f'''
[{self.__class__.__name__}]
Nome: {self.nome}
Descrição: {self.descricao}
Recompensa: {self.recompensa}
Status: {self.status.value}
'''
        return msg

    def __str__(self):
        return f'missão [{self.__class__.__name__}]: {self.nome} | status: {self.status.value}'


class MissaoCaca(Missao):
    """Caça: o herói precisa abater N inimigos de um tipo (TipoInimigo)."""
    XP_POR_INIMIGO = 10

    def __init__(self, nome, descricao, recompensa, tipo_inimigo, quantidade):
        super().__init__(nome, descricao, recompensa)
        if not isinstance(tipo_inimigo, TipoInimigo):
            raise TypeError("tipo_inimigo precisa ser um TipoInimigo")
        if quantidade <= 0:
            raise ValueError("A quantidade de inimigos precisa ser maior que zero")
        self.__tipo_inimigo = tipo_inimigo
        self.__quantidade = quantidade

    @property
    def tipo_inimigo(self):
        return self.__tipo_inimigo

    @property
    def quantidade(self):
        return self.__quantidade

    def calcular_recompensa(self):
        base = super().calcular_recompensa()
        if self.status is not StatusMissao.CONCLUIDA:
            return base
        return base + self.quantidade * self.XP_POR_INIMIGO

    def exibir_dados(self):
        return super().exibir_dados() + f"Alvo: {self.quantidade}x {self.tipo_inimigo.value}\n"


class MissaoColeta(Missao):
    """Coleta: o herói precisa juntar N unidades de um item."""
    XP_POR_ITEM = 5

    def __init__(self, nome, descricao, recompensa, item, quantidade):
        super().__init__(nome, descricao, recompensa)
        if quantidade <= 0:
            raise ValueError("A quantidade de itens precisa ser maior que zero")
        self.__item = item
        self.__quantidade = quantidade

    @property
    def item(self):
        return self.__item

    @property
    def quantidade(self):
        return self.__quantidade

    def calcular_recompensa(self):
        base = super().calcular_recompensa()
        if self.status is not StatusMissao.CONCLUIDA:
            return base
        return base + self.quantidade * self.XP_POR_ITEM

    def exibir_dados(self):
        return super().exibir_dados() + f"Coletar: {self.quantidade}x {self.item}\n"


class MissaoEntrega(Missao):
    """Entrega: levar uma mercadoria a um destinatário, a certa distância."""
    XP_POR_KM = 3

    def __init__(self, nome, descricao, recompensa, mercadoria, destinatario, distancia_km):
        super().__init__(nome, descricao, recompensa)
        if distancia_km <= 0:
            raise ValueError("A distância precisa ser maior que zero")
        self.__mercadoria = mercadoria
        self.__destinatario = destinatario
        self.__distancia_km = distancia_km

    @property
    def mercadoria(self):
        return self.__mercadoria

    @property
    def destinatario(self):
        return self.__destinatario

    @property
    def distancia_km(self):
        return self.__distancia_km

    def calcular_recompensa(self):
        base = super().calcular_recompensa()
        if self.status is not StatusMissao.CONCLUIDA:
            return base
        return base + self.distancia_km * self.XP_POR_KM

    def exibir_dados(self):
        return (super().exibir_dados()
                + f"Entregar: {self.mercadoria} para {self.destinatario} ({self.distancia_km} km)\n")
