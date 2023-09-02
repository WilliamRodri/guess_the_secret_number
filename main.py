import PySimpleGUI as sg
import random
import pygame
import json


def main():
    def ler_dados():
        with open("./users_config.json", "r") as index:
            dadosUsers = json.load(index)

        return dadosUsers

    def update_combo_with_data():
        opcoesUserList = list(dados.keys())
        return opcoesUserList

    def update_points(player, score, roundsPlayed):
        dadosUserForUpdate = ler_dados()

        if player in dadosUserForUpdate:
            dadosUserForUpdate[player] = {
                "totalScores": score,
                "roundsPlayed": roundsPlayed
            }
        with open("./users_config.json", "w") as index:
            json.dump(dadosUserForUpdate, index, indent=4)

    def deleteUser(player):
        if player in dados:
            del dados[player]

        with open("./users_config.json", "w") as index:
            json.dump(dados, index, indent=4)

        return True

    def createNewUser():
        create_user_main = [
            [sg.Text("Criando Jogador...")],
            [sg.Text("" * 10)],
            [sg.Text("Nome do Jogador: "), sg.Input(key='newUserName')],
            [sg.Text("" * 10)],
            [sg.Text("" * 10)],
            [sg.Button("Criar", key='createPlay'), sg.Button(button_text="Fechar", key="close")],
            [sg.Text("" * 10)],
        ]

        createNewUser = sg.Window("Criando novo jogador!", create_user_main)

        while True:
            eventCreateNewUser, valueCreateNewUser = createNewUser.read()

            if eventCreateNewUser == sg.WIN_CLOSED or eventCreateNewUser == "close":
                break

            newUserName = valueCreateNewUser['newUserName']
            if eventCreateNewUser == "createPlay":
                dados = ler_dados()

                if newUserName in dados:
                    sg.popup("Jogador com o mesmo nome ja existente")
                    continue
                else:
                    dictionary = {
                        newUserName: {
                            "totalScores": 1,
                            "roundsPlayed": 0
                        }
                    }

                    dados.update(dictionary)
                    with open("./users_config.json", "w") as index:
                        json.dump(dados, index, indent=4)

                    sg.popup("Jogador criado com Sucesso!")
                    opcoesUserListCreateNewuser = update_combo_with_data()
                    winStart['comboUsers'].update(values=opcoesUserListCreateNewuser)
                break
        createNewUser.close()

    dados = ler_dados()
    opcoesUserList = list(dados.keys())

    global playerSelected
    try:
        sg.theme("DarkBrown5")
        sg.set_options(font=('Roboto', 15))

        def gameColumn(game_rounds, total_rounds, attempts, score, playerUsername):
            """
            :type game_rounds: object
            :type total_rounds: object
            :type attempts: object
            :type score: object

            """
            one_column = [
                [sg.Text(f"{playerUsername} está jogando!", text_color="white")],
                [
                    sg.Text("Escolha o Número", font=("Roboto", 15)),
                    sg.Text("", font=("Roboto", 13), text_color='red', key='print_message'),
                ],
                [sg.Text(' ' * 10)],
                [
                    sg.ReadFormButton('1', size=(5, 3), font="Roboto", key=1),
                    sg.ReadFormButton('2', size=(5, 3), font="Roboto", key=2),
                    sg.ReadFormButton('3', size=(5, 3), font="Roboto", key=3),
                    sg.ReadFormButton('4', size=(5, 3), font="Roboto", key=4),
                    sg.ReadFormButton('5', size=(5, 3), font="Roboto", key=5),
                ],
                [
                    sg.ReadFormButton('6', size=(5, 3), font="Roboto", key=6),
                    sg.ReadFormButton('7', size=(5, 3), font="Roboto", key=7),
                    sg.ReadFormButton('8', size=(5, 3), font="Roboto", key=8),
                    sg.ReadFormButton('9', size=(5, 3), font="Roboto", key=9),
                    sg.ReadFormButton('10', size=(5, 3), font="Roboto", key=10),
                ]
            ]

            two_column = [
                [sg.Text("Pontuação", font=("Roboto", 13))],
                [sg.Text(score, font=("Roboto", 17), key='score')],
                [sg.Text("Rodada", font=("Roboto", 13))],
                [sg.Text(f"{game_rounds} / {total_rounds}", font=("Roboto", 17), key='round')],
                [sg.Text("Tentivas", font=("Roboto", 13))],
                [sg.Text(attempts, font=("Roboto", 17), key='attempts')],
            ]

            layout = [
                [
                    sg.Column(one_column),
                    sg.VSeperator(),
                    sg.Column(two_column),
                ]
            ]

            winGame = sg.Window(
                "Descubra o Número",
                layout,
                size=(600, 270),
                text_justification='center',
                element_justification='center'
            )

            return winGame

        start = [
            [sg.Text(' ' * 10)],
            [sg.Text("Escolha um jogador", )],
            [sg.Combo(opcoesUserList, key="comboUsers", readonly=True), sg.Button("Informações", key='informationPlayer')],
            [sg.Text(' ' * 10)],
            [sg.Text("Quantas as vezes você deseja jogar?", )],
            [sg.Text(' ' * 10)],
            [sg.Input(size=(10, 1), key='times_play'), sg.Button(button_text='Continuar', key='continue')],
            [sg.Text(' ' * 10)],
            [sg.Text("", key='message', text_color='red')],
            [sg.Button("Deseja criar um Jogador?", key='createNewUser'), sg.Button("Atualizar Dados", key='refresh')]
        ]

        winStart = sg.Window(
            "Descubra o Número",
            start,
            size=(450, 400),
            text_justification='center',
            element_justification='center',
        )

        def final():
            final_main = [
                [sg.Text("Deseja jogar novamente?")],
                [sg.Button("Sim", key='yes'), sg.Button("Não", key='no')]
            ]

            final_main = sg.Window("Final", final_main,
                                   text_justification='center',
                                   element_justification='center',
                                   )

            while True:
                eventFinalMain, valueFinalMain = final_main.read()

                if eventFinalMain == sg.WIN_CLOSED:
                    break

                if eventFinalMain == 'yes':
                    final_main.close()
                    main()
                else:
                    return False

        def informationPlayer(player):
            try:
                dados = ler_dados()[player]

                information_main = [
                    [sg.Text(f"Informação do Jogador(a): {player}")],
                    [sg.Text("" * 10)],
                    [sg.Text("" * 10)],
                    [sg.Text(f"Total de Scores\n {dados['totalScores']}")],
                    [sg.Text("" * 10)],
                    [sg.Text(f"Total de rodadas Jogadas\n {dados['roundsPlayed']}")],
                    [sg.Text("" * 10)],
                    [sg.Button("Excluir Jogador(a)?", key='deletePlay'), sg.Button(button_text="Fechar", key="close")],
                    [sg.Text("" * 10)],
                ]
            except KeyError as err:
                sg.popup(f"Error in file: users_config_file\n no verso:  {err}")

            informationWin = sg.Window(f"Informações - {player}", information_main,
                                       element_justification='center',
                                       text_justification='center')

            while True:
                eventInformation, valueInformation = informationWin.read()

                if eventInformation == sg.WIN_CLOSED or eventInformation == "close":
                    break

                if eventInformation == "deletePlay":
                    if deleteUser(player):
                        sg.popup("Deletado com Sucesso!")
                        winStart['comboUsers'].update(values=update_combo_with_data())
                        break
                    else:
                        sg.popup_error("Error no Sistema")

            informationWin.close()

        def logic(playerSelected, win, times_plays):

            dadosPlayerSelected = ler_dados()[playerSelected]

            win.close()
            score = dadosPlayerSelected['totalScores']

            for game_rounds in range(1, times_plays + 1):

                numberSecret = random.randint(1, 10)
                print(f"Numero secreto: {numberSecret}")
                attempts = 3

                winGame = gameColumn(game_rounds, times_plays, attempts, score, playerSelected)
                winGame.refresh()

                played = int(dadosPlayerSelected['roundsPlayed'])
                played += game_rounds

                def song_correct():
                    pygame.mixer.init()
                    pygame.mixer.music.load('assets/correct.mp3')
                    pygame.mixer.music.set_volume(0.3)
                    pygame.mixer.music.play()

                def songs_error():
                    pygame.mixer.init()
                    pygame.mixer.music.load('assets/error.mp3')
                    pygame.mixer.music.set_volume(0.3)
                    pygame.mixer.music.play()

                while attempts > 0:

                    if score < 0:
                        score = 0

                    eventWinGame, valueWinGame = winGame.read()

                    winGame['round'].update(f"{game_rounds} / {times_plays}")
                    winGame['attempts'].update(attempts - 1)
                    winGame['score'].update(abs(score))
                    winGame.refresh()

                    if eventWinGame == sg.WIN_CLOSED:
                        winGame.close()
                        return

                    response = eventWinGame

                    if response == numberSecret:
                        song_correct()
                        sg.popup(f"Parabêns você acertou!\nO número correto era {numberSecret}")
                        score += 3
                        break
                    else:
                        winGame['print_message'].update("")
                        songs_error()
                        winGame['print_message'].update("Você errou!")
                        score -= 1
                        if attempts == 2:
                            sg.popup('Você está na sua ultima tentativa')

                    attempts -= 1
                update_points(playerSelected, score, played)
                winGame.close()
            return True

        while True:
            event, value = winStart.read()

            try:
                playerSelected = value['comboUsers']
            except TypeError:
                pass

            if event == "createNewUser":
                createNewUser()

            if event == sg.WIN_CLOSED:
                break

            if event == "refresh":
                dados = ler_dados()
                dadosUsuarios = list(dados.keys())
                winStart['comboUsers'].update(values=dadosUsuarios)

            if event == 'informationPlayer':
                if playerSelected != '':
                    informationPlayer(playerSelected)
                else:
                    winStart['message'].update("Você precisa selecionar um Jogador!")
                continue

            if event == 'continue':
                if playerSelected != '':
                    try:
                        times_play = value['times_play']
                        times_play = int(times_play)
                        if times_play <= 0:
                            winStart['message'].update("Digite valores maiores que '0'")
                        else:
                            logic = logic(playerSelected, winStart, times_play)
                            if logic:
                                final()
                    except ValueError:
                        winStart['message'].update("Digite um valor Válido! ex. (1, 2 ou 3)")
                else:
                    winStart['message'].update("Selecione um Jogador ou crie um!")

        winStart.close()

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
