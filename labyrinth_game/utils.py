from . import constants, player_actions


def describe_current_room(game_state: dict) -> None:
    current_room = game_state['current_room']
    room_info = constants.ROOMS[current_room]
    print(f"Вы находитесь в комнате: {current_room.upper()}")
    print(f"{room_info['description']}")
    if room_info['items']:
        print(f"Заметные предметы: {', '.join(room_info['items'])}")
    print("Выходы: ")
    for number, (direction, name) in enumerate(room_info['exits'].items(), 1):
        print(f"  {number}. {direction} -> {name}")
    if room_info['puzzle']:
        print("Кажется, здесь есть загадка (используйте команду solve).")

def solve_puzzle(game_state: dict) -> None:
    puzzle = game_state['current_room']['puzzle']
    if not puzzle:
        print("Загадок здесь нет.")
    else:
        question, answer = puzzle
        print(f"Загадка: {question}")
        player_answer =player_actions.get_input("Ваш ответ: ")
        if player_answer.strip().lower() == answer.lower():
            print("Правильно! Вы решили загадку.")
            game_state['current_room']['puzzle'] = None
            # TODO: Нужно добавить награду за решение загадки
        else:
            print("Неверно. Попробуйте снова.")

def show_help():
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение") 