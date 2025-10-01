from . import constants, player_actions


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
    current_room = game_state['current_room']
    room_info = constants.ROOMS[current_room]
    puzzle = room_info['puzzle']
    if not puzzle:
        print("Загадок здесь нет.")
    else:
        question, answer = puzzle
        print(f"Загадка: {question}")
        player_answer = player_actions.get_input("Ваш ответ: ")
        if player_answer.strip().lower() == answer.lower():
            print("Правильно! Вы решили загадку.")
            room_info['puzzle'] = None
            # TODO: Нужно добавить награду за решение загадки
        else:
            print("Неверно. Попробуйте снова.")

def attempt_open_treasure(game_state: dict):
    current_room = game_state['current_room']
    room_info = constants.ROOMS[current_room]
    
    if 'treasure chest' not in room_info['items']:
        print("Сундук уже открыт или отсутствует.")
        return
    if (
        'treasure_key' in game_state['player_inventory'] 
        or 'rusty key' in game_state['player_inventory']
    ):
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        room_info['items'].remove('treasure chest')
        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
    else:
        raw_response = player_actions.get_input(
            "Сундук заперт. У вас нет ключа. Ввести код? (да/нет): "
            )
        response = raw_response.strip().lower()
        match response:
            case "да":
                code = player_actions.get_input("Введите код: ")
                puzzle = room_info['puzzle']
                if puzzle and code.strip().lower() == puzzle[1].lower():
                    print("Код верный! Сундук открыт!")
                    room_info['items'].remove('treasure chest')
                    print("В сундуке сокровище! Вы победили!")
                    game_state['game_over'] = True
                else:
                    print("Неверный код.")
            case "нет":
              print("Вы отступаете от сундука.")
            case _:
              print("Ответ не распознан. Вы отступаете от сундука.")
    