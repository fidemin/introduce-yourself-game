import json
from subprocess import call
from time import sleep

from art import text2art

from animation import Animator


def clear_screen():
    call('clear')


def import_game_data(file_path: str) -> dict:
    with open(file_path, 'r') as f:
        return json.loads(''.join(f.readlines()))


class User:
    def __init__(self, name, hp):
        self.name = name
        self._init_hp = hp
        self.hp = hp

    def lose_hp(self, amount):
        self.hp = self.hp - amount
        print(f'체력이 {amount}만큼 떨어졌습니다.')

    def print_status(self):
        print(f'{self.name} 님 체력: {self.hp}', end=' ')
        full_hp_bar_length = int(self._init_hp / 2)
        hp_bar_length = int(self.hp / 2)
        hp_bar = '[' + '=' * hp_bar_length + ' ' * (full_hp_bar_length - hp_bar_length) + ']'
        print(hp_bar)
        print('-----------------------------------------')
        print()


class Game:
    def __init__(self, game_data: dict):
        self._user = None
        self._game_data = game_data

    def start(self):
        self.prologue()
        for question in self._game_data['questions']:
            self.go_question(question)

    def prologue(self):
        clear_screen()
        art_str = text2art(self._game_data['title'])
        animator = Animator(art_str, width=150, height=40)
        delay = 1.0 / 10
        moves = [
            (-15, 10), (1, -1), (1, -2), (1, -3), (1, -4), (1, -5),
            (1, 4), (1, 3), (1, 2), (1, 1), (1, 0), (1, -1), (1, -2), (1, -3), (1, -4),
            (1, 3), (1, 2), (1, 1), (1, 0), (1, -1), (1, -2), (1, -3),
            (1, 2), (1, 1), (1, 0), (1, -1), (1, -2),
            (1, 1), (1, 0), (1, -1),
        ]
        for move in moves:
            clear_screen()
            animator.move(move[0], move[1])
            print(animator.to_string())
            sleep(delay)
        input()

        clear_screen()
        name = self._game_data["name"]
        num_of_questions = len(self._game_data["questions"])
        hp = 50
        print(f'이 게임은 {name}의 대한 {num_of_questions}개의 문제를 맞추는 게임입니다.')
        print(f'여러분은 {hp}의 체력을 가지며, 한 문제를 틀릴 때 마다 10점씩 에너지가 깎이게 됩니다.')
        print('우리 함께 여행을 떠나볼까요?')
        print('이름을 입력하세요!')
        username = input('>> ')
        self._user = User(username, hp)
        print(f'안녕하세요, {username}님! 저와 함께 {name}의 인생에 대한 여행을 떠나시죠!')
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
    game_data = import_game_data('./game_data.json')
    game = Game(game_data)
    game.start()
