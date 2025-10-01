import math

from . import constants, player_actions


def show_help(commands: dict = constants.COMMANDS) -> None:
    ALIGNMENT = 16
    print("\nДоступные команды:")
    for command, description in commands.items():
        print(f"{command.ljust(ALIGNMENT, ' ')}{description}")

def describe_current_room(game_state: dict) -> None:
    current_room = game_state['current_room']
    room_info = game_state['rooms'][current_room]
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
    room_info = game_state['rooms'][current_room]
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
            give_puzzle_reward(game_state)
        else:
            print("Неверно. Попробуйте снова.")

def give_puzzle_reward(game_state: dict):
    available_items = all_items_except_treasure(constants.ROOMS)
    if available_items:
        random_reward = pseudo_random(
            seed = game_state['steps_taken'], 
            modulo = len(available_items)
        )
        reward_item = available_items[random_reward]
        if reward_item not in game_state['player_inventory']:
          game_state['player_inventory'].append(reward_item)
          print(f"В награду вы получаете: {reward_item}")
        else:
          print(f"В награду вы получаете: {reward_item}, но он уже у вас есть.")
    else:
        print("Вы уже собрали все доступные предметы. Награды нет.")

def all_items_except_treasure(rooms: dict) -> list[str]:
    """
    Возвращает список всех предметов из всех комнат,
    кроме 'treasure chest'.
    """
    items = []
    for room in rooms.values():
        for item in room.get("items", []):
            if item != "treasure chest":
                items.append(item)
    return items

def attempt_open_treasure(game_state: dict):
    current_room = game_state['current_room']
    room_info = game_state['rooms'][current_room]
    
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

def trigger_trap(game_state: dict):
    print("Ловушка активирована! Пол стал дрожать...")
    inventory = game_state['player_inventory']
    if inventory:
        seed = game_state['steps_taken']
        intem_index = pseudo_random(seed = seed, modulo = len(inventory))
        lost_item = inventory.pop(intem_index)
        print(f"Вы потеряли предмет: {lost_item}")
    else:
        damage_probability = pseudo_random(seed = game_state['steps_taken'], modulo = 9)
        if damage_probability < 3:
            print("Вы получили травму от ловушки и не можете продолжать!")
            game_state['game_over'] = True
        else:
            print("Вы уцелели в ловушке!")

def find_coin(game_state: dict):
    print("Вы нашли монетку на полу!")
    if 'coin' not in game_state['player_inventory']:
        game_state['player_inventory'].append('coin')
        print("Монетка добавлена в ваш инвентарь.")
    else:
        print("У вас уже есть монетка.")

def frighten_player(game_state: dict):
    print("Вы слышите шорох! Что-то приближается...")
    if 'sword' in game_state['player_inventory']:
        print("К счастью, у вас есть меч, который отпугнул существо.")

def pseudo_random(seed: int, modulo: int) -> int:
    """
    Генерация детерминированного псевдослучайного числа на основе синусойды.

    :param seed: целое число, используемое для инициализации генератора
    :param modulo: целое число, задающее диапазон результата (от 0 до modulo-1)
    :return: псевдослучайное целое число в диапазоне [0, modulo)
    """
    raw_value = math.sin(seed * 12.9898) * 43758.5453
    fractional_part = raw_value - math.floor(raw_value)
    to_return = int(fractional_part * modulo)
    print(f"DEBUG: pseudo_random(seed={seed}, modulo={modulo}) -> {to_return}")
    return to_return

def random_event(game_state: dict):
    current_probaility = pseudo_random(
        seed = game_state['steps_taken'],
        modulo = constants.RANDOM_EVENT_PROBABILITY
    )
    will_event_happen = current_probaility == constants.RANDOM_EVENT_TRIGGER_THRESHOLD
    if will_event_happen:
        event_index = pseudo_random(
            seed = game_state['steps_taken'],
            modulo = len(constants.RANDOM_EVENT_SCENARIOS)
        )
        event = constants.RANDOM_EVENT_SCENARIOS[event_index]
        match event:
            case "trap":
                trigger_trap(game_state)
            case "find_item":
                find_coin(game_state)
            case "fright":
                frighten_player(game_state)