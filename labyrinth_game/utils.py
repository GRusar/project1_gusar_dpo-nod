import math

from . import constants, player_actions


def clone_rooms(rooms: dict) -> dict:
    """Создаёт независимую копию описания комнат."""
    def clone_nested(value):
        """Рекурсивно копирует словари, списки и кортежи."""
        if isinstance(value, dict):
            return {key: clone_nested(nested) for key, nested in value.items()}
        if isinstance(value, list):
            return [clone_nested(item) for item in value]
        if isinstance(value, tuple):
            return tuple(clone_nested(item) for item in value)
        return value

    return clone_nested(rooms)

def show_help(commands: dict = constants.COMMANDS) -> None:
    """
    Выводит справку по доступным командам.
    """
    print("\nДоступные команды:")
    for command, description in commands.items():
        print(
            f"{command.ljust(constants.HELP_ALIGNMENT, ' ')}{description}"
        )

def describe_current_room(game_state: dict) -> None:
    """
    Выводит описание текущей комнаты, включая доступные выходы,
    заметные предметы и наличие загадки."""
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
    """
    Решение загадки в текущей комнате.
    Если загадка решена, она удаляется из комнаты,
    и игрок получает награду.
    """
    current_room = game_state['current_room']
    room_info = game_state['rooms'][current_room]
    puzzle = room_info['puzzle']
    
    if not puzzle:
        print("Загадок здесь нет.") 
    else:
        question, answers = puzzle
        normalized_answers = (ans.lower() for ans in answers)
        print(f"Загадка: {question}")
        player_answer = player_actions.get_input("Ваш ответ: ")
        right_answer = player_answer.strip().lower() in normalized_answers
        if right_answer:
            print("Правильно! Вы решили загадку.")
            room_info['puzzle'] = None
            if current_room == "hall":
                if "treasure key" not in game_state['player_inventory']:
                  game_state['player_inventory'].append("treasure key")
                  print("В награду вы получаете: 'treasure key'")
            elif current_room == "library":
                if "rusty key" not in game_state['player_inventory']:
                  game_state['player_inventory'].append("rusty key")
                  print("В награду вы получаете: 'rusty key'")
            else:
              give_puzzle_reward(game_state)
        else:
            if current_room == "trap_room":
                trigger_trap(game_state)
                return
            print("Неверно. Попробуйте снова.")

def give_puzzle_reward(game_state: dict) -> None:
    """
    Выдаёт игроку случайный предмет из всех комнат, кроме 'treasure chest'.
    Если все предметы уже в инвентаре, награды нет.
    """
    available_items = all_items_except_treasure(constants.ROOMS)
    if available_items:
        random_reward = pseudo_random(
            seed=game_state['steps_taken'],
            modulo=len(available_items)
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

def attempt_open_treasure(game_state: dict) -> None:
    """
    Попытка открыть сундук с сокровищами.
    Если у игрока есть ключ, сундук открывается.
    Если нет, игроку предлагается ввести код.
    """
    current_room = game_state['current_room']
    room_info = game_state['rooms'][current_room]
    
    if 'treasure chest' not in room_info['items']:
        print("Сундук уже открыт или отсутствует.")
        return
    if (
        'treasure key' in game_state['player_inventory'] 
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
                if puzzle:
                    normalized_code = code.strip().lower()
                    valid_codes = (answer.lower() for answer in puzzle[1])
                    if normalized_code in valid_codes:
                        print("Код верный! Сундук открыт!")
                        room_info['items'].remove('treasure chest')
                        print("В сундуке сокровище! Вы победили!")
                        game_state['game_over'] = True
                    else:
                        print("Неверный код.")
                else:
                    print("Неверный код.")
            case "нет":
              print("Вы отступаете от сундука.")
            case _:
              print("Ответ не распознан. Вы отступаете от сундука.")

def trigger_trap(game_state: dict) -> None:
    """
    Срабатывание ловушки.

    С некоторой вероятностью игрок теряет случайный предмет
    из инвентаря, получает травму и не может продолжать игру
    или может уцелеть без потерь.
    """
    print("Ловушка активирована! Пол стал дрожать...")
    inventory = game_state['player_inventory']
    if inventory:
        seed = game_state['steps_taken']
        item_index = pseudo_random(seed=seed, modulo=len(inventory))
        lost_item = inventory.pop(item_index)
        print(f"Вы потеряли предмет: {lost_item}")
    else:
        damage_probability = pseudo_random(
            seed=game_state['steps_taken'],
            modulo=constants.TRAP_DAMAGE_MODULO,
        )
        if damage_probability < constants.TRAP_DAMAGE_THRESHOLD:
            print("Вы получили травму от ловушки и не можете продолжать!")
            game_state['game_over'] = True
        else:
            print("Вы уцелели в ловушке!")

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
    return to_return

def random_event(game_state: dict) -> None:
    """
    Случайное событие, которое может произойти при перемещении игрока.

    Событие зависит от количества сделанных шагов и размера инвентаря.
    Возможные события:
    - Найти монетку
    - Испугаться (если есть меч, существо отпугивается)
    - Активировать ловушку (если находимся в 'trap_room' и нет факела)
    """
    current_probability = pseudo_random(
        seed=game_state['steps_taken'],
        modulo=constants.RANDOM_EVENT_PROBABILITY
    )
    will_event_happen = current_probability == constants.RANDOM_EVENT_TRIGGER_THRESHOLD
    if will_event_happen:
        inventory_size = len(game_state['player_inventory'])
        scenario_seed = (
            (game_state['steps_taken'] + constants.EVENT_SCENARIO_STEP_OFFSET)
            * (
                inventory_size
                + constants.EVENT_SCENARIO_INVENTORY_SCALE
            )
            + constants.EVENT_SCENARIO_ADDITIVE_SHIFT
        )
        event_index = pseudo_random(
            seed=scenario_seed,
            modulo=len(constants.RANDOM_EVENT_SCENARIOS)
        )
        event = constants.RANDOM_EVENT_SCENARIOS[event_index]

        current_room = game_state['current_room']
        room_info = game_state['rooms'][current_room]
        match event:
            case "find_coin":
                print("Вы нашли монетку на полу!")
                room_info['items'].append("coin")
            case "fright":
                print("Вы слышите шорох! Что-то приближается...")
                if 'sword' in game_state['player_inventory']:
                    print("К счастью, у вас есть меч, который отпугнул существо.")
            case "trap":
                if (
                    game_state['current_room'] == "trap_room"
                    and "torch" not in game_state['player_inventory']
                ):
                  trigger_trap(game_state)