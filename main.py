from subprocess import call
from time import sleep
import json

from art import text2art


def clear_screen():
    call('clear')


def import_game_data(file_path: str) -> dict:
    with open(file_path, 'r') as f:
        return json.loads(''.join(f.readlines()))


class User:
    def __init__(self):
        self.name = None
        self.hp = 50

    def lose_hp(self, amount):
        self.hp = self.hp - amount
        print(f'체력이 {amount}만큼 떨어졌습니다.')

    def print_status(self):
        print(f'{self.name} 님 현재 체력: {self.hp}')
        print('-----------------------------------------')
        print()


class Game:
    def __init__(self, user: User, game_data: dict):
        self._user = user
        self._game_data = game_data

    def start(self):
        self.prologue()
        for question in self._game_data['questions']:
            self.go_question(question)

    def prologue(self):
        clear_screen()
        art = text2art(self._game_data['title'])
        print(art)
        for content in self._game_data['prologue']['contents']:
            print(content)
        username = input('>> ')
        self._user.name = username
        print(f'안녕하세요, {username}님! 저와 함께 민윤홍의 인생에 대한 여행을 떠나시죠!')
        print('이제 게임을 시작합니다! 엔터를 누르세요.')
        input()

    def go_question(self, question):
        clear_screen()
        self._user.print_status()

        problem = question['problem']
        for p in problem:
            print(p)
        answer_options = question['answer_options']
        answer_length = len(answer_options)
        for i, option in enumerate(answer_options, 1):
            print(f'{i}. {option}')

        selected_int = 0
        while True:
            selected = input('정답은? ')
            try:
                selected_int = int(selected)
            except Exception:
                print(f'잘못된 답변입니다. 1~{answer_length}까지 숫자를 입력해주세요')
                continue

            if not (1 <= selected_int <= answer_length):
                print(f'잘못된 답변입니다. 1~{answer_length}까지 숫자를 입력해주세요')
                continue
            break

        answer = question['answer']
        if selected_int != answer:
            print('정답이 틀렸습니다!')
            print(f'정답은 {answer}. {answer_options[answer-1]} 입니다!')
            self._user.lose_hp(10)
        else:
            print('정답입니다!')
        input()

        for explanation in question['explanations']:
            clear_screen()
            self._user.print_status()
            explanation_type = explanation['type']
            contents = explanation['contents']
            if explanation_type == 'text':
                for content in contents:
                    print(content)
        input()


if __name__ == '__main__':
    user = User()
    game_data = import_game_data('./game_data.json')
    game = Game(user, game_data)
    game.start()
