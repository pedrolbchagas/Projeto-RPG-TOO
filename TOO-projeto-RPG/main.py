from model.heroi import Heroi
from model.missao import MissaoCaca, MissaoColeta, MissaoEntrega
from model.enums import ClasseHeroi, StatusMissao, TipoInimigo


def main():
    heroi = Heroi("Arthur", ClasseHeroi.GUERREIRO, 100, 100, 15, 5)

    missoes = [
        MissaoCaca("Caça aos Orcs", "eliminar os orcs da floresta", 100, TipoInimigo.ORC, 5),
        MissaoColeta("Ervas Raras", "coletar ervas medicinais", 40, "Erva lunar", 6),
        MissaoEntrega("Carta Real", "entregar a carta ao rei", 60, "Carta lacrada", "Rei Alaric", 12),
    ]

    # Polimorfismo: mesmo método em todas as missões
    print("=== Missões disponíveis ===")
    for m in missoes:
        print(m.exibir_dados())
        print(f"Recompensa antes de concluir: {m.calcular_recompensa()}")

    # Ciclo completo até subir de nível
    print("\n=== ANTES ===")
    print(heroi.exibir_dados())

    caca = missoes[0]
    print(caca.iniciar_missao())
    print(f"Status: {caca.status.value}")
    xp = caca.concluir_missao(heroi)
    print(f"Missão concluída! Recompensa paga: {xp} XP")

    print("\n=== DEPOIS ===")
    print(heroi.exibir_dados())

    print("\n=== Recompensas finais ===")
    for m in missoes:
        print(f"{m} -> recompensa: {m.calcular_recompensa()}")

    try:
        caca.concluir_missao(heroi)  # recompensa duplicada
    except ValueError as e:
        print(f"Erro: {e}")

    # Erros de propósito
    print("\n=== Tratamento de erros ===")
    coleta = missoes[1]
    try:
        coleta.concluir_missao(heroi)  # pula EM_ANDAMENTO
    except ValueError as e:
        print(f"Erro: {e}")

    try:
        caca.status = StatusMissao.PENDENTE  # retrocede
    except ValueError as e:
        print(f"Erro: {e}")

    try:
        coleta.status = "CONCLUIDA"  # string em vez de enum
    except TypeError as e:
        print(f"Erro: {e}")


main()
