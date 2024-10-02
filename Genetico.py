import random

# Definindo as características do problema
compartimentos = {
    'D': (6800, 10), 
    'C': (8700, 16), 
    'T': (5300, 8)
}  # (volume, peso)

cargas = {
    'C1': (480, 18, 310),
    'C2': (650, 15, 380),
    'C3': (580, 23, 350),
    'C4': (390, 12, 285)
}

# Parâmetros do algoritmo genético
populacao_tamanho = 500
geracoes = 500
taxa_mutacao = 0.1
tamanho_torneio = 5  # Número de participantes do torneio

def inicializar_populacao():
    return [[random.uniform(0, 5) for _ in range(len(cargas) * len(compartimentos))] for _ in range(populacao_tamanho)]

def aptidao(cromossomo):
    lucro_total = 0
    volume_usado = {key: 0 for key in compartimentos}
    peso_usado = {key: 0 for key in compartimentos}
    
    for i, (nome_carga, (volume, peso, lucro)) in enumerate(cargas.items()):
        for j, compartimento in enumerate(compartimentos.keys()):
            quantidade = cromossomo[i * len(compartimentos) + j]
            if quantidade > 0:
                volume_usado[compartimento] += quantidade * volume
                peso_usado[compartimento] += quantidade * peso
                lucro_total += quantidade * lucro

    penalidade = 0

    # Verificando restrições de volume e peso
    for key in compartimentos.keys():
        volume_max, peso_max = compartimentos[key]
        if volume_usado[key] > volume_max:
            # Penalidade para excesso de volume
            penalidade += (volume_usado[key] - volume_max) # Ajuste o fator de penalidade conforme necessário
        if peso_usado[key] > peso_max:
            # Penalidade para excesso de peso
            penalidade += (peso_usado[key] - peso_max)  # Ajuste o fator de penalidade conforme necessário

    # Reduz o lucro total pela penalidade calculada
    # lucro_total -= penalidade * 4

    # return max(lucro_total, 0)  # Retorna 0 se o lucro for negativo
    return lucro_total - penalidade * 4

def selecao_torneio(populacao):
    vencedores = []
    for _ in range(len(populacao) // 2):
        torneio = random.sample(populacao, tamanho_torneio)
        vencedor = max(torneio, key=aptidao)
        vencedores.append(vencedor)
    return vencedores

def cruzamento(pai1, pai2):
    ponto = random.randint(1, len(pai1) - 1)
    filho1, filho2 = pai1.copy(), pai2.copy()
    if random.random() < 0.8:
        filho1 = pai1[:ponto] + pai2[ponto:]
        filho2 = pai2[:ponto] + pai1[ponto:]
    return filho1, filho2



def mutacao(cromossomo):
    for i in range(len(cromossomo)):
        if random.random() < 0.5:
            cromossomo[i] = random.uniform(0, 1)

def imprimir_alocacao(cromossomo):
    print("Alocação:")
    for i, (nome_carga, _) in enumerate(cargas.items()):
        alocacoes = [cromossomo[i * len(compartimentos) + j] for j in range(len(compartimentos))]
        alocacoes_formatadas = [f"{valor:.3f}" for valor in alocacoes]  # Formata os valores
        print(f"{nome_carga}: {alocacoes_formatadas}")

def algoritmo_genetico():
    populacao = inicializar_populacao()

    for geracao in range(geracoes):
        nova_populacao = selecao_torneio(populacao)
        while len(nova_populacao) < populacao_tamanho:
            pai1, pai2 = random.sample(nova_populacao, 2)
            filho1, filho2 = cruzamento(pai1, pai2)
            mutacao(filho1)
            mutacao(filho2)
            nova_populacao.append(filho1)
            nova_populacao.append(filho2)

        populacao = nova_populacao
        
        # Imprimindo aptidão e alocação da melhor solução de cada geração
        melhor_solucao = max(populacao, key=aptidao)
        lucro_maximo = aptidao(melhor_solucao)
        print(f"\nGeração {geracao + 1}: Aptidão = {lucro_maximo:.2f}")
        imprimir_alocacao(melhor_solucao)

    melhor_solucao = max(populacao, key=aptidao)
    return melhor_solucao, aptidao(melhor_solucao)

melhor_alocacao, lucro_maximo = algoritmo_genetico()

# Formata os valores na melhor_alocacao
melhor_alocacao_formatada = [f"{valor:.2f}" for valor in melhor_alocacao]

print("\nMelhor Alocação Final:", melhor_alocacao_formatada)
print(f"Lucro Máximo: {lucro_maximo:.2f}")
