import json


def ler_dados():
    with open("./users_config.json", "r") as index:
        dados = json.load(index)

    # print(dados)
    return dados

def adicionar_dados(nomeUser, pontuacao, roundsAll):
    with open("./users_config.json", "r") as index:
        dados_existente = json.load(index)

    dados = {
        nomeUser: {
            "totalScores": int(pontuacao),
            "roundsPlayed": int(roundsAll)
        }
    }

    dados_existente.update(dados)

    with open("./users_config.json", "w") as index:
        json.dump(dados_existente, index)

    print("Dados salvo")

def apagar_dados(dados):
    if "Will" in dados:
        del dados['Will']

    with open("./users_config.json", "w") as index:
        json.dump(dados, index)

    print("deletado")

def update_points(player, score, roundsPlayed):
    dados = ler_dados()

    if player in dados:
        dados[player] = {
            "totalScores": score,
            "roundsPlayed": roundsPlayed
        }
    with open("./users_config.json", "w") as index:
        json.dump(dados, index, indent=4)

