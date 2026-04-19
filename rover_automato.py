from automata.fa.dfa import DFA

# =============================================================================
# Autômato Finito Determinístico — Missão de Coleta do Rover Curiosity
# Disciplina: Linguagens Formais e Autômatos — 2026.1
# UTFPR — Campus Ponta Grossa
# =============================================================================
#
# Alfabeto:
#   A = objetivo         B = rota_ok          C = obstaculo
#   D = terreno_seguro   E = terreno_inseguro  F = alinhado
#   G = braco_pronto     H = coleta_ok         I = coleta_falha
#   J = armazenado       K = aborta            L = reset
#
# Estados:
#   Q0  = ocioso                Q1  = missão recebida
#   Q2  = navegando             Q3  = desvio obstáculo
#   Q4  = área alvo             Q5  = analisando terreno
#   Q6  = terreno aprovado      Q7  = terreno reprovado
#   Q8  = posicionando          Q9  = alinhado
#   Q10 = preparando braço      Q11 = braço pronto
#   Q12 = coletando             Q13 = validando amostra
#   Q14 = armazenando           Q15 = missão concluída (final)
#   Q16 = falha                 Q17 = abortado (final)
# =============================================================================

dfa = DFA(
    states={
        'Q0','Q1','Q2','Q3','Q4','Q5','Q6','Q7',
        'Q8','Q9','Q10','Q11','Q12','Q13','Q14','Q15','Q16','Q17'
    },
    input_symbols={'A','B','C','D','E','F','G','H','I','J','K','L'},
    transitions={
        'Q0':  {'A': 'Q1'},
        'Q1':  {'B': 'Q2',  'K': 'Q17'},
        'Q2':  {'B': 'Q4',  'C': 'Q3'},
        'Q3':  {'B': 'Q2',  'K': 'Q17'},
        'Q4':  {'D': 'Q5'},
        'Q5':  {'D': 'Q6',  'E': 'Q7'},
        'Q6':  {'F': 'Q8'},
        'Q7':  {'K': 'Q17', 'L': 'Q0'},
        'Q8':  {'F': 'Q9'},
        'Q9':  {'G': 'Q10'},
        'Q10': {'G': 'Q11'},
        'Q11': {'H': 'Q12', 'K': 'Q17'},
        'Q12': {'H': 'Q13'},
        'Q13': {'H': 'Q14', 'I': 'Q16'},
        'Q14': {'J': 'Q15'},
        'Q15': {},
        'Q16': {'L': 'Q0',  'K': 'Q17'},
        'Q17': {},
    },
    initial_state='Q0',
    final_states={'Q15', 'Q17'},
    allow_partial=True
)

# Descrição dos estados para exibição no traço
descricao_estados = {
    'Q0':  'ocioso',
    'Q1':  'missão recebida',
    'Q2':  'navegando',
    'Q3':  'desvio obstáculo',
    'Q4':  'área alvo',
    'Q5':  'analisando terreno',
    'Q6':  'terreno aprovado',
    'Q7':  'terreno reprovado',
    'Q8':  'posicionando',
    'Q9':  'alinhado',
    'Q10': 'preparando braço',
    'Q11': 'braço pronto',
    'Q12': 'coletando',
    'Q13': 'validando amostra',
    'Q14': 'armazenando',
    'Q15': 'missão concluída',
    'Q16': 'falha',
    'Q17': 'abortado',
}

# Descrição dos símbolos para exibição no traço
descricao_simbolos = {
    'A': 'objetivo',
    'B': 'rota_ok',
    'C': 'obstaculo',
    'D': 'terreno_seguro',
    'E': 'terreno_inseguro',
    'F': 'alinhado',
    'G': 'braco_pronto',
    'H': 'coleta_ok',
    'I': 'coleta_falha',
    'J': 'armazenado',
    'K': 'aborta',
    'L': 'reset',
}


def executar_fita(fita):
    """
    Executa o autômato sobre a fita fornecida.
    Exibe o traço de cada transição e informa se a palavra é aceita ou rejeitada.
    """
    simbolos = fita.strip().split()

    if not simbolos:
        print("Fita vazia — palavra rejeitada.\n")
        return

    print(f"\nFita de entrada: {' '.join(simbolos)}")
    print("-" * 50)

    estado_atual = dfa.initial_state

    for simbolo in simbolos:
        # Verifica se o símbolo pertence ao alfabeto
        if simbolo not in dfa.input_symbols:
            print(f"ERRO: símbolo '{simbolo}' não pertence ao alfabeto.")
            print("Palavra REJEITADA.\n")
            return

        # Verifica se existe transição definida para esse par (estado, símbolo)
        if simbolo not in dfa.transitions[estado_atual]:
            nome_estado = descricao_estados[estado_atual]
            nome_simbolo = descricao_simbolos[simbolo]
            print(f"({estado_atual}: {nome_estado}, {nome_simbolo}) => sem transição definida")
            print("Palavra REJEITADA.\n")
            return

        proximo_estado = dfa.transitions[estado_atual][simbolo]
        nome_atual    = descricao_estados[estado_atual]
        nome_proximo  = descricao_estados[proximo_estado]
        nome_simbolo  = descricao_simbolos[simbolo]

        print(f"({estado_atual}: {nome_atual}, {nome_simbolo}) => {proximo_estado}: {nome_proximo}")

        estado_atual = proximo_estado

    print("-" * 50)

    if estado_atual in dfa.final_states:
        print(f"Estado final: {estado_atual} ({descricao_estados[estado_atual]})")
        print("Palavra ACEITA.\n")
    else:
        print(f"Estado final: {estado_atual} ({descricao_estados[estado_atual]})")
        print("Palavra REJEITADA.\n")


# =============================================================================
# Testes
# =============================================================================

def rodar_testes():
    print("=" * 50)
    print("TESTES DO AUTÔMATO — ROVER CURIOSITY")
    print("=" * 50)

    testes = [
        # (descrição, fita)

        # Caminho feliz — missão concluída com sucesso
        (
            "Teste 1: missão concluída sem obstáculos",
            "A B B D D F F G G H H H J"
        ),

        # Missão com desvio de obstáculo
        (
            "Teste 2: missão com desvio de obstáculo",
            "A B C B B D D F F G G H H H J"
        ),

        # Missão abortada logo após receber objetivo
        (
            "Teste 3: aborto após receber missão",
            "A K"
        ),

        # Missão abortada durante navegação com obstáculo
        (
            "Teste 4: aborto durante desvio de obstáculo",
            "A B C K"
        ),

        # Terreno reprovado seguido de reset e nova missão
        (
            "Teste 5: terreno reprovado, reset e nova missão concluída",
            "A B B D E L A B B D D F F G G H H H J"
        ),

        # Terreno reprovado seguido de aborto
        (
            "Teste 6: terreno reprovado e aborto",
            "A B B D E K"
        ),

        # Falha na coleta seguida de aborto
        (
            "Teste 7: falha na coleta e aborto",
            "A B B D D F F G G H H I K"
        ),

        # Falha na coleta seguida de reset e nova missão
        (
            "Teste 8: falha na coleta, reset e nova missão",
            "A B B D D F F G G H H I L A B B D D F F G G H H H J"
        ),

        # Aborto durante operação do braço
        (
            "Teste 9: aborto com braço pronto",
            "A B B D D F F G G K"
        ),

        # Palavra rejeitada — símbolo inválido no meio
        (
            "Teste 10: símbolo inválido na fita",
            "A B X"
        ),

        # Palavra rejeitada — transição inexistente
        (
            "Teste 11: transição inexistente (Q0 recebe B)",
            "B"
        ),

        # Palavra rejeitada — para em estado não final
        (
            "Teste 12: fita incompleta, para em Q2 (navegando)",
            "A B"
        ),
    ]

    for descricao, fita in testes:
        print(f"\n{descricao}")
        executar_fita(fita)


# =============================================================================
# Modo interativo
# =============================================================================

def modo_interativo():
    print("\n" + "=" * 50)
    print("MODO INTERATIVO")
    print("Digite os símbolos separados por espaço.")
    print("Exemplo: A B B D D F F G G H H H J")
    print("Digite 'sair' para encerrar.")
    print("=" * 50)

    while True:
        fita = input("\nFita: ").strip()
        if fita.lower() == 'sair':
            print("Encerrando.")
            break
        executar_fita(fita)


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    rodar_testes()